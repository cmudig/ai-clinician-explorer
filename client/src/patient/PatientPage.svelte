<script>
  import { onMount, setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import DataStateList from './DataStateList.svelte';
  import Demographics from './Demographics.svelte';
  import Treatments from './Treatments.svelte';
  import LoadingBar from '../utils/LoadingBar.svelte';
  import Columns from '../utils/columns';
  import SegmentedControl from '../utils/SegmentedControl.svelte';
  import Predictions from './Predictions.svelte';
  import Antibiotics from './Antibiotics.svelte';
  import Cultures from './Cultures.svelte';
  import { StateCategory } from '../utils/strings';

  const NON_TIMESTEP_COLUMNS = [
    'timesteps',
    'antibiotics',
    'microbio',
    'notes',
  ];
  let patient = writable(null);
  let modelInfo = writable(null);
  let modelPredictions = writable(null);
  // let currentBloc = writable(0);
  export let currentBloc = writable(0);

  setContext('patient', {
    patient,
    modelInfo,
    modelPredictions,
    currentBloc,
  });

  export let patientID = '';
  export let modelID = 'mimiciv_220328_best';

  let loadingModelPrediction = false;
  let loadingPatientInfo = false;

  let treatmentTab = 1;
  let statesTab = StateCategory.VITALS;

  onMount(() => {
    if (!!patientID) loadPatientInfo(patientID);
  });

  async function loadPatientInfo(patientID) {
    loadingPatientInfo = true;
    try {
      let response = await fetch('./api/patient/' + patientID);
      if (response.status != 200) {
        loadingPatientInfo = false;
        console.log(
          `error ${response.status} loading patient info:`,
          await response.text(),
        );
        return;
      }
      response = await response.json();
      $patient = response.result;
      if ($currentBloc == 0) $currentBloc = 1;
      console.log('patient:', $patient);
      loadingPatientInfo = false;
    } catch (e) {
      console.log('error loading patient info:', e);
    }
  }

  $: if (!!$patient && $modelPredictions == null && !!modelID) {
    loadModelPrediction($patient, $currentBloc);
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
          await response.text(),
        );
        return;
      }
      response = await response.json();
      $modelInfo = response.model;
      console.log('model info:', $modelInfo);
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
        if (!NON_TIMESTEP_COLUMNS.includes(key)) state[key] = patientInfo[key];
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
      loadingModelPrediction = true;
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
          await response.text(),
        );
        loadingModelPrediction = false;
        return;
      }
      response = await response.json();
      console.log('response', response);
      $modelPredictions = response.results;
      loadingModelPrediction = false;
    } catch (e) {
      console.log('error loading model prediction:', e);
      loadingModelPrediction = false;
    }
  }

  let currentTime;
  let dayIndex;
  $: if (!!$patient && $currentBloc > 0) {
    dayIndex = Math.floor((($currentBloc - 1) * 4) / 24) + 1;
    let timestamp = $patient.timesteps[$currentBloc - 1].timestep;
    currentTime = new Date(timestamp * 1000).toLocaleTimeString('en-US', {
      hour: 'numeric',
      hour12: true,
    });
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked flex justify-between">
    <a class="link dim white dib mr3" href="/" title="Patient List"
      ><i class="arrow left" />&nbsp; Back to List</a
    >
    <a class="link dim white dib ml3" href="/logout" title="Sign Out"
      >Sign Out</a
    >
  </nav>
</header>
<main class="pa0 h-100">
  {#if loadingModelPrediction || loadingPatientInfo}
    <div class="flex flex-column h-100 items-center justify-center">
      <p class="mb3 f5 tc b dark-gray">
        Loading {loadingModelPrediction ? 'AI Clinician' : 'patient info'}...
      </p>
      <LoadingBar />
    </div>
  {:else}
    <div class="flex align-stretch h-100">
      <div class="sidebar bg-blue-gray">
        {#if !!$patient}
          <div
            class="timestep-selector bg-navy-gray flex justify-between items-center w-100 pv3 ph3 white"
          >
            <span class="f6 b pb0 mr3">Day {dayIndex}, {currentTime}</span>
            <input
              class="ph0"
              style="width: 180px;"
              type="range"
              bind:value={$currentBloc}
              min={1}
              max={$patient.timesteps.length}
              step={1}
            />
          </div>
        {/if}
        <Demographics />
      </div>
      {#if !!$patient}
        <div class="patient-info-container flex-auto flex h-100">
          <div class="data-column flex flex-column flex-auto h-100">
            <div
              class="context-info-controls pa2 flex items-center bg-near-white"
            >
              <SegmentedControl
                bind:selected={statesTab}
                options={[
                  { name: StateCategory.VITALS, value: StateCategory.VITALS },
                  { name: StateCategory.LABS, value: StateCategory.LABS },
                  {
                    name: StateCategory.CARDIOPULM,
                    value: StateCategory.CARDIOPULM,
                  },
                ]}
              />
            </div>
            <div class="data-state flex-auto">
              <DataStateList category={statesTab} />
            </div>
            <div
              class="context-info-controls pa2 flex items-center bg-near-white"
            >
              <SegmentedControl
                bind:selected={treatmentTab}
                options={[
                  { name: 'Fluids/Pressors', value: 1 },
                  { name: 'Antibiotics', value: 2 },
                  { name: 'Cultures', value: 3 },
                  { name: 'Notes', value: 4 },
                ]}
              />
            </div>
            <div class="data-treatments">
              {#if treatmentTab == 1}
                <DataStateList category={StateCategory.FLUIDS_PRESSORS} />
              {:else if treatmentTab == 2}
                <Antibiotics />
              {:else if treatmentTab == 3}
                <Cultures />
              {/if}
            </div>
          </div>
          <div class="prediction-column flex-auto h-100">
            <Predictions />
          </div>
        </div>
      {/if}
    </div>
  {/if}
</main>

<style>
  .sidebar {
    width: 320px;
    border-right: 1px solid #777777;
    overflow-y: scroll;
    flex: 0 0 auto;
  }

  .bg-blue-gray {
    background-color: #404a5a;
  }

  .bg-navy-gray {
    background-color: #2e3847;
  }

  main {
    padding-top: 48px;
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
    flex: 1;
    min-height: 0;
  }

  .context-info-controls {
    height: 48px;
    border-bottom: 1px solid #777777;
    flex: 0 0 auto;
  }

  .data-treatments {
    flex: 1;
    min-height: 0;
    overflow-y: scroll;
  }
  .prediction-column {
    flex-basis: 100%;
    overflow-y: scroll;
  }

  .timestep-selector {
    border-bottom: 1px solid #666666;
  }

  .arrow {
    border: solid white;
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 3px;
  }

  .arrow.left {
    transform: rotate(135deg);
    -webkit-transform: rotate(135deg);
  }
</style>
