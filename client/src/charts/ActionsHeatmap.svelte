<script>
  import { LayerCake, Svg } from 'layercake';
  import { scaleLinear } from 'd3-scale';
  import AxisX from './AxisX.svelte';
  import AxisY from './AxisY.svelte';
  import Rect from './Rect.svelte';
  import { interpolateRdBu } from 'd3-scale-chromatic';
  import Colorbar from './Colorbar.svelte';
  import Tooltip from './Tooltip.svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let data;
  export let vasopressorBins; // x axis labels
  export let fluidBins; // y axis labels
  export let formatTooltip; // function that takes a data point and returns a string describing it

  export let valueDomain; // range of values should be mapped to the ends of the color map
  export let colorMap = interpolateRdBu;
  export let nullColor = 'black';

  export let selectedAction = null;

  let hoveredAction = null;

  let visData;
  $: if (!!data && data.length == 25) {
    visData = data.map((d, i) => ({
      i,
      x: Math.floor(i / 5) - 0.5,
      y: (i % 5) - 0.5,
      z: d,
    }));
  }

  function formatTicks(bins) {
    return (b) =>
      bins[b].toLocaleString('en-US', {
        maximumSignificantDigits: 3,
        useGrouping: true,
      });
  }
</script>

<div class="actions-heatmap flex ">
  {#if !!visData}
    <div class="heatmap-plot h-100 flex-auto ml3">
      <LayerCake
        padding={{ top: 10, right: 10, bottom: 10, left: 35 }}
        x="x"
        y="y"
        z="z"
        extents={{ x: [-0.5, 4.5], y: [-0.5, 4.5] }}
        zScale={scaleLinear()}
        zDomain={valueDomain}
        zRange={[0, 1]}
        data={visData}
        custom={{
          selectedGet:
            selectedAction != null ? (d) => d.i == selectedAction : null,
          hoveredGet: (d) => d.i == hoveredAction,
        }}
      >
        <Svg>
          <AxisX
            gridlines={false}
            ticks={[0, 1, 2, 3, 4]}
            formatTick={formatTicks(fluidBins)}
            label="IV Fluid (mL/4h)"
          />
          <AxisY
            gridlines={false}
            dyTick={4}
            formatTick={formatTicks(vasopressorBins)}
            label="Vasopressor (ug/kg/min norep)"
            textAnchor="end"
          />
          <Rect
            {colorMap}
            {nullColor}
            on:hover={(e) => (hoveredAction = e.detail ? e.detail.i : null)}
            on:click={(e) => dispatch('select', e.detail.i)}
          />
          <Tooltip
            formatText={formatTooltip}
            dx={0.5}
            horizontalAlign="middle"
          />
        </Svg>
      </LayerCake>
    </div>
    <div class="legend-container h-100">
      <Colorbar width={60} {colorMap} {valueDomain} numTicks={6} />
    </div>
  {/if}
</div>

<style>
  .actions-heatmap {
    height: 220px;
  }

  .heatmap-plot {
    z-index: 10;
  }

  .legend-container {
    width: 60px;
  }
</style>
