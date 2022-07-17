<script>
  import { createEventDispatcher } from 'svelte';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  const dispatch = createEventDispatcher();

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
</script>

{#if !!stimulus}
  <MultipleChoice
    question="What IV fluid treatment do you prescribe for this patient?"
    choices={[
      { label: 'Begin or increase fluids', value: '1' },
      { label: 'End or decrease fluids', value: '-1' },
      { label: 'No change', value: '0' },
    ]}
    bind:selectedChoice={responses.fluidTreatment}
  />
  <MultipleChoice
    question="What vasopressor treatment do you prescribe for this patient?"
    choices={[
      { label: 'Begin or increase vasopressors', value: '1' },
      { label: 'End or decrease vasopressors', value: '-1' },
      { label: 'No change', value: '0' },
    ]}
    bind:selectedChoice={responses.vasopressorTreatment}
  />
  <Likert
    question="How confident are you in your decision?"
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
    question="How difficult would you rate this case?"
    elements={[
      '1 - extremely easy',
      '2',
      '3',
      '4',
      '5',
      '6',
      '7 - extremely difficult',
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
      question="How did the AI Clinician’s recommendation affect your confidence in your decision on this patient?"
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
