<script setup>
const props = defineProps({
  required: {
    type: Boolean,
    default: () => false
  },
  min: {
    type: String,
    default: () => ''
  },
  max: {
    type: String,
    default: () => ''
  },
})
const model = defineModel()
const visible = defineModel('visible')
</script>

<template>
<v-dialog
  v-model="visible"
  width="auto"
  >
  <v-card max-width="400">
    <v-card-title>
      <span class="text-h5">Select Date</span>
    </v-card-title>
    <v-card-text>
      <v-date-picker
        v-model="model"
        no-title
        scrollable
        @input="visible = false"
        :required="props.required"
        :min="props.min"
        :max="props.max"
      ></v-date-picker>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="visible = false">Cancel</v-btn>
      <v-btn text @click="visible = false">OK</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
</template>

<style scoped>

</style>