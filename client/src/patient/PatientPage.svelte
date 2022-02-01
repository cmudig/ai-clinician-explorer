<script>
  import { onMount } from 'svelte';

  let patientInfo = null;
  export let patientID = '';

  onMount(() => {
    if (!!patientID) loadPatientInfo(patientID);
  });

  function loadPatientInfo(patientID) {
    fetch('./api/patient/' + patientID)
      .then((d) => d.json())
      .then((d) => (patientInfo = d.result));
  }
</script>

<h1>Patient {patientID}</h1>
{#if !!patientInfo}
  {#each Object.keys(patientInfo) as key}
    <p>{key}: {patientInfo[key]}</p>
  {/each}
{/if}
