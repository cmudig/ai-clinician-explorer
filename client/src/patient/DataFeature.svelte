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
  export let extremeValue = 0; // 1 = too high, -1 = too low

  let historicalData = [];

  let valueString;
  $: {
    if (value === null || value === undefined) valueString = '--';
    else if (value instanceof String) valueString = value;
    else valueString = formatNumber(value);
  }

  function formatNumber(num) {
    if (Math.abs(Math.round(num) - num) <= 0.00001) return num.toString();
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

  $: console.log(feature, valueColor, defaultColor);

  let defaultColor;
  $: if (extremeValue != 0) defaultColor = dark ? 'light-red' : 'dark-red';
  else defaultColor = dark ? 'white' : 'black';
</script>

<tr
  class="feature-row pv2 bg-animate"
  class:dark
  class:hover-bg-near-white={!dark}
  class:hover-bg-dark-gray={dark}
>
  <td class="feature-name pl3 f6 {dark ? 'white' : 'dark-gray'}">
    {#if !!feature}
      {feature}
    {/if}
  </td>

  <td class="historical-chart pv3 pr2">
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
  </td>
  <td class="feature-value f4 fw5 pv2 pr3" class:white={dark}>
    <p class="mv0 {valueColor != null ? valueColor : defaultColor}">
      {#if trend != 0}
        <span class="trend-marker">{@html trend > 0 ? '&uarr;' : '&darr;'}</span
        >
      {/if}
      {valueString}
    </p>
    {#if !!unit && value != 0.0}
      <p class="mv0 f6">{@html unit}</p>
    {/if}
  </td>
</tr>

<style>
  .feature-row {
    border-bottom: 1px solid #cccccc;
  }

  .feature-row.dark {
    border-bottom: 1px solid #666666;
  }

  .historical-chart {
    height: 72px;
    padding-left: 30px;
  }

  .feature-name {
    width: 150px;
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
