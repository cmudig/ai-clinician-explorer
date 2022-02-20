<script>
  import { getContext } from 'svelte';
  import TextFeature from './TextFeature.svelte';

  let { patient, currentBloc } = getContext('patient');

  let timePoint;
  $: if (!!$patient && $currentBloc > 0)
    timePoint = $patient.timesteps[$currentBloc - 1];

  let microbioEvents = [];
  $: if (!!$patient && $currentBloc > 0) {
    microbioEvents = $patient.timesteps
      .slice(0, $currentBloc)
      .map((ts) => {
        if (!!ts.microbio) return ts.microbio;
        return [];
      })
      .flat()
      .sort((a, b) => b.charttime - a.charttime);
  }
</script>

<div class="pv2 ph2">
  {#if !!$patient}
    <TextFeature label="Antibiotics">
      {#if !!timePoint.antibiotics && timePoint.antibiotics.length > 0}
        {#each timePoint.antibiotics as ab}
          <p class="mv2">{ab.drug}, {ab.dose_val} {ab.dose_unit} {ab.route}</p>
        {/each}
      {:else}
        --
      {/if}
    </TextFeature>
    <TextFeature label="Microbio">
      {#if !!microbioEvents && microbioEvents.length > 0}
        {#each microbioEvents as event}
          <p class="mv2">
            {#if !!event.org_name}
              {event.spec_type_desc} - {event.org_name}
              {#if !!event.ab_name},
                {event.ab_name}
                {event.interpretation}
              {/if}
            {:else}
              {event.spec_type_desc} - none
            {/if}
          </p>
        {/each}
      {:else}
        --
      {/if}
    </TextFeature>
  {/if}
</div>
