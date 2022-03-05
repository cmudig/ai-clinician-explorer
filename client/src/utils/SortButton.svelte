<script>
  import Fa from 'svelte-fa';
  import {
    faSortUp,
    faSortDown,
    faSort,
  } from '@fortawesome/free-solid-svg-icons';

  export let name;
  export let active = false;
  export let isAscending = true;
</script>

<button
  class="ph2 mr2 link dib f6 {active
    ? 'white bg-dark-blue hover-bg-navy-dark'
    : 'dark-gray bg-transparent dim'}"
  on:click
>
  {name}

  {#if active && isAscending}
    <Fa icon={faSortUp} />
  {:else if active && !isAscending}
    <Fa icon={faSortDown} />
  {:else}
    <Fa icon={faSort} />
  {/if}
</button>

<style>
  button {
    border: none;
    outline: none;
  }

  .hover-bg-navy-dark:hover {
    background-color: #013274;
  }
</style>
