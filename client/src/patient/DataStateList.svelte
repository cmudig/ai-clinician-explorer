<script>
  import DataFeature from './DataFeature.svelte';
  import Columns from '../utils/columns';
  import { getContext } from 'svelte';
  import { StateCategory } from '../utils/strings';
  import { detectExtremeValue } from '../utils/ranges';

  let { patient, currentBloc } = getContext('patient');
  export let lastTrendWindow = 1; // number of timesteps to average over for last trend window
  export let currentTrendWindow = 1; // number of timesteps to average over for current trend window
  export let trendThreshold = 0.0; // fraction of last average value to consider as the same
  export let category; // category of features to display - null displays all
  export let highlightImputedValues = true;
  export let highlightHeldValues = false;

  let timePoint;
  let lastTimePoint;
  $: if (!!$patient && !!$currentBloc) {
    timePoint = $patient.timesteps[$currentBloc - 1];
    lastTimePoint =
      $currentBloc > 1 ? $patient.timesteps[$currentBloc - 2] : null;
  }

  function everVentilated(tp) {
    return (
      (tp[Columns.C_MECHVENT] || { value: null }).value ||
      (tp[Columns.C_EXTUBATED] || { value: null }).value
    );
  }

  const featureRowSpec = {
    [StateCategory.VITALS]: [
      {
        rows: [
          { feature: Columns.C_WEIGHT, name: 'Weight', unit: 'kg' },
          { feature: Columns.C_HR, maxDecimals: 0, unit: 'bpm' },
          {
            feature: Columns.C_TEMP_C,
            name: 'Temperature',
            maxDecimals: 1,
            unit: '&deg;C',
          },
          {
            feature: Columns.C_MEANBP,
            name: 'mAP',
            maxDecimals: 0,
            unit: 'mmHg',
          },
          {
            computed: (tp) =>
              `${tp[Columns.C_SYSBP].value.toFixed(0)}/${tp[
                Columns.C_DIABP
              ].value.toFixed(0)}`,
            name: 'Blood Pressure',
            unit: 'mmHg',
          },
          { feature: Columns.C_CVP, maxDecimals: 1, unit: 'mmHg' },
          { feature: Columns.C_GCS },
          { feature: Columns.C_RASS },
          { feature: Columns.C_SOFA },
          // { feature: Columns.C_SIRS },
          // { feature: Columns.C_SHOCK_INDEX, name: 'Shock Index' },
        ],
      },
    ],
    [StateCategory.LABS]: [
      {
        header: 'Chemistries',
        expanded: true,
        rows: [
          { feature: Columns.C_SODIUM, maxDecimals: 1, unit: 'mEq/L' },
          { feature: Columns.C_POTASSIUM, maxDecimals: 1, unit: 'mEq/L' },
          { feature: Columns.C_CHLORIDE, maxDecimals: 1, unit: 'mEq/L' },
          {
            feature: Columns.C_CO2_MEQL,
            name: 'Bicarbonate',
            maxDecimals: 1,
            unit: 'mMol/L',
          },
          { feature: Columns.C_CREATININE, maxDecimals: 1, unit: 'mg/dL' },
          { feature: Columns.C_BUN, maxDecimals: 1, unit: 'mg/dL' },
          { feature: Columns.C_GLUCOSE, maxDecimals: 1, unit: 'mmol/L' },
          { feature: Columns.C_CALCIUM, maxDecimals: 1, unit: 'mg/dL' },
          {
            feature: Columns.C_IONISED_CA,
            name: 'Ionized Ca',
            maxDecimals: 1,
            unit: 'mg/dL',
          },
          { feature: Columns.C_MAGNESIUM, maxDecimals: 1, unit: 'mEq/L' },
        ],
      },

      {
        header: 'CBC',
        expanded: true,
        rows: [
          {
            feature: Columns.C_WBC_COUNT,
            maxDecimals: 1,
            unit: 'x 10<sup>9</sup>/L',
          },
          {
            feature: Columns.C_HB,
            name: 'Hemoglobin',
            maxDecimals: 1,
            unit: 'gm/dL',
          },
          {
            feature: Columns.C_HT,
            name: 'Hematocrit',
            maxDecimals: 1,
            unit: '%',
          },
          {
            feature: Columns.C_PLATELETS_COUNT,
            name: 'Platelets',
            maxDecimals: 1,
            unit: 'x 10<sup>9</sup>/L',
          },
        ],
      },

      {
        header: 'Liver',
        expanded: true,
        rows: [
          {
            feature: Columns.C_SGOT,
            name: 'AST',
            maxDecimals: 1,
            unit: 'IU/L',
          },
          {
            feature: Columns.C_SGPT,
            name: 'ALT',
            maxDecimals: 1,
            unit: 'IU/L',
          },
          { feature: Columns.C_TOTAL_BILI, name: 'Total Bili', unit: 'mg/dL' },
          {
            feature: Columns.C_DIRECT_BILI,
            name: 'Direct Bili',
            unit: 'mg/dL',
          },
          {
            feature: Columns.C_TOTAL_PROTEIN,
            name: 'Total Protein',
            unit: 'gm/dL',
          },
          { feature: Columns.C_ALBUMIN, name: 'Albumin', unit: 'gm/dL' },
        ],
      },

      {
        header: 'Cardiac',
        expanded: true,
        rows: [
          {
            feature: Columns.C_ARTERIAL_LACTATE,
            name: 'Arterial Lactate',
            unit: 'mmol/L',
          },
          { feature: Columns.C_TROPONIN, name: 'Troponin', unit: 'ng/mL' },
          { feature: Columns.C_CRP, unit: 'mg/dL' },
        ],
      },

      {
        header: 'Coags',
        expanded: true,
        rows: [
          { feature: Columns.C_PTT, maxDecimals: 1, unit: 'sec' },
          { feature: Columns.C_PT, maxDecimals: 1, unit: 'sec' },
          { feature: Columns.C_INR, maxDecimals: 1 },
        ],
      },

      {
        header: 'ABG',
        expanded: true,
        rows: [
          { feature: Columns.C_ARTERIAL_PH, name: 'Arterial pH' },
          { feature: Columns.C_PAO2, name: 'paO<sub>2</sub>', unit: 'mmHg' },
          { feature: Columns.C_PACO2, name: 'paCO<sub>2</sub>', unit: 'mmHg' },
        ],
      },
      // { feature: Columns.C_RBC_COUNT, maxDecimals: 1 },
      // { feature: Columns.C_ACT, maxDecimals: 1 },
      // { feature: Columns.C_ARTERIAL_BE },
      // { feature: Columns.C_HCO3 },
    ],
    [StateCategory.CARDIOPULM]: [
      {
        header: 'Vent Settings',
        expanded: true,
        rows: [
          {
            name: 'Ever ventilated?',
            computed: (tp) => (everVentilated(tp) ? 'Yes' : 'No'),
          },
          {
            name: 'Currently ventilated?',
            computed: (tp) =>
              (tp[Columns.C_MECHVENT] || { value: null }).value ? 'Yes' : 'No',
          },
          {
            feature: Columns.C_TIDALVOLUME,
            maxDecimals: 1,
            unit: 'mL',
            condition: everVentilated,
          },
          {
            feature: Columns.C_RR,
            maxDecimals: 1,
            condition: everVentilated,
            unit: 'bpm',
          },
          {
            feature: Columns.C_PEEP,
            condition: everVentilated,
            unit: 'cmH<sub>2</sub>O',
          },
          {
            feature: Columns.C_FIO2_1,
            name: 'FiO2',
            maxDecimals: 2,
            unit: '%',
            condition: everVentilated,
          },
          {
            feature: Columns.C_SPO2,
            maxDecimals: 1,
            unit: '%',
            condition: everVentilated,
          },
          {
            feature: Columns.C_PAO2_FIO2,
            name: 'P:F ratio',
            maxDecimals: 1,
            condition: everVentilated,
          },
          {
            feature: Columns.C_MINUTEVENTIL,
            maxDecimals: 2,
            condition: everVentilated,
            unit: 'mL/min',
          },
          {
            feature: Columns.C_PAWPLATEAU,
            maxDecimals: 1,
            condition: everVentilated,
            unit: 'cmH<sub>2</sub>O',
          },
          {
            feature: Columns.C_PAWPEAK,
            maxDecimals: 1,
            condition: everVentilated,
            unit: 'cmH<sub>2</sub>O',
          },
          {
            feature: Columns.C_PAWMEAN,
            maxDecimals: 1,
            condition: everVentilated,
            unit: 'cmH<sub>2</sub>O',
          },
        ],
      },
      {
        header: 'O<sub>2</sub> Flow',
        expanded: true,
        rows: [{ feature: Columns.C_O2FLOW, unit: 'L/min' }],
      },
      {
        header: 'Other',
        expanded: true,
        rows: [
          { feature: Columns.C_CI, unit: 'L/min/m<sup>2</sup>' },
          { feature: Columns.C_PAPMEAN, unit: 'mmHg' },
          {
            computed: (tp) =>
              !!tp[Columns.C_PAPSYS].value && !!tp[Columns.C_PAPDIA].value
                ? `${tp[Columns.C_PAPSYS].value.toFixed(0)}/${tp[
                    Columns.C_PAPDIA
                  ].value.toFixed(0)}`
                : '--',
            name: 'PAP',
            unit: 'mmHg',
          },
          { feature: Columns.C_SVR },
          // { feature: Columns.C_INTERFACE },
          // { feature: Columns.C_ETCO2 },
          { feature: Columns.C_SVO2 },
          // { feature: Columns.C_MECHVENT },
          // { feature: Columns.C_EXTUBATED },
        ],
      },
    ],
    [StateCategory.FLUIDS_PRESSORS]: [
      {
        rows: [
          {
            feature: Columns.C_MAX_DOSE_VASO,
            name: 'Vasopressor',
            unit: 'ug/kg/min',
          },
          { feature: Columns.C_INPUT_STEP, name: 'IV Fluids', unit: 'ml/4h' },
          { feature: Columns.C_OUTPUT_STEP, name: 'Output', unit: 'ml/4h' },
          {
            feature: Columns.C_CUMULATED_BALANCE,
            maxDecimals: 0,
            name: 'Fluid Balance',
            unit: 'ml/4h',
          },
        ],
      },
    ],
  };

  let featureRows = [];
  $: if (category != null) {
    featureRows = featureRowSpec[category];
  } else {
    featureRows = [
      StateCategory.VITALS,
      StateCategory.LABS,
      StateCategory.CARDIOPULM,
      StateCategory.FLUIDS_PRESSORS,
    ]
      .map((c) => featureRowSpec[c] || [])
      .flat();
  }

  /*
    Computes whether the values for the given feature have increased or
    decreased in the past trendWindow timesteps relative to the trendWindow
    timesteps before that.
  */
  function computeTrend(feature, blocNumber) {
    if (!blocNumber || blocNumber < currentTrendWindow) return 0;
    let lastWindow = $patient.timesteps
      .slice(
        Math.max(0, blocNumber - currentTrendWindow - lastTrendWindow),
        blocNumber - currentTrendWindow,
      )
      .map((v) => (v[feature] != null ? v[feature].value : null))
      .filter((v) => v != null && v != undefined);
    if (lastWindow.length == 0) return 0;
    let lastValue =
      lastWindow.reduce((curr, v) => curr + v) / lastWindow.length;
    let currWindow = $patient.timesteps
      .slice(blocNumber - currentTrendWindow, blocNumber)
      .map((v) => (v[feature] != null ? v[feature].value : null))
      .filter((v) => v != null && v != undefined);
    if (currWindow.length == 0) return 0;
    let currValue =
      currWindow.reduce((curr, v) => curr + v) / currWindow.length;
    if (currValue - lastValue >= lastValue * trendThreshold + 1e-3) return 1;
    else if (currValue - lastValue <= -lastValue * trendThreshold - 1e-3)
      return -1;
    return 0;
  }
</script>

<div class="data-state-container w-100">
  <table class="w-100">
    {#if !!timePoint}
      {#each featureRows as section}
        {#if !!section.header}
          <tr>
            <td
              class="header-row pointer b f6 dark-gray"
              colspan="3"
              on:click={() => (section.expanded = !section.expanded)}
            >
              <i class="arrow {section.expanded ? 'down' : 'right'}" />
              <span class="pl2">{@html section.header}</span>
            </td>
          </tr>
        {/if}
        {#if !section.hasOwnProperty('expanded') || section.expanded}
          {#each section.rows as row}
            {#if !row.condition || row.condition(timePoint)}
              <DataFeature
                patientID={$patient[Columns.C_ICUSTAYID]}
                feature={row.name || row.feature}
                value={!!row.computed
                  ? row.computed(timePoint)
                  : timePoint[row.feature] != null
                  ? timePoint[row.feature].value
                  : null}
                historicalValues={$patient.timesteps
                  .slice(0, $currentBloc)
                  .map((ts) =>
                    !!row.computed ? row.computed(ts) : ts[row.feature],
                  )}
                extremeValue={!row.computed
                  ? detectExtremeValue(
                      row.feature,
                      timePoint[row.feature] != null
                        ? timePoint[row.feature].value
                        : null,
                      $patient.gender,
                    )
                  : 0}
                maxDecimals={row.hasOwnProperty('maxDecimals')
                  ? row.maxDecimals
                  : 3}
                trend={!row.computed
                  ? computeTrend(row.feature, $currentBloc)
                  : 0}
                unit={row.unit}
                {highlightHeldValues}
                {highlightImputedValues}
              />
            {/if}
          {/each}
        {/if}
      {/each}
    {/if}
  </table>
</div>

<style>
  .data-state-container table {
    border-collapse: collapse;
  }

  .header-row {
    padding: 18px 12px 18px 14px;
    background-color: #024fc220;
    border-bottom: 1px solid #cccccc;
    text-transform: uppercase;
  }

  .header-row:hover {
    padding: 18px 12px 18px 14px;
    background-color: rgba(2, 70, 172, 0.188);
    border-bottom: 1px solid #cccccc;
  }

  .header-row:focus {
    padding: 18px 12px 18px 14px;
    background-color: rgba(1, 60, 148, 0.188);
    border-bottom: 1px solid #cccccc;
  }

  .arrow {
    border: solid black;
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 3px;
  }

  .arrow.right {
    transform: rotate(-45deg) translateY(-2px);
    -webkit-transform: rotate(-45deg) translateY(-2px);
  }

  .arrow.down {
    transform: rotate(45deg) translateY(-4px);
    -webkit-transform: rotate(45deg) translateY(-4px);
  }
</style>
