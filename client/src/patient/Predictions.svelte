<script>
  import ActionsHeatmap from '../charts/ActionsHeatmap.svelte';
  import { interpolateBlues, interpolateGreens } from 'd3-scale-chromatic';
  import Columns from '../utils/columns';
  import { getContext } from 'svelte';

  let { patient, modelInfo, modelPredictions, currentBloc } =
    getContext('patient');

  let modelQ;
  let physicianProb;
  let modelRecommendationIdx;
  let physicianActionIdx;
  $: if (!!$modelPredictions && $currentBloc > 0) {
    let pred = $modelPredictions[$currentBloc - 1];
    modelQ = pred.model_Q;
    physicianProb = pred.physician_prob;
    modelRecommendationIdx = pred.recommendation;
    physicianActionIdx = pred.actual_action;
  } else {
    modelQ = null;
    physicianProb = null;
    modelRecommendationIdx = null;
    physicianActionIdx = null;
  }

  let maxPhysicianProb = 1.0;
  let minModelQ = 0.0;
  $: if (!!$modelPredictions) {
    // Compute thresholds for visualization based on all timesteps
    let maxProb = $modelPredictions
      .map((p) => p.physician_prob)
      .flat()
      .reduce((curr, p) => Math.max(curr, p), 0);
    maxPhysicianProb = Math.ceil(maxProb * 10) / 10;

    let minQ = $modelPredictions
      .map((p) => p.model_Q)
      .flat()
      .reduce((curr, p) => (p != null ? Math.min(curr, p) : curr), 1e9);
    let rewardResolution = rewardVal / 10;
    minModelQ = Math.floor(minQ / rewardResolution) * rewardResolution;
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
    // Fix timestep issue in AI Clinician
    actualFluidDose = $patient.timesteps[$currentBloc - 1][
      Columns.C_INPUT_STEP
    ].value.toLocaleString({ maximumSignificantDigits: 3 });
    actualVasopressorDose = $patient.timesteps[$currentBloc - 1][
      Columns.C_MAX_DOSE_VASO
    ].value.toLocaleString({ maximumSignificantDigits: 3 });
  }
</script>

{#if !!modelQ}
  <div class="flex-auto heatmap pr2">
    <h5 class="f5 tc b mb2">Predicted Treatment Values</h5>
    {#if !!$modelInfo && modelRecommendationIdx != null}
      <p class="f6 lh-copy above-plot">
        AI Clinician recommends {#if vasopressorDose(modelRecommendationIdx) == 0}
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
      valueDomain={!!rewardVal ? [minModelQ, rewardVal] : [0, 100]}
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
        The clinician action was {#if actualVasopressorDose == 0}
          <strong>no vasopressor</strong>{:else}
          a vasopressor dosage of <strong
            >{actualVasopressorDose} ug/kg/min</strong
          >
        {/if} and {#if actualFluidDose == 0}
          <strong>no IV fluids</strong>
        {:else}
          <strong>{actualFluidDose} mL/4h</strong>
          IV fluids{/if}.
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

<style>
  .heatmap {
    max-width: 340px;
    flex-basis: 100%;
  }

  .above-plot {
    min-height: 60px;
  }
</style>