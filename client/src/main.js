import PatientBrowser from './PatientBrowser.svelte';

const urlParams = new URLSearchParams(window.location.search);
const statesList = (urlParams.get('states') || '')
  .split(',')
  .filter((v) => v.length > 0)
  .map((v) => ({ value: v, label: v }));

const app = new PatientBrowser({
  target: document.body,
  props: {
    externalFilters: {
      state: statesList,
    },
  },
});

export default app;
