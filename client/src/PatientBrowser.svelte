<script>
  import { onMount } from 'svelte';
  import { fade } from 'svelte/transition';
  import LoadingBar from './utils/LoadingBar.svelte';
  import SortButton from './utils/SortButton.svelte';
  import Select from 'svelte-select';
  import SideBar from './utils/SideBar.svelte';
  import { interpolateReds, interpolateBlues } from 'd3-scale-chromatic';
  import TableCellBar from './utils/TableCellBar.svelte';

  let patients = [];
  let resultCount = 0;

  export let sort = 'icustayid';
  export let size = 20;
  export let isAscending = true;

  export let offset = 0;

  export let filteredStates = null;

  let isLoading = false;

  let filter = {};

  $: {
    isLoading = true;
    let url = `./api/patient/?sort=${sort}&ascending=${
      isAscending ? 1 : 0
    }&offset=${offset}`;
    if (!!filter) {
      if (!!filter.filters && filter.filters.length > 0)
        url += '&filters=' + encodeURIComponent(filter.filters);
      if (!!filter.comorbidityFilters && filter.comorbidityFilters.length > 0)
        url += '&cm_filters=' + encodeURIComponent(filter.comorbidityFilters);
    }
    fetch(url)
      .then((d) => d.json())
      .then((d) => {
        isLoading = false;
        patients = d.results;
        resultCount = d.result_count;
      });
  }

  function changeSort(sortingCriterion) {
    if (sortingCriterion != sort)
      isAscending = sortingCriterion == 'icustayid' ? true : false;
    else isAscending = !isAscending;
    offset = 0;
    sort = sortingCriterion;
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked">
    <a class="link dim white dib mr3" href="#" title="Patient List"
      >AI Clinician Explorer</a
    >
  </nav>
</header>

<main class="pa0 h-100 flex">
  <SideBar bind:filter bind:selectedStates={filteredStates} />

  <div class="pa0 h-100 patient-list-container">
    {#if patients.length > 0}
      <div class="h-100 w-100 vertical-scroll">
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
                  window
                    .open(
                      `/patient?id=${patient.icustayid}&bloc=${patient.bloc}`,
                      '_blank',
                    )
                    .focus()}
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
                  <TableCellBar
                    maxWidth={60}
                    fraction={(4 * patient.num_timesteps) / 160}
                    colorScale={interpolateBlues}
                  />
                  {4 * patient.num_timesteps} hrs
                </td>
                <td>
                  <span
                    class="mortality-indicator"
                    class:bg-dark-pink={patient.died_in_hosp}
                    class:bg-light-green={!patient.died_in_hosp}
                  />
                  {patient.died_in_hosp ? 'Death' : 'Alive'}
                </td>
                <td>
                  <TableCellBar
                    maxWidth={60}
                    fraction={patient.max_SOFA / 20}
                    colorScale={interpolateReds}
                  />
                  {patient.max_SOFA}
                </td>
                <td>
                  <TableCellBar
                    maxWidth={60}
                    fraction={patient.max_SIRS / 4}
                    colorScale={interpolateReds}
                  />
                  {patient.max_SIRS}
                </td>
                <td class="pr3">
                  <TableCellBar
                    maxWidth={60}
                    fraction={patient.elixhauser / 15}
                    colorScale={interpolateReds}
                  />
                  {patient.elixhauser}
                </td>
              </tr>
            {/each}
          </table>
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
          Page {(Math.floor(offset / size) + 1).toLocaleString()} of {Math.ceil(
            resultCount / size,
          ).toLocaleString()} ({resultCount.toLocaleString()}
          total patients)
        </p>
      </div>
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
  </div>
</main>

<style>
  main {
    padding-top: 48px;
  }

  .patient-list-container {
    position: relative;
    flex-grow: 1;
  }

  .vertical-scroll {
    overflow-y: scroll;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    background-color: #ffffffdd;
  }

  .patient-data {
    margin-left: auto;
    margin-right: auto;
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

  .mortality-indicator {
    display: inline-block;
    border-radius: 4px;
    width: 8px;
    height: 8px;
    transform: translateY(-2px);
  }
</style>
