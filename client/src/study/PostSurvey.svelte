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
    question="Overall, how useful to you would you rate the AI Clinician, and why?"
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
    question="The remainder of the survey will be conducted verbally with the researcher."
  />

  <button
    class="center tc br2 pa2 mt3 link dib white bg-dark-blue f6 b {isValidResponse(
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
