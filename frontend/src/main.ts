import { createApp } from 'vue'
import PrimeVue from 'primevue/config';
import Material from '@primevue/themes/material';
import './style.css'; // Tailwind CSS
import App from './App.vue'


const app = createApp(App);

app.use(PrimeVue, {
  theme: {
    preset: Material,
    options: {
      darkModeSelector: '.my-app-dark',
    },
  },
});


app.mount('#app');
