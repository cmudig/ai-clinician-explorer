<script>
  import { createEventDispatcher } from 'svelte';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  const dispatch = createEventDispatcher();

  export let responses = {};

  function isValidResponse(r) {
    return (
      r.jobTitle != null &&
      r.gender != null &&
      r.race != null &&
      r.hispanic != null &&
      r.yearsExperience != null &&
      r.technologyAdoption != null &&
      r.ehrSkill != null
    );
  }
</script>

<div class="center measure-wide pv4">
  <div class="f3 mb3">Pre-Study Survey</div>
  <MultipleChoice
    question="Which job title best describes you?"
    choices={[
      { label: 'Attending physician', value: 'attending' },
      { label: 'Fellow', value: 'fellow' },
      { label: 'Advanced practice provider (i.e. NP or PA)', value: 'app' },
      { label: 'Other', value: 'other' },
    ]}
    bind:selectedChoice={responses.jobTitle}
  />
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
  <Likert
    question="How would you rate your level of skill in using the electronic health record (EHR) system in your hospital?"
    elements={['1 - beginner', '2', '3 - intermediate', '4', '5 - expert']}
    bind:response={responses.ehrSkill}
  />
  <MultipleChoice
    question="When a new technology (hardware, software, or web application) becomes available, how quickly do you tend to adopt it?"
    choices={[
      { label: 'I never adopt it', value: '0' },
      { label: 'After most of my colleagues', value: '1' },
      { label: 'When it becomes mainstream', value: '2' },
      { label: 'Before most of my colleagues', value: '3' },
      { label: 'I’m one of the first to try it', value: '4' },
    ]}
    bind:selectedChoice={responses.technologyAdoption}
  />
  <MultipleChoice
    question="What is your gender?"
    choices={[
      { label: 'Female', value: 'female' },
      { label: 'Male', value: 'male' },
      { label: 'Other', value: 'other' },
      { label: 'Prefer not to answer', value: 'n/a' },
    ]}
    bind:selectedChoice={responses.gender}
  />

  <MultipleChoice
    question="Because this study is funded by the NIH we need some information about your race. Which of the following categories best applies to you?"
    choices={[
      { label: 'White', value: 'white' },
      { label: 'Black', value: 'black' },
      { label: 'Asian', value: 'asian' },
      { label: 'American Indian/Alaska Native', value: 'ai/an' },
      { label: 'Native Hawaiian/Pacific Islander', value: 'nhpi' },
      { label: 'Multiracial', value: 'multi' },
      { label: 'Prefer not to answer', value: 'n/a' },
    ]}
    bind:selectedChoice={responses.race}
  />
  <MultipleChoice
    question="Do you identify as Hispanic or Latino?"
    choices={[
      { label: 'Yes', value: '1' },
      { label: 'No', value: '0' },
      { label: 'Prefer not to answer', value: 'n/a' },
    ]}
    bind:selectedChoice={responses.hispanic}
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
