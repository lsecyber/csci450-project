import {defineStore} from 'pinia'
import {ref} from 'vue'

export const useLoadingStore = defineStore('loading', () => {
    const loading = ref(false)
    const justStartedLoadingTimeout = ref(null)

    const justStartedLoading = ref(false)

    const startLoading = () => {
        clearTimeout(justStartedLoadingTimeout.value)
        loading.value = true
        justStartedLoading.value = true
        justStartedLoadingTimeout.value = setTimeout(() => {
            justStartedLoading.value = false
        }, 200)
    }

    const stopLoading = () => {
        loading.value = false
    }

    return {
        loading,
        startLoading,
        stopLoading,
        justStartedLoading
    }
})