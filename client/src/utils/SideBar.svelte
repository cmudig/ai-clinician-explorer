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

  let clinicianFluidBound = [0, 4];
  let clinicianVasoBound = [0, 4];
  let modelFluidBound = [0, 4];
  let modelVasoBound = [0, 4];
  let actionDifferenceBound = [0, 5];
  let selectedStates = null;

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
      'avg_action_difference >= ' + actionDifferenceBound[0],
      'avg_action_difference <= ' + actionDifferenceBound[1],
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

    let allowedPhysicianActions = new Array(25)
      .fill(0)
      .map((_, ac) => ac)
      .filter(
        (ac) =>
          Math.floor(ac / 5) >= clinicianFluidBound[0] &&
          Math.floor(ac / 5) <= clinicianFluidBound[1] &&
          Math.floor(ac % 5) >= clinicianVasoBound[0] &&
          Math.floor(ac % 5) <= clinicianVasoBound[1],
      );
    if (allowedPhysicianActions.length < 25)
      filters.push(
        'physician_action in (' + allowedPhysicianActions.join(', ') + ')',
      );

    let allowedModelActions = new Array(25)
      .fill(0)
      .map((_, ac) => ac)
      .filter(
        (ac) =>
          Math.floor(ac / 5) >= modelFluidBound[0] &&
          Math.floor(ac / 5) <= modelFluidBound[1] &&
          Math.floor(ac % 5) >= modelVasoBound[0] &&
          Math.floor(ac % 5) <= modelVasoBound[1],
      );
    if (allowedModelActions.length < 25)
      filters.push('model_action in (' + allowedModelActions.join(', ') + ')');

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
    clinicianFluidBound[0] == 0 &&
    clinicianFluidBound[1] == 4 &&
    clinicianVasoBound[0] == 0 &&
    clinicianVasoBound[1] == 4 &&
    modelFluidBound[0] == 0 &&
    modelFluidBound[1] == 4 &&
    modelVasoBound[0] == 0 &&
    modelVasoBound[1] == 4 &&
    actionDifferenceBound[0] == 0 &&
    actionDifferenceBound[1] == 5 &&
    !selectedGender &&
    !selectedOutcome &&
    (!selectedComorbidities || selectedComorbidities.length == 0);

  function resetFilter() {
    ageBound = [18, 100];
    sofaBound = [0, 20];
    sirsBound = [0, 4];
    elixBound = [0, 15];
    lengthOfStayBound = [0, 160];
    clinicianFluidBound = [0, 4];
    clinicianVasoBound = [0, 4];
    modelFluidBound = [0, 4];
    modelVasoBound = [0, 4];
    actionDifferenceBound = [0, 5];
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

<div class="sidebar bg-light-blue-gray flex flex-column">
  <div class="flex items-center pv3 mb2 ph3">
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
  <div class="sidebar-filter-view flex-auto pb3 ph3">
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
    <hr class="mv3" />
    <RangeFilter
      min={0}
      max={5}
      step={0.1}
      name={'Avg Action Difference'}
      bind:range={actionDifferenceBound}
    />
    <RangeFilter
      min={0}
      max={4}
      name={'Clinician Fluids'}
      bind:range={clinicianFluidBound}
    />
    <RangeFilter
      min={0}
      max={4}
      name={'Clinician Vasopressors'}
      bind:range={clinicianVasoBound}
    />
    <RangeFilter
      min={0}
      max={4}
      name={'Model Fluids'}
      bind:range={modelFluidBound}
    />
    <RangeFilter
      min={0}
      max={4}
      name={'Model Vasopressors'}
      bind:range={modelVasoBound}
    />
    <!-- <ActionFilter bind:clinicianActions /> -->
  </div>
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
    flex: 0 0 auto;
  }

  .sidebar-filter-view {
    overflow-y: scroll;
  }

  .chart-container {
    width: 100%;
    height: 100%;
  }

  .disabled-button {
    opacity: 0.2;
  }
</style>
