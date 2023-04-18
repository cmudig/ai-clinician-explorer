import PatientPage from './PatientPage.svelte';
import { writable } from 'svelte/store';

const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id') || '';
const bloc = parseInt(urlParams.get('bloc')) || 0;

const app = new PatientPage({
  target: document.body,
  props: {
    patientID: id,
    currentBloc: writable(bloc),
    showLogoutButton: false,
  },
});

export default app;
