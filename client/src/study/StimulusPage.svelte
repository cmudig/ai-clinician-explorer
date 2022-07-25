<script>
  import { getContext } from 'svelte';
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

  let { patient, currentBloc } = getContext('patient');

  export let stimulus;
  export let stimulusResponse;

  let treatmentTab = 1;
  let statesTab = StateCategory.VITALS;
</script>

{#if !!stimulus}
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
      <Demographics showOutcomes={false} patientName={stimulus.patient_name} />
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
            <div class="information ph4 lh-copy mv4">
              {@html stimulus.narrative}
            </div>
          {/if}
          <Predictions {stimulus} />
          <div class="information ph4 lh-copy mv4">
            Using the provided information, please make an assessment of this
            patient and choose a dosage level of IV fluids and vasopressors to
            administer in the next 4 hours.
          </div>
          <div class="ph4">
            <StimulusQuestions
              {stimulus}
              bind:responses={stimulusResponse}
              on:continue={submitStimulusResponse}
            />
          </div>
        </div>
      </div>
    {/if}
  </div>
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
</style>
