<script>
  export let width = 200;
</script>

<div
  class="bg-moon-gray br-pill h1 overflow-y-hidden"
  style="width: {width}px;"
>
  <div class="bg-blue progress-bar br-pill h1 shadow-1 w-100" />
</div>

<style>
  .progress-bar {
    background-image: linear-gradient(
      -45deg,
      rgba(255, 255, 255, 0.35) 25%,
      rgba(255, 255, 255, 0) 25%,
      rgba(255, 255, 255, 0) 50%,
      rgba(255, 255, 255, 0.35) 50%,
      rgba(255, 255, 255, 0.35) 75%,
      rgba(255, 255, 255, 0) 75%,
      rgba(255, 255, 255, 0)
    );
    background-repeat: repeat-x;
    background-size: 20px 20px;
    animation: stripes 1s linear infinite;
  }
  @-webkit-keyframes stripes {
    to {
      background-position: 20px 0;
    }
  }
  @-moz-keyframes stripes {
    to {
      background-position: 20px 0;
    }
  }
  @keyframes stripes {
    to {
      background-position: 20px 0;
    }
  }
</style>
