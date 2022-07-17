<script>
  import { fluidDose, vasopressorDose } from '../utils/helpers';
  import { getContext } from 'svelte';
  import FeatureImportanceChart from '../charts/FeatureImportanceChart.svelte';
  import ActionValueChart from '../charts/ActionValueChart.svelte';

  let { patient, modelInfo, modelPredictions, currentBloc } =
    getContext('patient');

  export let stimulus;

  let modelRecommendationIdx;
  let modelQ;
  let physicianActionIdx;
  let stateExplanations;
  let predictedState;
  $: if (!!$modelPredictions && $currentBloc > 0) {
    console.log('model predictions:', $modelPredictions);
    let pred = $modelPredictions[$currentBloc - 1];
    modelQ = pred.model_Q;
    predictedState = pred.state;
    modelRecommendationIdx = pred.recommendation;
    physicianActionIdx = pred.actual_action;
    stateExplanations = pred.state_explanation;
    console.log(modelQ, modelRecommendationIdx, stateExplanations);
  } else {
    modelQ = null;
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
          >{Math.round(
            vasopressorDose($modelInfo, modelRecommendationIdx) * 1000,
          ) / 1000} ug/kg/min</strong
        >
      {/if} and {#if fluidDose($modelInfo, modelRecommendationIdx) == 0}
        <strong>no IV fluids</strong>
      {:else}
        <strong
          >{Math.round(fluidDose($modelInfo, modelRecommendationIdx))} mL/4h</strong
        >
        IV fluids{/if}.
    </div>
    {#if stimulus.show_state_explanation && !!stateExplanations}
      <div class="information ph4 lh-copy mv4">
        Out of 750 possible states, AI Clinician categorized this patient as
        currently in a state characterized by the following features:
      </div>
      <div class="explanations-chart w-100">
        <FeatureImportanceChart
          importances={stateExplanations.feature_importances}
          deviations={stateExplanations.deviations}
          numKeys={5}
        />
      </div>
    {/if}
    {#if stimulus.show_alternative_actions && !!modelQ && !!stateExplanations}
      <div class="information ph4 lh-copy mv4">
        The AI Clinician assigned decision quality scores (from -100 to 100) to
        25 possible IV fluid and vasopressor treatment levels. These are the
        highest-rated treatment levels:
      </div>
      <div class="explanations-chart w-100">
        <ActionValueChart
          {modelQ}
          actionCounts={stateExplanations.action_counts}
        />
      </div>
    {/if}
  {/if}
{/if}

<style>
  .explanations-chart {
    height: 240px;
    padding: 0 80px;
  }
</style>
