<script>
  import ActionFilter from './ActionFilter.svelte';
  import RangeFilter from './RangeFilter.svelte';
  import SelectFilter from './SelectFilter.svelte';
  import { Comorbidities } from '../utils/strings';
  import TextFilter from './TextFilter.svelte';
  import { onMount } from 'svelte';

  export let externalFilters;

  let FilterSpec = [
    {
      id: 'gender',
      name: 'Gender',
      type: 'select',
      items: [
        { label: 'Male', value: 0 },
        { label: 'Female', value: 1 },
      ],
      value: null,
    },
    {
      id: 'age',
      name: 'Age',
      type: 'range',
      default: [18, 110],
      value: [18, 110],
    },
    {
      id: 'elixhauser',
      name: 'Elixhauser',
      type: 'range',
      default: [0, 15],
      value: [0, 15],
    },
    {
      id: 'comorbidities',
      comorbidities: true,
      name: 'Comorbidities',
      type: 'select',
      multi: true,
      items: Object.keys(Comorbidities).map((k) => ({
        value: k,
        label: Comorbidities[k],
      })),
      value: null,
      filterFunction: (value) =>
        !!value
          ? '(' + value.map((v) => `${v.value} = 1`).join(' or ') + ')'
          : [],
    },
    {
      id: 'num_timesteps',
      name: 'ICU Stay Length',
      type: 'range',
      step: 4,
      default: [0, 160],
      value: [0, 160],
      filterFunction: (value) => {
        return [
          'num_timesteps >= ' + value[0] / 4,
          'num_timesteps <= ' + value[1] / 4,
        ];
      },
    },
    {
      id: 'died_in_hosp',
      name: 'Discharge Status',
      type: 'select',
      items: [
        { label: 'Alive', value: 0 },
        { label: 'Death', value: 1 },
      ],
      value: null,
    },
    {
      id: 'max_SOFA',
      name: 'Max SOFA',
      type: 'range',
      default: [0, 20],
      value: [0, 20],
    },
    {
      id: 'max_SIRS',
      name: 'Max SIRS',
      type: 'range',
      default: [0, 4],
      value: [0, 4],
    },
    {
      type: 'divider',
    },
    {
      type: 'title',
      name: 'Aggregate Actions',
    },
    {
      id: 'avg_action_difference',
      name: 'Avg Action Difference',
      type: 'range',
      step: 0.1,
      default: [0, 7],
      value: [0, 7],
      tooltip:
        'The combined difference between the fluid and vasopressor dosage levels prescribed by the clinician and the model, averaged over the patient trajectory.',
    },
    {
      id: 'avg_phys_probability',
      name: 'Avg Clinician Probability',
      type: 'range',
      step: 0.05,
      default: [0, 1],
      value: [0, 1],
      tooltip:
        'The probability of the action the clinician took compared to all actions taken by clinicians in each state, averaged over the patient trajectory.',
    },
    {
      id: 'avg_model_probability',
      name: 'Avg Model Probability',
      type: 'range',
      step: 0.05,
      default: [0, 1],
      value: [0, 1],
      tooltip:
        'The probability of the action the model chose compared to all actions taken by clinicians in each state, averaged over the patient trajectory.',
    },
    {
      type: 'divider',
    },
    {
      type: 'title',
      name: 'Timestep-Specific',
    },
    {
      id: 'state',
      name: 'States',
      type: 'select',
      multi: true,
      items: new Array(750).fill(0).map((_, i) => i),
      value: null,
    },
    {
      type: 'group',
      elements: [
        {
          name: 'Clinician Fluids',
          type: 'range',
          default: [0, 4],
          value: [0, 4],
        },
        {
          name: 'Clinician Vasopressors',
          type: 'range',
          default: [0, 4],
          value: [0, 4],
        },
      ],
      filterFunction: (values) => {
        let allowedPhysicianActions = new Array(25)
          .fill(0)
          .map((_, ac) => ac)
          .filter(
            (ac) =>
              Math.floor(ac / 5) >= values[0][0] &&
              Math.floor(ac / 5) <= values[0][1] &&
              Math.floor(ac % 5) >= values[1][0] &&
              Math.floor(ac % 5) <= values[1][1],
          );
        if (allowedPhysicianActions.length < 25)
          return [
            'physician_action in (' + allowedPhysicianActions.join(', ') + ')',
          ];
        return [];
      },
    },
    {
      type: 'group',
      elements: [
        {
          name: 'Model Fluids',
          type: 'range',
          default: [0, 4],
          value: [0, 4],
        },
        {
          name: 'Model Vasopressors',
          type: 'range',
          default: [0, 4],
          value: [0, 4],
        },
      ],
      filterFunction: (values) => {
        let allowedModelActions = new Array(25)
          .fill(0)
          .map((_, ac) => ac)
          .filter(
            (ac) =>
              Math.floor(ac / 5) >= values[0][0] &&
              Math.floor(ac / 5) <= values[0][1] &&
              Math.floor(ac % 5) >= values[1][0] &&
              Math.floor(ac % 5) <= values[1][1],
          );
        if (allowedModelActions.length < 25)
          return ['model_action in (' + allowedModelActions.join(', ') + ')'];
        return [];
      },
    },
    {
      id: 'phys_probability',
      name: 'Clinician Probability',
      type: 'range',
      step: 0.05,
      default: [0, 1],
      value: [0, 1],
      tooltip:
        'The probability of the action the clinician took compared to all actions taken by clinicians in this state.',
    },
    {
      id: 'model_probability',
      name: 'Model Probability',
      type: 'range',
      step: 0.05,
      default: [0, 1],
      value: [0, 1],
      tooltip:
        'The probability of the action the model chose compared to all actions taken by clinicians in this state.',
    },
    {
      id: 'phys_Q',
      name: 'Clinician Action Value',
      type: 'range',
      step: 5,
      default: [-100, 100],
      value: [-100, 100],
      tooltip: 'The model-predicted value of the action the clinician took.',
    },
    {
      id: 'model_Q',
      name: 'Model Action Value',
      type: 'range',
      step: 5,
      default: [-100, 100],
      value: [-100, 100],
      tooltip: 'The model-predicted value of the action the model chose',
    },
    {
      id: 'physician_entropy',
      name: 'Clinician Entropy',
      type: 'range',
      step: 0.1,
      default: [0, 5],
      value: [0, 5],
      tooltip:
        'The entropy of the clinician action distribution (lower is more "peaky").',
    },
    {
      id: 'model_entropy',
      name: 'Model Entropy',
      type: 'range',
      step: 0.1,
      default: [0, 5],
      value: [0, 5],
      tooltip:
        'The entropy of the model value distribution (lower is more "peaky").',
    },
  ];

  function makeEmptyFilter() {
    return { filters: '', comorbidityFilters: '' };
  }
  export let filter;
  onMount(() => {
    filter = makeEmptyFilter();
    if (!!externalFilters) applyExternalFilters();
  });

  // Store the filter statement that would be generated with the current values.
  // When the user clicks the Apply button this statement will be transferred to
  // the filterStatement variable.
  let tempFilters = '';
  let tempComorbidityFilters = '';

  let filterEmpty = true;

  function makeFiltersFromFilterSpec(f) {
    if (!!f.filterFunction) {
      if (f.type == 'group')
        return f.filterFunction(f.elements.map((subf) => subf.value));
      return f.filterFunction(f.value);
    }
    if (f.type == 'range')
      return [`${f.id} >= ${f.value[0]}`, `${f.id} <= ${f.value[1]}`];
    else if (f.type == 'select' && !f.multi)
      return f.value != null ? [`${f.id} = ` + f.value.value] : [];
    else if (f.type == 'select' && f.multi)
      return f.value != null
        ? [`${f.id} in (` + f.value.map((v) => v.value).join(', ') + ')']
        : [];
    else if (f.type == 'group')
      return f.elements.map(makeFiltersFromFilterSpec).flat();
    return [];
  }

  function resetFiltersRecursive(f) {
    let obj = Object.assign({}, f);
    obj.value = obj.default || null;
    if (obj.type == 'group')
      obj.elements = obj.elements.map(resetFiltersRecursive);
    return obj;
  }

  function filtersEmptyRecursive(f) {
    if (f.type == 'group') return f.elements.every(filtersEmptyRecursive);
    else if (f.type == 'range')
      return f.value[0] == f.default[0] && f.value[1] == f.default[1];
    else if (f.type == 'select' && !f.multi) return f.value == null;
    else if (f.type == 'select' && f.multi)
      return !f.value || f.value.length == 0;
    return true;
  }

  $: {
    tempFilters = FilterSpec.filter(
      (f) => !f.comorbidities && !f.antibiotics && !f.microbio,
    )
      .filter((f) => !filtersEmptyRecursive(f))
      .map(makeFiltersFromFilterSpec)
      .flat()
      .join(';');

    /*if (!filter.filters) {
      let obj = makeEmptyFilter();
      Object.assign(obj, filter);
      obj.filters = tempFilters;
      filter = obj;
      console.log('reassigning filter', filter);
    }*/

    tempComorbidityFilters = FilterSpec.filter((f) => f.comorbidities)
      .filter((f) => !filtersEmptyRecursive(f))
      .map(makeFiltersFromFilterSpec)
      .flat()
      .join(';');
    if (!!tempFilters || tempComorbidityFilters)
      console.log(tempFilters, tempComorbidityFilters);
  }

  $: if (!!externalFilters) {
    applyExternalFilters();
  }

  function applyExternalFilters() {
    let newSpec = [...FilterSpec];
    Object.keys(externalFilters).forEach((k) => {
      let index = FilterSpec.findIndex((f) => f.id == k);
      if (index >= 0) {
        let obj = Object.assign({}, FilterSpec[index]);
        obj.value = externalFilters[k];
        newSpec[index] = obj;
      } else {
        console.warn('No filter found with id ' + k);
      }
    });
    FilterSpec = newSpec;
    setTimeout(() => {
      if (filterNeedsUpdate) updateFilter();
    });
  }

  $: filterEmpty = FilterSpec.every(filtersEmptyRecursive);

  function resetFilter() {
    FilterSpec = FilterSpec.map(resetFiltersRecursive);
    setTimeout(() => {
      if (filterNeedsUpdate) updateFilter();
    });
  }

  function updateFilter() {
    console.log('temp filters:', tempFilters);
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
    {#each FilterSpec.map( (f) => (f.type == 'group' ? f.elements : [f]), ).flat() as f}
      {#if f.type == 'range'}
        <RangeFilter
          min={f.default[0]}
          max={f.default[1]}
          step={f.step || 1}
          name={f.name}
          tooltip={f.tooltip}
          bind:range={f.value}
        />
      {:else if f.type == 'select'}
        <SelectFilter
          name={f.name}
          items={f.items}
          multi={f.multi}
          tooltip={f.tooltip}
          bind:selected={f.value}
        />
      {:else if f.type == 'divider'}
        <hr class="mv3" />
      {:else if f.type == 'title'}
        <p class="mt0 mb4 f6 ttu b">{f.name}</p>
      {/if}
    {/each}
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
