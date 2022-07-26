<script>
  import { getContext } from 'svelte';
  import Columns from '../utils/columns';
  import { Comorbidities } from '../utils/strings';
  import DataFeature from './DataFeature.svelte';
  import TextFeature from './TextFeature.svelte';

  let { patient, currentBloc } = getContext('patient');

  export let showOutcomes = true;
  export let showReadmission = true;
  export let showVentilation = false;
  export let showVasopressors = false;

  export let patientName = null;
</script>

<div class="pv2 ph2 bg-blue-gray white">
  {#if !!$patient}
    <h3 class="f3 fw3 pl2">
      {#if !!patientName}{patientName}{:else}Patient {$patient.icustayid}{/if}
    </h3>
    <table class="w-100">
      <DataFeature
        dark
        feature="Age/Gender"
        value="{$patient.age}-year-old {$patient.gender ? 'female' : 'male'}"
      />
      <TextFeature dark label="Comorbidities">
        {#if $patient.comorbidities.length == 0}
          <p class="mv2">None</p>
        {:else}
          {#each $patient.comorbidities as com}
            <p class="mv2">{Comorbidities[com]}</p>
          {/each}
        {/if}
        <!--{$patient.comorbidities.map((c) => Comorbidities[c]).join(', ')}-->
      </TextFeature>
      {#if showReadmission}
        <DataFeature
          dark
          feature="Is Re-Admission"
          value={$patient.re_admission ? 'Yes' : 'No'}
        />
      {/if}
      {#if showVentilation}
        <DataFeature
          dark
          feature="Currently Ventilated"
          value={$patient.timesteps[$currentBloc - 1][Columns.C_MECHVENT].value
            ? 'Yes'
            : 'No'}
        />
      {/if}
      {#if showVasopressors}
        <DataFeature
          dark
          feature="Receiving Vasopressors"
          value={$patient.timesteps[$currentBloc - 1][Columns.C_MAX_DOSE_VASO]
            .value > 0
            ? 'Yes'
            : 'No'}
        />
      {/if}
      {#if showOutcomes}
        <DataFeature
          dark
          feature="Discharge Status"
          value={$patient.died_in_hosp ? 'Death' : 'Alive'}
        />
        <DataFeature
          dark
          feature="ICU Length of Stay"
          value={($patient.num_timesteps * 4 > 24
            ? `${Math.floor(($patient.num_timesteps * 4) / 24)}d `
            : '') + `${($patient.num_timesteps * 4) % 24}h`}
        />
      {/if}
    </table>
  {/if}
</div>

<style>
  .comorbidity {
    display: inline-block;
    padding: 3px;
    border-radius: 4px;
    background-color: lightblue;
    border: 1px solid steelblue;
    margin: 3px 3px;
  }

  table {
    border-collapse: collapse;
  }
</style>
