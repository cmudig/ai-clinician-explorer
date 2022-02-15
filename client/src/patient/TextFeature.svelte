<script>
  export let label;
</script>

<div
  class="text-feature ph3 pv2 bg-animate hover-bg-near-white flex justify-between items-center"
>
  {#if !!label}
    <p class="f6">{label}</p>
  {/if}
  <div class="text-feature-content flex-auto ml3 tr f6 b pv2">
    <slot />
  </div>
</div>

<style>
  .text-feature {
    min-height: 64px;
    border-bottom: 1px solid #bbbbbb;
  }
</style>
