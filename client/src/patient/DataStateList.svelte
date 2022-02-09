<script>
  import DataFeature from './DataFeature.svelte';
  import Columns from '../utils/columns';

  export let patient;
  export let bloc; // the index of the time to show

  let timePoint;
  let lastTimePoint;
  $: if (!!patient && !!bloc) {
    timePoint = patient.timesteps[bloc - 1];
    lastTimePoint = bloc > 1 ? patient.timesteps[bloc - 2] : null;
  }

  /*

*/
  const featureRowSpec = [
    { feature: Columns.C_SOFA },
    { feature: Columns.C_SIRS },
    { feature: Columns.C_SHOCK_INDEX },
    { feature: Columns.C_PAO2_FIO2 },
    { feature: Columns.C_HEIGHT },
    { feature: Columns.C_WEIGHT },
    { feature: Columns.C_GCS },
    { feature: Columns.C_RASS },
    { feature: Columns.C_HR, maxDecimals: 0 },
    {
      computed: (tp) =>
        `${tp[Columns.C_SYSBP].toFixed(0)}/${tp[Columns.C_DIABP].toFixed(0)}`,
      name: 'Blood Pressure',
    },
    { feature: Columns.C_RR },
    { feature: Columns.C_SPO2 },
    { feature: Columns.C_TEMP_C, maxDecimals: 1 },
    { feature: Columns.C_CVP },
    { feature: Columns.C_PAPSYS },
    { feature: Columns.C_PAPMEAN },
    { feature: Columns.C_PAPDIA },
    { feature: Columns.C_CI },
    { feature: Columns.C_SVR },
    { feature: Columns.C_INTERFACE },
    { feature: Columns.C_FIO2_1 },
    { feature: Columns.C_O2FLOW },
    { feature: Columns.C_PEEP },
    { feature: Columns.C_TIDALVOLUME },
    { feature: Columns.C_MINUTEVENTIL },
    { feature: Columns.C_PAWMEAN },
    { feature: Columns.C_PAWPEAK },
    { feature: Columns.C_PAWPLATEAU },
    { feature: Columns.C_POTASSIUM },
    { feature: Columns.C_SODIUM },
    { feature: Columns.C_CHLORIDE },
    { feature: Columns.C_GLUCOSE },
    { feature: Columns.C_BUN },
    { feature: Columns.C_CREATININE },
    { feature: Columns.C_MAGNESIUM },
    { feature: Columns.C_CALCIUM },
    { feature: Columns.C_IONISED_CA },
    { feature: Columns.C_CO2_MEQL },
    { feature: Columns.C_SGOT },
    { feature: Columns.C_SGPT },
    { feature: Columns.C_TOTAL_BILI },
    { feature: Columns.C_DIRECT_BILI },
    { feature: Columns.C_TOTAL_PROTEIN },
    { feature: Columns.C_ALBUMIN },
    { feature: Columns.C_TROPONIN },
    { feature: Columns.C_CRP },
    { feature: Columns.C_HB },
    { feature: Columns.C_HT },
    { feature: Columns.C_RBC_COUNT },
    { feature: Columns.C_WBC_COUNT },
    { feature: Columns.C_PLATELETS_COUNT },
    { feature: Columns.C_PTT },
    { feature: Columns.C_PT },
    { feature: Columns.C_ACT },
    { feature: Columns.C_INR },
    { feature: Columns.C_ARTERIAL_PH },
    { feature: Columns.C_PAO2 },
    { feature: Columns.C_PACO2 },
    { feature: Columns.C_ARTERIAL_BE },
    { feature: Columns.C_ARTERIAL_LACTATE },
    { feature: Columns.C_HCO3 },
    { feature: Columns.C_ETCO2 },
    { feature: Columns.C_SVO2 },
    { feature: Columns.C_MECHVENT },
    { feature: Columns.C_EXTUBATED },
    { feature: Columns.C_MEDIAN_DOSE_VASO },
    { feature: Columns.C_MAX_DOSE_VASO },
    { feature: Columns.C_INPUT_TOTAL },
    { feature: Columns.C_INPUT_STEP },
    { feature: Columns.C_OUTPUT_TOTAL },
    { feature: Columns.C_OUTPUT_STEP },
    { feature: Columns.C_CUMULATED_BALANCE },
  ];
</script>

<div class="data-state-container ph2 w-100">
  {#if !!timePoint}
    {#each featureRowSpec as row}
      <DataFeature
        feature={row.name || row.feature}
        value={!!row.computed
          ? row.computed(timePoint)
          : timePoint[row.feature]}
        historicalValues={patient.timesteps
          .slice(0, bloc)
          .map((ts) => (!!row.computed ? row.computed(ts) : ts[row.feature]))}
        maxDecimals={row.hasOwnProperty('maxDecimals') ? row.maxDecimals : 3}
      />
    {/each}
    <!-- C_GCS, C_HR, C_SYSBP, C_MEANBP, C_DIABP,
    C_RR, C_TEMP_C, C_FIO2_1, C_POTASSIUM, C_SODIUM,
    C_CHLORIDE, C_GLUCOSE, C_MAGNESIUM, C_CALCIUM, C_HB,
    C_WBC_COUNT, C_PLATELETS_COUNT, C_PTT, C_PT, C_ARTERIAL_PH,
    C_PAO2, C_PACO2, C_ARTERIAL_BE, C_HCO3, C_ARTERIAL_LACTATE,
    C_SOFA, C_SIRS, C_SHOCK_INDEX, C_PAO2_FIO2, C_CUMULATED_BALANCE,
    C_SPO2, C_BUN, C_CREATININE, C_SGOT, C_SGPT,
    C_TOTAL_BILI, C_INR, C_INPUT_TOTAL, C_INPUT_STEP, C_OUTPUT_TOTAL,
    C_OUTPUT_STEP -->
  {/if}
</div>

<style>
</style>
