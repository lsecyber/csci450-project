<script setup>
import {useVModel} from "@vueuse/core";
import {ref} from "vue";
import pluralize from 'pluralize';
import {useApiCall} from "@/composables/apiCall.js";
import {useLoadingStore} from "@/stores/loading.js";

import {getTableHeaders} from "@/utils/tableHeaders.js";
import {storeToRefs} from "pinia";

const props = defineProps({
  itemsPerPage: {
    type: Number,
    default: () => 10
  },
  table: {
    type: String,
    required: true
  }
})

const totalItems = ref(0)
const serverItems = ref([])
const pluralTable = ref(pluralize(props.table))

const apiCall = useApiCall()
const {apiGet, apiPost} = apiCall

const loadingStore = useLoadingStore()
const {loading} = storeToRefs(loadingStore)

const loadItems = async ({page, itemsPerPage, sortBy}) => {
  // uses api call to fetch
  // data from the server
  // and updates serverItems and totalItems
  console.log('running load items; page: ', page, ' itemsPerPage: ', itemsPerPage, ' sortBy: ', sortBy, 'itemsPerPage: ', itemsPerPage)
  const params = {
    limit: itemsPerPage,
    page: page,
  }
  if (search.value) {
    params.search = search.value
  }
  if (sortBy && sortBy.length > 0) {
    params.sortBy = sortBy.map((item) => {
      return item.key + ':' + item.order
    }).join(',')
  }

  // builds url with params
  const url = `/${pluralTable.value}?${new URLSearchParams(params).toString()}`

  const response = await apiGet(url)
  console.log('response: ', response)

  serverItems.value = response.items
  totalItems.value = response.total

}

const itemsPerPage = ref(props.itemsPerPage)


if (!itemsPerPage.value) {
  itemsPerPage.value = 10
}

const search = ref("")

const headers = getTableHeaders(pluralTable.value)
headers.value = headers.value.filter((header) => {
  return header.showInList !== false
})

console.log('headers: ', headers.value)
</script>

<template>
  <v-card class="ma-2" style="max-width: 1000px;">
    <v-row>
      <v-col cols="4">
        <v-card-title>
          <v-text-field
              v-model="search"
              class="ma-2"
              placeholder="Search"
              hide-details
              density="compact"
          />
        </v-card-title>
      </v-col>
      <v-col cols="4">
        <v-card-title class="text-center">
          {{ pluralTable[0].toUpperCase() + pluralTable.slice(1) }}
        </v-card-title>
      </v-col>
      <v-col cols="4" />
    </v-row>


    <v-data-table-server
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="serverItems"
        :items-length="totalItems"
        :loading="loading"
        :search="search"
        item-value="name"
        @update:options="loadItems"
    />

  </v-card>

</template>

<style scoped>

</style>