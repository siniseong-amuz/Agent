import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

const initializeApp = () => {
  const storedTheme = localStorage.getItem('theme')
  if (storedTheme) {
    document.documentElement.classList.toggle('dark', storedTheme === 'dark')
  } else {
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    document.documentElement.classList.toggle('dark', prefersDark)
  }

  const app = createApp(App)
  app.use(router)
  app.mount('#app')
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp)
} else {
  initializeApp()
}
