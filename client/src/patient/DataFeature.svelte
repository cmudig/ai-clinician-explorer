<script>
  import { LayerCake, Svg } from 'layercake';
  import Line from '../charts/Line.svelte';
  import AxisX from '../charts/AxisX.svelte';
  import AxisY from '../charts/AxisY.svelte';

  export let dark = false;

  export let feature;
  export let unit = '';
  export let value = null;
  export let valueColor = null;
  export let trend = 0;
  export let maxDecimals = 3;
  export let historicalValues = [];
  let historicalData = [];

  let valueString;
  $: {
    if (value === null || value === undefined) valueString = '--';
    else if (value instanceof String) valueString = value;
    else valueString = formatNumber(value);
  }

  function formatNumber(num) {
    if (Math.abs(Math.round(num) - num) <= 0.001) return num.toString();
    else
      return num.toLocaleString('en-US', {
        maximumFractionDigits: maxDecimals,
      });
  }

  $: {
    if (historicalValues.length <= 1) {
      historicalData = [];
    } else {
      historicalData = historicalValues.map((v, i) => {
        return {
          t: i,
          value: v,
        };
      });
    }
  }

  let ticks = [];
  $: {
    let nonNull = historicalData
      .map((v) => v.value)
      .filter((v) => typeof v == 'number' && v != null && v != undefined);
    if (nonNull.length > 0) {
      ticks = [
        nonNull.reduce((curr, v) => Math.min(curr, v), 1e12),
        nonNull.reduce((curr, v) => Math.max(curr, v), -1e12),
      ];
    } else ticks = [];
  }
</script>

<div
  class="feature-row ph2 pv2 bg-animate flex justify-between items-center"
  class:dark
  class:hover-bg-near-white={!dark}
  class:hover-bg-dark-gray={dark}
>
  {#if !!feature}
    <p class="feature-name f6 {dark ? 'white' : 'dark-gray'}">{feature}</p>
  {/if}
  <div class="historical-chart pv2">
    {#if historicalData.length > 0}
      <LayerCake x="t" y="value" data={historicalData} padding={{ left: 4 }}>
        <Svg>
          <AxisY
            gridlines={false}
            tickMarks={false}
            {ticks}
            formatTick={formatNumber}
            textAnchor="end"
            dyTick="0.5em"
          />
          <Line stroke="steelblue" />
        </Svg>
      </LayerCake>
    {/if}
  </div>
  <p class="feature-value f4 fw5 mv2" class:white={dark}>
    {#if trend != 0}
      <span class="trend-marker">{@html trend > 0 ? '&uarr;' : '&darr;'}</span>
    {/if}
    <span style="color: {valueColor || (dark ? 'white' : 'black')};"
      >{valueString}</span
    >
    {#if !!unit}
      <span class="f5">{@html unit}</span>
    {/if}
  </p>
</div>

<style>
  .feature-row {
    border-bottom: 1px solid #cccccc;
  }

  .feature-row.dark {
    border-bottom: 1px solid #666666;
  }

  .historical-chart {
    flex-grow: 1;
    height: 60px;
    margin-left: 30px;
  }

  .feature-name {
    width: 110px;
    word-wrap: break-word;
  }

  .feature-value {
    width: 110px;
    text-align: right;
  }

  .trend-marker {
    font-size: 0.8rem;
    display: inline-block;
  }
</style>
