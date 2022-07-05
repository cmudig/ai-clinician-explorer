<script>
  import { fluidDose, vasopressorDose } from '../utils/helpers';
  import { getContext } from 'svelte';

  let { patient, modelInfo, modelPredictions, currentBloc } =
    getContext('patient');

  export let stimulus;

  let modelRecommendationIdx;
  let physicianActionIdx;
  let stateExplanations;
  let predictedState;
  $: if (!!$modelPredictions && $currentBloc > 0) {
    console.log('model predictions:', $modelPredictions);
    let pred = $modelPredictions[$currentBloc - 1];
    predictedState = pred.state;
    modelRecommendationIdx = pred.recommendation;
    physicianActionIdx = pred.actual_action;
    stateExplanations = pred.state_explanation;
  } else {
    predictedState = null;
    modelRecommendationIdx = null;
    physicianActionIdx = null;
    stateExplanations = null;
  }
</script>

{#if !!stimulus}
  {#if stimulus.show_ai_clinician}
    <div class="information ph4 lh-copy mv4">
      The AI Clinician recommends {#if vasopressorDose($modelInfo, modelRecommendationIdx) == 0}
        <strong>no vasopressor</strong>{:else}
        a vasopressor dosage of <strong
          >{vasopressorDose($modelInfo, modelRecommendationIdx).toLocaleString({
            maximumSignificantDigits: 3,
          })} ug/kg/min</strong
        >
      {/if} and {#if fluidDose($modelInfo, modelRecommendationIdx) == 0}
        <strong>no IV fluids</strong>
      {:else}
        <strong
          >{fluidDose($modelInfo, modelRecommendationIdx).toLocaleString({
            maximumSignificantDigits: 3,
          })} mL/4h</strong
        >
        IV fluids{/if}.
    </div>
  {/if}
{/if}
