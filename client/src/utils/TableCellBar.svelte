<script>
  export let fraction = 1.0;
  export let maxWidth = 60;

  export let colorScale = null;
</script>

<span
  class="bar"
  style="width: {(maxWidth - 6) * fraction + 6}px; {colorScale != null
    ? 'background-color: ' + colorScale(fraction)
    : 'background-color: lightgray;'}"
/>

<style>
  .bar {
    display: inline-block;
    border-radius: 3px;
    height: 6px;
    transform: translateY(-3px);
  }
</style>
