<script>
  import { LayerCake, Svg } from 'layercake';
  import Line from '../charts/Line.svelte';
  import AxisX from '../charts/AxisX.svelte';
  import AxisY from '../charts/AxisY.svelte';

  export let feature;
  export let value = null;
  export let referenceRange = [-1e9, 1e9];
  export let maxDecimals = 3;
  export let historicalValues = [];
  let historicalData = [];

  let valueString;
  $: {
    if (value === null || value === undefined) valueString = '--';
    else if (value instanceof String) valueString = value;
    else if (Math.abs(Math.round(value) - value) <= 0.001)
      valueString = value.toString();
    else
      valueString = value.toLocaleString('en-US', {
        maximumFractionDigits: maxDecimals,
      });
  }

  $: {
    if (historicalValues.length <= 1) {
      historicalData = [];
    } else {
      historicalData = historicalValues.map((v, i) => {
        if (v == null || v == undefined) console.log(feature, v);
        return {
          t: i,
          value: v,
        };
      });
    }
  }
</script>

<div
  class="feature-row ph3 pv2 bg-animate hover-bg-near-white flex justify-between items-center"
>
  {#if !!feature}
    <p class="feature-name f6 dark-gray">{feature}</p>
  {/if}
  <div class="historical-chart pv2">
    {#if historicalData.length > 0}
      <LayerCake x="t" y="value" data={historicalData}>
        <Svg>
          <AxisY gridlines={false} tickMarks={false} />
          <Line stroke="steelblue" />
        </Svg>
      </LayerCake>
    {/if}
  </div>
  <p class="feature-value f4 fw5 mv2">{valueString}</p>
</div>

<style>
  .feature-row {
    border-bottom: 1px solid #cccccc;
  }

  .historical-chart {
    flex-grow: 1;
    height: 60px;
  }

  .feature-name {
    width: 100px;
    word-wrap: break-word;
  }

  .feature-value {
    width: 80px;
    text-align: right;
  }
</style>
