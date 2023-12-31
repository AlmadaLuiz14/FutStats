import {createApp} from 'vue'
import {createRouter, createWebHistory} from 'vue-router'
import FootballTable from '../components/FootballTable.vue'
import ResultsTable from '../components/ResultsTable.vue'
import TopsTable from '../components/TopsTable.vue'
import NewsTable from '../components/NewsTable.vue'
import TablesHome from '../views/TablesHome.vue'
import Login_screen from '../views/Login_screen.vue'
import Cad_screen from '../views/Cad_screen.vue'
import time_screen from '../components/time_screen.vue'
import EstatisticasBrasileiro from '../components/EstatisticasBrasileiro.vue'
import SimulaTable from '../components/SimulaTable.vue'
import User_screen from '../views/User_screen.vue'
import Adm_screen from '../views/Adm_screen.vue'
import Recuper_screen from '../views/RecuperarSenha_screen.vue'

createApp(createRouter)

const routes = [
    {
        path: '/TabelaCampeonato',
        name: 'FootballTable',
        component: FootballTable
    },

    {
        path: '/SimulaTable',
        name: 'SimulaTable',
        component: SimulaTable
    },

    {
        path: '/Estatisticas',
        name: 'EstatisticasBrasileiro',
        component: EstatisticasBrasileiro
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
    },

    {
        path: '/time/:id',
        name: 'time_screen',
        component: time_screen,
        props: true
    },

    {
        path: '/Usuario',
        name: 'User_screen',
        component: User_screen
    },

    {
        path: '/Adm',
        name: 'Adm_screen',
        component: Adm_screen
    },

    {
        path:'/RecuperarSenha',
        name: 'RecuperarSenha_screen',
        component: Recuper_screen
    }

]

const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    base: 'http://localhost:8080',
    routes
})

export default router
