<!--
  @component
  Generates a highlight that spans the Y-axis and a portion in the X direction.
 -->
<script>
  import { createEventDispatcher, getContext } from 'svelte';

  const dispatch = createEventDispatcher();
  const { data, x, xScale, yRange } = getContext('LayerCake');

  export let color = 'lightblue';
  export let highlightFn = null;
  export let padding = 2;

  let segments = [];

  $: if (!!highlightFn) {
    let xs = $data.map((d) => $x(d));
    segments = [];
    $data.forEach((d, i) => {
      if (highlightFn(d)) {
        let startX = ((i > 0 ? xs[i - 1] : xs[i]) + xs[i]) * 0.5;
        let endX = ((i < $data.length - 1 ? xs[i + 1] : xs[i]) + xs[i]) * 0.5;
        segments.push([startX, endX, d]);
      }
    });
  }
</script>

{#each segments as segment}
  <rect
    x={$xScale(segment[0])}
    y={$yRange[1] - padding}
    width={$xScale(segment[1]) - $xScale(segment[0])}
    height={$yRange[0] - $yRange[1] + 2 * padding}
    fill={color}
    on:mouseenter={() => dispatch('hover', segment[2])}
    on:mouseleave={() => dispatch('hover', null)}
  />
{/each}

<style>
</style>
