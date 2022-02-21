<script>
  export let label;
  export let dark = false;
</script>

<tr
  class="text-feature ph2 pv2 bg-animate"
  class:dark
  class:hover-bg-near-white={!dark}
  class:hover-bg-dark-gray={dark}
>
  <td class="f6 pl3">
    {#if !!label}
      {label}
    {/if}
  </td>
  <td />
  <td class="text-feature-content flex-auto ph3 tr f6 b pv2">
    <slot />
  </td>
</tr>

<style>
  .text-feature {
    min-height: 64px;
    border-bottom: 1px solid #bbbbbb;
  }
  .text-feature.dark {
    border-bottom: 1px solid #666666;
  }
</style>
