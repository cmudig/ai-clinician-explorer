<script>
  import { getContext } from 'svelte';
  import Columns from '../utils/columns';

  let { patient, currentBloc } = getContext('patient');

  let blocTime;
  $: if (!!$patient && $currentBloc > 0) {
    // This is the start time of the bloc - we need to try to get the end time
    blocTime = $patient.timesteps[$currentBloc - 1][Columns.C_TIMESTEP];
    if ($patient.timesteps.length > 1)
      blocTime +=
        $patient.timesteps[1][Columns.C_TIMESTEP] -
        $patient.timesteps[0][Columns.C_TIMESTEP];
  } else {
    blocTime = null;
  }

  const rtf = new Intl.RelativeTimeFormat('en', {
    localeMatcher: 'best fit',
    numeric: 'always',
    style: 'long',
  });

  let cultures;
  $: if (!!$patient && blocTime != null) {
    cultures = ($patient.microbio || [])
      .filter((mb) => mb.charttime <= blocTime)
      .sort((a, b) => b.charttime - a.charttime);
  }

  function deltaTime(timestamp) {
    if (timestamp == null) return '--';
    let numMins = (timestamp - blocTime) / 60;
    if (Math.abs(numMins) / 60 >= 24)
      return rtf.format(Math.round(numMins / (60 * 24)), 'day');
    else if (Math.abs(numMins) >= 60)
      return rtf.format(Math.round(numMins / 60), 'hour');
    return rtf.format(Math.round(numMins), 'minute');
  }

  let expandedIndex = -1;
  $: console.log(expandedIndex);
</script>

<div class="h-100">
  {#if cultures.length > 0}
    <table class="w-100 f6">
      {#each cultures as event, i}
        <tr
          class="pv2 bg-animate hover-bg-near-white"
          class:pointer={!!event.antibiotics && event.antibiotics.length > 0}
          on:click={() => {
            if (expandedIndex == i) expandedIndex = -1;
            else if (!!event.antibiotics && event.antibiotics.length > 0)
              expandedIndex = i;
          }}
        >
          <td class="ph3">
            {#if !!event.antibiotics && event.antibiotics.length > 0}<i
                class="arrow {expandedIndex == i ? 'down' : 'right'}"
              />{/if}
          </td>
          <td class="b">{event.spec_type_desc}</td>
          <td>
            {#if !!event.org_name}
              {event.org_name}
            {:else}
              Negative
            {/if}
          </td>
          <td class="pr3 tr time-delta">{deltaTime(event.charttime)}</td>
        </tr>
        {#if expandedIndex == i}
          {#each event.antibiotics as ab}
            <tr class="pv2">
              <td /><td /><td>{ab.ab_name}</td><td>{ab.interpretation}</td>
            </tr>
          {/each}
        {/if}
      {/each}
    </table>
  {:else}
    <div class="flex h-100 items-center justify-center">
      <p class="dark-gray f5">No cultures</p>
    </div>
  {/if}
</div>

<style>
  table {
    border-collapse: collapse;
  }

  tr {
    border-bottom: 1px solid #cccccc;
    height: 48px;
  }

  .time-delta {
    width: 100px;
  }

  .arrow {
    border: solid black;
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 3px;
  }

  .arrow.right {
    transform: rotate(-45deg);
    -webkit-transform: rotate(-45deg);
  }

  .arrow.down {
    transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
  }
</style>
