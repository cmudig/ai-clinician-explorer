<script>
  import { LayerCake, Svg } from 'layercake';
  import { scaleLinear } from 'd3-scale';
  import AxisX from './AxisX.svelte';
  import AxisY from './AxisY.svelte';
  import Rect from './Rect.svelte';

  export let data;

  let visData;
  $: if (!!data && data.length == 25) {
    visData = data.map((d, i) => ({
      x: Math.floor(i / 5),
      y: i % 5,
      z: d,
    }));
  }
</script>

<div class="actions-heatmap">
  {#if !!visData}
    <LayerCake
      padding={{ top: 10, right: 10, bottom: 10, left: 10 }}
      x="x"
      y="y"
      z="z"
      extents={{ x: [0, 5], y: [0, 5] }}
      zScale={scaleLinear()}
      zRange={[0, 1]}
      data={visData}
    >
      <Svg>
        <AxisX gridlines={false} />
        <AxisY gridlines={false} />
        <Rect />
      </Svg>
    </LayerCake>
  {/if}
</div>

<style>
  .actions-heatmap {
    height: 300px;
    width: 300px;
  }
</style>
