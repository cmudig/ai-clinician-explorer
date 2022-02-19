<script>
  import { onMount } from 'svelte';
  import DataStateList from './DataStateList.svelte';
  import Demographics from './Demographics.svelte';

  import Treatments from './Treatments.svelte';
  import ActionsHeatmap from '../charts/ActionsHeatmap.svelte';
  import { interpolateGreens, interpolateBlues } from 'd3-scale-chromatic';
  import LoadingBar from '../utils/LoadingBar.svelte';
  import Columns from '../utils/columns';

  let patient = null;
  export let patientID = '';
  export let modelID = 'mimiciv_220217_best';

  let isLoading;

  let modelInfo;

  let modelPredictions;

  onMount(() => {
    if (!!patientID) loadPatientInfo(patientID);
  });

  function loadPatientInfo(patientID) {
    fetch('./api/patient/' + patientID)
      .then((d) => d.json())
      .then((d) => {
        patient = d.result;
        console.log('patient:', patient);
        currentBloc = 1;
      });
  }

  let currentBloc = 0;

  $: if (!!patient && modelPredictions == null && !!modelID) {
    loadModelPrediction(patient, currentBloc);
  }

  $: if (!!modelID) {
    loadModelInfo(modelID);
  }

  async function loadModelInfo(id) {
    try {
      let response = await fetch(`./api/model/${modelID}`);
      if (response.status != 200) {
        console.log(
          `error ${response.status} loading model info:`,
          await response.text()
        );
        return;
      }
      response = await response.json();
      modelInfo = response.model;
      console.log('model info:', modelInfo);
    } catch (e) {
      console.log('error loading model info:', e);
    }
  }

  async function loadModelPrediction(patientInfo, bloc) {
    let states = patientInfo.timesteps.map((ts) => {
      let state = {};
      Object.keys(ts).forEach((key) => {
        if (typeof ts[key] == 'number') state[key] = ts[key];
        else if (ts[key].hasOwnProperty('value')) state[key] = ts[key].value;
      });
      // TODO make the model API just take a patient object as-is
      Object.keys(patientInfo).forEach((key) => {
        if (key != 'timesteps') state[key] = patientInfo[key];
      });
      return state;
    });

    // TODO resolve this issue with AI Clinician methodology. Currently the
    // model predicts the best action to take in time interval t, but it also
    // takes as input the clinicians' fluid input and vasopressor dosages during
    // the same interval t. It should either take the clinician action from t - 1,
    // or predict the action in t + 1.
    let actions = patientInfo.timesteps.map((ts) => {
      let ac = {};
      [Columns.C_INPUT_STEP, Columns.C_MAX_DOSE_VASO].forEach((key) => {
        if (typeof ts[key] == 'number') ac[key] = ts[key];
        else if (ts[key].hasOwnProperty('value')) ac[key] = ts[key].value;
      });
      return ac;
    });

    let body = { states, actions };
    console.log('body:', body);
    try {
      isLoading = true;
      let response = await fetch(`./api/model/${modelID}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      if (response.status != 200) {
        console.log(
          `error ${response.status} loading model prediction:`,
          await response.text()
        );
        isLoading = false;
        return;
      }
      response = await response.json();
      console.log('response', response);
      modelPredictions = response.results;
      isLoading = false;
    } catch (e) {
      console.log('error loading model prediction:', e);
      isLoading = false;
    }
  }

  let modelQ;
  let physicianProb;
  let modelRecommendationIdx;
  let physicianActionIdx;
  $: if (!!modelPredictions && currentBloc > 0) {
    let pred = modelPredictions[currentBloc - 1];
    modelQ = pred.model_Q;
    physicianProb = pred.physician_prob;
    modelRecommendationIdx = pred.recommendation;
    physicianActionIdx = pred.actual_action;
  } else {
    modelQ = null;
    physicianProb = null;
    modelRecommendationIdx = null;
    physicianActionIdx = null;
  }

  let maxPhysicianProb = 1.0;
  let minModelQ = 0.0;
  $: if (!!modelPredictions) {
    // Compute thresholds for visualization based on all timesteps
    let maxProb = modelPredictions
      .map((p) => p.physician_prob)
      .flat()
      .reduce((curr, p) => Math.max(curr, p), 0);
    maxPhysicianProb = Math.ceil(maxProb * 10) / 10;

    let minQ = modelPredictions
      .map((p) => p.model_Q)
      .flat()
      .reduce((curr, p) => (p != null ? Math.min(curr, p) : curr), 1e9);
    let rewardResolution = rewardVal / 10;
    minModelQ = Math.floor(minQ / rewardResolution) * rewardResolution;
  }

  let rewardVal = null;
  let actionBins = null;
  $: if (!!modelInfo) {
    rewardVal = modelInfo.params.reward_val;
    actionBins = modelInfo.actions.action_bins;
    console.log(actionBins);
  }

  function fluidDose(action) {
    if (!!modelInfo)
      return modelInfo.actions.action_medians[0][
        Math.floor(action / modelInfo.actions.n_action_bins)
      ];
    return 0;
  }

  function vasopressorDose(action) {
    if (!!modelInfo)
      return modelInfo.actions.action_medians[1][
        action % modelInfo.actions.n_action_bins
      ];
    return 0;
  }

  let actualFluidDose;
  let actualVasopressorDose;
  $: if (!!patient && currentBloc > 0) {
    // Fix timestep issue in AI Clinician
    actualFluidDose = patient.timesteps[currentBloc - 1][
      Columns.C_INPUT_STEP
    ].value.toLocaleString({ maximumSignificantDigits: 3 });
    actualVasopressorDose = patient.timesteps[currentBloc - 1][
      Columns.C_MAX_DOSE_VASO
    ].value.toLocaleString({ maximumSignificantDigits: 3 });
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv3 pv4-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked">
    <a class="link dim white dib mr3" href="/" title="Home">Home</a>
  </nav>
</header>
<main class="pa0 h-100">
  {#if isLoading}
    <div class="flex flex-column h-100 items-center justify-center">
      <p class="mb3 f5 tc b dark-gray">Loading...</p>
      <LoadingBar />
    </div>
  {:else}
    <div class="flex align-stretch h-100">
      <div class="sidebar">
        {#if !!patient}
          <div
            class="timestep-selector flex justify-center items-center w-100 pv3"
          >
            <span class="f6 b pb0 mr3"
              >Hour {currentBloc * 4}/{patient.timesteps.length * 4}</span
            >
            <input
              class="ph0"
              style="width: 140px;"
              type="range"
              bind:value={currentBloc}
              min={1}
              max={patient.timesteps.length}
              step={1}
            />
          </div>
        {/if}
        <Demographics {patient} />
      </div>
      {#if !!patient}
        <div class="patient-info-container flex-auto flex h-100">
          <div class="data-column flex flex-column flex-auto h-100">
            <div class="data-state flex-auto">
              <DataStateList {patient} bloc={currentBloc} />
            </div>
            <div class="data-treatments">
              <Treatments {patient} bloc={currentBloc} />
            </div>
          </div>
          <div
            class="prediction-column flex-auto h-100 flex justify-center ph4"
          >
            {#if !!modelQ}
              <div class="flex-auto heatmap pr2">
                <h5 class="f5 tc b mb2">Predicted Treatment Values</h5>
                {#if !!modelInfo && modelRecommendationIdx != null}
                  <p class="f6 lh-copy above-plot">
                    AI Clinician recommends {#if vasopressorDose(modelRecommendationIdx) == 0}
                      <strong>no vasopressor</strong>{:else}
                      a vasopressor dosage of <strong
                        >{vasopressorDose(
                          modelRecommendationIdx
                        ).toLocaleString({ maximumSignificantDigits: 3 })} ug/kg/min</strong
                      >
                      (norep equivalent){/if} and {#if fluidDose(modelRecommendationIdx) == 0}
                      <strong>no IV fluids</strong>
                    {:else}
                      <strong
                        >{fluidDose(modelRecommendationIdx).toLocaleString({
                          maximumSignificantDigits: 3,
                        })} mL/4h</strong
                      >
                      IV fluids{/if}.
                  </p>
                {/if}
                <ActionsHeatmap
                  data={modelQ}
                  valueDomain={!!rewardVal ? [minModelQ, rewardVal] : [0, 100]}
                  colorMap={interpolateBlues}
                  fluidBins={actionBins != null ? actionBins[0] : null}
                  vasopressorBins={actionBins != null ? actionBins[1] : null}
                  nullColor="#f7f7f7"
                />
              </div>
            {/if}
            {#if !!physicianProb}
              <div class="flex-auto heatmap pl2">
                <h5 class="f5 tc b mb2">Clinician Probabilities</h5>
                {#if !!modelInfo && modelRecommendationIdx != null}
                  <p class="f6 lh-copy above-plot">
                    The clinician action was {#if actualVasopressorDose == 0}
                      <strong>no vasopressor</strong>{:else}
                      a vasopressor dosage of <strong
                        >{actualVasopressorDose} ug/kg/min</strong
                      >
                      (norep equivalent){/if} and {#if actualFluidDose == 0}
                      <strong>no IV fluids</strong>
                    {:else}
                      <strong>{actualFluidDose} mL/4h</strong>
                      IV fluids{/if}.
                  </p>
                {/if}
                <ActionsHeatmap
                  data={physicianProb}
                  valueDomain={[0, maxPhysicianProb]}
                  colorMap={interpolateGreens}
                  fluidBins={actionBins != null ? actionBins[0] : null}
                  vasopressorBins={actionBins != null ? actionBins[1] : null}
                  nullColor="#f7f7f7"
                />
              </div>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</main>

<style>
  .sidebar {
    width: 300px;
    border-right: 1px solid #777777;
    overflow-y: scroll;
    flex: 0 0 auto;
  }

  main {
    padding-top: 80px;
  }

  .bg-navy-90 {
    background-color: #001b44e7;
  }

  .data-column {
    flex-basis: 60%;
    border-right: 1px solid #777777;
  }

  .data-state {
    overflow-y: scroll;
    border-bottom: 1px solid #777777;
  }

  .data-treatments {
    height: 240px;
    flex: 0 0 auto;
    overflow-y: scroll;
  }
  .prediction-column {
    flex-basis: 100%;
  }

  .timestep-selector {
    border-bottom: 1px solid #777777;
  }

  .heatmap {
    max-width: 340px;
    flex-basis: 100%;
  }

  .above-plot {
    min-height: 60px;
  }
</style>
