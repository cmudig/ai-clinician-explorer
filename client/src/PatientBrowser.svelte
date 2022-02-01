<script>
  import { onMount } from 'svelte';

  let patients = [];

  onMount(() => {
    loadPatients();
  });

  function loadPatients() {
    fetch('./api/patient/')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }
</script>

<h1>MIMIC Data</h1>
{#each patients as patient}
  <p>
    <a href="/patient?id={patient.icustayid}">Patient ID {patient.icustayid}</a>
  </p>
{/each}
