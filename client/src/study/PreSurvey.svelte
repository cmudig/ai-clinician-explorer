<script>
  import { shuffle } from 'd3';

  import { createEventDispatcher } from 'svelte';
  import FreeResponseQuestion from './FreeResponseQuestion.svelte';
  import Likert from './Likert.svelte';
  import MultipleChoice from './MultipleChoice.svelte';

  const dispatch = createEventDispatcher();

  export let responses = {};

  const techSavvyQuestions = shuffle([
    {
      question:
        'The use of clinical protocols and decision support tools make me a better clinician.',
      resultID: 'protocolBetterClinician',
    },
    {
      question:
        'Clinical protocols and decision support tools in health care generally lead to improved patient outcomes.',
      resultID: 'protocolBetterOutcomes',
    },
    {
      question:
        'When they are available, I try to adopt clinical protocols and decision support tools in my daily practice. ',
      resultID: 'protocolAdoption',
    },
    {
      question:
        'Artificial intelligence is likely to improve health care for the better.',
      resultID: 'aiImproveHealthCare',
    },
    {
      question:
        'I’m ready to use artificial intelligence-based tools in my daily practice.',
      resultID: 'aiAdoption',
    },
    {
      question:
        'Decision support tools built on artificial intelligence will help health care providers make better clinical decisions.',
      resultID: 'aiBetterDecisions',
    },
    {
      question:
        'I like to buy new tech products as soon as they become available.',
      resultID: 'techBuyProducts',
    },
    {
      question:
        'It’s easy for me to master new technology, even when it’s complex.',
      resultID: 'techEasy',
    },
    {
      question: 'I’m often one of the first to try the latest smartphone app.',
      resultID: 'techAdoption',
    },
  ]);

  function isValidResponse(r) {
    return (
      r.jobTitle != null &&
      r.gender != null &&
      r.race != null &&
      r.hispanic != null &&
      r.yearsExperience != null &&
      techSavvyQuestions.every((q) => r[q.resultID] != null)
    );
  }
</script>

<div class="center measure-wide pv4">
  <div class="f3 mb3">Pre-Study Survey</div>
  <p class="measure-wide lh-copy">
    Throughout the study, please feel free to expand on any answer verbally.
  </p>
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
  <div class="br2 bg-near-white pa4 mb4">
    <p class="f5 b lh-copy mb3">
      Please rate your agreement with the following statements.
    </p>
    {#each techSavvyQuestions as item}
      <Likert
        background={false}
        boldQuestion={false}
        question={item.question}
        elements={[
          '1 - strongly disagree',
          '2 - disagree',
          '3 - neither agree nor disagree',
          '4 - agree',
          '5 - strongly agree',
        ]}
        bind:response={responses[item.resultID]}
      />
    {/each}
  </div>

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
