<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="my_jquery_functions.js"></script>
<script src="https://kit.fontawesome.com/0b0399a79b.js" crossorigin="anonymous"></script>
</head>

<script>
  import { onMount } from 'svelte';

  let patients = [];

  onMount(() => {
    loadPatients();
  });

  function loadPatients() {
    fetch('./api/patient/')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }

  export let sort = "icustayid";
  let cursor_id = "30850150";
  let cursor_sort = "21";
  let size = 20;

  function reSort(sortParam) {
    fetch(`./api/patient/?sort=${sortParam}`)
      .then((d) => d.json())
      .then((d) => (patients = d.results));
  }

  function changeSort(sortingCriterion) {
    sort = sortingCriterion;
    reSort(sortingCriterion);
  }

</script>
<style>
.patient-data {
  margin-left: auto;
  margin-right: auto;

}

.fa-cog {
  color: white;
}

.entry {
  text-align: center;
  color: inherit;
  text-decoration: inherit;
}

table, td {
  width: 80%;
  padding-top: 10px;
  padding-bottom: 20px;
  padding-left: 40px;
  padding-right: 40px;
}

th {
  width: 80%;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 40px;
  padding-right: 40px;
  background-color: #323b87;
  color: white;
  opacity: 0.9;
}

a {
  color: rgb(0, 0, 0);
}
tr {
  background-color: #fcfdff;
  opacity: 0.8;
}
.gradient {
  height: auto;
  width: auto;
  color: inherit;
  background-image: linear-gradient(
      349deg,
      #bcedf5 12%,
      rgba(255, 255, 255, 0) 89%
    ),
    radial-gradient(
      ellipse at 106% -172%,
      #a291c0 6%,
      rgba(255, 255, 255, 0) 69%
    ),
    linear-gradient(76deg, #e4e585 2%, rgba(255, 255, 255, 0) 74%),
    linear-gradient(80deg, #e50290 16%, rgba(255, 255, 255, 0) 68%),
    radial-gradient(circle at -31% -20%, #1cd3fb 54%, rgba(255, 255, 255, 0) 0%);
}
@font-face {
  font-family: Aldrich;
  src: url(https://fonts.googleapis.com/css2?family=Aldrich:wght@400);
}
.text-image {
  background-image: url(https://www.genengnews.com/wp-content/uploads/2020/11/Jan1_2020_GettyImages_1157048386_BinaryCode3DIllustration-scaled.jpg);
  background-position-x: 5%;
  background-position-y: bottom;
  background-size: cover;
  filter: blur(0px);
  font-family: Aldrich;
  font-size: 35px;
  font-style: normal;
  font-weight: 600;
  letter-spacing: 0em;
  line-height: 1;
  mix-blend-mode: none;
  opacity: 1;
  padding-bottom: 2px;
  padding-left: 2px;
  padding-top: 2px;
  padding-right: 0px;
  text-transform: none;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>

<div class="gradient">

<h1 class="text-image">MIMIC Data</h1>
<div on:mousemove>Currently sorting based on {sort}</div>
<div style="overflow-x:auto">
<table class="patient-data">
<tr>
  <th>
  <button
    on:click={changeSort("icustayid")}
    on:click={reSort()}
    on:click={() => console.log('Sorting ID!')}>
  Patient ID <i class="fa-solid fa-sort"></i>
  </button></th>
  <th>
  <button
    on:click={changeSort("age")}
    on:click={() => console.log('Sorting Age!')}>
    Age <i class="fa-solid fa-sort"></i>
  </button></th>
  <th>
  <button
    on:click={changeSort("gender")}
    on:click={() => console.log('Filtering Gender!')}>
    Gender <i class="fa-solid fa-filter"></i>
  </button></th>
  <th>
    <button

      on:click={() => console.log('Sorting duration of stay')}>
      Duration of Stay <i class="fa-solid fa-filter"></i>
    </button></th>
    <th>
      <button
      
        on:click={() => console.log('Sorting readmission!')}>
        Re-Admission<i class="fa-solid fa-filter"></i>
      </button></th>
    <th>
      <button
       
        on:click={() => console.log('Sorting morta_90!')}>
        90-Day Mortality<i class="fa-solid fa-filter"></i>
      </button></th>
    <th>
      <button

        on:click={() => console.log('Sorting outcome!')}>
        Patient Outcome<i class="fa-solid fa-filter"></i>
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
    {patient.delay_end_of_record_and_discharge_or_death}
  </td>
  <td>
    {patient.re_admission}
  </td>
  <td>
    {patient.morta_90}
  </td>
  <td>
    {patient.died_in_hosp}
  </td>
</tr>
{/each}
</table>
</div>
<ul>
  <li>
    <button>
      First
    </button>
  </li>
  <li>
    <button>
     Previous
    </button>
  </li>
  <li>
  </li>
</ul>
</div>