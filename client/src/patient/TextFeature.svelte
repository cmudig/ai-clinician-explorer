<script>
  export let label;
  export let dark = false;
</script>

<div
  class="text-feature ph2 pv2 bg-animate flex justify-between items-center"
  class:dark
  class:hover-bg-near-white={!dark}
  class:hover-bg-dark-gray={dark}
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
  .text-feature.dark {
    border-bottom: 1px solid #666666;
  }
</style>
