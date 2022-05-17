<script>
  // Source: https://svelte.dev/repl/3c1ad3f6e36f403e93d2b729e124ab04
  export let grid = [4, 4];

  $: col = `repeat(${grid[1]}, 1fr)`;
  $: row = `repeat(${grid[0]}, 1fr)`;
  $: is_active = Array(grid[0])
    .fill(0)
    .map((_) => Array(grid[1]).fill(false));

  let start = [];
  let end = [];
  let hover_end = [];
  let clicked = false;

  function select(i, j) {
    if (clicked) {
      end = [i, j];
    } else {
      start = [i, j];
    }

    clicked = !clicked;
    check_active([i, j]);
  }

  function hover(i, j) {
    if (!clicked) return;
    hover_end = [i, j];
    check_active(hover_end);
  }

  function is_in_range([i, j], [i2, j2]) {
    return (i - start[0]) * (i - i2) <= 0 && (j - start[1]) * (j - j2) <= 0;
  }

  function check_active(end) {
    is_active = is_active.map((a, i) =>
      a.map((_, j) => is_in_range([i, j], end)),
    );
  }
</script>

<div
  class="container"
  style="grid-template-rows: {row}; grid-template-columns: {col};"
>
  {#each { length: grid[0] } as _, i (i)}
    {#each { length: grid[1] } as _, j (j)}
      <div class:active={is_active[i][j]} on:click={() => select(i, j)} />
    {/each}
  {/each}
</div>
<strong>Current: </strong>{hover_end}<br />
<strong>Coords:</strong>
{start}
{end[0] ? '-' : ''}
{end}

<style>
  .container {
    display: grid;
    border: 1px solid #999;
    border-radius: 2px;
    width: 200px;
    height: 200px;
    grid-gap: 1px;
    background: #999;
  }

  .container div {
    background: #fff;
  }

  div.active {
    background: orange;
  }
</style>
