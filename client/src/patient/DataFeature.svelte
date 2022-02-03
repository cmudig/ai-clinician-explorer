<script>
  export let feature;
  export let value = null;
  export let referenceRange = [-1e9, 1e9];
  export let maxDecimals = 3;

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
</script>

<div
  class="feature-row ph3 pv2 bg-animate hover-bg-near-white flex justify-between items-center"
>
  {#if !!feature}
    <span class="f6 dark-gray">{feature}</span>
  {/if}
  <span class="f4 fw5 mv2">{valueString}</span>
</div>

<style>
  .feature-row {
    border-bottom: 1px solid #cccccc;
  }
</style>
