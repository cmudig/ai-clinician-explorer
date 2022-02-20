<script>
  import { getContext } from 'svelte';
  import { Comorbidities } from '../utils/strings';
  import DataFeature from './DataFeature.svelte';
  import TextFeature from './TextFeature.svelte';

  let { patient } = getContext('patient');
</script>

<div class="pv2 ph3 bg-blue-gray white">
  {#if !!$patient}
    <h3 class="f3 fw3 pl2">Patient {$patient.icustayid}</h3>
    <DataFeature
      dark
      feature="Profile"
      value="{$patient.age} y/o {$patient.gender ? 'female' : 'male'}"
    />
    <DataFeature dark feature="Height" value={$patient.Height_cm} unit="cm" />
    <DataFeature
      dark
      feature="Length of Stay"
      value={$patient.num_timesteps * 4}
      unit="hrs"
    />
    <DataFeature
      dark
      feature="Outcome"
      value={$patient.died_in_hosp ? 'Death' : 'Discharge'}
    />
    <TextFeature dark label="Comorbidities">
      {#each $patient.comorbidities as com}
        <p class="mv2">{Comorbidities[com]}</p>
      {/each}
      <!--{$patient.comorbidities.map((c) => Comorbidities[c]).join(', ')}-->
    </TextFeature>
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
</style>
