import DefaultTheme from 'vitepress/theme'
import ResearchHome from './ResearchHome.vue'
import './style.css'
export default { extends: DefaultTheme, enhanceApp({app}) { app.component('ResearchHome',ResearchHome) } }
