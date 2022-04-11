<script>
  import ActionsHeatmap from '../charts/ActionsHeatmap.svelte';
  import {
    interpolateBlues,
    interpolateGreens,
    interpolateReds,
  } from 'd3-scale-chromatic';
  import Columns from '../utils/columns';
  import { getContext } from 'svelte';
  import FeatureImportanceChart from '../charts/FeatureImportanceChart.svelte';
  import Colorbar from '../charts/Colorbar.svelte';

  let { patient, modelInfo, modelPredictions, currentBloc } =
    getContext('patient');

  let modelQ;
  let physicianProb;
  let modelRecommendationIdx;
  let physicianActionIdx;
  let stateExplanations;
  let predictedState;
  $: if (!!$modelPredictions && $currentBloc > 0) {
    let pred = $modelPredictions[$currentBloc - 1];
    modelQ = pred.model_Q;
    predictedState = pred.state;
    physicianProb = pred.physician_prob;
    modelRecommendationIdx = pred.recommendation;
    physicianActionIdx = pred.actual_action;
    stateExplanations = pred.state_explanation;
  } else {
    modelQ = null;
    physicianProb = null;
    predictedState = null;
    modelRecommendationIdx = null;
    physicianActionIdx = null;
    stateExplanations = null;
  }

  let maxPhysicianProb = 1.0;
  let minModelQ = 0.0;
  let maxModelQ = 0.0;
  $: if (!!$modelPredictions) {
    // Compute thresholds for visualization based on all timesteps
    let maxProb = $modelPredictions[$currentBloc - 1].physician_prob
      // .map((p) => p.physician_prob)
      // .flat()
      .reduce((curr, p) => Math.max(curr, p), 0);
    maxPhysicianProb = Math.ceil(maxProb * 10) / 10;

    let minQ = $modelPredictions[$currentBloc - 1].model_Q
      // .map((p) => p.model_Q)
      // .flat()
      .reduce((curr, p) => (p != null ? Math.min(curr, p) : curr), 1e9);
    let rewardResolution = rewardVal / 100;
    minModelQ = Math.floor(minQ / rewardResolution) * rewardResolution;
    let maxQ = $modelPredictions[$currentBloc - 1].model_Q
      // .map((p) => p.model_Q)
      // .flat()
      .reduce((curr, p) => (p != null ? Math.max(curr, p) : curr), -1e9);
    maxModelQ = Math.ceil(maxQ / rewardResolution) * rewardResolution;
    console.log(minQ, maxQ, minModelQ, maxModelQ);
  }

  let rewardVal = null;
  let actionBins = null;
  $: if (!!$modelInfo) {
    rewardVal = $modelInfo.params.reward_val;
    actionBins = $modelInfo.actions.action_medians;
  }

  function fluidDose(action) {
    if (!!$modelInfo)
      return $modelInfo.actions.action_medians[0][
        Math.floor(action / $modelInfo.actions.n_action_bins)
      ];
    return 0;
  }

  function vasopressorDose(action) {
    if (!!$modelInfo)
      return $modelInfo.actions.action_medians[1][
        action % $modelInfo.actions.n_action_bins
      ];
    return 0;
  }

  let actualFluidDose;
  let actualVasopressorDose;
  $: if (!!$patient && $currentBloc > 0) {
    if ($currentBloc < $patient.timesteps.length) {
      actualFluidDose = $patient.timesteps[$currentBloc][
        Columns.C_INPUT_STEP
      ].value.toLocaleString({ maximumSignificantDigits: 3 });
      actualVasopressorDose = $patient.timesteps[$currentBloc][
        Columns.C_MAX_DOSE_VASO
      ].value.toLocaleString({ maximumSignificantDigits: 3 });
    } else {
      actualFluidDose = null;
      actualVasopressorDose = null;
    }
  }
</script>

<div class="flex justify-center ph4">
  {#if !!modelQ}
    <div class="flex-auto heatmap pr2">
      <h5 class="f5 tc b mb2">Predicted Treatment Values</h5>
      {#if !!$modelInfo && modelRecommendationIdx != null}
        <p class="f6 lh-copy above-plot">
          In the next epoch, AI Clinician recommends {#if vasopressorDose(modelRecommendationIdx) == 0}
            <strong>no vasopressor</strong>{:else}
            a vasopressor dosage of <strong
              >{vasopressorDose(modelRecommendationIdx).toLocaleString({
                maximumSignificantDigits: 3,
              })} ug/kg/min</strong
            >
          {/if} and {#if fluidDose(modelRecommendationIdx) == 0}
            <strong>no IV fluids</strong>
          {:else}
            <strong
              >{fluidDose(modelRecommendationIdx).toLocaleString({
                maximumSignificantDigits: 3,
              })} mL/4h</strong
            >
            IV fluids{/if}.
        </p>
      {/if}
      <ActionsHeatmap
        data={modelQ}
        valueDomain={!!rewardVal ? [minModelQ, maxModelQ] : [0, 100]}
        colorMap={interpolateBlues}
        fluidBins={actionBins != null ? actionBins[0] : null}
        vasopressorBins={actionBins != null ? actionBins[1] : null}
        nullColor="#f7f7f7"
        selectedAction={modelRecommendationIdx}
        formatTooltip={(d) =>
          modelQ[d.i] == null
            ? 'Insufficient data to\nestimate treatment value'
            : `Predicted treatment\nvalue: ${modelQ[d.i].toLocaleString({
                maximumSignificantDigits: 3,
              })}`}
      />
    </div>
  {/if}
  {#if !!physicianProb}
    <div class="flex-auto heatmap pl2">
      <h5 class="f5 tc b mb2">Clinician Probabilities</h5>
      {#if !!$modelInfo && physicianActionIdx != null}
        <p class="f6 lh-copy above-plot">
          {#if actualVasopressorDose == null || actualFluidDose == null}
            The clinician action in the next epoch is unavailable because this
            is the last available epoch.
          {:else}
            The next clinician action was {#if actualVasopressorDose == 0}
              <strong>no vasopressor</strong>{:else}
              a vasopressor dosage of <strong
                >{actualVasopressorDose} ug/kg/min</strong
              >
            {/if} and {#if actualFluidDose == 0}
              <strong>no IV fluids</strong>
            {:else}
              <strong>{actualFluidDose} mL/4h</strong>
              IV fluids{/if}.
          {/if}
        </p>
      {/if}
      <ActionsHeatmap
        data={physicianProb}
        valueDomain={[0, maxPhysicianProb]}
        colorMap={interpolateGreens}
        fluidBins={actionBins != null ? actionBins[0] : null}
        vasopressorBins={actionBins != null ? actionBins[1] : null}
        nullColor="#f7f7f7"
        selectedAction={physicianActionIdx}
        formatTooltip={(d) =>
          `Probability: ${physicianProb[d.i].toLocaleString({
            maximumSignificantDigits: 3,
          })}`}
      />
    </div>
  {/if}
</div>
{#if !!stateExplanations}
  <div class="ph4">
    <h5 class="f5 tc b mb2">Predicted Patient State</h5>
    {#if !!$modelInfo && physicianActionIdx != null}
      <p class="f6 lh-copy">
        The patient is predicted to be in state <strong>{predictedState}</strong
        >, which has been observed
        <strong>{stateExplanations.count} times</strong> in the dataset {#if stateExplanations.count_percentile < 50}
          (less than {(100 - stateExplanations.count_percentile).toFixed(0)}% of
          states).
        {:else}
          (more than {stateExplanations.count_percentile.toFixed(0)}% of
          states).
        {/if} Patients in this state are distinguished based on these features:
      </p>
    {/if}
    <div class="state-interpret-container flex">
      <div class="h-100 flex-auto">
        <FeatureImportanceChart
          importances={stateExplanations.feature_importances}
          deviations={stateExplanations.deviations}
        />
      </div>
      <div class="death-rate-bar h-100">
        <Colorbar
          colorMap={interpolateReds}
          valueDomain={[0, 0.8]}
          width={120}
          title="Mortality"
          margin={{ top: 42, left: 54, bottom: 32 }}
          markerValue={stateExplanations.mortality}
          markerText={(stateExplanations.mortality * 100).toFixed(1) + '%'}
        />
      </div>
    </div>
  </div>
{/if}

<style>
  .heatmap {
    max-width: 340px;
    flex-basis: 100%;
  }

  .above-plot {
    min-height: 64px;
  }

  .state-interpret-container {
    height: 240px;
  }

  .death-rate-bar {
    width: 120px;
    flex: 0 0 auto;
  }
</style>
