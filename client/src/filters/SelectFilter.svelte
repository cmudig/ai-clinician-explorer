<script>
  import Select from 'svelte-select';

  export let name;
  export let items;
  export let multi;
  export let tooltip;

  export let selected = null;
  export let dark = false;

  let dummySelected = [];
  let oldSelected = [];
  $: if (oldSelected !== selected) {
    dummySelected = selected;
    oldSelected = selected;
  }

  $: updateSelection(dummySelected);

  function updateSelection(dummy) {
    selected = dummy;
  }
</script>

<div class="flex items-center mb3" title={tooltip}>
  <div class="w-50 pr3 {dark ? 'white' : 'black'}">
    <h4 class="tr f6 b mt0 mb1">
      {name}
    </h4>
    {#if multi && !!selected && selected.length > 0}
      <p class="tr f6 mv0 dark-gray">
        {selected.length} item{selected.length != 1 ? 's' : ''}
      </p>{/if}
  </div>
  <div class="w-50">
    <Select
      {items}
      isMulti={multi}
      value={dummySelected}
      on:select={(e) => (dummySelected = e.detail)}
    />
  </div>
</div>
