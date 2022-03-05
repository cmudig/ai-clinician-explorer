<script>
  import { onMount } from 'svelte';

  let patients = [];

  onMount(() => {
    loadPatients();
  });

  function loadPatients() {
    fetch('./api/patient?size=100')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }
</script>

<h1 class="f1 fw3">MIMIC Data</h1>
{#each patients as patient}
  <p>
    <a class="link blue dim" href="/patient?id={patient.icustayid}"
      >Patient ID {patient.icustayid}</a
    >
  </p>
{/each}
