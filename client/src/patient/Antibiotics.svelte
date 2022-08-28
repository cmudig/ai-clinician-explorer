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

  let antibiotics;
  $: if (!!$patient && blocTime != null) {
    antibiotics = ($patient.antibiotics || [])
      .filter((ab) => ab.start <= blocTime || ab.end <= blocTime)
      .sort((a, b) => b.start - a.start);
  }

  function titleCase(txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  }

  function deltaTime(start, end) {
    if (start == null || end == null) return '--';
    if (end >= blocTime) {
      let numMins = (start - blocTime) / 60;
      if (Math.abs(numMins) / 60 >= 24)
        return 'Started ' + rtf.format(Math.round(numMins / (60 * 24)), 'day');
      else if (Math.abs(numMins) >= 60)
        return 'Started ' + rtf.format(Math.round(numMins / 60), 'hour');
      else if (Math.abs(numMins) <= 2) return 'Started just now';
      return 'Started ' + rtf.format(Math.round(numMins), 'minute');
    } else {
      let numMins = (end - blocTime) / 60;
      if (Math.abs(numMins) / 60 >= 24)
        return (
          'Last dose ' + rtf.format(Math.round(numMins / (60 * 24)), 'day')
        );
      else if (Math.abs(numMins) >= 60)
        return 'Last dose ' + rtf.format(Math.round(numMins / 60), 'hour');
      return 'Last dose ' + rtf.format(Math.round(numMins), 'minute');
    }
  }
</script>

<div class="h-100">
  {#if antibiotics.length > 0}
    <table class="w-100 f6">
      {#each antibiotics as ab}
        <tr class="pv2 bg-animate hover-bg-near-white">
          <td class="pl3 b">
            {titleCase(ab.drug)}
          </td>
          <td>{ab.dose_val} {ab.dose_unit} {ab.route}</td>
          <td class="pr3 tr">{deltaTime(ab.start, ab.end)}</td>
        </tr>
      {/each}
    </table>
  {:else}
    <div class="flex h-100 items-center justify-center">
      <p class="dark-gray f5">No antibiotics</p>
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
</style>
