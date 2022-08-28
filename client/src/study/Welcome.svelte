<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let resumeErrorMessage;
  let participantID;
  let resumingPrevious = false;
</script>

<div class="mt4">
  <div class="information f5 lh-copy measure-wide mb3 center">
    {#if resumingPrevious}
      <div class="bg-light-blue-gray br2 pa3 w-100 center pb4">
        <form>
          <fieldset id="login" class="ba b--transparent ph0 mh0">
            <p class="mb3 mt0 f5">
              Type the Participant ID displayed during the previous session to
              pick up where you left off.
            </p>
            {#if !!resumeErrorMessage}
              <div class="pa2 mv2 br2 bg-washed-red f5">
                {resumeErrorMessage}
              </div>
            {/if}
            <div>
              <label class="db fw6 lh-copy f6" for="participant_id"
                >Participant ID</label
              >
              <input
                class="pa2 ba bg-white w-100"
                type="username"
                name="participant_id"
                id="participant_id"
                bind:value={participantID}
              />
            </div>
          </fieldset>
          <div class="">
            <input
              class="pa2 br2 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b bg-animate"
              type="submit"
              value="Continue"
              disabled={!participantID || participantID.length == 0}
              on:click|preventDefault={() => dispatch('resume', participantID)}
            />
          </div>
        </form>
        <a
          class="center mt2 pa2 link dib dim bg-animate f6"
          href="#"
          on:click={() => (resumingPrevious = false)}
        >
          Hide</a
        >
      </div>
    {:else}
      <a
        class="center mt2 link dib dim bg-animate f6"
        href="#"
        on:click={() => (resumingPrevious = true)}
      >
        Click here to resume a previous session.</a
      >
    {/if}
    <h4>Our Research</h4>
    <p>
      We are trying to understand the acceptability of decision support tools
      (DST) for the ICU. Through this study, we hope to learn how to best
      present AI information to physicians. This study is led by Dr. Jeremy Kahn
      at the University of Pittsburgh Medical Center and is funded by the
      National Institutes of Health.
    </p>

    <h4>Your Role</h4>
    <p>
      You will imagine you are working an ICU shift and making decisions about
      the patients currently in the ICU. We’ll present you with a description of
      each patient as well as a summary of their recent chart and lab data, to
      help you get a sense of their current condition. You will also be able to
      see any IV fluids, vasopressors, and antibiotics that the patient has been
      given while in the ICU. Your task will be to prescribe a treatment plan,
      in terms of IV fluids and norepinephrine-equivalent vasopressors, for this
      patient for the next 4 hours. We’ll repeat this process for four different
      patients. After this, I’ll ask you a few questions about the process to
      determine additional ways that we might assist with your decision making.
      This process will take a approximately 30 minutes.
    </p>

    <h4>Compensation</h4>
    <p>
      You will earn $50 for participating. All compensation is taxable income to
      the participant regardless of the amount. If a participant receives $600
      or more in a calendar year from one organization, that organization is
      required by law to file a Form 1099—Miscellaneous with the IRS and provide
      a copy to the taxpayer. Individuals who do not provide a social security
      number may still participate in the research, but the IRS requires that
      24% of the payment be sent by the institution to the IRS for "backup
      withholding"; thus, you would only receive 76% of the expected payment.
    </p>

    <h4>Risks & Benefits</h4>
    <p>
      The only risk associated with participation in this study is breach of
      confidentiality. We will de-identify all data to limit this risk. There is
      no direct benefit to you for your study participation.
    </p>

    <h4>Data & Privacy</h4>
    <p>
      With your permission, we would like to audio/video record this session so
      that we can more accurately capture your feedback. Other than that, we
      will not be collecting any personal identifiers about you. You can always
      back out at any time. All data will be housed on a secure server located
      at the University of Pittsburgh. Identifiable responses will only be
      available to the research team. If data are shared with other researchers,
      they will be stripped of identifiers in accordance with IRB protocol.
    </p>

    <h4>Rights & Questions</h4>
    <p>
      Your participation is voluntary. Refusal to participate will involve no
      penalty or loss of benefits to which you are otherwise entitled, and you
      may discontinue participation at any time without penalty or loss of
      benefits to which you are otherwise entitled. Should you decide to
      withdraw, any data collected to that point will continue to be used for
      research purposes. You can contact Jeremy Kahn, the study PI, at
      jeremykahn@pitt.edu or by calling 412-383-0839 at any time should you have
      any questions or concerns.
    </p>

    <hr />
    <p>
      By clicking Begin below, I acknowledge that all my questions about the
      study have been answered, and I allow this session to be recorded. I
      understand that I may contact the Human Subjects Protection Advocate of
      the Human Research Protection office, University of Pittsburgh
      (1-866-212-2668) to discuss problems, concerns, and questions; obtain
      information; offer input; or discuss situations that occurred during my
      participation.
    </p>
  </div>
  <div
    class="measure-wide center flex flex-column items-center justify-center pb4"
  >
    <a
      class="center br2 pa2 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b bg-animate"
      href="#"
      on:click={() => dispatch('initialize')}
    >
      Begin</a
    >
  </div>
</div>
