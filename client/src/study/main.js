import StudyPage from './StudyPage.svelte';

let csrf = document.getElementsByName('csrf-token')[0].content;
let errorMessage = document.getElementsByName('open-template-params')[0]
  .content;

const app = new StudyPage({
  target: document.body,
  props: {
    csrf,
    errorMessage,
  },
});

export default app;
