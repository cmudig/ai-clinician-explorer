<script>
  import { createEventDispatcher, getContext } from 'svelte';
  import DataStateList from '../patient/DataStateList.svelte';
  import Demographics from '../patient/Demographics.svelte';
  import Treatments from '../patient/Treatments.svelte';
  import SegmentedControl from '../utils/SegmentedControl.svelte';
  import Predictions from '../study/Predictions.svelte';
  import Antibiotics from '../patient/Antibiotics.svelte';
  import Cultures from '../patient/Cultures.svelte';
  import { StateCategory } from '../utils/strings';
  import ActionButtonSet from './ActionButtonSet.svelte';
  import StimulusQuestions from './StimulusQuestions.svelte';

  const dispatch = createEventDispatcher();

  let { patient, currentBloc } = getContext('patient');

  export let devMode = false;
  export let stimulus;
  export let stimulusResponse;
  export let firstPatient = false;
  export let lastPatient = false;

  let treatmentTab = 1;
  let statesTab = StateCategory.VITALS;

  let showingNarrative = false;
  let oldPatientID = null;
  $: if (
    !devMode &&
    !!$patient &&
    $patient.icustayid != oldPatientID &&
    !!stimulus &&
    !!stimulus.narrative
  ) {
    showingNarrative = true;
    oldPatientID = $patient.icustayid;
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
</script>

{#if !!stimulus}
  <div class="flex align-stretch h-100">
    <div class="sidebar bg-blue-gray">
      {#if !!$patient}
        <div
          class="timestep-selector bg-navy-gray flex justify-between items-center w-100 pv3 ph3 white"
        >
          <span class="f6 b pb0 mr3"
            >{currentTime}, day {dayIndex} of ICU stay</span
          >
        </div>
      {/if}
      <Demographics
        {devMode}
        showOutcomes={false}
        patientName={stimulus.patient_name}
        showReadmission={false}
        showVentilation={true}
        showVasopressors={true}
      />
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
          {#if !!stimulus.narrative}
            <div class="information ph4 lh-copy mv4 f6">
              {@html stimulus.narrative}
            </div>
          {/if}
          <Predictions {stimulus} />
          <div class="information ph4 lh-copy mv4">
            What do you do next for this patient?
          </div>
          <div class="ph4">
            <StimulusQuestions
              {stimulus}
              submitText={lastPatient ? 'Submit' : 'See Next Patient'}
              bind:responses={stimulusResponse}
              on:continue={() => dispatch('submit', stimulusResponse)}
            />
          </div>
        </div>
      </div>
    {/if}
  </div>
  {#if showingNarrative}
    <div
      class="overlay w-100 h-100 fixed top-0 left-0 flex flex-column items-center justify-center"
    >
      <div class="bg-white pa4 lh-copy measure br3">
        {#if firstPatient}
          <p class="mt0">
            <em
              >At the beginning of your ICU shift, you are called to the bedside
              of a patient being treated for sepsis:</em
            >
          </p>
        {/if}
        {@html stimulus.narrative}
        <div class="w-100 flex justify-center">
          <button
            class="tc br2 pa2 mv3 link dib white bg-dark-blue f6 b hover-bg-navy-dark pointer bg-animate"
            href="#"
            on:click={() => (showingNarrative = false)}
          >
            See Patient Details</button
          >
        </div>
      </div>
    </div>
  {/if}
{/if}

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

  .overlay {
    background-color: #eeeeeeee;
  }
</style>
