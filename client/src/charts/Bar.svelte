<!--
  @component
  Generates an SVG bar chart.
 -->
<script>
  import { createEventDispatcher, getContext } from 'svelte';

  const dispatch = createEventDispatcher();

  const { data, x, xGet, yGet, xScale, yScale, xDomain } =
    getContext('LayerCake');

  /** @type {String} [fill='#00bbff'] - The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let fill = '#00bbff';

  export let fillFn = null;
</script>

<g class="bar-group">
  {#each $data as d, i}
    {#if $x(d) < 0}
      <rect
        class="group-rect"
        data-id={i}
        x={$xGet(d)}
        y={$yGet(d)}
        height={$yScale.bandwidth()}
        width={$xScale($xDomain[0]) - $xGet(d)}
        fill={!!fillFn ? fillFn(d) : fill}
        on:mouseenter={() => dispatch('hover', d)}
        on:mouseleave={() => dispatch('hover', null)}
      />
    {:else}
      <rect
        class="group-rect"
        data-id={i}
        x={$xScale($xDomain[0])}
        y={$yGet(d)}
        height={$yScale.bandwidth()}
        width={$xGet(d) - $xScale($xDomain[0])}
        fill={!!fillFn ? fillFn(d) : fill}
        on:mouseenter={() => dispatch('hover', d)}
        on:mouseleave={() => dispatch('hover', null)}
      />
    {/if}
  {/each}
</g>
