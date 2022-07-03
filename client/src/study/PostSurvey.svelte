<script>
  import { createEventDispatcher } from 'svelte';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';

  const dispatch = createEventDispatcher();

  export let responses = {};

  function isValidResponse(r) {
    return r.visualizationUsefulness != null && r.aiClinicianUsefulness != null;
  }
</script>

<div class="center measure-wide pv4">
  <div class="f3 mb3">Post-Study Survey</div>
  <Likert
    question="How useful would you rate the visualizations showing the patient state over time?"
    elements={[
      '1 - not at all useful',
      '2',
      '3',
      '4',
      '5',
      '6',
      '7 - extremely useful',
    ]}
    bind:response={responses.visualizationUsefulness}
  />
  <FreeResponseQuestion
    question="How could the visualizations be improved to better communicate the information you need?"
  />
  <Likert
    question="How useful overall would you rate the AI Clinician, and why?"
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
    question="When or for whom do you believe a tool like the AI Clinician could be useful?"
  />
  <FreeResponseQuestion
    question="What additional information would you like the AI Clinician to provide?"
  />
  <FreeResponseQuestion
    question="How much would you trust an AI in general to make the best decision?"
  />
  <FreeResponseQuestion
    question="How much would you trust another ICU doctor that you don’t know to make the best decision?"
  />
  <FreeResponseQuestion
    question="Do you have any other suggestions on how to improve the interface or the decision-making process?"
  />

  <button
    class="center br2 pa2 mt3 link dib white bg-dark-blue f6 b hover-bg-navy-dark pointer bg-animate"
    disabled={!isValidResponse(responses)}
    class:disabled={!isValidResponse(responses)}
    href="#"
    on:click={() => dispatch('continue')}
  >
    Continue</button
  >
</div>
