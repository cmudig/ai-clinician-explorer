import Columns from './columns';

export const Comorbidities = {
  [Columns.C_CONGESTIVE_HEART_FAILURE]: 'Congestive heart failure',
  [Columns.C_CARDIAC_ARRHYTHMIAS]: 'Cardiac arrhythmias',
  [Columns.C_VALVULAR_DISEASE]: 'Valvular disease',
  [Columns.C_PULMONARY_CIRCULATION]: 'Pulmonary circulation disorder',
  [Columns.C_PERIPHERAL_VASCULAR]: 'Peripheral vascular disorder',
  [Columns.C_HYPERTENSION]: 'Hypertension',
  [Columns.C_PARALYSIS]: 'Paralysis',
  [Columns.C_OTHER_NEUROLOGICAL]: 'Other neurological disorder',
  [Columns.C_CHRONIC_PULMONARY]: 'Chronic pulmonary disorder',
  [Columns.C_DIABETES_UNCOMPLICATED]: 'Diabetes (uncomplicated)',
  [Columns.C_DIABETES_COMPLICATED]: 'Diabetes (complicated)',
  [Columns.C_HYPOTHYROIDISM]: 'Hypothyroidism',
  [Columns.C_RENAL_FAILURE]: 'Renal failure',
  [Columns.C_LIVER_DISEASE]: 'Liver disease',
  [Columns.C_PEPTIC_ULCER]: 'Peptic ulcer',
  [Columns.C_AIDS]: 'AIDS',
  [Columns.C_LYMPHOMA]: 'Lymphoma',
  [Columns.C_METASTATIC_CANCER]: 'Metastatic cancer',
  [Columns.C_SOLID_TUMOR]: 'Solid tumor',
  [Columns.C_RHEUMATOID_ARTHRITIS]: 'Rheumatoid arthritis',
  [Columns.C_COAGULOPATHY]: 'Coagulopathy',
  [Columns.C_OBESITY]: 'Obesity',
  [Columns.C_WEIGHT_LOSS]: 'Weight loss',
  [Columns.C_FLUID_ELECTROLYTE]: 'Fluid or electrolyte disorder',
  [Columns.C_BLOOD_LOSS_ANEMIA]: 'Blood loss anemia',
  [Columns.C_DEFICIENCY_ANEMIAS]: 'Deficiency anemia',
  [Columns.C_ALCOHOL_ABUSE]: 'Alcohol abuse',
  [Columns.C_DRUG_ABUSE]: 'Drug abuse',
  [Columns.C_PSYCHOSES]: 'Psychoses',
  [Columns.C_DEPRESSION]: 'Depression',
};

export const FeatureNames = {
  [Columns.C_GENDER]: 'Gender',
  [Columns.C_MECHVENT]: 'Ventilated',
  [Columns.C_RE_ADMISSION]: 'Re-Admission',
  [Columns.C_AGE]: 'Age',
  [Columns.C_WEIGHT]: 'Weight',
  [Columns.C_GCS]: 'GCS',
  [Columns.C_HR]: 'HR',
  [Columns.C_SYSBP]: 'Systolic BP',
  [Columns.C_MEANBP]: 'mAP',
  [Columns.C_DIABP]: 'Diastolic BP',
  [Columns.C_RR]: 'RR',
  [Columns.C_TEMP_C]: 'Temperature (C)',
  [Columns.C_FIO2_1]: 'FiO2',
  [Columns.C_POTASSIUM]: 'Potassium',
  [Columns.C_SODIUM]: 'Sodium',
  [Columns.C_CHLORIDE]: 'Chloride',
  [Columns.C_GLUCOSE]: 'Glucose',
  [Columns.C_MAGNESIUM]: 'Magnesium',
  [Columns.C_CALCIUM]: 'Calcium',
  [Columns.C_HB]: 'Hb',
  [Columns.C_WBC_COUNT]: 'WBC',
  [Columns.C_PLATELETS_COUNT]: 'Platelets',
  [Columns.C_PTT]: 'PTT',
  [Columns.C_PT]: 'PT',
  [Columns.C_ARTERIAL_PH]: 'Arterial pH',
  [Columns.C_PAO2]: 'PaO2',
  [Columns.C_PACO2]: 'PaCO2',
  [Columns.C_ARTERIAL_BE]: 'Arterial BE',
  [Columns.C_HCO3]: 'Bicarb',
  [Columns.C_ARTERIAL_LACTATE]: 'Arterial Lactate',
  [Columns.C_SOFA]: 'SOFA',
  [Columns.C_SIRS]: 'SIRS',
  [Columns.C_SHOCK_INDEX]: 'Shock Index',
  [Columns.C_PAO2_FIO2]: 'PaO2/FiO2',
  [Columns.C_CUMULATED_BALANCE]: 'Fluid Balance',
  [Columns.C_SPO2]: 'SpO2',
  [Columns.C_BUN]: 'BUN',
  [Columns.C_CREATININE]: 'Creatinine',
  [Columns.C_SGOT]: 'AST',
  [Columns.C_SGPT]: 'ALT',
  [Columns.C_TOTAL_BILI]: 'Total Bili',
  [Columns.C_INR]: 'INR',
  [Columns.C_INPUT_TOTAL]: 'Total Fluid Input',
  [Columns.C_INPUT_STEP]: 'Fluid Input Last 4h',
  [Columns.C_OUTPUT_TOTAL]: 'Total Fluid Output',
  [Columns.C_OUTPUT_STEP]: 'Fluid Output Last 4h',
};

export const StateCategory = {
  VITALS: 'Vitals',
  LABS: 'Labs',
  CARDIOPULM: 'Cardiopulmonary',
  FLUIDS_PRESSORS: 'Fluids/Pressors',
};
