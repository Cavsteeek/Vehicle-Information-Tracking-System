import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import VesselDashboard from '../views/VesselDashboard.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/dashboard',
        component: Dashboard,
        meta: { requiresAuth: true, allowedRoles: ['logistics', 'admin', 'multi_dept'] }
    },
    {
        path: '/vessel-dashboard',
        component: VesselDashboard,
        meta: { requiresAuth: true, allowedRoles: ['vessel', 'admin', 'multi_dept'] }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Enhanced auth guard with role checking
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    const userRole = localStorage.getItem('role')

    // If route requires auth and no token, redirect to login
    if (to.meta.requiresAuth && !token) {
        next('/login')
        return
    }

    // If route has allowed roles and user role is not in the list, redirect to appropriate dashboard
    if (to.meta.allowedRoles && !to.meta.allowedRoles.includes(userRole)) {
        if (userRole === 'vessel') {
            next('/vessel-dashboard')
        } else if (['logistics', 'admin', 'multi_dept'].includes(userRole)) {
            next('/dashboard')
        } else {
            next('/login')
        }
        return
    }

    next()
})

export default router
