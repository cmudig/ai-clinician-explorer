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

 $("#age-sort").click(function(){
    fetch('./api/patient?sort=age')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
 });
 $("#id-sort").click(function(){
    fetch('./api/patient?sort=icustayid')
      .then((d) => d.json())
      .then((d) => (patients = d.results));
 });


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
  color: white;
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
<div style="overflow-x:auto">
<table class="patient-data">
<tr>
  <th>
  <a class="id-sort">Patient ID <i class="fa-solid fa-sort"></i></a></th>
  <th><a class="age-sort">Age <i class="fa-solid fa-sort"></a></th>
  <th><a class="gender-filter">Gender <i class="fa-solid fa-filter"></a></th>
  <th>Duration of Stay <i class="fa-solid fa-sort"></th>
  <th>Re-Admission</th>
  <th>90-Day Mortality</th>
  <th>Patient Outcome <i class="fa-solid fa-filter"></th>
</tr>
{#each patients as patient}
<tr>
  <td>
    <a class="rel" href="/patient?id={patient.icustayid}">ID {patient.icustayid}</a>
  </td>
  <td>
    <a class="entry">{patient.age}</a>
  </td>
  <td>
    <a class="entry">{patient.gender}</a>
  </td>
  <td>
    <a class="entry">{patient.delay_end_of_record_and_discharge_or_death}</a>
  </td>
  <td>
    <a class="entry">{patient.re_admission}</a>
  </td>
  <td>
    <a class="entry">{patient.morta_90}</a>
  </td>
  <td>
    <a class="entry">{patient.died_in_hosp}</a>
  </td>
</tr>
{/each}
</table>
</div>


</div>
