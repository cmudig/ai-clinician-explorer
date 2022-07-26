import StudyPage from './StudyPage.svelte';

const urlParams = new URLSearchParams(window.location.search);
const devMode = urlParams.get('dev') || '';
let csrf = document.getElementsByName('csrf-token')[0].content;
let errorMessage = document.getElementsByName('open-template-params')[0]
  .content;

const app = new StudyPage({
  target: document.body,
  props: {
    csrf,
    devMode: devMode == '1',
    errorMessage,
  },
});

export default app;
