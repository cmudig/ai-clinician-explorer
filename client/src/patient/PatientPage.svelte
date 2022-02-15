<script>
  import { onMount } from 'svelte';
  import DataStateList from './DataStateList.svelte';
  import Demographics from './Demographics.svelte';

  import { LayerCake, Svg } from 'layercake';
  import Line from '../charts/Line.svelte';
  import Area from '../charts/Area.svelte';
  import AxisX from '../charts/AxisX.svelte';
  import AxisY from '../charts/AxisY.svelte';
  import Treatments from './Treatments.svelte';

  let patient = null;
  export let patientID = '';

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
          <div class="prediction-column flex-auto h-100" />
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
    flex-basis: 70%;
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
