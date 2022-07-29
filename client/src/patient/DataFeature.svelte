<script>
  import { Html, LayerCake, Svg } from 'layercake';
  import Line from '../charts/Line.svelte';
  import AxisY from '../charts/AxisY.svelte';
  import ShadingX from '../charts/ShadingX.svelte';
  import Tooltip from '../charts/Tooltip.svelte';
  import AxisX from '../charts/AxisX.svelte';

  export let dark = false;

  export let feature;
  export let unit = '';
  export let value = null;
  export let valueColor = null;
  export let trend = 0;
  export let maxDecimals = 3;
  export let numHoursPerStep = 4; // number of hours between each historical value
  export let historicalValues = [];
  export let extremeValue = 0; // 1 = too high, -1 = too low
  export let patientID = null;
  export let highlightImputedValues = true;
  export let highlightHeldValues = false;
  export let valueTooltips = false;

  let historicalData = [];

  let valueString;
  $: {
    valueString = formatValue(value, maxDecimals);
  }

  function formatValue(num, dec) {
    if (num === null || num === undefined) return '--';
    else if (num instanceof String) return num;

    if (Math.abs(Math.round(num) - num) <= 0.00001) return num.toString();
    else
      return num.toLocaleString('en-US', {
        maximumFractionDigits: dec,
      });
  }

  function formatTimeDelta(deltaDays, short = false) {
    // calculate how far away dataIndex is from the end of the list of historical values
    let hours = Math.round(deltaDays * 24);
    if (short) {
      if (hours == 0) return 'now';
      if (historicalData.length > (24 / numHoursPerStep) * 1.5 && hours < 0) {
        return hours == 0 ? '' : `${hours}h`;
      }
      return `${deltaDays.toLocaleString({ maximumFractionDigits: 1 })}d`;
    }
    return hours == 0 ? 'Just now' : hours + ' hours ago';
  }

  function createXTicks(data) {
    if (data.every((d) => d.value === null || d.value === undefined)) return [];
    if (data.length <= 24 / numHoursPerStep) {
      // tick every interval
      return data.map((d) => d.t);
    } else if ((data.length * numHoursPerStep) / 24 <= 2) {
      // every 12 h
      return data.map((d) => d.t).filter((d) => Math.round(d / 0.5) * 0.5 == d);
    } else {
      // every day
      return data.map((d) => d.t).filter((d) => Math.round(d) == d);
    }
  }

  $: {
    if (historicalValues.length <= 1) {
      historicalData = [];
    } else {
      historicalData = historicalValues.map((v, i) => {
        return {
          i,
          t: (i + 1 - historicalValues.length) / (24 / numHoursPerStep), // time in days from end
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

  let hoveredSegment = null;

  function suspectedMissingValue(d, knn = true, sah = true) {
    // Look up its provenance
    if (d.value == null) return false;
    let provenance = historicalValues[d.i].provenance;
    if (!provenance) return false;
    if (knn && !!provenance.KNN && !!patientID && provenance.KNN != patientID)
      return true;
    if (sah && provenance.SAH && !provenance.not_SAH) return true;
    return false;
  }

  function valueTooltipFn(d) {
    return `${formatTimeDelta(d.t, false)}: <strong>${formatValue(
      d.value,
      maxDecimals,
    )} ${!!unit ? unit : ''}</strong>`;
  }

  function missingValueExplanation(d) {
    let provenance = historicalValues[d.i].provenance;
    if (!provenance) return '';
    if (!!provenance.KNN && !!patientID && provenance.KNN != patientID) {
      return 'Values imputed';
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
      {@html feature}
    {/if}
  </td>

  <td class="historical-chart pv3 pr2">
    {#if historicalData.length > 0}
      <LayerCake
        x="t"
        y="value"
        data={historicalData}
        padding={{ left: 4, bottom: 8 }}
        custom={{
          hoveredGet: (d) => {
            if (valueTooltips || highlightImputedValues || highlightHeldValues)
              return d.i == hoveredSegment;
            return false;
          },
        }}
      >
        <Svg>
          <ShadingX
            highlightFn={(d) => suspectedMissingValue(d, true, false)}
            color={highlightImputedValues ? '#FF725C33' : 'transparent'}
            on:hover={(e) =>
              (hoveredSegment =
                e.detail != null && highlightImputedValues ? e.detail.i : null)}
          />
          <ShadingX
            highlightFn={(d) => suspectedMissingValue(d, false, true)}
            color={highlightHeldValues ? '#FF725C33' : 'transparent'}
            on:hover={(e) =>
              (hoveredSegment =
                e.detail != null && highlightHeldValues ? e.detail.i : null)}
          />
          <AxisX
            gridlines={false}
            tickMarks={false}
            ticks={createXTicks(historicalData)}
            formatTick={(t) => formatTimeDelta(t, true)}
            color="#999"
            snapTicks={true}
          />
          <AxisY
            gridlines={false}
            tickMarks={false}
            {ticks}
            formatTick={(t) => formatValue(t, maxDecimals)}
            textAnchor="end"
            dyTick="0.5em"
            color="#999"
          />
          <Line
            stroke="steelblue"
            dashFn={highlightImputedValues ? suspectedMissingValue : null}
          />
          {#if valueTooltips}
            <ShadingX
              highlightFn={(d) => true}
              color="transparent"
              on:hover={(e) =>
                (hoveredSegment = e.detail != null ? e.detail.i : null)}
            />
          {/if}
        </Svg>
        <Html pointerEvents={false}>
          <Tooltip
            formatText={valueTooltips
              ? valueTooltipFn
              : missingValueExplanation}
          />
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
    {#if !!unit}
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
