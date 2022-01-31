<script>
  import { onMount } from 'svelte';

  let patients = [];

  onMount(() => {
    loadPatients();
  });

  function loadPatients() {
    fetch('./patient/')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }
</script>

<h1>MIMIC Data</h1>
{#each patients as patient}
  <p>Patient ID {patient.icustayid}</p>
{/each}
