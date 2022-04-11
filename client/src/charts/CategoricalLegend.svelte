<script>
  import { getContext } from 'svelte';
  import { getTextWidth } from '../utils/helpers';

  const { width, height } = getContext('LayerCake');

  export let scale = null;
  export let anchor = 'bottom right'; // 'top left', 'top right', 'bottom left', 'bottom right'
  export let shape = 'square'; // 'square', 'circle'

  export let inset = {};
  let defaultInset = { x: 12, y: 12 };
  let actualInset;
  $: actualInset = {
    x: inset.x != null ? inset.x : defaultInset.x,
    y: inset.y != null ? inset.y : defaultInset.y,
  };

  export let padding = 6;
  let textWidth = 0;
  let legendWidth = 0;
  let legendHeight = 0;

  $: if (!!scale) {
    let w = scale
      .domain()
      .map((d) => getTextWidth(d, '10pt sans-serif'))
      .reduce((curr, next) => Math.max(curr, next), 0);
    console.log(scale.domain().join('\n'), w);
    textWidth = w;
  }

  const itemSpacing = 18;
  const iconDimension = 12;
  const iconSpacing = 6;

  $: legendWidth = textWidth + iconDimension + iconSpacing + padding * 2;
  $: legendHeight =
    itemSpacing * (scale != null ? scale.domain().length : 0) + padding * 2;

  function getX(i, containerWidth) {
    if (anchor.endsWith('left')) return actualInset.x + padding;
    else if (anchor.endsWith('right'))
      return containerWidth - textWidth - actualInset.x - padding;
    console.error('unsupported anchor value ' + anchor);
  }

  function getY(i, containerHeight) {
    if (anchor.startsWith('top'))
      return actualInset.y + padding + itemSpacing * i;
    else if (anchor.startsWith('bottom'))
      return (
        containerHeight -
        actualInset.y -
        padding -
        itemSpacing * (scale.domain().length - i - 0.5)
      );
    console.error('unsupported anchor value ' + anchor);
  }
</script>

{#if !!scale}
  <g class="legend-container">
    <rect
      x={getX(0, $width) - padding}
      y={getY(0, $height) - itemSpacing / 2 - padding}
      rx="3"
      ry="3"
      width={legendWidth}
      height={legendHeight}
      class="legend-background"
    />
    <!-- <rect
      x={getX(0, $width)}
      y={getY(0, $height) - itemSpacing / 2}
      width={textWidth + iconDimension + iconSpacing}
      height={itemSpacing * scale.domain().length}
      fill="red"
    /> -->
    {#each scale.domain() as d, i}
      {#if shape == 'square'}
        <rect
          x={getX(0, $width)}
          y={getY(i, $height) - iconDimension / 2}
          width={iconDimension}
          height={iconDimension}
          fill={scale(d)}
        />
      {:else if shape == 'circle'}
        <ellipse
          cx={getX(0, $width) + iconDimension / 2}
          cy={getY(i, $height)}
          rx={iconDimension / 2}
          ry={iconDimension / 2}
          fill={scale(d)}
        />
      {/if}
      <text
        class="legend-label"
        x={getX(i, $width) + iconDimension + iconSpacing}
        y={getY(i, $height)}
        alignment-baseline="middle">{d}</text
      >
    {/each}
  </g>
{/if}

<style>
  .legend-label {
    font-size: 10pt;
    color: #333;
  }

  .legend-background {
    stroke: #ccc;
    fill: white;
  }
</style>
