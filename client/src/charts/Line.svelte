<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script>
  import { getContext } from 'svelte';

  const { data, x, y, xScale, yScale } = getContext('LayerCake');

  /** @type {String} [stroke='#ab00d6'] - The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let stroke = '#ab00d6';

  export let dashFn = null;

  let paths = [];

  $: {
    // Generate path, omitting null or undefined values
    let segments = $data.map((d, i) => {
      let yCoord = $y(d);
      if (yCoord == null || yCoord == undefined)
        return {
          startX: null,
          endX: null,
          startY: null,
          endY: null,
          dash: null,
        };

      let previousX = i > 0 ? $x($data[i - 1]) : null;
      let nextX = i < $data.length - 1 ? $x($data[i + 1]) : null;
      let startX =
        ((previousX != null ? previousX : $x($data[i])) + $x($data[i])) * 0.5;
      let endX = ((nextX != null ? nextX : $x($data[i])) + $x($data[i])) * 0.5;
      let previousY = i > 0 ? $y($data[i - 1]) : null;
      let nextY = i < $data.length - 1 ? $y($data[i + 1]) : null;
      let startY =
        ((previousY != null ? previousY : $y($data[i])) + $y($data[i])) * 0.5;
      let endY = ((nextY != null ? nextY : $y($data[i])) + $y($data[i])) * 0.5;
      let dash = !!dashFn && dashFn(d);
      return {
        startX,
        endX,
        startY,
        endY,
        dash,
      };
    });

    paths = [{ path: '', dash: false }];
    segments.forEach(({ startX, endX, startY, endY, dash }) => {
      if (startX == null) {
        paths.push({ path: '', dash: false });
      } else {
        let startDesc = `${$xScale(startX)} ${$yScale(startY)}`;
        if (dash != paths[paths.length - 1].dash) {
          // Connect with a differently-dashed line to the last point
          paths.push({ path: `M${startDesc}`, dash });
        }
        let path = paths[paths.length - 1];
        let endDesc = `${$xScale(endX)} ${$yScale(endY)}`;
        if (path.path.length == 0) path.path += `M${startDesc}`;
        path.path += `L${endDesc}`;
      }
    });
  }
</script>

{#each paths as pathObj}
  <path class="path-line" class:dash={pathObj.dash} d={pathObj.path} {stroke} />
{/each}

<style>
  .path-line {
    fill: none;
    stroke-linejoin: round;
    stroke-linecap: round;
    stroke-width: 2;
  }

  .path-line.dash {
    stroke-dasharray: 2, 6;
  }
</style>
