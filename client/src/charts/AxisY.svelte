<!--
  @component
  Generates an HTML y-axis.
 -->
<script>
  import { getContext } from 'svelte';

  const { padding, xRange, yScale, width, height } = getContext('LayerCake');

  /** @type {Boolean} [gridlines=true] - Extend lines from the ticks into the chart space */
  export let gridlines = true;

  /** @type {Boolean} [tickMarks=false] - Show a vertical mark for each tick. */
  export let tickMarks = false;

  /** @type {Function} [formatTick=d => d] - A function that passes the current tick value and expects a nicely formatted value in return. */
  export let formatTick = (d) => d;

  /** @type {Number|Array|Function} [ticks=4] - If this is a number, it passes that along to the [d3Scale.ticks](https://github.com/d3/d3-scale) function. If this is an array, hardcodes the ticks to those values. If it's a function, passes along the default tick values and expects an array of tick values in return. */
  export let ticks = 4;

  /** @type {Number} [xTick=0] - How far over to position the text marker. */
  export let xTick = 0;

  /** @type {Number} [yTick=0] - How far up and down to position the text marker. */
  export let yTick = 0;

  /** @type {Number} [dxTick=0] - Any optional value passed to the `dx` attribute on the text marker and tick mark (if visible). This is ignored on the text marker if your scale is ordinal. */
  export let dxTick = 0;

  /** @type {Number} [dyTick=-4] - Any optional value passed to the `dy` attribute on the text marker and tick mark (if visible). This is ignored on the text marker if your scale is ordinal. */
  export let dyTick = -4;

  /** @type {String} [textAnchor='start'] The CSS `text-anchor` passed to the label. This is automatically set to "end" if the scale has a bandwidth method, like in ordinal scales. */
  export let textAnchor = 'start';

  export let color = '#333';

  export let label;

  $: isBandwidth = typeof $yScale.bandwidth === 'function';

  $: tickVals = Array.isArray(ticks)
    ? ticks
    : isBandwidth
    ? $yScale.domain()
    : typeof ticks === 'function'
    ? ticks($yScale.ticks())
    : $yScale.ticks(ticks);
</script>

<g class="axis y-axis" transform="translate({-$padding.left}, 0)">
  {#each tickVals as tick}
    <g
      class="tick tick-{tick}"
      transform="translate({$xRange[0] + $padding.left - 4}, {$yScale(tick)})"
    >
      {#if gridlines !== false}
        <line
          class="gridline"
          x2="100%"
          y1={yTick + (isBandwidth ? $yScale.bandwidth() / 2 : 0)}
          y2={yTick + (isBandwidth ? $yScale.bandwidth() / 2 : 0)}
        />
      {/if}
      {#if tickMarks === true}
        <line
          class="tick-mark"
          x1="0"
          x2={isBandwidth ? -6 : 6}
          y1={yTick + (isBandwidth ? $yScale.bandwidth() / 2 : 0)}
          y2={yTick + (isBandwidth ? $yScale.bandwidth() / 2 : 0)}
        />
      {/if}
      <text
        x={xTick}
        y={yTick + (isBandwidth ? $yScale.bandwidth() / 2 : 0)}
        dx={isBandwidth ? -9 : dxTick}
        dy={isBandwidth ? 4 : dyTick}
        style="text-anchor:{isBandwidth ? 'end' : textAnchor}; fill: {color};"
        >{formatTick(tick)}</text
      >
    </g>
  {/each}
  {#if !!label}
    <g class="axis-label" transform="translate(-18, {$height}) rotate(-90)">
      <text x={$height * 0.5} y={0} text-anchor="middle" style="fill: {color};"
        >{label}</text
      >
    </g>
  {/if}
</g>

<style>
  .tick {
    font-size: 0.725em;
    font-weight: 400;
  }

  .tick line {
    stroke: #aaa;
  }
  .tick .gridline {
    stroke-dasharray: 2;
  }

  .tick.tick-0 line {
    stroke-dasharray: 0;
  }

  .axis-label {
    font-size: 0.8em;
    fill: #333;
    font-weight: 500;
  }
</style>
