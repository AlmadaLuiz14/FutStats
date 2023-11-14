import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
//import store from './store/index'

// Importe o arquivo CSS com a imagem de fundo
import './assets/background.css'

const app = createApp(App)
app.use(router)
//app.use(store)

app.mount('#app')

