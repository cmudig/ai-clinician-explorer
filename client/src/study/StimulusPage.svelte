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
  import MultipleChoice from './MultipleChoice.svelte';
  import Columns from '../utils/columns';

  const dispatch = createEventDispatcher();

  let { patient, currentBloc } = getContext('patient');
  let { modelName } = getContext('strings');

  export let devMode = false;
  export let stimulus;
  export let responses;
  export let firstPatient = false;

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

  let lastFluidDose = 0;
  let lastVasoDose = 0;
  $: if (!!$patient && !!$currentBloc) {
    lastFluidDose =
      $patient.timesteps[$currentBloc - 1][Columns.C_INPUT_STEP].value;
    lastVasoDose =
      $patient.timesteps[$currentBloc - 1][Columns.C_MAX_DOSE_VASO].value;
  }

  function isValidResponse(r) {
    return r.fluidTreatment != null && r.vasopressorTreatment != null;
  }
</script>

{#if !!stimulus && !!$patient}
  <div class="flex align-stretch h-100">
    <div class="patient-data-view flex flex-column h-100">
      <!-- <div class="study-guide-header pa2 tc f4 bg-light-blue-gray">
        Assess Patient
      </div> -->
      <div class="patient-data-view-content flex flex-auto">
        <div class="sidebar bg-blue-gray">
          <Demographics
            {devMode}
            showOutcomes={false}
            patientName={stimulus.patient_name}
            showReadmission={false}
            showVentilation={true}
            showVasopressors={true}
            showLOS={true}
          />
        </div>
        <div class="data-column flex flex-column h-100">
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
              valueTooltips={true}
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
                valueTooltips={true}
              />
            {:else if treatmentTab == 2}
              <Antibiotics />
            {:else if treatmentTab == 3}
              <Cultures />
            {/if}
          </div>
        </div>
      </div>
    </div>

    <div class="flex-auto flex flex-column h-100">
      <!-- <div class="study-guide-header pa2 tc f4 bg-light-blue-gray">
        Make Decision
      </div> -->
      <div class="prediction-column flex-auto h-100">
        {#if !!stimulus.narrative}
          <div class="information br2 bg-near-white pa3 ma4 lh-copy mv4 f6 ">
            <strong>Narrative: </strong>{@html stimulus.narrative}
          </div>
        {/if}
        <Predictions {stimulus} />
        <div class="information ph4 lh-copy mv4">
          What do you do next for this patient?
        </div>
        {#if !!responses}
          <div class="ph4">
            <div class="br2 bg-near-white pa4 mb4">
              <MultipleChoice
                background={false}
                question="Vasopressor treatment:"
                choices={[
                  {
                    label:
                      lastVasoDose > 0
                        ? 'Increase vasopressors'
                        : 'Begin vasopressors',
                    value: '1',
                  },
                  ...(lastVasoDose > 0
                    ? [{ label: 'End or decrease vasopressors', value: '-1' }]
                    : []),
                  { label: 'No change', value: '0' },
                ]}
                bind:selectedChoice={responses.vasopressorTreatment}
              />
              <MultipleChoice
                background={false}
                question="IV fluid treatment:"
                choices={[
                  {
                    label:
                      lastFluidDose > 0 ? 'Increase fluids' : 'Begin fluids',
                    value: '1',
                  },
                  ...(lastFluidDose > 0
                    ? [{ label: 'End or decrease fluids', value: '-1' }]
                    : []),
                  { label: 'No change', value: '0' },
                ]}
                bind:selectedChoice={responses.fluidTreatment}
              />
            </div>
            <button
              class="center tc br2 pa2 mt3 mb4 link dib white bg-dark-blue f6 b {isValidResponse(
                responses,
              )
                ? 'hover-bg-navy-dark pointer bg-animate'
                : 'o-50'}"
              disabled={!isValidResponse(responses)}
              href="#"
              on:click={() => dispatch('continue')}
            >
              Continue</button
            >
          </div>
        {/if}
      </div>
    </div>
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
        {#if stimulus.show_ai_clinician}<p>
            <em>
              {#if !stimulus.show_state_explanation && !stimulus.show_alternative_actions}
                Your hospital has recently implemented a computerized decision
                support tool for sepsis called {@html $modelName}. {@html $modelName}
                analyzes patients’ electronic health records and uses an artificial
                intelligence-based algorithm to recommend fluids and vasopressor
                doses that optimize mortality based on historical data. On the next
                screen, the right panel shows the {@html $modelName} recommendation.
              {:else}
                On the next screen, the right panel shows the {@html $modelName}
                recommendation augmented with additional information.
              {/if}
            </em>
          </p>
        {/if}

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

  .patient-data-view {
    border-right: 1px solid #777777;
  }

  .study-guide-header {
    border-bottom: 1px solid #777777;
  }

  .data-column {
    width: 480px;
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
