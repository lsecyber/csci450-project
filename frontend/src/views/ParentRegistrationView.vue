<script setup>
import {ref} from 'vue'
import ParentRegistrationForm from "@/components/ParentRegistrationForm.vue";

const formData = ref({})

const handleSubmit = () => {
  console.log('Form submitted:', formData.value);
  // Perform any additional actions here, such as sending the data to an API
  // TODO - DO SOMETHING!
}
</script>

<template>
  <h2 class="text-center text-h2 mt-4 mb-7">Camp Registration</h2>
  <div class="d-flex flex-col align-items-center justify-center">
    <suspense>
      <template #default>
        <ParentRegistrationForm
            v-model="formData"
            style="max-width: 500px"
            @submit="handleSubmit"
        />
      </template>
      <template #fallback>
        <v-skeleton-loader type="card" style="max-width: 500px; min-width: 20rem; min-height: 400px;"/>
      </template>
    </suspense>
  </div>

</template>

<style scoped>

</style>