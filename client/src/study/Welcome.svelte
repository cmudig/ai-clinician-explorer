<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let resumeErrorMessage;
  let participantID;
  let resumingPrevious = false;
</script>

<div class="flex flex-column h-100 items-center justify-center">
  <div class="information f5 lh-copy measure-wide mb3">
    In this study, you will be presented with four vignettes of patients with
    sepsis. In each case, you will be asked to choose an appropriate level of IV
    fluids and vasopressors based on the available patient data.
  </div>
  {#if resumingPrevious}
    <div class="bg-light-blue-gray br2 pa3 measure-wide">
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
    </div>
    <a
      class="center mt2 pa2 link dib dim bg-animate f6"
      href="#"
      on:click={() => (resumingPrevious = false)}
    >
      Begin new session...</a
    >
  {:else}
    <a
      class="center br2 pa2 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b bg-animate"
      href="#"
      on:click={() => dispatch('initialize')}
    >
      Begin</a
    >
    <a
      class="center mt2 pa2 link dib dim bg-animate f6"
      href="#"
      on:click={() => (resumingPrevious = true)}
    >
      Resume previous session...</a
    >
  {/if}
</div>
