<script>
    export let name;
    export let active = false;
    export let isAscending = true;

</script>

<style>
    
    .active {
		background-color: #6666FF;
	}

</style>

<button
      class:active={active}
      on:click>
      {name}

      {#if active && isAscending}
        <i class="fa-solid fa-sort-up"></i>
      {:else if active && !isAscending}
        <i class="fa-solid fa-sort-down"></i>
      {/if}

</button>