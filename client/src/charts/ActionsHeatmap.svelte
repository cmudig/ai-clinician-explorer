<script>
  import { LayerCake, Svg } from 'layercake';
  import { scaleLinear } from 'd3-scale';
  import AxisX from './AxisX.svelte';
  import AxisY from './AxisY.svelte';
  import Rect from './Rect.svelte';
  import { interpolateRdBu } from 'd3-scale-chromatic';
  import Colorbar from './Colorbar.svelte';

  export let data;
  export let vasopressorBins; // x axis labels
  export let fluidBins; // y axis labels

  export let valueDomain; // range of values should be mapped to the ends of the color map
  export let colorMap = interpolateRdBu;

  let visData;
  $: if (!!data && data.length == 25) {
    visData = data.map((d, i) => ({
      x: Math.floor(i / 5) - 0.5,
      y: (i % 5) - 0.5,
      z: d,
    }));
  }
</script>

<div class="actions-heatmap flex">
  {#if !!visData}
    <div class="heatmap-plot h-100 flex-auto">
      <LayerCake
        padding={{ top: 10, right: 10, bottom: 10, left: 10 }}
        x="x"
        y="y"
        z="z"
        extents={{ x: [-0.5, 4.5], y: [-0.5, 4.5] }}
        zScale={scaleLinear()}
        zDomain={valueDomain}
        zRange={[0, 1]}
        data={visData}
      >
        <Svg>
          <AxisX gridlines={false} ticks={[0, 1, 2, 3, 4]} />
          <AxisY gridlines={false} dyTick={4} />
          <Rect {colorMap} />
        </Svg>
      </LayerCake>
    </div>
    <div class="legend-container h-100">
      <Colorbar width={60} {colorMap} {valueDomain} numTicks={5} />
    </div>
  {/if}
</div>

<style>
  .actions-heatmap {
    height: 250px;
    width: 300px;
  }

  .legend-container {
    width: 60px;
  }
</style>
