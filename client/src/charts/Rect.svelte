<!--
  @component
  Generates SVG rectangles for each data point.
 -->
<script>
  import { getContext } from 'svelte';

  import { interpolateRdBu } from 'd3-scale-chromatic';

  const { data, xGet, yGet, zGet, xScale, yScale } = getContext('LayerCake');

  export let colorMap = interpolateRdBu;

  /** @type {String} [stroke='#ab00d6'] - The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let stroke = '#ab00d6';

  export let xBinSize = 1;
  export let yBinSize = 1;

  export let padding = 2;

  let width;
  let height;

  $: width = Math.abs($xScale(xBinSize) - $xScale(0));
  $: height = Math.abs($yScale(yBinSize) - $yScale(0));
  /*let path;

  $: {
    // Generate path, omitting null or undefined values
    path = '';
    let lastUndefined = true;
    $data.forEach((d) => {
      let y = $yGet(d);
      if (y == null || y == undefined) lastUndefined = true;
      else {
        if (lastUndefined) path += `M${$xGet(d)} ${y}`;
        else path += `L${$xGet(d)} ${y}`;
        lastUndefined = false;
      }
    });
  }*/
</script>

{#each $data as d}
  <rect
    x={$xGet(d) + padding / 2}
    y={$yGet(d) - height + padding / 2}
    width={width - padding}
    height={height - padding}
    style="fill:{colorMap($zGet(d))}"
  />
{/each}

<style>
  .path-line {
    fill: none;
    stroke-linejoin: round;
    stroke-linecap: round;
    stroke-width: 2;
  }
</style>
