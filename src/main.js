import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

// Configuração global, se necessário
// Vue.config.productionTip = false

// Importe o arquivo CSS com a imagem de fundo
import './assets/background.css'

app.mount('#app')
