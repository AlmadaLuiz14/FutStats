import {createApp} from 'vue'
import {createRouter, createWebHistory} from 'vue-router'
import FootballTable from '../components/FootballTable.vue'
import ResultsTable from '../components/ResultsTable.vue'
import TopsTable from '../components/TopsTable.vue'
import NewsTable from '../components/NewsTable.vue'
/*import LoginT from '../components/LoginTe.vue'*/

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
    }

    /*{
        path: '/Login',
        name: 'Login',
        component: LoginTe
    }*/
]

const router = createRouter({
    mode: 'history',
    history: createWebHistory(),
    base: 'http://localhost:8080',
    routes
})

export default router