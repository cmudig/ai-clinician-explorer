<script>
  import { createEventDispatcher, onMount } from 'svelte';

  const dispatch = createEventDispatcher();

  let transparent = true;

  function exit() {
    transparent = true;
    setTimeout(() => dispatch('exit'), 300);
  }

  onMount(() => {
    setTimeout(() => (transparent = false));
  });
</script>

<div
  class="fixed z-9999 top-0 left-0 right-0 bottom-0 w-100 h-100 translucent-overlay flex items-center justify-center"
  style="opacity: {transparent ? 0.0 : 1.0};"
  on:click={exit}
>
  <div class="pa4 measure-wide lh-copy bg-white br2">
    <h2 class="mv0">AI Clinician Explorer</h2>
    <p>
      This tool allows clinicians and clinical data experts to browse and
      analyze trajectories for patients with sepsis. The data shown is a random
      sample of patients from the MIMIC-IV dataset, shown here for demonstration
      purposes only.
    </p>
    <p>
      To learn more about the system, please see our paper: <a
        class="link blue dim"
        target="_blank"
        href="https://arxiv.org/abs/2302.00096"
        >Ignore, Trust, or Negotiate: Understanding Clinician Acceptance of
        AI-Based Treatment Recommendations in Health Care</a
      >.
    </p>
    <button
      class="pa2 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b"
      on:click={exit}
    >
      Dismiss
    </button>
  </div>
</div>

<style>
  .translucent-overlay {
    background-color: rgba(0, 0, 0, 0.8);
    transition: opacity 0.3s ease-in-out;
  }
</style>
