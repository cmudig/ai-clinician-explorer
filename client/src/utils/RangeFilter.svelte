<script>
  export let range;
  export let name;
  import Slider from '@bulatdashiev/svelte-slider';
</script>

<h4>{name}</h4>
<Slider min="0" max="100" step="1" bind:value={range} range order />
