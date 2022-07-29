<script>
  import { createEventDispatcher, getContext } from 'svelte';
  import Columns from '../utils/columns';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  let { patient, currentBloc } = getContext('patient');

  const dispatch = createEventDispatcher();

  export let responses = {};
  export let stimulus = null;

  function isValidResponse(r) {
    if (
      !!stimulus &&
      stimulus.show_ai_clinician &&
      (r.aiClinicianUsefulness == null || r.aiClinicianConfidenceEffect == null)
    )
      return false;
    return r.confidence != null && r.caseDifficulty != null;
  }

  let lastFluidDose = 0;
  let lastVasoDose = 0;
  $: if (!!$patient && !!$currentBloc) {
    lastFluidDose =
      $patient.timesteps[$currentBloc - 1][Columns.C_INPUT_STEP].value;
    lastVasoDose =
      $patient.timesteps[$currentBloc - 1][Columns.C_MAX_DOSE_VASO].value;
  }
</script>

{#if !!stimulus}
  <div class="center measure-wide pv4">
    <div class="f3 mb3">
      Questions for {stimulus.patient_name || stimulus.patient_id}
    </div>
    {#if !!stimulus.narrative}
      <div class="information br2 bg-near-white pa3 lh-copy mv4 f6 ">
        <p><strong>Narrative: </strong>{@html stimulus.narrative}</p>
        <p>
          <strong>Chosen treatment:</strong>
          {#if responses.vasopressorTreatment == '1'}{lastVasoDose > 0
              ? 'increase'
              : 'begin'} vasopressors{:else if responses.vasopressorTreatment == '-1'}end
            or decrease vasopressors{:else}no change in vasopressors{/if}, {#if responses.fluidTreatment == '1'}{lastFluidDose >
            0
              ? 'increase'
              : 'begin'}
            fluids{:else if responses.fluidTreatment == '-1'}end/decrease fluids{:else}no
            change in fluids{/if}
        </p>
      </div>
    {/if}
    <Likert
      question="How confident are you in your treatment choices?"
      elements={[
        '1 - not at all confident',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7 - extremely confident',
      ]}
      bind:response={responses.confidence}
    />
    <Likert
      question="How challenging would you rate this case?"
      elements={[
        '1 - extremely easy',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7 - extremely challenging',
      ]}
      bind:response={responses.caseDifficulty}
    />
    {#if stimulus.show_ai_clinician}
      <Likert
        question="How useful would you rate the AI Clinician's recommendations for this patient?"
        elements={[
          '1 - not at all useful',
          '2',
          '3',
          '4',
          '5',
          '6',
          '7 - extremely useful',
        ]}
        bind:response={responses.aiClinicianUsefulness}
      />
      <MultipleChoice
        question="Did the AI Clinician’s recommendation affect your confidence in your treatment choices on this patient? If so, how?"
        choices={[
          { label: 'Yes', value: 1 },
          { label: 'No', value: 0 },
        ]}
        bind:selectedChoice={responses.aiClinicianConfidenceEffect}
      />
    {/if}
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
      Submit</button
    >
  </div>
{/if}
