<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import LoadingBar from './utils/LoadingBar.svelte';
  import SortButton from './utils/SortButton.svelte';

  let patients = [];

  export let sort = 'icustayid';
  export let size = 20;
  export let isAscending = true;

  export let offset = 0;

  let isLoading = false;

  $: {
    isLoading = true;
    fetch(
      `./api/patient/?sort=${sort}&ascending=${
        isAscending ? 1 : 0
      }&offset=${offset}`
    )
      .then((d) => d.json())
      .then((d) => {
        isLoading = false;
        patients = d.results;
      });
  }

  function changeSort(sortingCriterion) {
    if (sortingCriterion != sort) isAscending = true;
    else isAscending = !isAscending;
    offset = 0;
    sort = sortingCriterion;
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked">
    <a class="link dim white dib mr3" href="/" title="Patient List"
      >Patient List</a
    >
  </nav>
</header>
<main class="pa0 h-100">
  {#if patients.length > 0}
    <div class="patient-list-container">
      <div class="w-100 horizontal-scroll">
        <table class="patient-data">
          <thead>
            <tr>
              <th class="pl3">
                <SortButton
                  active={sort == 'icustayid'}
                  {isAscending}
                  name={'Patient ID'}
                  on:click={() => changeSort('icustayid')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'age'}
                  {isAscending}
                  name={'Age'}
                  on:click={() => changeSort('age')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'gender'}
                  {isAscending}
                  name={'Gender'}
                  on:click={() => changeSort('gender')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'num_timesteps'}
                  {isAscending}
                  name={'ICU Length of Stay'}
                  on:click={() => changeSort('num_timesteps')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'died_in_hosp'}
                  {isAscending}
                  name={'Discharge Status'}
                  on:click={() => changeSort('died_in_hosp')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'max_SOFA'}
                  {isAscending}
                  name={'Max SOFA Score'}
                  on:click={() => changeSort('max_SOFA')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'max_SIRS'}
                  {isAscending}
                  name={'Max SIRS Score'}
                  on:click={() => changeSort('max_SIRS')}
                />
              </th>
              <th>
                <SortButton
                  active={sort == 'elixhauser'}
                  {isAscending}
                  name={'Elixhauser Score'}
                  on:click={() => changeSort('elixhauser')}
                />
              </th>
            </tr>
          </thead>
          {#each patients as patient}
            <tr
              class="hover-bg-near-white pointer"
              on:click={(e) =>
                (document.location = `/patient?id=${patient.icustayid}`)}
            >
              <td class="pl3">
                {patient.icustayid}
              </td>
              <td>
                {patient.age} yrs
              </td>
              <td>
                {patient.gender ? 'Female' : 'Male'}
              </td>
              <td>
                {4 * patient.num_timesteps} hrs
              </td>
              <td>
                {patient.died_in_hosp ? 'Death' : 'Discharge'}
              </td>
              <td>
                {patient.max_SOFA}
              </td>
              <td>
                {patient.max_SIRS}
              </td>
              <td class="pr3">
                {patient.elixhauser}
              </td>
            </tr>
          {/each}
        </table>
      </div>
    </div>
    <div class="flex w-100 justify-center mt4">
      <button
        class="pa2 mh1 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b"
        on:click={() => (offset = 0)}
      >
        First
      </button>
      <button
        class="pa2 mh1 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b"
        on:click={() => (offset -= size)}
      >
        Previous
      </button>
      <button
        class="pa2 mh1 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b"
        on:click={() => (offset += size)}
      >
        Next
      </button>
    </div>
    <p class="w-100 tc f6 pb4">
      Page {Math.floor(offset / size) + 1} / xxx
    </p>
  {/if}
  {#if isLoading}
    <div
      transition:fade={{ duration: 200 }}
      class="loading-overlay w-100 h-100 flex flex-column items-center justify-center"
    >
      <p class="mb3 f5 tc b dark-gray">Loading records...</p>
      <LoadingBar />
    </div>
  {/if}
</main>

<style>
  main {
    padding-top: 48px;
    position: relative;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    background-color: #ffffffdd;
  }

  .patient-list-container {
    overflow-x: auto;
    overflow-y: scroll;
  }

  .patient-data {
    margin-left: auto;
    margin-right: auto;
  }

  .bg-navy-90 {
    background-color: #001b44e7;
    z-index: 1;
  }

  .hover-bg-navy-dark:hover {
    background-color: #013274;
  }

  table {
    border-collapse: collapse;
  }

  ul {
    width: 70%;
    margin: auto;
    text-align: center;
  }

  th {
    background-color: #eeeeee;
    border-bottom: 2px solid #cccccc;
    padding-top: 8px;
    padding-bottom: 8px;
    min-width: 84px;
  }

  tr {
    background-color: white;
    border-bottom: 1px solid #cccccc;
  }

  td {
    min-height: 54px;
    padding-top: 8px;
    padding-bottom: 8px;
    min-width: 84px;
  }

  button {
    border: none;
    outline: none;
  }
</style>
