<script>
  export let patient;
</script>

<div class="pv2 ph3">
  {#if !!patient}
    <h3 class="f3 fw3">Patient {patient.icustayid}</h3>
    <p class="f5 mb1 mt0">
      {patient.age} y/o {patient.gender ? 'female' : 'male'}
    </p>
    <p class="f5 mb1 mt0">
      <strong>Elixhauser score:</strong>
      {patient.elixhauser}
    </p>
    <p class="f5 mb1 mt0">
      <strong>Length of stay:</strong>
      {patient.num_timesteps * 4} hrs
    </p>
    <p class="f5 mb1 mt0">
      <strong>Outcome:</strong>
      {#if patient.died_in_hosp}
        <span class="dark-red">Death</span>
      {:else}
        <span class="dark-blue">Discharge</span>
      {/if}
    </p>
  {/if}
</div>
