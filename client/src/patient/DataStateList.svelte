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

  let timePoint;
  let lastTimePoint;
  $: if (!!$patient && !!$currentBloc) {
    timePoint = $patient.timesteps[$currentBloc - 1];
    lastTimePoint =
      $currentBloc > 1 ? $patient.timesteps[$currentBloc - 2] : null;
  }

  const featureRowSpec = {
    [StateCategory.VITALS]: [
      { feature: Columns.C_WEIGHT, name: 'Weight', unit: 'kg' },
      { feature: Columns.C_HR, maxDecimals: 0, unit: 'bpm' },
      {
        feature: Columns.C_TEMP_C,
        name: 'Temperature',
        maxDecimals: 1,
        unit: '&deg;C',
      },
      { feature: Columns.C_MEANBP, name: 'mAP', maxDecimals: 0 },
      {
        computed: (tp) =>
          `${tp[Columns.C_SYSBP].value.toFixed(0)}/${tp[
            Columns.C_DIABP
          ].value.toFixed(0)}`,
        name: 'Blood Pressure',
      },
      { feature: Columns.C_GCS },
      { feature: Columns.C_RASS },
      { feature: Columns.C_SOFA },
      { feature: Columns.C_SIRS },
      { feature: Columns.C_SHOCK_INDEX, name: 'Shock Index' },
    ],
    [StateCategory.LABS]: [
      { feature: Columns.C_POTASSIUM, maxDecimals: 1 },
      { feature: Columns.C_SODIUM, maxDecimals: 1 },
      { feature: Columns.C_CHLORIDE, maxDecimals: 1 },
      { feature: Columns.C_GLUCOSE, maxDecimals: 1 },
      { feature: Columns.C_BUN, maxDecimals: 1 },
      { feature: Columns.C_CREATININE, maxDecimals: 1 },
      { feature: Columns.C_MAGNESIUM, maxDecimals: 1 },
      { feature: Columns.C_CALCIUM, maxDecimals: 1 },
      { feature: Columns.C_IONISED_CA, maxDecimals: 1 },
      { feature: Columns.C_CO2_MEQL, maxDecimals: 1 },
      { feature: Columns.C_SGOT, maxDecimals: 1 },
      { feature: Columns.C_SGPT, maxDecimals: 1 },
      { feature: Columns.C_TOTAL_BILI },
      { feature: Columns.C_DIRECT_BILI },
      { feature: Columns.C_TOTAL_PROTEIN },
      { feature: Columns.C_ALBUMIN },
      { feature: Columns.C_TROPONIN },
      { feature: Columns.C_CRP },
      { feature: Columns.C_HB, maxDecimals: 1 },
      { feature: Columns.C_HT, maxDecimals: 1 },
      { feature: Columns.C_RBC_COUNT, maxDecimals: 1 },
      { feature: Columns.C_WBC_COUNT, maxDecimals: 1 },
      { feature: Columns.C_PLATELETS_COUNT, maxDecimals: 1 },
      { feature: Columns.C_PTT, maxDecimals: 1 },
      { feature: Columns.C_PT, maxDecimals: 1 },
      { feature: Columns.C_ACT, maxDecimals: 1 },
      { feature: Columns.C_INR, maxDecimals: 1 },
      { feature: Columns.C_ARTERIAL_PH },
      { feature: Columns.C_PAO2 },
      { feature: Columns.C_PACO2 },
      { feature: Columns.C_ARTERIAL_BE },
      { feature: Columns.C_ARTERIAL_LACTATE },
      { feature: Columns.C_HCO3 },
    ],
    [StateCategory.RESPIRATORY]: [
      { feature: Columns.C_PAO2_FIO2, maxDecimals: 1 },
      { feature: Columns.C_RR, maxDecimals: 1 },
      { feature: Columns.C_SPO2, maxDecimals: 1 },
      { feature: Columns.C_PAPSYS },
      { feature: Columns.C_PAPMEAN },
      { feature: Columns.C_PAPDIA },
      { feature: Columns.C_CI },
      { feature: Columns.C_SVR },
      { feature: Columns.C_INTERFACE },
      { feature: Columns.C_FIO2_1, name: 'FiO2', maxDecimals: 2 },
      { feature: Columns.C_O2FLOW },
      { feature: Columns.C_PEEP },
      { feature: Columns.C_TIDALVOLUME, maxDecimals: 1 },
      { feature: Columns.C_MINUTEVENTIL, maxDecimals: 2 },
      { feature: Columns.C_PAWMEAN, maxDecimals: 1 },
      { feature: Columns.C_PAWPEAK, maxDecimals: 1 },
      { feature: Columns.C_PAWPLATEAU, maxDecimals: 1 },
      { feature: Columns.C_ETCO2 },
      { feature: Columns.C_SVO2 },
      { feature: Columns.C_CVP, maxDecimals: 1 },
      { feature: Columns.C_MECHVENT },
      { feature: Columns.C_EXTUBATED },
    ],
    [StateCategory.FLUIDS_PRESSORS]: [
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
  };

  let featureRows = [];
  $: if (category != null) {
    featureRows = featureRowSpec[category];
  } else {
    featureRows = [
      StateCategory.VITALS,
      StateCategory.LABS,
      StateCategory.RESPIRATORY,
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
        blocNumber - currentTrendWindow
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

<div class="data-state-container w-100 ph2">
  <table class="w-100">
    {#if !!timePoint}
      {#each featureRows as row}
        <DataFeature
          feature={row.name || row.feature}
          value={!!row.computed
            ? row.computed(timePoint)
            : timePoint[row.feature] != null
            ? timePoint[row.feature].value
            : null}
          historicalValues={$patient.timesteps
            .slice(0, $currentBloc)
            .map((ts) =>
              !!row.computed
                ? row.computed(ts)
                : ts[row.feature] != null
                ? ts[row.feature].value
                : null
            )}
          extremeValue={!row.computed
            ? detectExtremeValue(
                row.feature,
                timePoint[row.feature] != null
                  ? timePoint[row.feature].value
                  : null,
                $patient.gender
              )
            : 0}
          maxDecimals={row.hasOwnProperty('maxDecimals') ? row.maxDecimals : 3}
          trend={!row.computed ? computeTrend(row.feature, $currentBloc) : 0}
          unit={row.unit}
        />
      {/each}
    {/if}
  </table>
</div>

<style>
  .data-state-container table {
    border-collapse: collapse;
  }
</style>
