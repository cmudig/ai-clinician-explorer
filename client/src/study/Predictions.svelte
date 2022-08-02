<script>
  import { fluidDose, vasopressorDose } from '../utils/helpers';
  import { getContext } from 'svelte';
  import FeatureImportanceChart from '../charts/FeatureImportanceChart.svelte';
  import ActionValueChart from '../charts/ActionValueChart.svelte';

  let { patient, modelInfo, modelPredictions, currentBloc } =
    getContext('patient');

  let { modelName } = getContext('strings');

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
      {#if !stimulus.show_state_explanation && !stimulus.show_alternative_actions}<p
        >
          Your hospital has recently implemented a computerized decision support
          tool for sepsis called {@html $modelName}. {@html $modelName} analyzes
          patients’ electronic health records and uses an artificial intelligence-based
          algorithm to recommend fluids and vasopressor doses that optimize mortality
          based on historical data.
        </p>{/if}

      For this patient, {@html $modelName} is recommending
      {#if vasopressorDose($modelInfo, modelRecommendationIdx) == 0}
        <strong>no vasopressor</strong>{:else}
        a vasopressor at a dose of <strong
          >{Math.round(
            vasopressorDose($modelInfo, modelRecommendationIdx) * 1000,
          ) / 1000} ug/kg/min</strong
        > norepinephrine-equivalents
      {/if} and {#if fluidDose($modelInfo, modelRecommendationIdx) == 0}
        <strong>no IV fluids</strong>.
      {:else}
        IV fluids at a dose of
        <strong
          >{Math.round(fluidDose($modelInfo, modelRecommendationIdx))} mL</strong
        >
        over the next 4 hours.{/if}
    </div>
    {#if stimulus.show_state_explanation && !!stateExplanations}
      <div class="information ph4 lh-copy mv4">
        <strong>Why is {@html $modelName} making this recommendation?</strong>
        {@html $modelName} categorized this patient to one of 750 different states,
        and the recommended action above optimizes mortality for patients within
        this state. This patient is predicted to be in a state characterized by the
        following features:
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
        <p>
          <strong>Why is {@html $modelName} making this recommendation?</strong>
          {@html $modelName} estimated decision quality scores (from -100 to 100)
          to 25 possible IV fluid and vasopressor treatment levels, based on
          <strong>{stateExplanations.stay_count} patients</strong> that were
          observed in this state. A higher quality score means that patients
          receiving that treatment experienced better outcomes. {@html $modelName}
          is programmed to recommend the treatment with the highest quality score.
        </p>
        <p>
          Here are the quality scores for some possible treatment plans.
          Darker-colored bars indicate that a treatment action was taken more
          frequently for patients in this state, regardless of outcome.
        </p>
      </div>
      <div class="explanations-chart w-100">
        <ActionValueChart
          {modelQ}
          actionProbabilities={stateExplanations.physician_prob}
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
