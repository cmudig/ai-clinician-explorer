import PatientBrowser from './PatientBrowser.svelte';

const urlParams = new URLSearchParams(window.location.search);
const statesList = (urlParams.get('states') || '')
  .split(',')
  .filter((v) => v.length > 0);

const app = new PatientBrowser({
  target: document.body,
  props: {
    filteredStates: statesList,
  },
});

export default app;
