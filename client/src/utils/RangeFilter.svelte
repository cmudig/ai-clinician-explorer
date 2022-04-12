<script>
  import Slider from '@bulatdashiev/svelte-slider';

  export let dark = false;

  export let range = [0, 100];
  export let name;

  export let min = 0;
  export let max = 100;
  export let step = 1;
</script>

<div class="flex items-center mb3">
  <div class="w-50 pr3 {dark ? 'white' : 'black'}">
    <h4 class="tr f5 b mt0 mb1">
      {name}
    </h4>
    <p class="tr f6 mv0">
      {range[0].toLocaleString()} - {range[1].toLocaleString()}
    </p>
  </div>
  <div class="w-50">
    <Slider {min} {max} {step} bind:value={range} range order />
  </div>
</div>
