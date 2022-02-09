<!--
  @component
  Generates an SVG area shape using the `area` function from [d3-shape](https://github.com/d3/d3-shape).
 -->
<script>
  import { getContext } from 'svelte';

  const { data, xGet, yGet } = getContext('LayerCake');

  /** @type {String} [stroke='#ab00d6'] - The shape's fill color. This is technically optional because it comes with a default value but you'll likely want to replace it with your own color. */
  export let stroke = '#ab00d6';

  let path;

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
    console.log('path', path);
  }
</script>

<path class="path-line" d={path} {stroke} />

<style>
  .path-line {
    fill: none;
    stroke-linejoin: round;
    stroke-linecap: round;
    stroke-width: 2;
  }
</style>
