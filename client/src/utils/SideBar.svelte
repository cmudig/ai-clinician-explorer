<script>
  import ActionFilter from './ActionFilter.svelte';
  import RangeFilter from './RangeFilter.svelte';
  import SelectFilter from './SelectFilter.svelte';
  import { Comorbidities } from './strings';

  let ageBound = [18, 100];
  let sofaBound = [0, 20];
  let sirsBound = [0, 4];
  let elixBound = [0, 15];
  let lengthOfStayBound = [0, 160];
  let selectedGender = null;
  let selectedOutcome = null;
  let selectedComorbidities = null;

  let clinicianActions = new Set();

  export let died_in_hosp = 0;
  export let isFilterByDeath = false;
  export let filters = [];
  export let deathFilter;
  export let clinicianFilter;

  function makeEmptyFilter() {
    return { filters: '', comorbidityFilters: '' };
  }
  export let filter = makeEmptyFilter();

  // Store the filter statement that would be generated with the current values.
  // When the user clicks the Apply button this statement will be transferred to
  // the filterStatement variable.
  let tempFilters = '';
  let tempComorbidityFilters = '';

  let filterEmpty = true;

  $: {
    let temp = [];
    for (let i = 0; i < 25; i++) {
      if (clinicianActions[i]) {
        temp.push(toString(i));
      }
    }
    clinicianFilter = 'clinician action in(' + temp.join(',') + ')';
    deathFilter = isFilterByDeath ? 'died_in_hosp = ' + died_in_hosp : '';

    filters = [
      'max_SOFA >= ' + sofaBound[0],
      'max_SOFA <= ' + sofaBound[1],
      'max_SIRS >= ' + sirsBound[0],
      'max_SIRS <= ' + sirsBound[1],
      'age >= ' + ageBound[0],
      'age <= ' + ageBound[1],
      'elixhauser >= ' + elixBound[0],
      'elixhauser <= ' + elixBound[1],
      'num_timesteps >= ' + lengthOfStayBound[0] / 4,
      'num_timesteps <= ' + lengthOfStayBound[1] / 4,
      // clinician actions
      // clinicianFilter,
    ];

    if (isFilterByDeath) {
      filters.push(deathFilter);
    }
    if (!!selectedGender) {
      filters.push('gender = ' + selectedGender.value);
    }
    if (!!selectedOutcome) {
      filters.push('died_in_hosp = ' + selectedOutcome.value);
    }

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

    tempFilters = filters.join(';');
    if (!filter.filters) {
      let obj = makeEmptyFilter();
      Object.assign(obj, filter);
      obj.filters = tempFilters;
      filter = obj;
    }

    if (!!selectedComorbidities && selectedComorbidities.length > 0) {
      tempComorbidityFilters = selectedComorbidities
        .map((v) => `${v.value} = 1`)
        .join(';');
    } else {
      tempComorbidityFilters = '';
    }
  }

  $: filterEmpty =
    ageBound[0] == 18 &&
    ageBound[1] == 100 &&
    sofaBound[0] == 0 &&
    sofaBound[1] == 20 &&
    sirsBound[0] == 0 &&
    sirsBound[1] == 4 &&
    elixBound[0] == 0 &&
    elixBound[1] == 15 &&
    lengthOfStayBound[0] == 0 &&
    lengthOfStayBound[1] == 160 &&
    !selectedGender &&
    !selectedOutcome &&
    (!selectedComorbidities || selectedComorbidities.length == 0);

  function resetFilter() {
    ageBound = [18, 100];
    sofaBound = [0, 20];
    sirsBound = [0, 4];
    elixBound = [0, 15];
    lengthOfStayBound = [0, 160];
    selectedGender = null;
    selectedOutcome = null;
    selectedComorbidities = null;
    setTimeout(() => {
      if (filterNeedsUpdate()) updateFilter();
    });
  }

  function updateFilter() {
    filter = {
      filters: tempFilters,
      comorbidityFilters: tempComorbidityFilters,
    };
  }

  let filterNeedsUpdate;

  $: {
    filterNeedsUpdate =
      filter.filters != tempFilters ||
      filter.comorbidityFilters != tempComorbidityFilters;
  }
</script>

<div class="sidebar bg-light-blue-gray ph3">
  <div class="flex items-center pv3 mb2">
    <p class="mv0 flex-auto f4">Filters</p>
    <input
      type="button"
      class="pa2 mh1 link dib white bg-gray f6 b {!filterEmpty
        ? 'pointer hover-bg-dark-gray'
        : 'disabled-button'}"
      disabled={filterEmpty}
      value="Reset"
      on:click={resetFilter}
    />
    <input
      type="button"
      class="pa2 mh1 link dib white bg-dark-blue f6 b {filterNeedsUpdate
        ? 'pointer hover-bg-navy-dark '
        : 'disabled-button'}"
      disabled={!filterNeedsUpdate}
      value="Apply"
      on:click={updateFilter}
    />
  </div>
  <SelectFilter
    name="Gender"
    items={[
      { label: 'Male', value: 0 },
      { label: 'Female', value: 1 },
    ]}
    bind:selected={selectedGender}
  />
  <RangeFilter min={18} max={100} name={'Age'} bind:range={ageBound} />
  <RangeFilter min={0} max={15} name={'Elixhauser'} bind:range={elixBound} />
  <SelectFilter
    name="Comorbidities"
    multi
    items={Object.keys(Comorbidities).map((k) => ({
      value: k,
      label: Comorbidities[k],
    }))}
    bind:selected={selectedComorbidities}
  />
  <RangeFilter
    min={0}
    max={160}
    step={4}
    name={'ICU Stay Length'}
    bind:range={lengthOfStayBound}
  />
  <SelectFilter
    name="Discharge Status"
    items={[
      { label: 'Alive', value: 0 },
      { label: 'Death', value: 1 },
    ]}
    bind:selected={selectedOutcome}
  />
  <RangeFilter min={0} max={20} name={'Max SOFA'} bind:range={sofaBound} />
  <RangeFilter min={0} max={4} name={'Max SIRS'} bind:range={sirsBound} />
  <!-- <ActionFilter bind:clinicianActions /> -->
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
  .sidebar {
    width: 400px;
    border-right: 1px solid #777777;
    overflow-y: scroll;
    flex: 0 0 auto;
  }

  .chart-container {
    width: 100%;
    height: 100%;
  }

  .disabled-button {
    opacity: 0.2;
  }
</style>
