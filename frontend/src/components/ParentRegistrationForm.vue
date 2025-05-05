<script setup>
import {computed, ref, watch, watchEffect} from "vue";
import DatePicker from "@/components/DatePicker.vue";
import * as EmailValidator from 'email-validator';
import {useApiCall} from "@/composables/apiCall.js";

const {apiGet} = useApiCall()

const model = defineModel()

const emit = defineEmits(['submit'])

await new Promise(resolve => setTimeout(resolve, 100))

const datePickerOpen = ref(false)

const displayableDoB = ref('')

const formIsValid = ref(false)

watch(model, (newModel) => {
  const childDOB = newModel.childDOB
  if (childDOB) {
    const date = new Date(childDOB)
    const options = {year: 'numeric', month: '2-digit', day: '2-digit'};
    displayableDoB.value = date.toLocaleDateString('en-US', options)
  } else {
    displayableDoB.value = ''
  }

  formIsValid.value =
      newModel.parentEmail &&
      newModel.childFirstName &&
      newModel.childLastName &&
      newModel.childDOB &&
      newModel.sessionId &&
      EmailValidator.validate(newModel.parentEmail)
  console.log('formIsValid: ', formIsValid.value, '; because: ', newModel.parentEmail, newModel.childFirstName, newModel.childLastName, newModel.childDOB)

}, {deep: true})

const today = new Date()
const dd = String(today.getDate()).padStart(2, '0')
const mm = String(today.getMonth() + 1).padStart(2, '0') // January is 0!
const yyyy = today.getFullYear()
const todayString = yyyy + '-' + mm + '-' + dd

const sessions = ref([])
const sessionsResponse = await apiGet('/sessions?limit=1000&page=1&sort_key=created_on&sort_order=desc')
sessions.value = sessionsResponse.items.map(session => {
  return {
    title: `${session.name} (${session.start_date} - ${session.end_date})`,
    value: session.id
  }
})
</script>

<template>
<v-card min-width="35vw">
  <v-card-title>Register your child for camp!</v-card-title>
  <v-card-subtitle>Fill out the form below to complete your registration.</v-card-subtitle>

  <v-card-text>
    <v-form>
      <v-text-field
          v-model="model.parentEmail"
          label="Parent/Guardian Email"
          required
          type="email"
          hint="This is used to link your registration to your family."
          persistent-hint
          class="mb-4"
      ></v-text-field>

      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
              v-model="model.childFirstName"
              label="Child's First Name"
              required
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
              v-model="model.childLastName"
              label="Child's Last Name"
              required
          ></v-text-field>
        </v-col>
      </v-row>

      <p>Child Date of Birth: {{displayableDoB}}</p>
      <v-row class="mb-4">
        <v-col cols="12">
          <v-btn @click="datePickerOpen  = !datePickerOpen">Select Child Date of Birth</v-btn>
        </v-col>
      </v-row>
      <DatePicker
          v-model="model.childDOB"
          v-model:visible="datePickerOpen"
          required
          min="1920-01-01"
          :max="todayString"
      ></DatePicker>

      <v-autocomplete
        label="Select a session"
        v-model="model.sessionId"
        :items="sessions"
      />


      <v-btn @click="emit('submit')" variant="elevated" color="primary" :disabled="!formIsValid">Submit Registration</v-btn>
    </v-form>
  </v-card-text>

</v-card>
</template>

<style scoped>

</style>