import {createRouter, createWebHistory} from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import {storeToRefs} from "pinia";
import {useUserStore} from "@/stores/user.js";


// Assumes requiresAuth is true if not defined as false
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'dashboard',
            component: DashboardView,
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            meta: {requiresAuth: false},
        },
        {
            path: '/campers',
            name: 'campers',
            component: () => import('../views/CampersView.vue'),
        },
        {
            path: '/sessions',
            name: 'sessions',
            component: () => import('../views/sessionsView.vue'),
        },
        {
            path: '/families',
            name: 'families',
            component: () => import('../views/FamiliesView.vue'),
        },
        {
            path: '/notifications',
            name: 'notifications',
            component: () => import('../views/NotificationsView.vue'),
        },
        {
            path: '/registrations',
            name: 'registrations',
            component: () => import('../views/RegistrationsView.vue'),
        },
        {
            path: '/parent-registration',
            name: 'parent-registration',
            component: () => import('../views/ParentRegistrationView.vue'),
        }
    ],
})

router.beforeEach((to) => {
    const userStore = useUserStore()
    const {loggedIn} = storeToRefs(userStore)
    console.log('logged in is: ', loggedIn.value)
    if (!loggedIn.value && to.meta.requiresAuth !== false) {
        console.log('pushing to login')
        //return {name: 'login'}
    }

    return true
})

export default router
