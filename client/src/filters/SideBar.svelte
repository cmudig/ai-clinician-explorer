<script>
  import ActionFilter from './ActionFilter.svelte';
  import RangeFilter from './RangeFilter.svelte';
  import SelectFilter from './SelectFilter.svelte';
  import { Comorbidities } from '../utils/strings';
  import TextFilter from './TextFilter.svelte';

  export let ageBound = [18, 100];
  export let sofaBound = [0, 20];
  export let sirsBound = [0, 4];
  export let elixBound = [0, 15];
  export let lengthOfStayBound = [0, 160];
  export let selectedGender = null;
  export let selectedOutcome = null;
  export let selectedComorbidities = null;

  export let clinicianFluidBound = [0, 4];
  export let clinicianVasoBound = [0, 4];
  export let modelFluidBound = [0, 4];
  export let modelVasoBound = [0, 4];
  export let actionDifferenceBound = [0, 5];
  export let selectedStates = null;

  let clinicianActions = new Set();
  let physicianActions = new Set();

  export let died_in_hosp = 0;
  export let isFilterByDeath = false;
  export let filters = [];
  export let deathFilter;
  export let clinicianFilter;

  let grid = [5, 5];
  $: rows = `repeat(${grid[0]}, 1fr) 20px`;
  $: cols = `20px repeat(${grid[1]}, 1fr)`;

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

  let temp = [];
  // for (let i = 1; i < 26; i++) {
  //   if (clinicianActions[i]) {
  //     temp.push(toString(i));
  //   }
  // }

  $: {
    clinicianFilter = 'clinician action in(' + temp.join(',') + ')';
    deathFilter = isFilterByDeath ? 'died_in_hosp = ' + died_in_hosp : '';

    console.log('updating filters');

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

    if (!!selectedStates && selectedStates.length > 0) {
      filters.push(
        'state in (' + selectedStates.map((v) => v).join(', ') + ')',
      );
    }

    let allowedPhysicianActions = Array.from(clinicianActions);

    if (allowedPhysicianActions.length > 0)
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

    tempFilters = filters.join(';');
    if (!filter.filters) {
      let obj = makeEmptyFilter();
      Object.assign(obj, filter);
      obj.filters = tempFilters;
      filter = obj;
      console.log('reassigning filter', filter);
    }

    if (!!selectedComorbidities && selectedComorbidities.length > 0) {
      tempComorbidityFilters = selectedComorbidities
        .map((v) => `${v.value} = 1`)
        .join(';');
    } else {
      tempComorbidityFilters = '';
    }
    console.log(tempFilters);
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
    (!selectedComorbidities || selectedComorbidities.length == 0) &&
    (!selectedStates || selectedStates.length == 0);

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
    selectedStates = null;
    clinicianActions = new Set();
    physicianAction = new Set();

    setTimeout(() => {
      if (filterNeedsUpdate) updateFilter();
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

  let vaso = [0, 0.04, 0.113, 0.225, 0.54];
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
    <!-- <ActionFilter bind:actionFilter={selectedActions} /> -->
    <!-- Put everything below in ActionFilter.svelte -->
    <h4>Clinician Actions</h4>
    <div class="flex items-center mb3">
      <div>
        <div>Vasopressor (ug/kg/min)</div>
      </div>
      <div
        class="container"
        style="grid-template-rows: {rows}; grid-template-columns: {cols};"
      >
        {#each { length: 5 } as _, row (row)}
          <div>
            {vaso[row]}
          </div>
          {#each { length: 5 } as _, col (col)}
            <div
              class={clinicianActions.has(col * 5 - row + 4)
                ? 'bg-blue'
                : 'bg-white'}
              on:click={() => {
                let index = col * 5 - row + 4;
                if (clinicianActions.has(index)) {
                  clinicianActions.delete(index);
                } else {
                  clinicianActions.add(index);
                }
                clinicianActions = new Set(clinicianActions);
                console.log('Clicking' + row + ' ' + col);
                console.log(clinicianActions);
              }}
            />
          {/each}
        {/each}
        <div>
          <div />
        </div>
        <div>
          <div>0</div>
        </div>
        <div>
          <div>20</div>
        </div>
        <div>
          <div>100</div>
        </div>
        <div>
          <div>300</div>
        </div>
        <div>
          <div>819</div>
        </div>
      </div>
    </div>
    <div>
      <div />
      <bold>IV Fluid (mL/4h)</bold>
    </div>
    <h4>Model Actions</h4>
    <div class="flex items-center mb3">
      <div>
        <div>Vasopressor (ug/kg/min)</div>
      </div>
      <div
        class="container bg-light-blue-gray"
        style="grid-template-rows: {rows}; grid-template-columns: {cols};"
      >
        {#each { length: 5 } as _, row (row)}
          <div>
            {vaso[row]}
          </div>
          {#each { length: 5 } as _, col (col)}
            <div
              class={physicianActions.has(col * 5 - row + 4)
                ? 'bg-blue'
                : 'bg-white'}
              on:click={() => {
                let index = col * 5 - row + 4;
                if (physicianActions.has(index)) {
                  physicianActions.delete(index);
                } else {
                  physicianActions.add(index);
                }
                physicianActions = new Set(physicianActions);
                console.log('Clicking' + row + ' ' + col);
                console.log(physicianActions);
              }}
            />
          {/each}
        {/each}
        <div>
          <div />
        </div>
        <div>
          <div>0</div>
        </div>
        <div>
          <div>20</div>
        </div>
        <div>
          <div>100</div>
        </div>
        <div>
          <div>300</div>
        </div>
        <div>
          <div>819</div>
        </div>
      </div>
    </div>
    <div><bold>IV Fluid (mL/4h)</bold></div>

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
    <SelectFilter
      name={'States'}
      bind:selected={selectedStates}
      multi
      items={new Array(750).fill(0).map((_, i) => i)}
    />
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

  .disabled-button {
    opacity: 0.2;
  }

  .container {
    display: grid;
    border: 1px solid #dfe4eb;
    border-radius: 2px;
    width: 200px;
    height: 200px;
    grid-gap: 4px;
    /* background: #999; */
    /* background-color: #dfe4eb; */
  }
</style>
