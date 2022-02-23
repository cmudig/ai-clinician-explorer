import Columns from '../utils/columns';

export const NormalRanges = {
  // Chart events
  [Columns.C_GCS]: { min: 12 },
  [Columns.C_RASS]: { min: -3, max: 2 },
  [Columns.C_HR]: { min: 60, max: 100 },
  [Columns.C_SYSBP]: { max: 129 },
  [Columns.C_MEANBP]: { min: 60, max: 100 },
  [Columns.C_DIABP]: { max: 79 },
  [Columns.C_RR]: { min: 12, max: 20 },
  // C_SPO2: 'SpO2',
  [Columns.C_TEMP_C]: { min: 36.5, max: 37.2 },
  // C_CVP: 'CVP',
  // C_PAPSYS: 'PAPsys',
  // C_PAPMEAN: 'PAPmean',
  // C_PAPDIA: 'PAPdia',
  // C_CI: 'CI',
  // C_SVR: 'SVR',
  // C_FIO2_1: 'FiO2_1',
  // C_O2FLOW: 'O2flow',
  // C_PEEP: 'PEEP',
  // C_TIDALVOLUME: 'TidalVolume',
  // C_MINUTEVENTIL: 'MinuteVentil',
  // C_PAWMEAN: 'PAWmean',
  // C_PAWPEAK: 'PAWpeak',
  // C_PAWPLATEAU: 'PAWplateau',

  // Labs
  [Columns.C_POTASSIUM]: { min: 3.4, max: 5 },
  [Columns.C_SODIUM]: { min: 135, max: 145 },
  [Columns.C_CHLORIDE]: { min: 95, max: 108 },
  [Columns.C_GLUCOSE]: { min: 70, max: 110 },
  [Columns.C_BUN]: { min: 8, max: 25 },
  [Columns.C_CREATININE]: {
    female: { min: 0.6, max: 1.8 },
    male: { min: 0.8, max: 2.4 },
  },
  [Columns.C_MAGNESIUM]: { min: 1.7, max: 2.2 },
  [Columns.C_CALCIUM]: { min: 8.5, max: 10.5 },
  [Columns.C_IONISED_CA]: { min: 4.8, max: 5.6 },
  // C_CO2_MEQL: 'CO2_mEqL',
  [Columns.C_SGOT]: { female: { min: 9, max: 25 }, male: { min: 10, max: 40 } },
  [Columns.C_SGPT]: { female: { min: 7, max: 30 }, male: { min: 10, max: 55 } },
  [Columns.C_TOTAL_BILI]: { min: 0, max: 1 },
  [Columns.C_DIRECT_BILI]: { min: 0, max: 0.4 },
  [Columns.C_TOTAL_PROTEIN]: { min: 6, max: 8.3 },
  [Columns.C_ALBUMIN]: { min: 3.1, max: 4.3 },
  [Columns.C_TROPONIN]: { max: 0.04 },
  [Columns.C_CRP]: { max: 10 },
  [Columns.C_HB]: { female: { min: 12, max: 16 }, male: { min: 13, max: 18 } },
  [Columns.C_HT]: { female: { min: 36, max: 46 }, male: { min: 37, max: 49 } },
  [Columns.C_RBC_COUNT]: {
    female: { min: 3.92, max: 5.13 },
    male: { min: 4.35, max: 5.65 },
  },
  [Columns.C_WBC_COUNT]: { min: 4.5, max: 11 },
  [Columns.C_PLATELETS_COUNT]: { min: 130, max: 400 },
  [Columns.C_PTT]: { min: 60, max: 70 },
  [Columns.C_PT]: { min: 11, max: 13.5 },
  [Columns.C_ACT]: { min: 70, max: 120 },
  [Columns.C_INR]: { min: 0.8, max: 1.1 },
  [Columns.C_ARTERIAL_PH]: { min: 7.35, max: 7.45 },
  [Columns.C_PAO2]: { min: 75, max: 100 },
  [Columns.C_PACO2]: { min: 35, max: 45 },
  [Columns.C_ARTERIAL_BE]: { min: -4, max: 2 },
  [Columns.C_ARTERIAL_LACTATE]: { min: 0.5, max: 1.6 },
  [Columns.C_HCO3]: { min: 20, max: 32 },
  [Columns.C_ETCO2]: { min: 35, max: 45 },
  [Columns.C_SVO2]: { min: 65, max: 75 },

  // Computed
  [Columns.C_SHOCK_INDEX]: { min: 0.5, max: 0.7 },
  [Columns.C_PAO2_FIO2]: { min: 400, max: 500 },
};

// returns 1 if the value is too high for the feature, -1 if too low, 0 otherwise
export function detectExtremeValue(feature, value, isFemale) {
  if (!NormalRanges.hasOwnProperty(feature) || value == null) return 0;
  let range = NormalRanges[feature];
  if (range.female) {
    range = isFemale ? range.female : range.male;
  }
  if (range.hasOwnProperty('min') && value < range.min) {
    return -1;
  } else if (range.hasOwnProperty('max') && value > range.max) {
    return 1;
  }
  return 0;
}
