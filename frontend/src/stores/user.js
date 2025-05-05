import {ref} from 'vue'
import {useApiCall} from "@/composables/apiCall.js";
import {defineStore} from "pinia";

export const useUserStore = defineStore('user', () => {
    const {apiGet, apiPost} = useApiCall()
    const userDetails = ref({})
    const loggedIn = ref(false)
    const loading = ref(false)
    const token = ref(null)

    const getUserDetails = async () => {
        loading.value = true
        try {
            await apiGet('/user')
            userDetails.value = apiGet.data
            loggedIn.value = true
        } catch (error) {
            console.error('Error fetching user details:', error)
        } finally {
            loading.value = false
        }
    }

    const logInEmailPassword = async (email, password, rememberMe) => {
        try {
            const response = await apiPost('/login', {email, password})
            if (rememberMe) {
                localStorage.setItem('userEmail', email)
            }
            token.value = response.token
            loggedIn.value = true
        } catch (error) {
            console.error('Error logging in:', error)
            throw error
        }
    }

    const logOut = async () => {
        try {
            await apiPost('/logout')
            loggedIn.value = false
            userDetails.value = {}
        } catch (error) {
            console.error('Error logging out:', error)
        }
    }

    const sendPasswordResetEmail = async (email) => {
        try {
            await apiPost('/password-reset', {email}) // TODO figure out if this is right
        } catch (error) {
            console.error('Error sending password reset email:', error)
        }
    }

    const registerUser = async (firstname, lastname, email, password) => {
        try {
            const response = await apiPost('/register', {firstname, lastname, email, password})
            token.value = response.token
            loggedIn.value = true
        } catch (error) {
            console.error('Error registering user:', error)
            throw error
        }
    }

    return {
        userDetails,
        loggedIn,
        loading,
        getUserDetails,
        logInEmailPassword,
        logOut,
        sendPasswordResetEmail,
        registerUser
    }
})