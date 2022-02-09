const Columns = {
  // Demographics and timestamps
  C_BLOC: 'bloc',
  C_ICUSTAYID: 'icustayid',
  C_CHARTTIME: 'charttime',
  C_GENDER: 'gender',
  C_AGE: 'age',
  C_ELIXHAUSER: 'elixhauser',
  C_RE_ADMISSION: 're_admission',
  C_DIED_IN_HOSP: 'died_in_hosp',
  C_DIED_WITHIN_48H_OF_OUT_TIME: 'died_within_48h_of_out_time',
  C_MORTA_90: 'morta_90',
  C_DELAY_END_OF_RECORD_AND_DISCHARGE_OR_DEATH:
    'delay_end_of_record_and_discharge_or_death',

  // Chart events
  C_HEIGHT: 'Height_cm',
  C_WEIGHT: 'Weight_kg',
  C_GCS: 'GCS',
  C_RASS: 'RASS',
  C_HR: 'HR',
  C_SYSBP: 'SysBP',
  C_MEANBP: 'MeanBP',
  C_DIABP: 'DiaBP',
  C_RR: 'RR',
  C_SPO2: 'SpO2',
  C_TEMP_C: 'Temp_C',
  C_TEMP_F: 'Temp_F',
  C_CVP: 'CVP',
  C_PAPSYS: 'PAPsys',
  C_PAPMEAN: 'PAPmean',
  C_PAPDIA: 'PAPdia',
  C_CI: 'CI',
  C_SVR: 'SVR',
  C_INTERFACE: 'Interface',
  C_FIO2_100: 'FiO2_100',
  C_FIO2_1: 'FiO2_1',
  C_O2FLOW: 'O2flow',
  C_PEEP: 'PEEP',
  C_TIDALVOLUME: 'TidalVolume',
  C_MINUTEVENTIL: 'MinuteVentil',
  C_PAWMEAN: 'PAWmean',
  C_PAWPEAK: 'PAWpeak',
  C_PAWPLATEAU: 'PAWplateau',

  // Labs
  C_POTASSIUM: 'Potassium',
  C_SODIUM: 'Sodium',
  C_CHLORIDE: 'Chloride',
  C_GLUCOSE: 'Glucose',
  C_BUN: 'BUN',
  C_CREATININE: 'Creatinine',
  C_MAGNESIUM: 'Magnesium',
  C_CALCIUM: 'Calcium',
  C_IONISED_CA: 'Ionised_Ca',
  C_CO2_MEQL: 'CO2_mEqL',
  C_SGOT: 'SGOT',
  C_SGPT: 'SGPT',
  C_TOTAL_BILI: 'Total_bili',
  C_DIRECT_BILI: 'Direct_bili',
  C_TOTAL_PROTEIN: 'Total_protein',
  C_ALBUMIN: 'Albumin',
  C_TROPONIN: 'Troponin',
  C_CRP: 'CRP',
  C_HB: 'Hb',
  C_HT: 'Ht',
  C_RBC_COUNT: 'RBC_count',
  C_WBC_COUNT: 'WBC_count',
  C_PLATELETS_COUNT: 'Platelets_count',
  C_PTT: 'PTT',
  C_PT: 'PT',
  C_ACT: 'ACT',
  C_INR: 'INR',
  C_ARTERIAL_PH: 'Arterial_pH',
  C_PAO2: 'paO2',
  C_PACO2: 'paCO2',
  C_ARTERIAL_BE: 'Arterial_BE',
  C_ARTERIAL_LACTATE: 'Arterial_lactate',
  C_HCO3: 'HCO3',
  C_ETCO2: 'ETCO2',
  C_SVO2: 'SvO2',

  // Ventilation
  C_MECHVENT: 'mechvent',
  C_EXTUBATED: 'extubated',

  // Computed
  C_SHOCK_INDEX: 'Shock_Index',
  C_PAO2_FIO2: 'PaO2_FiO2',

  // Vasopressors, input/output
  C_MEDIAN_DOSE_VASO: 'median_dose_vaso',
  C_MAX_DOSE_VASO: 'max_dose_vaso',
  C_INPUT_TOTAL: 'input_total',
  C_INPUT_STEP: 'input_step',
  C_OUTPUT_TOTAL: 'output_total',
  C_OUTPUT_STEP: 'output_step',
  C_CUMULATED_BALANCE: 'cumulated_balance',

  // Onset data

  C_ONSET_TIME: 'onset_time',
  C_FIRST_TIMESTEP: 'first_timestep',
  C_LAST_TIMESTEP: 'last_timestep',

  // Derived dataframes

  C_BLOC: 'bloc',
  C_TIMESTEP: 'timestep',
  C_BIN_INDEX: 'bin_index',
  C_SOFA: 'SOFA',
  C_SIRS: 'SIRS',
  C_LAST_VASO: 'last_vaso',
  C_LAST_SOFA: 'last_SOFA',
  C_NUM_BLOCS: 'num_blocs',
  C_MAX_SOFA: 'max_SOFA',
  C_MAX_SIRS: 'max_SIRS',

  // For raw data

  C_HADM_ID: 'hadm_id',
  C_SUBJECT_ID: 'subject_id',
  C_STARTDATE: 'startdate',
  C_ENDDATE: 'enddate',
  C_STARTTIME: 'starttime',
  C_ENDTIME: 'endtime',
  C_CHARTTIME: 'charttime',
  C_CHARTDATE: 'chartdate',
  C_ITEMID: 'itemid',
  C_ADMITTIME: 'admittime',
  C_DISCHTIME: 'dischtime',
  C_ADM_ORDER: 'adm_order',
  C_UNIT: 'unit',
  C_INTIME: 'intime',
  C_OUTTIME: 'outtime',
  C_LOS: 'los',
  C_DOB: 'dob',
  C_DOD: 'dod',
  C_EXPIRE_FLAG: 'expire_flag',
  C_MORTA_HOSP: 'morta_hosp',
  C_VALUE: 'value',
  C_VALUENUM: 'valuenum',
  C_SELFEXTUBATED: 'selfextubated',
  C_INPUT_PREADM: 'input_preadm',
  C_AMOUNT: 'amount',
  C_RATE: 'rate',
  C_TEV: 'tev',
  C_RATESTD: 'ratestd',
  C_DATEDIFF_MINUTES: 'datediff_minutes',
  C_GSN: 'gsn',
  C_NDC: 'ndc',
  C_DOSE_VAL: 'dose_val',
  C_TEST_ITEMID: 'test_itemid',
  C_SPEC_ITEMID: 'spec_itemid',
  C_AB_ITEMID: 'ab_itemid',
  C_INTERPRETATION: 'interpretation',

  // Comorbidities
  C_CONGESTIVE_HEART_FAILURE: 'congestive_heart_failure',
  C_CARDIAC_ARRHYTHMIAS: 'cardiac_arrhythmias',
  C_VALVULAR_DISEASE: 'valvular_disease',
  C_PULMONARY_CIRCULATION: 'pulmonary_circulation',
  C_PERIPHERAL_VASCULAR: 'peripheral_vascular',
  C_HYPERTENSION: 'hypertension',
  C_PARALYSIS: 'paralysis',
  C_OTHER_NEUROLOGICAL: 'other_neurological',
  C_CHRONIC_PULMONARY: 'chronic_pulmonary',
  C_DIABETES_UNCOMPLICATED: 'diabetes_uncomplicated',
  C_DIABETES_COMPLICATED: 'diabetes_complicated',
  C_HYPOTHYROIDISM: 'hypothyroidism',
  C_RENAL_FAILURE: 'renal_failure',
  C_LIVER_DISEASE: 'liver_disease',
  C_PEPTIC_ULCER: 'peptic_ulcer',
  C_AIDS: 'aids',
  C_LYMPHOMA: 'lymphoma',
  C_METASTATIC_CANCER: 'metastatic_cancer',
  C_SOLID_TUMOR: 'solid_tumor',
  C_RHEUMATOID_ARTHRITIS: 'rheumatoid_arthritis',
  C_COAGULOPATHY: 'coagulopathy',
  C_OBESITY: 'obesity',
  C_WEIGHT_LOSS: 'weight_loss',
  C_FLUID_ELECTROLYTE: 'fluid_electrolyte',
  C_BLOOD_LOSS_ANEMIA: 'blood_loss_anemia',
  C_DEFICIENCY_ANEMIAS: 'deficiency_anemias',
  C_ALCOHOL_ABUSE: 'alcohol_abuse',
  C_DRUG_ABUSE: 'drug_abuse',
  C_PSYCHOSES: 'psychoses',
  C_DEPRESSION: 'depression',

  // Additional computed fields on raw data
  C_NORM_INFUSION_RATE: 'norm_infusion_rate',
};
export default Columns;