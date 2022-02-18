<script>
  import * as d3 from 'd3';

  // add the legend now
  export let height = null;
  export let width = 50;

  export let colorMap;
  export let valueDomain = [-3, 3];

  export let numStops = 100;

  export let numTicks = 7;

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
    var out = [];
    var delta = (end - start) / (n - 1);

    var i = 0;
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
    var legendScale = d3
      .scaleLinear()
      .domain(valueDomain)
      .range([actualHeight - actualMargin.top - actualMargin.bottom, 0]);
    legendAxis = d3
      .axisRight()
      .scale(legendScale)
      .tickValues(linspace(valueDomain[0], valueDomain[1], numTicks))
      .tickFormat(d3.format('.2r'));
  }

  $: if (!!legendAxisContainer && !!legendAxis) {
    let sel = d3.select(legendAxisContainer);
    sel.selectAll('*').remove();
    sel.call(legendAxis);
  }
</script>

<div
  style="width: 100%; height: 100%;"
  bind:clientWidth={actualWidth}
  bind:clientHeight={actualHeight}
>
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
  </svg>
</div>
