<script setup>
import {RouterLink, RouterView, useRoute, useRouter} from 'vue-router'
import {computed, ref} from "vue";
import {useUserStore} from "@/stores/user.js";

const navDrawerVisible = ref(false)

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const {logOut} = userStore

const linkClicked = (routeName) => {
  navDrawerVisible.value = false
  console.log('about to push: ', routeName)
  router.push({name: routeName})
}

const listItems = ref([
  { title: 'Campers', name: 'campers' },
  { title: 'Camp Sessions', name: 'sessions' },
  { title: 'Families', name: 'families' },
  { title: 'Notifications', name: 'notifications' },
  { title: 'Registrations', name: 'registrations' }
])

const showMenu = computed(() => {
  return route.name !== 'login' && route.name !== 'register' && route.name !== 'parent-registration'
})

// random number between 1 and 99
const randomNum = ref(Math.floor(Math.random() * 99) + 1)
</script>

<template>
  <v-app>
    <v-navigation-drawer v-model="navDrawerVisible" class="ps-4 me-0 pt-5 pe-4" v-if="showMenu">
      <v-list-item
          :prepend-avatar="`https://randomuser.me/api/portraits/men/${randomNum}.jpg`"
          title="Joe Smith"
          class="pb-5"
      >
        <template v-slot="subtitle">
          <v-list-item-subtitle>
            <span @click="logOut()" class="click-cursor">
              <u>Log Out</u>
            </span>
          </v-list-item-subtitle>
        </template>
      </v-list-item>
      <v-list-item title="STEManager" subtitle="Dashboard" @click="linkClicked('dashboard')" :active="route.name === 'dashboard'" />
      <template v-for="item in listItems" :key="item.title">
        <v-list-item link @click="linkClicked(item.name)" :title="item.title" :active="route.name === item.name" />
      </template>
    </v-navigation-drawer>

    <v-app-bar style="background-color: #083351;">
      <v-app-bar-nav-icon @click="navDrawerVisible = !navDrawerVisible" style="color: white;" v-if="showMenu"></v-app-bar-nav-icon>

      <v-app-bar-title style="color: white;">STEManager</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>

  </v-app>

</template>

<style scoped>
.click-cursor {
  cursor: pointer;
}
</style>
