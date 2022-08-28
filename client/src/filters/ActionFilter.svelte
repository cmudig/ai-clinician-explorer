<script>
  export let vasopressorBins; // x axis labels
  export let fluidBins; // y axis labels
  export let name = '';
  export let selectedActions = [];

  let grid = [5, 5];
  $: rows = `repeat(${grid[0]}, 1fr) 25px`;
  $: cols = `40px repeat(${grid[1]}, 30px)`;

  let isClicking = false;
  let isAdding = false;

  function onMousedown(action) {
    isClicking = true;
    let idx = selectedActions.indexOf(action);
    isAdding = idx < 0;
    if (isAdding && idx < 0) selectedActions = [...selectedActions, action];
    else if (!isAdding && idx >= 0) {
      selectedActions = [
        ...selectedActions.slice(0, idx),
        ...selectedActions.slice(idx + 1),
      ];
    }
  }

  function onMouseup() {
    if (!isClicking) return;
    isClicking = false;
    isAdding = false;
  }

  function onMouseenter(action) {
    if (!isClicking) return;
    let idx = selectedActions.indexOf(action);
    if (isAdding && idx < 0) selectedActions = [...selectedActions, action];
    else if (!isAdding && idx >= 0) {
      selectedActions = [
        ...selectedActions.slice(0, idx),
        ...selectedActions.slice(idx + 1),
      ];
    }
  }
</script>

<svelte:window on:mouseup={() => onMouseup(null)} />
<div class="ph3 mt2 mb3 w-100">
  <h4 class="tc f6 b">
    {name}
  </h4>
</div>
<div class="flex items-center f6 mr4">
  <div class="flex-auto pr2 tr">
    <div>Vasopressor (ug/kg/min)</div>
  </div>
  <div
    class="container"
    style="grid-template-rows: {rows}; grid-template-columns: {cols}"
  >
    {#each { length: 5 } as _, row (row)}
      <div class="tr" style="align-self: center">
        {!!vasopressorBins ? vasopressorBins[4 - row] : 'N/A'}
      </div>
      {#each { length: 5 } as _, col (col)}
        <div
          class="bg-animate br1 {selectedActions.includes(col * 5 - row + 4)
            ? 'bg-dark-blue hover-bg-navy-dark'
            : 'bg-medium-blue-gray hover-bg-blue-gray'}"
          on:mousedown|preventDefault={() => onMousedown(col * 5 - row + 4)}
          on:mouseup|preventDefault={() => onMouseup(col * 5 - row + 4)}
          on:mouseenter|preventDefault={() => onMouseenter(col * 5 - row + 4)}
        />
      {/each}
    {/each}
    <div />
    {#if !!fluidBins}
      {#each fluidBins as col}
        <div class="center">
          <div>{col.toFixed(0)}</div>
        </div>
      {/each}
    {/if}
  </div>
</div>
<div class="f6 flex justify-end mr2 mb3">
  <div class="flex-auto pr2" />
  <div class="tc" style="width: 200px;">IV Fluid (mL/4h)</div>
</div>

<style>
  .container {
    display: grid;
    border: 1px solid #dfe4eb;
    border-radius: 2px;
    width: 200px;
    height: 200px;
    grid-gap: 4px;
    /* background: #999; */
    /* background-color: #dfe4eb; */
  }
</style>
