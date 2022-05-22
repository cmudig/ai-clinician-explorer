<script>
  import { getContext } from 'svelte';

  import SegmentedControl from '../utils/SegmentedControl.svelte';

  export let selectedAction;

  let { modelInfo } = getContext('patient');

  let selectedFluids = 0;
  let selectedVaso = 0;

  let fluidBinLabels = [0, 1, 2, 3, 4];
  let vasoBinLabels = [0, 1, 2, 3, 4];

  const fluidFormatParams = { maximumFractionDigits: 0 };
  const vasoFormatParams = { maximumSignificantDigits: 3 };

  $: if (!!$modelInfo && selectedFluids > 0 && selectedVaso > 0) {
    console.log('selected action non-null');
    selectedAction =
      (selectedFluids - 1) * $modelInfo.actions.n_action_bins +
      (selectedVaso - 1);
  } else {
    console.log('selected action null');
    selectedAction = null;
  }

  $: if (!!$modelInfo) {
    fluidBinLabels = $modelInfo.actions.action_bins[0].map((b, i) => {
      if (i == 0) return b.toFixed(0);
      if (i == $modelInfo.actions.n_action_bins - 1) return '> ' + b.toFixed(0);
      let next = $modelInfo.actions.action_bins[0][i + 1];
      return `${b.toFixed(0)}-${next.toFixed(0)}`;
    });
    vasoBinLabels = $modelInfo.actions.action_bins[1].map((b, i) => {
      if (i == 0) return b.toLocaleString(vasoFormatParams);
      if (i == $modelInfo.actions.n_action_bins - 1)
        return '> ' + b.toLocaleString(vasoFormatParams);
      let next = $modelInfo.actions.action_bins[1][i + 1];
      return `${b.toLocaleString(vasoFormatParams)}-${next.toLocaleString(
        vasoFormatParams,
      )}`;
    });
  }
</script>

<div class="w-100">
  <div class="ph4 flex w-100 items-center mb3">
    <span class="f5 flex-auto tr">IV Fluids:</span>
    <div class="control-container mh2">
      <SegmentedControl
        bind:selected={selectedFluids}
        options={fluidBinLabels.map((l, i) => ({ value: i + 1, name: l }))}
        unselectedTextClass="dark-blue"
      />
    </div>
    <span class="f6 suffix">mL/4 h</span>
  </div>
  <div class="ph4 flex w-100 items-center mb3">
    <span class="f5 flex-auto tr">Vasopressors:</span>
    <div class="control-container mh2">
      <SegmentedControl
        bind:selected={selectedVaso}
        options={vasoBinLabels.map((l, i) => ({ value: i + 1, name: l }))}
        unselectedTextClass="dark-blue"
      />
    </div>
    <span class="f6 suffix">ug/kg/min norepinephrine equiv.</span>
  </div>
</div>

<style>
  .control-container {
    width: 60%;
  }

  .suffix {
    width: 120px;
  }
</style>
