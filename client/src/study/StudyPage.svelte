<script>
  import { onMount, setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import DataStateList from '../patient/DataStateList.svelte';
  import Demographics from '../patient/Demographics.svelte';
  import Treatments from '../patient/Treatments.svelte';
  import LoadingBar from '../utils/LoadingBar.svelte';
  import Columns from '../utils/columns';
  import SegmentedControl from '../utils/SegmentedControl.svelte';
  import Predictions from '../patient/Predictions.svelte';
  import Antibiotics from '../patient/Antibiotics.svelte';
  import Cultures from '../patient/Cultures.svelte';
  import { StateCategory } from '../utils/strings';
  import ActionButtonSet from './ActionButtonSet.svelte';

  export let csrf;

  const NON_TIMESTEP_COLUMNS = [
    'timesteps',
    'antibiotics',
    'microbio',
    'notes',
  ];
  let patient = writable(null);
  let modelInfo = writable(null);
  let modelPredictions = writable(null);
  // let currentBloc = writable(0);
  export let currentBloc = writable(0);

  setContext('patient', {
    patient,
    modelInfo,
    modelPredictions,
    currentBloc,
  });

  export let patientID = '';
  export let modelID = 'mimiciv_220328_best';

  let participantID = null;

  let loadingStudy = false;
  let loadingModelPrediction = false;
  let loadingPatientInfo = false;
  let submitting = false;

  let treatmentTab = 1;
  let statesTab = StateCategory.VITALS;

  let studyStimuli;
  let studyIndex = -1;

  let initializedStudyResponses = false;
  let studyComplete = false;

  async function initializeStudy() {
    loadingStudy = true;
    try {
      let response = await fetch('./api/study/init', {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrf,
        },
      });
      if (response.status != 200) {
        loadingStudy = false;
        console.log(
          `error ${response.status} initializing study:`,
          await response.text(),
        );
        return;
      }
      response = await response.json();
      participantID = response.participant_id;
      initializedStudyResponses = true;
      await loadStudyStimuli();
    } catch (e) {
      console.log('error initializing study:', e);
    }
  }

  $: if (initializedStudyResponses && !studyStimuli) {
    loadStudyStimuli();
  }

  async function loadStudyStimuli() {
    loadingStudy = true;
    try {
      let response = await fetch('./api/study/');
      if (response.status != 200) {
        loadingStudy = false;
        console.log(
          `error ${response.status} loading study:`,
          await response.text(),
        );
        studyStimuli = null;
        studyIndex = -1;
        return;
      }
      response = await response.json();
      console.log(response);
      studyStimuli = response.stimuli;
      studyIndex = 0;
      loadingStudy = false;
    } catch (e) {
      console.log('error loading study:', e);
      studyStimuli = null;
      studyIndex = -1;
    }
  }

  $: if (
    !!studyStimuli &&
    studyIndex >= 0 &&
    studyIndex < studyStimuli.length
  ) {
    patientID = studyStimuli[studyIndex].patient_id;
    $currentBloc = studyStimuli[studyIndex].timestep;
    console.log(patientID, $currentBloc);
  }
  $: if (!!patientID) loadPatientInfo(patientID);

  async function loadPatientInfo(patientID) {
    loadingPatientInfo = true;
    try {
      let response = await fetch('./api/patient/' + patientID);
      if (response.status != 200) {
        loadingPatientInfo = false;
        console.log(
          `error ${response.status} loading patient info:`,
          await response.text(),
        );
        return;
      }
      response = await response.json();
      $patient = response.result;
      if ($currentBloc == 0) $currentBloc = 1;
      console.log('patient:', $patient);
      loadingPatientInfo = false;
    } catch (e) {
      console.log('error loading patient info:', e);
    }
  }

  $: if (!!$patient && $modelPredictions == null && !!modelID) {
    loadModelPrediction($patient, $currentBloc);
  }

  $: if (!!modelID) {
    loadModelInfo(modelID);
  }

  async function loadModelInfo(id) {
    try {
      let response = await fetch(`./api/model/${modelID}`);
      if (response.status != 200) {
        console.log(
          `error ${response.status} loading model info:`,
          await response.text(),
        );
        return;
      }
      response = await response.json();
      $modelInfo = response.model;
      console.log('model info:', $modelInfo);
    } catch (e) {
      console.log('error loading model info:', e);
    }
  }

  async function loadModelPrediction(patientInfo, bloc) {
    let states = patientInfo.timesteps.map((ts) => {
      let state = {};
      Object.keys(ts).forEach((key) => {
        if (typeof ts[key] == 'number') state[key] = ts[key];
        else if (ts[key].hasOwnProperty('value')) state[key] = ts[key].value;
      });
      // TODO make the model API just take a patient object as-is
      Object.keys(patientInfo).forEach((key) => {
        if (!NON_TIMESTEP_COLUMNS.includes(key)) state[key] = patientInfo[key];
      });
      return state;
    });

    // TODO resolve this issue with AI Clinician methodology. Currently the
    // model predicts the best action to take in time interval t, but it also
    // takes as input the clinicians' fluid input and vasopressor dosages during
    // the same interval t. It should either take the clinician action from t - 1,
    // or predict the action in t + 1.
    let actions = patientInfo.timesteps.map((ts) => {
      let ac = {};
      [Columns.C_INPUT_STEP, Columns.C_MAX_DOSE_VASO].forEach((key) => {
        if (typeof ts[key] == 'number') ac[key] = ts[key];
        else if (ts[key].hasOwnProperty('value')) ac[key] = ts[key].value;
      });
      return ac;
    });

    let body = { states, actions };
    console.log('body:', body);
    try {
      loadingModelPrediction = true;
      let response = await fetch(`./api/model/${modelID}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      if (response.status != 200) {
        console.log(
          `error ${response.status} loading model prediction:`,
          await response.text(),
        );
        loadingModelPrediction = false;
        return;
      }
      response = await response.json();
      console.log('response', response);
      $modelPredictions = response.results;
      loadingModelPrediction = false;
    } catch (e) {
      console.log('error loading model prediction:', e);
      loadingModelPrediction = false;
    }
  }

  let currentTime;
  let dayIndex;
  $: if (!!$patient && $currentBloc > 0) {
    dayIndex = Math.floor((($currentBloc - 1) * 4) / 24) + 1;
    let timestamp = $patient.timesteps[$currentBloc - 1].timestep;
    currentTime = new Date(timestamp * 1000).toLocaleTimeString('en-US', {
      hour: 'numeric',
      hour12: true,
    });
  }

  let selectedAction = null;
  $: console.log('selected', selectedAction);

  let submitEnabled = false;
  $: submitEnabled =
    !!studyStimuli && studyIndex >= 0 && selectedAction != null;

  async function submitResponse() {
    submitting = true;
    try {
      let response = await fetch('./api/study/update', {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          participant_id: participantID,
          stimulus_id: studyStimuli[studyIndex].stimulus_id,
          chosen_action: selectedAction,
          confidence: 5,
        }),
      });
      if (response.status != 200) {
        submitting = false;
        console.log(
          `error ${response.status} submitting response:`,
          await response.text(),
        );
        return;
      }
      submitting = false;
      response = await response.json();
      if (studyIndex + 1 == studyStimuli.length) {
        studyComplete = true;
      } else {
        studyIndex += 1;
        selectedAction = null;
      }
    } catch (e) {
      submitting = false;
      console.log('error submitting response:', e);
    }
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked flex justify-between">
    {#if !initializedStudyResponses || studyComplete}
      <span class="white dib mr3">Sepsis Treatment Study</span>
    {:else if !!studyStimuli && studyIndex >= 0}
      <span class="white dib mr3"
        >Patient {studyIndex + 1} of {studyStimuli.length}</span
      >
    {/if}
    {#if !!participantID}
      <span class="white dib mr3">Participant ID: {participantID}</span>
    {/if}
  </nav>
</header>
<main class="pa0 h-100">
  {#if !initializedStudyResponses}
    <div class="flex flex-column h-100 items-center justify-center">
      <div class="information f5 lh-copy measure-wide mb3">
        In this study, you will be presented with four vignettes of patients
        with sepsis. In each case, you will be asked to choose an appropriate
        level of IV fluids and vasopressors based on the available patient data.
      </div>
      <a
        class="center br2 pa2 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b bg-animate"
        href="#"
        on:click={initializeStudy}
      >
        Continue</a
      >
    </div>
  {:else if studyComplete}
    <div class="flex flex-column h-100 items-center justify-center">
      <div class="information f5 lh-copy measure-wide mb3">
        You have completed the study and may now close this window.
      </div>
    </div>
  {:else if loadingModelPrediction || loadingPatientInfo || loadingStudy || submitting}
    <div class="flex flex-column h-100 items-center justify-center">
      <p class="mb3 f5 tc b dark-gray">
        {#if submitting}
          Submitting response...
        {:else if loadingStudy}
          Initializing study...
        {:else if loadingModelPrediction}
          Loading AI Clinician...
        {:else}
          Loading patient info...
        {/if}
      </p>
      <LoadingBar />
    </div>
  {:else}
    <div class="flex align-stretch h-100">
      <div class="sidebar bg-blue-gray">
        {#if !!$patient}
          <div
            class="timestep-selector bg-navy-gray flex justify-between items-center w-100 pv3 ph3 white"
          >
            <span class="f6 b pb0 mr3"
              >Day {dayIndex}, {currentTime} ({$currentBloc * 4} hours in ICU)</span
            >
          </div>
        {/if}
        <Demographics showOutcomes={false} />
      </div>
      {#if !!$patient}
        <div class="patient-info-container flex-auto flex h-100">
          <div class="data-column flex flex-column flex-auto h-100">
            <div
              class="context-info-controls pa2 flex items-center bg-near-white"
            >
              <SegmentedControl
                bind:selected={statesTab}
                options={[
                  { name: StateCategory.VITALS, value: StateCategory.VITALS },
                  { name: StateCategory.LABS, value: StateCategory.LABS },
                  {
                    name: StateCategory.CARDIOPULM,
                    value: StateCategory.CARDIOPULM,
                  },
                ]}
              />
            </div>
            <div class="data-state flex-auto">
              <DataStateList
                category={statesTab}
                highlightImputedValues={false}
              />
            </div>
            <div
              class="context-info-controls pa2 flex items-center bg-near-white"
            >
              <SegmentedControl
                bind:selected={treatmentTab}
                options={[
                  { name: 'Fluids/Pressors', value: 1 },
                  { name: 'Antibiotics', value: 2 },
                  { name: 'Cultures', value: 3 },
                  { name: 'Notes', value: 4 },
                ]}
              />
            </div>
            <div class="data-treatments">
              {#if treatmentTab == 1}
                <DataStateList
                  category={StateCategory.FLUIDS_PRESSORS}
                  highlightImputedValues={false}
                />
              {:else if treatmentTab == 2}
                <Antibiotics />
              {:else if treatmentTab == 3}
                <Cultures />
              {/if}
            </div>
          </div>
          <div class="prediction-column flex-auto h-100">
            <div class="information ph4 lh-copy mv4">
              Using the information to the left, please make an assessment of
              this patient and choose a dosage level of IV fluids and
              vasopressors to administer in the next 4 hours.
            </div>
            <ActionButtonSet bind:selectedAction />
            <div class="flex items-center justify-center">
              <button
                class="center br2 pa2 link dib white {submitEnabled
                  ? 'bg-dark-blue hover-bg-navy-dark pointer bg-animate'
                  : 'bg-light-gray'} f6 b"
                href="#"
                disabled={!submitEnabled}
                on:click={submitResponse}
              >
                Submit</button
              >
            </div>
          </div>
        </div>
      {/if}
    </div>
  {/if}
</main>

<style>
  .sidebar {
    width: 320px;
    border-right: 1px solid #777777;
    overflow-y: scroll;
    flex: 0 0 auto;
  }

  .bg-blue-gray {
    background-color: #404a5a;
  }

  .bg-navy-gray {
    background-color: #2e3847;
  }

  main {
    padding-top: 48px;
  }

  .bg-navy-90 {
    background-color: #001b44e7;
  }

  .data-column {
    flex-basis: 60%;
    border-right: 1px solid #777777;
  }

  .data-state {
    overflow-y: scroll;
    border-bottom: 1px solid #777777;
    flex: 1;
    min-height: 0;
  }

  .context-info-controls {
    height: 48px;
    border-bottom: 1px solid #777777;
    flex: 0 0 auto;
  }

  .data-treatments {
    flex: 1;
    min-height: 0;
    overflow-y: scroll;
  }
  .prediction-column {
    flex-basis: 100%;
    overflow-y: scroll;
  }

  .timestep-selector {
    border-bottom: 1px solid #666666;
  }

  .arrow {
    border: solid white;
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 3px;
  }

  .arrow.left {
    transform: rotate(135deg);
    -webkit-transform: rotate(135deg);
  }
</style>
