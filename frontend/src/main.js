import { createApp } from 'vue'
import App from './App.vue'

// Router
import router from './router'

// MDI icons
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader


// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },
    styles: {
        configFile: 'src/styles/settings.scss',
    }
})

// Pinia
import { createPinia } from 'pinia'
const pinia = createPinia()

const app = createApp(App)

app.use(router)

app.use(vuetify)

app.use(pinia)

app.mount('#app')
