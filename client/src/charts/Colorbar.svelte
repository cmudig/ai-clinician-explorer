<script>
  import * as d3 from 'd3';

  // add the legend now
  export let height = null;
  export let width = 50;

  export let colorMap;
  export let valueDomain = [-3, 3];

  export let numStops = 100;

  export let numTicks = 7;
  export let ticks = null;

  export let markerValue = null;
  export let markerText = null;

  export let title = null;

  let gradientID = 'gradient' + Math.floor(Math.random() * 999999);

  export let margin = {};
  let defaultMargin = { top: 20, bottom: 20, left: 5, right: 40 };

  let actualMargin;
  $: actualMargin = {
    top: margin.top != null ? margin.top : defaultMargin.top,
    bottom: margin.bottom != null ? margin.bottom : defaultMargin.bottom,
    left: margin.left != null ? margin.left : defaultMargin.left,
    right: margin.right != null ? margin.right : defaultMargin.right,
  };

  let actualWidth;
  let actualHeight;

  // $: if (!!colorMap && !!legendSvg) updateColourScale(colorMap);

  function linspace(start, end, n) {
    let out = [];
    let delta = (end - start) / (n - 1);

    let i = 0;
    while (i < n - 1) {
      out.push(start + i * delta);
      i++;
    }

    out.push(end);
    return out;
  }

  let legendAxis;
  let legendAxisContainer;

  $: {
    let legendScale = d3
      .scaleLinear()
      .domain(valueDomain)
      .range([actualHeight - actualMargin.top - actualMargin.bottom, 0]);
    legendAxis = d3.axisRight().scale(legendScale);
    if (!!ticks) legendAxis = legendAxis.tickValues(ticks);
    else
      legendAxis = legendAxis
        .tickValues(linspace(valueDomain[0], valueDomain[1], numTicks))
        .tickFormat(d3.format('.3g'));
  }

  $: if (!!legendAxisContainer && !!legendAxis) {
    let sel = d3.select(legendAxisContainer);
    sel.selectAll('*').remove();
    sel.call(legendAxis);
  }

  let markerX;
  let markerY;
  let markerWidth = 18;
  let markerHeight = 5;
  $: if (markerValue != null && !!actualHeight) {
    markerX = actualMargin.left + markerWidth * 0.75;
    let height = actualHeight - actualMargin.top - actualMargin.bottom;
    markerY =
      actualMargin.top +
      height *
        (1.0 -
          (markerValue - valueDomain[0]) / (valueDomain[1] - valueDomain[0]));
  } else {
    markerX = null;
    markerY = null;
  }
</script>

<div
  style="width: 100%; height: 100%;"
  bind:clientWidth={actualWidth}
  bind:clientHeight={actualHeight}
>
  {#if !!title}
    <p class="colorbar-title">{title}</p>
  {/if}
  <svg
    style="width: 100%; height: 100%;"
    transform="translate({actualMargin.left}px, {actualMargin.top}px)"
  >
    <defs>
      <linearGradient
        id={gradientID}
        x1="0%"
        y1="100%"
        x2="0%"
        y2="0%"
        spreadMethod="pad"
      >
        {#each linspace(0, 1, numStops) as stop}
          <stop
            offset={(stop * 100).toFixed(0) + '%'}
            stop-color={colorMap(stop)}
            stop-opacity={1}
          />
        {/each}
      </linearGradient>
    </defs>
    <rect
      x={actualMargin.left}
      y={actualMargin.top}
      style="width: calc(100% - {actualMargin.left +
        actualMargin.right}px); height: calc(100% - {actualMargin.top +
        actualMargin.bottom}px); fill: url('#{gradientID}');"
    />
    <g
      bind:this={legendAxisContainer}
      x={0}
      y={0}
      width="100%"
      height="100%"
      style="transform: translate(calc(100% - {actualMargin.right -
        2}px), {actualMargin.top}px);"
    />
    {#if markerValue != null && !!markerX && !!markerY}
      <polygon
        points="{markerX},{markerY} {markerX - markerWidth},{markerY -
          markerHeight} {markerX - markerWidth},{markerY + markerHeight}"
        style="fill:#333;stroke:white;stroke-width:2"
      />
      {#if !!markerText}
        <text
          x={markerX - markerWidth - 2}
          y={markerY}
          text-anchor="end"
          alignment-baseline="central"
          class="marker-text">{markerText}</text
        >
      {/if}
    {/if}
  </svg>
</div>

<style>
  .colorbar-title {
    position: absolute;
    text-align: center;
    top: 0;
    left: 0;
    width: 100%;
    font-size: 0.8em;
    fill: #333;
    font-weight: 500;
  }

  .marker-text {
    fill: #333;
    font-weight: 500;
  }
</style>
