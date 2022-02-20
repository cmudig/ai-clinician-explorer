<script>
  import { getContext } from 'svelte';

  const { data, x, y, xScale, yScale, custom } = getContext('LayerCake');

  export let formatText = null;
  export let dx = 0; // in plot coordinates
  export let dy = 0; // in plot coordinates

  export let verticalAlign = 'text-top';
  export let horizontalAlign = 'left';

  let padding = 8;

  let tooltipTexts = [];
  let tooltipBackgroundContainer;

  function formatTooltip(d) {
    if (!!formatText) return formatText(d);
    return Object.keys(d)
      .map((k) => `${k}: ${d[k]}`)
      .join('\n');
  }

  function getHovered(customVals, d) {
    let fn = (customVals || {}).hoveredGet || (() => false);
    return fn(d);
  }

  $: if (!!tooltipBackgroundContainer) {
    while (tooltipBackgroundContainer.firstChild) {
      tooltipBackgroundContainer.removeChild(
        tooltipBackgroundContainer.firstChild
      );
    }
    var svgns = 'http://www.w3.org/2000/svg';
    tooltipTexts.forEach((elem, i) => {
      if (!elem) return;
      var bounds = elem.getBBox();
      var bg = document.createElementNS(svgns, 'rect');
      var style = getComputedStyle(elem);
      bg.setAttribute('x', bounds.x - padding);
      bg.setAttribute('y', bounds.y - padding);
      bg.setAttribute('width', bounds.width + padding * 2);
      bg.setAttribute('height', bounds.height + padding * 2);
      bg.setAttribute('fill', style['background-color']);
      bg.setAttribute('rx', style['border-radius']);
      bg.setAttribute('stroke-width', style['border-top-width']);
      bg.setAttribute('stroke', style['border-top-color']);
      if (elem.hasAttribute('transform')) {
        bg.setAttribute('transform', elem.getAttribute('transform'));
      }
      tooltipBackgroundContainer.appendChild(bg);
    });
  }
</script>

<g>
  <g bind:this={tooltipBackgroundContainer} />
  {#each $data as d, i}
    {#if getHovered($custom, d)}
      <text
        bind:this={tooltipTexts[i]}
        y={$yScale($y(d) - dy) + padding}
        alignment-baseline={verticalAlign}
        text-anchor={horizontalAlign}
      >
        {#each formatTooltip(d).split('\n') as line, i}
          <tspan
            x={$xScale($x(d) + dx) +
              (horizontalAlign == 'middle' ? 0 : padding)}
            dy="1.2em">{line}</tspan
          >
        {/each}
      </text>
    {/if}
  {/each}
</g>

<style>
  text {
    background-color: white;
    border: 1px solid #bbb;
    fill: #333;
    font-weight: 300;
  }
</style>
