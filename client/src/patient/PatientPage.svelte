<script>
  import { onMount } from 'svelte';
  import DataStateList from './DataStateList.svelte';
  import Demographics from './Demographics.svelte';

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
          <div class="data-column flex-auto h-100">
            <DataStateList {patient} bloc={currentBloc} />
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
    border-right: 2px solid #bbbbbb;
  }

  main {
    padding-top: 80px;
  }

  .bg-navy-90 {
    background-color: #001b44e7;
  }

  .data-column {
    flex-basis: 50%;
    overflow-y: scroll;
    border-right: 1px solid #bbbbbb;
  }

  .prediction-column {
    flex-basis: 100%;
  }

  .timestep-selector {
    border-bottom: 1px solid #bbbbbb;
  }
</style>
