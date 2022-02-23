<script>
  import { getContext } from 'svelte';

  const { data, x, y, xScale, yScale, custom } = getContext('LayerCake');

  export let formatText = null;
  export let dx = null; // in plot coordinates
  export let dy = null; // in plot coordinates

  let padding = 8;

  function formatTooltip(d) {
    if (!!formatText) return formatText(d);
    return Object.keys(d).map((k) => `<p><strong>${k}:</strong> ${d[k]}</p>`);
  }

  function getHovered(customVals, d) {
    let fn = (customVals || {}).hoveredGet || (() => false);
    return fn(d);
  }
</script>

{#each $data as d, i}
  {#if getHovered($custom, d)}
    <div
      class="tooltip"
      style="left: {$xScale(dx != null ? $x(d) + dx : $x(d))}px; top: {$yScale(
        dy != null ? $y(d) - dy : $y(d)
      ) + padding}px; padding: {padding}px;"
    >
      {@html formatTooltip(d)}
    </div>
  {/if}
{/each}

<style>
  .tooltip {
    background-color: white;
    z-index: 100;
    border: 1px solid #bbb;
    color: #333;
    font-weight: 300;
    position: absolute;
  }
</style>
