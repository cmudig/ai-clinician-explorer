<script>
  export let ageLowerBound = 50;
  export let ageUpperBound = 59;

  export let SOFAUpperBound = 20;
  export let SOFALowerBound = 0;

  export let elixUpperBound = 15;
  export let elixLowerBound = 0;

  export let idUpperBound = 39994129;
  export let idLowerBound = 30001446;

  export let died_in_hosp = 0;
  export let isFilterByDeath = false;

  export let filters = [];
  export let SOFAFilter;
  export let ageFilter;
  export let elixFilter;
  export let idFilter;
  export let deathFilter;
  // export let clinicianActions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
  //                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
  //                                21, 22, 23, 24, 25];
  // let clinicianFormatted;
  // export let physicianActions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
  //                                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
  //                                21, 22, 23, 24, 25];
  // let physicianFormatted;
  export let filterStatement;

  $: {
    SOFAFilter =
      'max_SOFA' +
      ' >= ' +
      SOFALowerBound +
      ';' +
      'max_SOFA' +
      ' <= ' +
      SOFAUpperBound +
      ';';
    ageFilter =
      'age' +
      ' >= ' +
      ageLowerBound +
      ';' +
      'age' +
      ' <= ' +
      ageUpperBound +
      ';';
    elixFilter =
      'elixhauser' +
      ' >= ' +
      elixLowerBound +
      ';' +
      'elixhauser' +
      ' <= ' +
      elixUpperBound +
      ';';
    idFilter =
      'icustayid' +
      ' >= ' +
      idLowerBound +
      ';' +
      'icustayid' +
      ' <= ' +
      idUpperBound +
      ';';
    deathFilter = isFilterByDeath ? 'died_in_hosp = ' + died_in_hosp : '';

    // clinicianFormatted = "(";
    // for (var i = 0; i < clinicianActions.length; i++) {
    //   clinicianFormatted += clinicianActions[i].toString();
    // }
    // clinicianFormatted += ");";

    // physicianFormatted = "(";
    // for (var i = 0; i < physicianActions.length; i++) {
    //   physicianFormatted += clinicianActions[i].toString();
    // }
    // physicianFormatted += ")";

    filterStatement =
      SOFAFilter + ageFilter + elixFilter + idFilter + deathFilter;

    console.log(filterStatement);
  }
</script>

<div class="sidebar bg-blue-gray">
  <h4>Enter an age lower bound:</h4>
  <input bind:value={ageLowerBound} />
  <h4>Enter an age upper bound:</h4>
  <input bind:value={ageUpperBound} />
  <h4>Enter a SOFA lower bound:</h4>
  <input bind:value={SOFALowerBound} />
  <h4>Enter a SOFA upper bound:</h4>
  <input bind:value={SOFAUpperBound} />
  <h4>Enter an ELIX lower bound:</h4>
  <input bind:value={elixLowerBound} />
  <h4>Enter an ELIX upper bound:</h4>
  <input bind:value={elixUpperBound} />

  <button on:click={() => (isFilterByDeath = !isFilterByDeath)}
    >Filter by Death</button
  >
  {#if isFilterByDeath}
    <button on:click={() => (died_in_hosp = died_in_hosp == 0 ? 1 : 0)}>
      {#if died_in_hosp == 0}
        Death only
      {:else}
        Discharge only
      {/if}
    </button>
  {/if}
</div>

<!-- Age histogram -->

<!-- <div class="chart-container">
        <LayerCake
          padding={{ top: 0, right: 0, bottom: 20, left: 20 }}
          x={'Age'}
          y={'Frequency'}
          xScale={scaleBand().paddingInner([0.02]).round(true)}
          xDomain={['0-20', '20-40', '40-60', '60-80', '80-100', '100-120']}
          yDomain={[0, null]}
          data={patientData}
        >
          <Svg>
            <Column/>
            <AxisX
              gridlines={false}
            />
            <AxisY
              gridlines={false}
            />
          </Svg>
        </LayerCake>
      </div> -->

<!-- Question: How to make this clickable? -->
<!-- If we want to implement multiselect on the histogram directly -->

<!-- Select age ranges
    <span class="f6 b pb0 mr3"
        >Age Ranges</span
    >
    <!-- <Select items={ageOptions} isMulti={true}></Select> -->

<!-- Select comorbidities -->
<!-- <span class="f6 b pb0 mr3"
        >Comorbidities</span
    > -->
<!-- <Select items={comorbidities} isMulti={true}></Select> -->

<!-- Select predicted treatment value -->

<!-- Select clinician action -->

<!-- Previous work below: -->

<!-- <Select items={comorbidities}> </Select> -->

<!-- <span class="f6 b pb0 mr3"
            >Clinician Action(s)</span
    > -->

<!-- Implement multi-select on the 5x5 grid -->

<!-- <span class="f6 b pb0 mr3"
            >Model Action(s)</span
    >  -->

<!-- Implement multi-select on the 5x5 grid -->
<style>
  button {
    border: none;
    outline: none;
  }

  .sidebar {
    width: 400px;
    border-right: 1px solid #777777;
    overflow-y: scroll;
    flex: 0 0 auto;
  }

  .hover-bg-navy-dark:hover {
    background-color: #013274;
  }
  .chart-container {
    width: 100%;
    height: 100%;
  }

  .bg-blue-gray {
    background-color: #404a5a;
  }

  .bg-navy-gray {
    background-color: #2e3847;
  }
</style>
