<script>
  export let csrf;
  export let errorMessage = '';
</script>

<header class="bg-navy-90 fixed w-100 ph3 pv2 pv3-ns ph3-m ph4-l">
  <nav class="f6 fw6 ttu tracked">
    <a class="link dim white dib mr3" href="#" title="Home"
      >AI Clinician Explorer</a
    >
  </nav>
</header>

<main class="pa0 h-100 flex flex-column items-center justify-center">
  <div class="bg-light-blue-gray login-parent br2 pa3 w-30">
    <form class="measure center" method="POST" action="/login">
      <fieldset id="login" class="ba b--transparent ph0 mh0">
        <legend class="f4 fw6 ph0 mh0">Sign In</legend>
        {#if !!errorMessage}
          <div class="pa2 mv2 br2 bg-washed-red f5">
            {errorMessage}
          </div>
        {/if}
        <div class="mt3">
          <label class="db fw6 lh-copy f6" for="user_id">User ID</label>
          <input
            class="pa2 input-reset ba bg-white w-100"
            type="username"
            name="user_id"
            id="user_id"
          />
        </div>
        <div class="mv3">
          <label class="db fw6 lh-copy f6" for="password">Password</label>
          <input
            class="b pa2 input-reset ba bg-white w-100"
            type="password"
            name="password"
            id="password"
          />
        </div>
        <label class="pa0 ma0 mb2 lh-copy f6 pointer"
          ><input type="checkbox" name="remember" /> Remember me</label
        >
      </fieldset>
      <input type="hidden" name="csrf_token" value={csrf} />
      <div class="">
        <input
          class="pa2 link dib white bg-dark-blue hover-bg-navy-dark pointer f6 b bg-animate"
          type="submit"
          value="Sign In"
        />
      </div>
    </form>
  </div>
</main>
