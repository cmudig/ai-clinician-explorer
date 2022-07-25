<script>
  import { createEventDispatcher } from 'svelte';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  const dispatch = createEventDispatcher();

  export let responses = {};

  function isValidResponse(r) {
    return true; // r.yearsExperience != null && r.technologyProficiency != null;
  }
</script>

<div class="center measure-wide pv4">
  <div class="f3 mb3">Pre-Study Survey</div>
  <p class="lh-copy w-100">
    For questions without an answer box, you can respond verbally.
  </p>
  <FreeResponseQuestion question="What is your current role?" />
  <MultipleChoice
    question="Approximately how many years of experience do you have working in the ICU?"
    choices={[
      { label: '<1 year', value: '0' },
      { label: '1-2 years', value: '1' },
      { label: '3-5 years', value: '2' },
      { label: '5-10 years', value: '3' },
      { label: '10+ years', value: '4' },
    ]}
    bind:selectedChoice={responses.yearsExperience}
  />
  <MultipleChoice
    question="Which of the following best describes your level of proficiency with technological devices and programs?"
    choices={[
      { label: 'I have trouble using or learning any technology', value: '0' },
      {
        label:
          'I am comfortable with a few technologies, but I have trouble learning to use most other technologies',
        value: '1',
      },
      {
        label:
          'I am comfortable with most technologies, but I have trouble learning to use new technologies',
        value: '2',
      },
      {
        label:
          'I am comfortable with most technologies, and I can easily learn to use new technologies',
        value: '3',
      },
    ]}
    bind:response={responses.technologyProficiency}
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
