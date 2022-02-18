<script>
  import { onMount } from 'svelte';
  import DataStateList from './DataStateList.svelte';
  import Demographics from './Demographics.svelte';

  import Treatments from './Treatments.svelte';
  import ActionsHeatmap from '../charts/ActionsHeatmap.svelte';
  import { interpolateGreens } from 'd3-scale-chromatic';

  let patient = null;
  export let patientID = '';
  export let modelID = 'mimiciv_220217_best';

  let modelInfo;

  let modelQ;
  let physicianProb;

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

  $: if (!!patient && currentBloc > 0 && !!modelID) {
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
      modelInfo = response;
      console.log('model info:', modelInfo);
    } catch (e) {
      console.log('error loading model info:', e);
    }
  }

  async function loadModelPrediction(patientInfo, bloc) {
    let state = {};
    let ts = patientInfo.timesteps[bloc - 1];
    Object.keys(ts).forEach((key) => {
      if (typeof ts[key] == 'number') state[key] = ts[key];
      else if (ts[key].hasOwnProperty('value')) state[key] = ts[key].value;
    });
    Object.keys(patientInfo).forEach((key) => {
      if (key != 'timesteps') state[key] = patientInfo[key];
    });
    let body = { state };
    console.log('body:', body);
    try {
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
        return;
      }
      response = await response.json();
      console.log('response', response);
      modelQ = response.model_Q;
      physicianProb = response.physician_prob;
    } catch (e) {
      console.log('error loading model prediction:', e);
    }
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv3 pv4-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked">
    <a class="link dim white dib mr3" href="/" title="Home">Home</a>
  </nav>
</header>
<main class="pa0 h-100">
  <div class="flex align-stretch h-100">
    <div class="sidebar">
      <Demographics {patient} />
    </div>
    {#if !!patient}
      <div class="patient-info-container flex-auto flex flex-column h-100">
        <div
          class="timestep-selector flex justify-center items-center w-100 pv3"
        >
          <span class="f6 b pb0 mr3"
            >Timestep: Hour {(currentBloc - 1) * 4 + 1}</span
          >
          <input
            class="ph0"
            type="range"
            width="200"
            bind:value={currentBloc}
            min={1}
            max={patient.timesteps.length}
            step={1}
          />
        </div>
        <div class="patient-info flex flex-auto">
          <div class="data-column flex flex-column flex-auto h-100">
            <div class="data-state flex-auto">
              <DataStateList {patient} bloc={currentBloc} />
            </div>
            <div class="data-treatments">
              <Treatments {patient} bloc={currentBloc} />
            </div>
          </div>
          <div class="prediction-column flex-auto h-100">
            {#if !!modelQ}
              <ActionsHeatmap data={modelQ} valueDomain={[-100, 100]} />
            {/if}
            {#if !!physicianProb}
              <ActionsHeatmap
                data={physicianProb}
                valueDomain={[0, 1]}
                colorMap={interpolateGreens}
              />
            {/if}
          </div>
        </div>
      </div>
    {/if}
  </div>
</main>

<style>
  .sidebar {
    width: 300px;
    border-right: 1px solid #777777;
    overflow-y: scroll;
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
</style>
