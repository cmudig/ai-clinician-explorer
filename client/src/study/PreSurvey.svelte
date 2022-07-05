<script>
  import { createEventDispatcher } from 'svelte';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  const dispatch = createEventDispatcher();

  export let responses = {};

  function isValidResponse(r) {
    return r.yearsExperience != null && r.technologyProficiency != null;
  }
</script>

<div class="center measure-wide pv4">
  <div class="f3 mb3">Pre-Study Survey</div>
  <FreeResponseQuestion question="What is your current role?" />
  <MultipleChoice
    question="Approximately how many years of experience do you have working in the ICU?"
    choices={[
      { label: '<1 year', value: '0' },
      { label: '1-2 years', value: '1' },
      { label: '3-5 years', value: '2' },
      { label: '5+ years', value: '3' },
    ]}
    bind:selectedChoice={responses.yearsExperience}
  />
  <MultipleChoice
    question="Approximately how many years of experience do you have treating patients with sepsis?"
    choices={[
      { label: '<1 year', value: '0' },
      { label: '1-2 years', value: '1' },
      { label: '3-5 years', value: '2' },
      { label: '5+ years', value: '3' },
    ]}
    bind:selectedChoice={responses.yearsICUExperience}
  />
  <Likert
    question="How would you rate your proficiency with technology?"
    elements={['1 - novice', '2', '3', '4', '5', '6', '7 - Power user']}
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
