import {createApp} from 'vue'
import {createRouter, createWebHistory} from 'vue-router'
import FootballTable from '../components/FootballTable.vue'
import ResultsTable from '../components/ResultsTable.vue'
import TopsTable from '../components/TopsTable.vue'
import NewsTable from '../components/NewsTable.vue'
import TablesHome from '../views/TablesHome.vue'
import Login_screen from '../views/Login_screen.vue'
import Cad_screen from '../views/Cad_screen.vue'

createApp(createRouter)

const routes = [
    {
        path: '/TabelaCampeonato',
        name: 'FootballTable',
        component: FootballTable
    },

    {
        path: '/Resultados',
        name: 'ResultsTable',
        component: ResultsTable
    },

    {
        path: '/Artilheiros',
        name: 'TopsTable',
        component: TopsTable
    },

    {
        path: '/Noticias',
        name: 'NewsTable',
        component: NewsTable
    },

    {
        path: '/',
        name: 'TablesHome',
        component: TablesHome
    },

    {
        path: '/Login',
        name: 'Login_screen',
        component: Login_screen
    },

    {
        path: '/Cadastro',
        name: 'Cad_screen',
        component: Cad_screen
    }

]

const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    base: 'http://localhost:8080',
    routes
})

export default router
