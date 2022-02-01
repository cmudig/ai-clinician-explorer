import PatientPage from './PatientPage.svelte';

const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id') || '';

const app = new PatientPage({
  target: document.body,
  props: {
    patientID: id,
  },
});

export default app;
