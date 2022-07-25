<script>
  import { Html, LayerCake, Svg } from 'layercake';
  import AxisX from './AxisX.svelte';
  import AxisY from './AxisY.svelte';
  import Bar from './Bar.svelte';
  import { scaleBand, scaleLinear, scaleOrdinal } from 'd3-scale';
  import { interpolateGreens } from 'd3-scale-chromatic';
  import Tooltip from './Tooltip.svelte';
  import CategoricalLegend from './CategoricalLegend.svelte';
  import { FeatureNames } from '../utils/strings';
  import { fluidDose, vasopressorDose } from '../utils/helpers';
  import { getContext } from 'svelte';
  import Colorbar from './Colorbar.svelte';

  let { modelInfo } = getContext('patient');

  export let modelQ;
  export let actionCounts;
  export let numKeys = 5;

  let colorScale;
  let colorScheme = interpolateGreens;

  let featureNames = [];
  $: if (!!modelQ) {
    let keys = modelQ
      .map((q, i) => ({ i, q }))
      .sort((a, b) => b.q - a.q)
      .map((x) => x.i);
    featureNames = keys.slice(0, numKeys);
  }

  let barData;
  $: if (
    featureNames.length > 0 &&
    !!$modelInfo &&
    !!actionCounts &&
    !!modelQ
  ) {
    barData = featureNames.map((feature) => ({
      name: makeActionDescription(feature),
      feature,
      actionCount: actionCounts[feature],
      value: modelQ[feature],
    }));
    colorScale = scaleLinear()
      .domain([
        0,
        actionCounts.reduce(
          (curr, next) => (next != null ? Math.max(curr, next) : curr),
          0,
        ),
      ])
      .nice();
  } else {
    barData = null;
    colorScale = null;
  }

  let minQ = 100;
  let maxQ = 0;
  $: if (!!barData) {
    minQ = barData.reduce(
      (curr, p) => (p.value != null ? Math.min(curr, p.value) : curr),
      100,
    );
    minQ = Math.floor(minQ / 5) * 5;
    maxQ = barData.reduce(
      (curr, p) => (p.value != null ? Math.max(curr, p.value) : curr),
      0,
    );
    maxQ = Math.ceil(maxQ / 5) * 5;
  }

  function makeActionDescription(actionIdx) {
    console.log(actionIdx, vasopressorDose($modelInfo, actionIdx));
    let vaso =
      vasopressorDose($modelInfo, actionIdx) == 0
        ? 'no vasopressor'
        : `${
            Math.round(vasopressorDose($modelInfo, actionIdx) * 1000) / 1000
          } ug/kg/min vasopressor`;
    let fluid =
      fluidDose($modelInfo, actionIdx) == 0
        ? 'no IV fluids'
        : `${Math.round(fluidDose($modelInfo, actionIdx))} mL/4h fluids`;
    return vaso + ', ' + fluid;
  }

  let hoveredFeature = null;
  function makeTooltipText(d) {
    return `Treatment was observed ${d.actionCount} times for patients in this state`;
  }
</script>

<div class="w-100 h-100 pl5 pr3 flex">
  {#if !!barData && !!colorScale}
    <div class="h-100 flex-auto">
      <LayerCake
        padding={{ top: 20, bottom: 40, left: 120 }}
        x="value"
        y="name"
        yScale={scaleBand().paddingInner([0.05]).round(true)}
        xDomain={[minQ, maxQ]}
        yDomain={barData.map((b) => b.name).reverse()}
        data={barData}
        custom={{ hoveredGet: (d) => d.feature == hoveredFeature }}
      >
        <Svg>
          <AxisX
            gridlines={true}
            baseline={true}
            snapTicks={true}
            label="Score"
            ticks={5}
          />
          <AxisY gridlines={false} />
          <Bar
            fillFn={(d) => colorScheme(colorScale(d.actionCount))}
            on:hover={(e) =>
              (hoveredFeature = e.detail != null ? e.detail.feature : null)}
          />
        </Svg>
        <Html pointerEvents={false}>
          <Tooltip formatText={makeTooltipText} />
        </Html>
      </LayerCake>
    </div>
    <div class="legend-container h-100 ml1">
      <Colorbar
        width={50}
        colorMap={colorScheme}
        valueDomain={colorScale.domain()}
        ticks={colorScale.ticks(5)}
        margin={{ top: 40, bottom: 30, left: 20 }}
        title="# patients"
      />
    </div>
  {/if}
</div>

<style>
  .legend-container {
    width: 80px;
  }
</style>
