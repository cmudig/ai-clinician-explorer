<script>
  import Select from 'svelte-select';

  export let name;
  export let items;
  export let multi;

  export let selected = null;
  export let dark = false;
</script>

<div class="flex items-center mb3">
  <div class="w-50 pr3 {dark ? 'white' : 'black'}">
    <h4 class="tr f5 b mt0 mb1">
      {name}
    </h4>
    {#if multi && !!selected && selected.length > 0}
      <p class="tr f6 mv0">
        {selected.length} item{selected.length != 1 ? 's' : ''}
      </p>{/if}
  </div>
  <div class="w-50">
    <Select {items} isMulti={multi} bind:value={selected} />
  </div>
</div>
