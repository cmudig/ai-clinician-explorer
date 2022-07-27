<script>
  import { createEventDispatcher, getContext } from 'svelte';
  import Columns from '../utils/columns';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  const dispatch = createEventDispatcher();

  let { patient, currentBloc } = getContext('patient');

  export let responses = {};
  export let stimulus = null;

  function isValidResponse(r) {
    if (
      !!stimulus &&
      stimulus.show_ai_clinician &&
      r.aiClinicianUsefulness == null
    )
      return false;
    return (
      r.fluidTreatment != null &&
      r.vasopressorTreatment != null &&
      r.confidence != null &&
      r.caseDifficulty != null
    );
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
  <div class="br2 bg-near-white pa4 mb4">
    <MultipleChoice
      background={false}
      question="Vasopressor treatment:"
      choices={[
        {
          label:
            lastVasoDose > 0 ? 'Increase vasopressors' : 'Begin vasopressors',
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
          label: lastFluidDose > 0 ? 'Increase fluids' : 'Begin fluids',
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
    <FreeResponseQuestion
      question="Did the AI Clinician’s recommendation affect your confidence in your treatment choices on this patient? If so, how?"
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
{/if}
