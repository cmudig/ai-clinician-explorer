<script>
  export let name;
  export let value = '';
  export let placeholder = 'Enter a value...';
  export let dark = false;
</script>

<div class="flex items-center mb3">
  <h4 class="tr f5 b mt0 mb1 w-50 pr3 {dark ? 'white' : 'black'}">
    {name}
  </h4>
  <div class="w-50">
    <input type="text" bind:value {placeholder} />
  </div>
</div>
