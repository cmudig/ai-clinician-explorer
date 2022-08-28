<script>
  export let question = '';
  export let choices = [];
  export let selectedChoice = null;
  export let background = true;

  let randomID = 'multiple-choice-' + Math.floor(Math.random() * 1e8);

  $: console.log(selectedChoice);
</script>

<div class={background ? 'br2 bg-near-white pa4 mb4' : 'pa0 mb2'}>
  <div class="measure-wide lh-copy">
    <p class="f5 b mt0 mb2">{@html question}</p>
    {#each choices as choice}
      <label
        ><input
          type="radio"
          label={choice.label}
          value={choice.value}
          name={randomID}
          bind:group={selectedChoice}
        />
        {@html choice.label}</label
      >
    {/each}
  </div>
</div>
