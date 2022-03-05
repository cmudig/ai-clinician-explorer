<script>
  import { onMount } from 'svelte';
  import SortButton from './utils/SortButton.svelte';

  let patients = [];

  onMount(() => {
    loadPatients();
  });

  function loadPatients() {
    fetch('./api/patient?size=')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }

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
  <div style="overflow-x:auto">
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
              name={'Number of Timesteps'}
              on:click={() => changeSort('num_timesteps')}
            />
          </th>
          <th>
            <SortButton
              active={sort == 'morta_90'}
              {isAscending}
              name={'90-Day Mortality'}
              on:click={() => changeSort('morta_90')}
            />
          </th>
          <th>
            <SortButton
              active={sort == 'died_in_hosp'}
              {isAscending}
              name={'Patient Outcome'}
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
          <th class="pr3">
            <SortButton
              active={sort == 'max_dose_vaso'}
              {isAscending}
              name={'Max Vasopressor Dose'}
              on:click={() => changeSort('max_dose_vaso')}
            />
          </th>
        </tr>
      </thead>
      {#each patients as patient}
        <tr>
          <td class="pl3">
            <a class="link black dim" href="/patient?id={patient.icustayid}"
              >{patient.icustayid}</a
            >
          </td>
          <td>
            {patient.age} yrs
          </td>
          <td>
            {patient.gender ? 'Female' : 'Male'}
          </td>
          <td>
            {patient.num_timesteps}
          </td>
          <td>
            {patient.morta_90 ? 'Yes' : 'No'}
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
            {patient.max_dose_vaso}
          </td>
        </tr>
      {/each}
    </table>
  </div>
  <br /><br />
  <ul>
    <button on:click={() => (offset = 0)}> First </button>
    <button on:click={() => (offset -= size)}> Previous </button>
    <button on:click={() => (offset += size)}> Next </button>
  </ul>
  <br />
  <ul>
    Page {Math.floor(offset / size) + 1} / xxx
  </ul>
  <br /><br /><br />
</main>

<style>
  main {
    padding-top: 48px;
  }

  .patient-data {
    margin-left: auto;
    margin-right: auto;
  }

  .bg-navy-90 {
    background-color: #001b44e7;
    z-index: 1;
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
  }

  tr {
    background-color: white;
    border-bottom: 1px solid #cccccc;
  }

  td {
    min-height: 54px;
    padding-top: 8px;
    padding-bottom: 8px;
  }
</style>
