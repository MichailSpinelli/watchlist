import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Research from '../views/Research.vue'
import DbAnimeResearch  from '../views/DbAnimeResearch.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/research', component: Research },
        { path: '/research-db', component: DbAnimeResearch }
]

export default createRouter({
    history: createWebHistory(),
    routes
})