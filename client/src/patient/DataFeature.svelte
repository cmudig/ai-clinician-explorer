<script>
  import { Html, LayerCake, Svg } from 'layercake';
  import Line from '../charts/Line.svelte';
  import AxisY from '../charts/AxisY.svelte';
  import ShadingX from '../charts/ShadingX.svelte';
  import Tooltip from '../charts/Tooltip.svelte';

  export let dark = false;

  export let feature;
  export let unit = '';
  export let value = null;
  export let valueColor = null;
  export let trend = 0;
  export let maxDecimals = 3;
  export let historicalValues = [];
  export let extremeValue = 0; // 1 = too high, -1 = too low
  export let patientID = null;

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
          value: v.value,
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

  let defaultColor;
  $: if (extremeValue != 0) defaultColor = dark ? 'light-red' : 'dark-red';
  else defaultColor = dark ? 'white' : 'black';

  let hoveredMissingValueSegment = null;

  function suspectedMissingValue(d) {
    // Look up its provenance
    if (d.value == null) return false;
    let provenance = historicalValues[d.t].provenance;
    if (!provenance) return false;
    if (!!provenance.KNN && !!patientID && provenance.KNN != patientID)
      return true;
    if (provenance.SAH && !provenance.not_SAH) return true;
    return false;
  }

  function missingValueExplanation(d) {
    let provenance = historicalValues[d.t].provenance;
    if (!provenance) return '';
    if (!!provenance.KNN && !!patientID && provenance.KNN != patientID) {
      console.log(provenance.KNN, patientID);
      return 'Value imputed from another patient';
    }
    if (provenance.SAH && !provenance.not_SAH)
      return 'Value assumed constant from previous timestep';
    return '';
  }
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
      <LayerCake
        x="t"
        y="value"
        data={historicalData}
        padding={{ left: 4 }}
        custom={{ hoveredGet: (d) => d.t == hoveredMissingValueSegment }}
      >
        <Svg>
          <ShadingX
            highlightFn={suspectedMissingValue}
            color="transparent"
            on:hover={(e) =>
              (hoveredMissingValueSegment =
                e.detail != null ? e.detail.t : null)}
          />
          <AxisY
            gridlines={false}
            tickMarks={false}
            {ticks}
            formatTick={formatNumber}
            textAnchor="end"
            dyTick="0.5em"
          />
          <Line stroke="steelblue" dashFn={suspectedMissingValue} />
        </Svg>
        <Html pointerEvents={false}>
          <Tooltip formatText={missingValueExplanation} />
        </Html>
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
