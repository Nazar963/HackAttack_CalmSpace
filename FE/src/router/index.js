import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import Record from '../components/Record.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage,
    },
    {
        path: '/about',
        name: 'About',
        component: Record,
    },
    // Add other routes here as needed
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
