<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="my_jquery_functions.js"></script>
<script src="https://kit.fontawesome.com/0b0399a79b.js" crossorigin="anonymous"></script>
</head>

<script>
  import { onMount } from 'svelte';
  import SortButton from './utils/SortButton.svelte';

  let patients = [];

  onMount(() => {
    loadPatients();
  });

  function loadPatients() {
    fetch('./api/patient?size=100')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }

  let active = false;

  export let sort = "icustayid";
  export let size = 20;
  export let isAgeAscending = 1;
  export let isFemale = 1;
  export let isIDAscending = 1;
  export let isTimeAscending = 1;
  export let isMorta90 = 1;
  export let isDeath = 1;
  export let isSOFA = 1;
  export let isSIRS = 1;
  export let isVaso = 1;
  export let isAscending = 1;
  export let offset = 0;
  export let changeCriterion = true;

  function reSort(sortParam, changeOffset) {
    if (changeCriterion) {
      if (sortParam == "age") {
        isAgeAscending = (isAgeAscending + 1) % 2;
        isAscending = isAgeAscending;
      } else if (sortParam == "icustayid") {
        isIDAscending = (isIDAscending + 1) % 2;
        isAscending = isIDAscending;
      } else if (sortParam == "morta_90") {
        isMorta90 = (isMorta90 + 1) % 2;
        isAscending = isMorta90Ascending;
      } else if (sortParam == "died_in_hosp") {
        isDeath = (isDeath + 1) % 2;
        isAscending = isDeath;
      } else if (sortParam == "gender") {
        isFemale = (isFemale + 1) % 2;
        isAscending = isFemale;
      } else if (sortParam == "num_timesteps") {
        isTimeAscending = (isTimeAscending + 1) % 2;
        isAscending = isTimeAscending;
      } else if (sortParam == "max_SOFA") {
        isSOFA = (isSOFA + 1) % 2;
        isAscending = isSOFA;
      } else if (sortParam == "max_SIRS") {
        isSIRS = (isSIRS + 1) % 2;
        isAscending = isSIRS;
      } else if (sortParam == "max_dose_vaso") {
        isVaso = (isVaso + 1) % 2;
        isAscending = isVaso;
      }
    } else {
      changeCriterion = true;
    }
    if (offset + changeOffset < 0) {
      offset = 0;
    } else {
      offset = offset + changeOffset;
    }
    fetch(`./api/patient/?sort=${sortParam}&ascending=${isAscending}&offset=${offset}`)
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }

  function changeSort(sortingCriterion, changeOffset=0) {
    sort = sortingCriterion;
    reSort(sortingCriterion, changeOffset);
  }

</script>
<style>
.patient-data {
  margin-left: auto;
  margin-right: auto;
}

.bg-navy-90 {
    background-color: #001b44e7;
    z-index: 1;
  }

table, td {
  width: 60%;
  padding-top: 10px;
  padding-bottom: 20px;
  padding-left: 40px;
  padding-right: 40px;
  border-bottom: 2px solid #FFFFFF;
  border-collapse: collapse;
}

ul {
    width: 70%;
    margin: auto;
    text-align: center;
}

th {
  width: 80%;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 40px;
  padding-right: 40px;
  background-color: #678bc0e7;
  color: #6666FF;;
  opacity: 0.9;
}

a {
  color: rgb(0, 0, 0);
}
tr {
  background-color: #e9f0fae7;
  opacity: 0.8;
}


</style>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked">
    <a class="link dim white dib mr3" href="/" title="Patient List">Patient List</a>
  </nav>
</header>
<br><br><br><br>
<div on:mousemove>Currently sorting based on {sort}</div>
<div on:mousemove>isAgeAscending: {isAgeAscending}</div>
<div on:mousemove>isIDAscending: {isIDAscending}</div>
<div on:mousemove>isTimeAscending: {isTimeAscending}</div>
<div on:mousemove>isMorta90: {isMorta90}</div>
<div on:mousemove>isDeath: {isDeath}</div>
<div on:mousemove>isAscending: {isAscending}</div>
<div on:mousemove>Displaying the {offset}th patient entry</div>

<div style="overflow-x:auto">
<table class="patient-data">
<tr>
  <th>
    <SortButton
      active={sort == "icustayid"} 
      isAscending={isIDAscending}
      name={"Patient ID"}
      on:click={() => changeSort("icustayid", -offset)}
      on:click={() => console.log('Sorting ID!')}>
    </SortButton></th>
  <th>
    <button
      class:active={active} on:click="{() => active = !active}"
      on:click={() => changeSort("age", -offset)}
      on:click={() => console.log('Sorting Age!')}>
      Age <i class="fa-solid fa-sort"></i>
    </button></th>
  <th>
    <button
      class:active={active} on:click="{() => active = !active}"
      on:click={() => changeSort("gender", -offset)}
      on:click={() => console.log('Filtering Gender!')}>
      Gender <i class="fa-solid fa-filter"></i>
    </button></th>
  <th>
    <button
      class:active={active} on:click="{() => active = !active}"
      on:click={() => changeSort("num_timesteps", -offset)}
      on:click={() => console.log('Sorting num_timesteps')}>
      Number of Timesteps <i class="fa-solid fa-filter"></i>
    </button></th>
    <!-- <th>
      <button
        class:active={active} on:click="{() => active = !active}"
        on:click={() => console.log('Sorting readmission!')}>
        Re-Admission<i class="fa-solid fa-filter"></i>
      </button></th> -->
    <th>
      <button
        class:active={active} on:click="{() => active = !active}"
        on:click={() => changeSort("morta_90", -offset)}
        on:click={() => console.log('Sorting morta_90!')}>
        90-Day Mortality<i class="fa-solid fa-filter"></i>
      </button></th>
    <th>
      <button
        class:active={active} on:click="{() => active = !active}"
        on:click={() => changeSort("died_in_hosp", -offset)}
        on:click={() => console.log('Sorting outcome!')}>
        Patient Outcome<i class="fa-solid fa-filter"></i>
      </button></th>
    <th>
      <button
        class:active={active} on:click="{() => active = !active}"
        on:click={() => changeSort("max_SOFA", -offset)}
        on:click={() => console.log('Sorting max_SOFA!')}>
        max_SOFA<i class="fa-solid fa-sort"></i>
      </button></th>
    <th>
      <button
        class:active={active} on:click="{() => active = !active}"
        on:click={() => changeSort("max_SIRS", -offset)}
        on:click={() => console.log('Sorting max_SIRS!')}>
        max_SIRS<i class="fa-solid fa-sort"></i>
      </button></th>
    <th>
      <button
        class:active={active} on:click="{() => active = !active}"
        on:click={() => changeSort("max_dose_vaso", -offset)}
        on:click={() => console.log('Sorting max_dose_vaso!')}>
        max_dose_vaso<i class="fa-solid fa-sort"></i>
      </button></th>
</tr>
{#each patients as patient}
<tr>
  <td>
    <a href="/patient?id={patient.icustayid}">Patient ID {patient.icustayid}</a>
  </td>
  <td>
    {patient.age}
  </td>
  <td>
    {patient.gender}
  </td>
  <td>
    {patient.num_timesteps}
  </td>
  <!-- <td>
    {patient.re_admission}
  </td> -->
  <td>
    {patient.morta_90}
  </td>
  <td>
    {patient.died_in_hosp}
  </td>
  <td>
    {patient.max_SOFA}
  </td>
  <td>
    {patient.max_SIRS}
  </td>
  <td>
    {patient.max_dose_vaso}
  </td>
</tr>
{/each}
</table>
</div>
<br><br>
<ul>
    <button 
      class:active={active} on:click="{() => active = !active}"
      on:click={() => changeCriterion = false}
      on:click={() => changeSort(sort, -offset)}>
      First
    </button>
    <button
      class:active={active} on:click="{() => active = !active}"
      on:click={() => changeCriterion = false}
      on:click={() => changeSort(sort, -size)}>
     Previous
    </button>
<!-- Tried to set changeCriterion to false when changing pages -->
<!-- on:click={() => changeCriterion = false} -->    
    <button 
      class:active={active} on:click="{() => active = !active}"
      on:click={() => changeCriterion = false}
      on:click={() => changeSort(sort, size)}>
      Next
    </button>
</ul>
<br>
<ul>
  Page {Math.floor(offset/20)+1} / xxx
</ul>
<br><br><br>
