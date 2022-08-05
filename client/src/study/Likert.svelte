<script lang="ts">
  export let question;
  export let elements;
  export let response;
  export let background = true;
  export let boldQuestion = true;

  let randomID = 'likert-' + Math.floor(Math.random() * 1e8);
</script>

<div class={background ? 'br2 bg-near-white pa4 mb4' : 'pa0 mb4'}>
  <form action="">
    <label for="text" class="f5 lh-copy mb3" class:b={boldQuestion}>
      {@html question}
    </label>
    <ul
      class="likert"
      style="--likert-border-left:{Math.round(
        100 / elements.length / 2,
      )}%;--likert-border-width:{Math.round(
        (100 * (elements.length - 1)) / elements.length,
      )}%;"
    >
      {#each elements as element, i}
        <li style="width: {Math.round(100 / elements.length)}%;">
          <input
            type="radio"
            name={randomID}
            value={i + 1}
            bind:group={response}
          />
          <label for={i.toString()} class="f6">{@html element}</label>
        </li>
      {/each}
    </ul>
  </form>
</div>

<style>
  form .likert {
    list-style: none;
    width: 100%;
    margin: 0;
    padding: 0;
    display: block;
    border-bottom: 2px solid #7b8794;
  }
  form .likert:last-of-type {
    border-bottom: 0;
  }
  form .likert:before {
    content: '';
    position: relative;
    top: 11px;
    /*left: 11%;*/
    left: var(--likert-border-left);
    display: block;
    background-color: #7b8794;
    height: 4px;
    /*width: 78%;*/
    width: var(--likert-border-width);
  }
  form .likert li {
    display: inline-block;
    text-align: center;
    vertical-align: top;
  }
  form .likert li input[type='radio'] {
    display: block;
    position: relative;
    top: 0;
    left: 50%;
  }
  form .likert li label {
    width: 100%;
    margin-top: 7px;
    font-size: 0.9em;
  }
</style>
