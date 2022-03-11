<script>
  import { getContext } from 'svelte';
  import { Comorbidities } from '../utils/strings';
  import DataFeature from './DataFeature.svelte';
  import TextFeature from './TextFeature.svelte';

  let { patient } = getContext('patient');
</script>

<div class="pv2 ph2 bg-blue-gray white">
  {#if !!$patient}
    <h3 class="f3 fw3 pl2">Patient {$patient.icustayid}</h3>
    <table class="w-100">
      <DataFeature
        dark
        feature="Age/Gender"
        value="{$patient.age} y/o {$patient.gender ? 'female' : 'male'}"
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
      <DataFeature
        dark
        feature="Is Re-Admission"
        value={$patient.re_admission ? 'Yes' : 'No'}
      />
      <DataFeature
        dark
        feature="Discharge Status"
        value={$patient.died_in_hosp ? 'Death' : 'Discharge'}
      />
      <DataFeature
        dark
        feature="ICU Length of Stay"
        value={$patient.num_timesteps * 4}
        unit="hrs"
      />
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
