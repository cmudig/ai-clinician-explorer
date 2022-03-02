<script>
  import { Html, LayerCake, Svg } from 'layercake';
  import AxisX from './AxisX.svelte';
  import AxisY from './AxisY.svelte';
  import Bar from './Bar.svelte';
  import { scaleBand } from 'd3-scale';
  import Tooltip from './Tooltip.svelte';

  export let importances;
  export let deviations;
  export let numKeys = 10;

  let featureNames = [];
  $: if (!!importances) {
    let keys = Object.keys(importances).sort(
      // (a, b) => Math.abs(importances[b]) - Math.abs(importances[a])
      (a, b) => importances[b] - importances[a]
    );
    featureNames = keys.slice(0, numKeys);
    // featureNames = [
    //   ...keys.slice(0, numKeys / 2),
    //   ...keys.slice(keys.length - numKeys / 2),
    // ];
  }

  let barData;
  $: if (featureNames.length > 0) {
    barData = featureNames.map((name) => ({
      feature: name,
      absImportance: Math.abs(importances[name]),
      importance: importances[name],
      decrease: !!deviations && !!deviations[name] && deviations[name].raw < 0,
    }));
  } else barData = null;

  let maxImportance = 0;
  $: if (!!barData) {
    maxImportance = barData.reduce(
      (curr, p) => Math.max(curr, p.absImportance),
      0
    );
    maxImportance = Math.ceil(maxImportance / 0.5) * 0.5;
  }

  let hoveredFeature = null;
  function makeTooltipText(d) {
    // On bar hover, show information about how much the value deviates from
    // the average
    let dev = (deviations || {})[d.feature];
    if (!dev)
      return `<strong>${d.feature}:</strong> ${d.importance.toFixed(3)}`;
    if (dev.type == 'binary') {
      return `<strong>${d.feature}</strong> is ${(
        Math.abs(dev.percent) * 100
      ).toFixed(0)}% ${
        dev.percent > 0 ? 'more' : 'less'
      } likely to be 1 compared to other states`;
    }
    if (dev.raw > 0)
      return `<strong>${
        d.feature
      }</strong> is on average ${dev.raw.toLocaleString({
        maximumSignificantDigits: 3,
      })} higher than in other states`;
    else
      return `<strong>${
        d.feature
      }</strong> is on average ${(-dev.raw).toLocaleString({
        maximumSignificantDigits: 3,
      })} lower than in other states`;
  }
</script>

<div class="w-100 h-100 pl5 pr4">
  {#if !!barData}
    <LayerCake
      padding={{ top: 20, bottom: 40, left: 30 }}
      x="importance"
      y="feature"
      yScale={scaleBand().paddingInner([0.05]).round(true)}
      xDomain={[0, maxImportance]}
      yDomain={featureNames.reverse()}
      data={barData}
      custom={{ hoveredGet: (d) => d.feature == hoveredFeature }}
    >
      <Svg>
        <AxisX
          gridlines={true}
          baseline={true}
          snapTicks={true}
          label="Importance"
        />
        <AxisY gridlines={false} />
        <Bar
          fillFn={(d) => (d.decrease ? '#ff7f0e' : '#1f77b4')}
          on:hover={(e) =>
            (hoveredFeature = e.detail != null ? e.detail.feature : null)}
        />
        <!-- interpolateRdBu((d.importance + maxImportance) / (2 * maxImportance)) -->
      </Svg>
      <Html pointerEvents={false}>
        <Tooltip formatText={makeTooltipText} />
      </Html>
    </LayerCake>
  {/if}
</div>
