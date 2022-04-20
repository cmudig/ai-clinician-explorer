<script>
  import { Html, LayerCake, Svg } from 'layercake';
  import { scaleLinear } from 'd3-scale';
  import AxisX from '../charts/AxisX.svelte';
  import AxisY from '../charts/AxisY.svelte';
  import Rect from '../charts/Rect.svelte';
  import { interpolateRdBu } from 'd3-scale-chromatic';
  import Colorbar from '../charts/Colorbar.svelte';
  import Tooltip from '../charts/Tooltip.svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let data;
  export let vasopressorBins; // x axis labels
  export let fluidBins; // y axis labels
  export let formatTooltip; // function that takes a data point and returns a string describing it

  export let valueDomain; // range of values should be mapped to the ends of the color map
  export let colorMap = interpolateRdBu;
  export let nullColor = 'black';

  export let selectedAction = null;

  let hoveredAction = null;

  export let clinicianActions = new Set();
  export let physicianActions = new Set();
</script>

<div class="container" style="grid-template-rows: 5; grid-template-columns: 5;">
  {#each Array(5) as row}
    <div>
      {#each Array(5) as col}
        <button
          class:active={clinicianActions.has(row * 5 + col)}
          on:click={() => {
            if (clinicianActions.has(row * 5 + col)) {
              clinicianActions.delete(row * 5 + col);
            } else {
              clinicianActions.add(row * 5 + col);
            }
          }}
        />
      {/each}
    </div>
  {/each}
</div>

<div class="container" style="grid-template-rows: 5; grid-template-columns: 5;">
  {#each Array(5) as row}
    <div>
      {#each Array(5) as col}
        <button
          class:active={physicianActions.has(row * 5 + col)}
          on:click={() => {
            if (physicianActions.has(row * 5 + col)) {
              physicianActions.delete(row * 5 + col);
            } else {
              physicianActions.add(row * 5 + col);
            }
          }}
        />
      {/each}
    </div>
  {/each}
</div>

<style>
  .actions-heatmap {
    height: 220px;
  }

  .heatmap-plot {
    z-index: 10;
  }

  .legend-container {
    width: 60px;
  }

  .active {
    background-color: pink;
  }
</style>
