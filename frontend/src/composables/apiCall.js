import {ref} from 'vue';
import {useLoadingStore} from "@/stores/loading.js";

export function useApiCall() {
    const data = ref(null);
    const error = ref(null);

    const loadingStore = useLoadingStore();
    const {startLoading, stopLoading} = loadingStore;

    const baseUrl = import.meta.env.VITE_API_URL;

    /*
    * Fetches data from the API.
    * @param {string} url The URL to fetch. Start with /, don't include base url.
    * @param {object} options The options to pass to the fetch function.
    * @param {boolean} triggerLoading Whether to trigger loading state.
    * @return {Promise<void>}
     */
    const apiGet = async (url, options = {}, triggerLoading=true) => {
        if (triggerLoading) {
            startLoading()
        }
        error.value = null;

        let returnThis;

        try {
            console.log('about to fetch: ', baseUrl + url)
            const response = await fetch(baseUrl + url, { ...options, method: 'GET' });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            data.value = await response.json();

            // return the data without the created_at and updated_at fields
            if (data.value.items) {
                data.value.items = data.value.items.map(item => {
                    const {created_at, updated_at, ...rest} = item;
                    return rest;
                });
            }

            // take any date fields that are in the format "0000-00-00" and convert to MM/DD/YYYY
            if (data.value.items) {
                data.value.items = data.value.items.map(item => {
                    const newItem = {...item};
                    for (const key in newItem) {
                        if (newItem[key] && typeof newItem[key] === 'string' && newItem[key].match(/^\d{4}-\d{2}-\d{2}$/)) {
                            const date = new Date(newItem[key]);
                            newItem[key] = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
                        }
                    }
                    return newItem;
                });
            }

            returnThis = data.value;
        } catch (err) {
            error.value = err.message;
            returnThis = error.value;
        } finally {
            if (triggerLoading) {
                stopLoading()
            }
        }

        return returnThis
    };

    /*
    * Posts data to the API.
    * @param {string} url The URL to post to. Start with /, don't include base url.
    * @param {object} payload The data to post.
    * @param {object} options The options to pass to the fetch function.
    * @param {boolean} triggerLoading Whether to trigger loading state.
    * @return {Promise<void>}
     */
    const apiPost = async (url, payload, options = {}, triggerLoading=true) => {
        if (triggerLoading) {
            startLoading()
        }
        error.value = null;
        let returnThis;

        try {
            const response = await fetch(baseUrl + url, {
                ...options,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            data.value = await response.json();
            returnThis = data.value;
        } catch (err) {
            error.value = err.message;
            returnThis = error.value;
        } finally {
            if (triggerLoading) {
                stopLoading()
            }
        }

        return returnThis
    };

    return {apiGet, apiPost};
}