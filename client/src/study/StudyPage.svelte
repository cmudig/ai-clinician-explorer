<script>
  import { onMount, setContext } from 'svelte';
  import { writable } from 'svelte/store';
  import LoadingBar from '../utils/LoadingBar.svelte';
  import Columns from '../utils/columns';
  import Welcome from './Welcome.svelte';
  import PreSurvey from './PreSurvey.svelte';
  import PostSurvey from './PostSurvey.svelte';
  import StimulusPage from './StimulusPage.svelte';

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

  let loadingMessage = null;

  let studyStimuli;
  let studyIndex = -1;

  let resumeErrorMessage = null;

  let preSurveyResponses;
  let postSurveyResponses;
  let stimulusResponse;
  let allStimulusResponses = [];

  const StudyStates = {
    WELCOME: 0,
    PRE_SURVEY: 1,
    STIMULI: 2,
    POST_SURVEY: 3,
    COMPLETE: 4,
  };

  let state = StudyStates.WELCOME;

  function advanceState() {
    if (state != StudyStates.STIMULI) {
      syncState();
      state += 1;
    } else if (studyIndex == studyStimuli.length) {
      console.log('advancing state to', state + 1);
      state += 1;
    }
  }

  async function initializeStudy() {
    console.log('initializing');
    loadingMessage = 'Initializing study...';
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
        loadingMessage = null;
        console.log(
          `error ${response.status} initializing study:`,
          await response.text(),
        );
        participantID = null;
        studyStimuli = null;
        studyIndex = -1;
        return;
      }
      loadingMessage = null;
      response = await response.json();
      participantID = response.participant_id;
      studyStimuli = response.stimuli;
      studyIndex = 0;
      advanceState();
    } catch (e) {
      console.log('error initializing study:', e);
    }
  }

  async function resumeFromPrevious(e) {
    loadingMessage = 'Initializing study...';
    let pid = e.detail;

    try {
      let response = await fetch('./api/study/init', {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ participant_id: pid }),
      });
      if (response.status != 200) {
        loadingMessage = null;
        resumeErrorMessage = response.text();
        participantID = '';
        return;
      }
      response = await response.json();
      console.log(response);
      participantID = response.participant_id;
      studyStimuli = response.stimuli;
      studyIndex = 0;

      state = StudyStates[response.state] || StudyStates.WELCOME;
      studyIndex = response.study_index != null ? response.study_index : 0;
      console.log(state, studyIndex);
      advanceState();
      console.log(state, studyIndex);
      loadingMessage = null;
    } catch (e) {
      console.log('error initializing study:', e);
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
    loadingMessage = 'Loading patient info...';
    $patient = null;
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
      loadingMessage = null;
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
      loadingMessage = 'Loading AI Clinician...';
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
      loadingMessage = null;
    } catch (e) {
      console.log('error loading model prediction:', e);
      loadingMessage = null;
    }
  }

  let currentTime;
  let dayIndex;
  $: if (!!$patient && $currentBloc > 0) {
    console.log($patient, $currentBloc);
    dayIndex = Math.floor((($currentBloc - 1) * 4) / 24) + 1;
    let timestamp = $patient.timesteps[$currentBloc - 1].timestep;
    currentTime = new Date(timestamp * 1000).toLocaleTimeString('en-US', {
      hour: 'numeric',
      hour12: true,
    });
  }

  async function syncState() {
    try {
      let studyData = {
        participant_id: participantID,
        state: Object.keys(StudyStates).find((v) => StudyStates[v] == state),
        study_index: studyIndex,
        stimulus_responses: allStimulusResponses,
      };
      if (!!preSurveyResponses)
        studyData.pre_survey_responses = preSurveyResponses;
      if (!!postSurveyResponses)
        studyData.post_survey_responses = postSurveyResponses;
      let response = await fetch('./api/study/update', {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrf,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studyData),
      });
      if (response.status != 200) {
        console.log(
          `error ${response.status} syncing state:`,
          await response.text(),
        );
        return false;
      }
      return true;
    } catch (e) {
      console.log('error syncing state:', e);
    }
  }

  async function submitStimulusResponse() {
    loadingMessage = 'Submitting response...';
    console.log(stimulusResponse);
    stimulusResponse.stimulus_id = studyStimuli[studyIndex].stimulus_id;
    allStimulusResponses.push(stimulusResponse);
    stimulusResponse = {};
    $modelPredictions = null;
    studyIndex += 1;
    try {
      await syncState();
      loadingMessage = null;
      advanceState();
    } catch (e) {
      loadingMessage = null;
      console.log('error submitting response:', e);
    }
    /*try {
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
          state: Object.keys(StudyStates).find((v) => StudyStates[v] == state),
          study_index: studyIndex,
          response: {
            stimulus_id: studyStimuli[studyIndex].stimulus_id,
            chosen_action: selectedAction,
            confidence: 5,
          },
        }),
      });
      if (response.status != 200) {
        loadingMessage = null;
        console.log(
          `error ${response.status} submitting response:`,
          await response.text(),
        );
        return;
      }
      loadingMessage = null;
      response = await response.json();
      advanceState();
    } catch (e) {
      loadingMessage = null;
      console.log('error submitting response:', e);
    }*/
  }
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked flex justify-between">
    {#if state == StudyStates.STIMULI}
      <span class="white dib mr3"
        >Patient {studyIndex + 1} of {studyStimuli.length}</span
      >
    {:else}
      <span class="white dib mr3">Sepsis Treatment Study</span>
    {/if}
    {#if state > StudyStates.WELCOME && !!participantID && participantID.length > 0}
      <span class="white dib mr3">Participant ID: {participantID}</span>
    {/if}
  </nav>
</header>
<main class="pa0 h-100">
  {#if !!loadingMessage}
    <div class="flex flex-column h-100 items-center justify-center">
      <p class="mb3 f5 tc b dark-gray">
        {loadingMessage}
      </p>
      <LoadingBar />
    </div>
  {:else if state == StudyStates.WELCOME}
    <Welcome
      on:initialize={() => initializeStudy()}
      on:resume={(e) => resumeFromPrevious(e)}
      {resumeErrorMessage}
    />
  {:else if state == StudyStates.PRE_SURVEY}
    <PreSurvey on:continue={advanceState} bind:responses={preSurveyResponses} />
  {:else if state == StudyStates.POST_SURVEY}
    <PostSurvey
      on:continue={advanceState}
      bind:responses={postSurveyResponses}
    />
  {:else if state == StudyStates.COMPLETE}
    <div class="flex flex-column h-100 items-center justify-center">
      <div class="information f5 lh-copy measure-wide mb3">
        You have completed the study and may now close this window.
      </div>
    </div>
  {:else if state == StudyStates.STIMULI}
    <StimulusPage
      patientName={studyStimuli[studyIndex].patient_name}
      bind:stimulusResponse
    />
  {/if}
</main>

<style>
  main {
    padding-top: 48px;
  }

  .bg-navy-90 {
    background-color: #001b44e7;
  }
</style>
