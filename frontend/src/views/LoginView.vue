<script setup>
import { computed, ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import { useLoadingStore } from "@/stores/loading.js";
import { storeToRefs } from "pinia";
import * as EmailValidator from 'email-validator';

const userStore = useUserStore();
const loadingStore = useLoadingStore();
const { loading } = storeToRefs(loadingStore);
const { startLoading, stopLoading } = loadingStore;

const INITIALLOGINSTATE = 1000;
const FORGOTPASSWORDSTATE = 1002;
const FORGOTPASSWORDEMAILSENTSTATE = 1005;
const REGISTERSTATE = 1006;

const state = ref(INITIALLOGINSTATE);
const router = useRouter();
const route = useRoute();

const username = ref("");
const password = ref("");
const rememberMe = ref(false);
const firstName = ref("");
const lastName = ref("");
const register = async () => {
  startLoading();

  if (!firstName.value || !lastName.value) {
    error.value = "First and last name are required";
    stopLoading();
    return;
  }

  if (!EmailValidator.validate(username.value)) {
    error.value = "Invalid email address";
    stopLoading();
    return;
  }

  if (!password.value) {
    error.value = "Password is required";
    stopLoading();
    return;
  }

  try {
    await userStore.registerAccount(firstName.value, lastName.value, username.value, password.value);
    await router.push("/");
  } catch (e) {
    error.value = e.message;
  }

  stopLoading();
};

const error = ref("");
const info = ref("");

const readQueryParams = () => {
  if (route.query.passwordReset) {
    info.value = "Please log in with your new password.";
  }
  router.replace({ query: {} });
};

const login = async () => {
  startLoading();

  if (!EmailValidator.validate(username.value)) {
    error.value = "Invalid email address";
    stopLoading();
    return;
  }
  if (!password.value) {
    error.value = "Password is required";
    stopLoading();
    return;
  }

  try {
    await userStore.logInEmailPassword(username.value, password.value, rememberMe.value);
    await router.push("/");
  } catch (e) {
    error.value = e.message;
  }

  stopLoading();
};

const resetPassword = async () => {
  startLoading();
  try {
    if (!EmailValidator.validate(username.value)) {
      error.value = "Invalid email address";
      stopLoading();
      return;
    }
    await userStore.sendPasswordResetEmail(username.value);
    state.value = FORGOTPASSWORDEMAILSENTSTATE;
  } catch (e) {
    error.value = e.message;
  }
  stopLoading();
};

const currentYear = computed(() => new Date().getFullYear());
const copyrightName = computed(() => import.meta.env.VITE_COPYRIGHT_NAME);

const title = computed(() => {
  switch (state.value) {
    case INITIALLOGINSTATE: return "Log In";
    case FORGOTPASSWORDSTATE: return "Forgot Password";
  }
});

watch(state, () => {
  error.value = "";
  info.value = "";
});

readQueryParams();
</script>

<template>
  <div class="background-div">
    <v-container class="w-100 d-flex h-auto justify-center align-content-center align-center">
      <v-card max-width="600px" min-width="350px" class="pa-2 curved-corner-v-card" style="background-color: rgba(255, 255, 255, 0.95);">
        <v-card-title class="text-center">{{ title }}</v-card-title>

        <v-alert v-if="error" type="error">{{ error }}</v-alert>
        <v-spacer v-if="error" class="mt-2 mb-4" />

        <v-alert v-if="info" type="info">{{ info }}</v-alert>
        <v-spacer v-if="info" class="mt-2 mb-4" />

        <template v-if="state === INITIALLOGINSTATE">
          <v-form @submit.prevent="login">
            <p class="text-center mb-5">Please login to access STEManager.</p>
            <v-text-field
                v-model="username"
                label="Email"
                required
                autocomplete="username"
            />
            <v-text-field
                v-model="password"
                label="Password"
                required
                type="password"
                autocomplete="current-password"
            />
            <v-checkbox v-model="rememberMe" label="Stay Logged In">
              <v-tooltip activator="parent" location="bottom">
                Not recommended on shared computers.
              </v-tooltip>
            </v-checkbox>
            <div class="d-flex align-center justify-center w-100">
              <v-btn
                  type="submit"
                  :disabled="loading || !username || !password"
                  class="w-50"
              >
                Login
              </v-btn>
            </div>
            <div class="d-flex align-center justify-center w-100">
              <v-btn
                  @click="state = FORGOTPASSWORDSTATE"
                  class="mt-2 w-66"
                  size="small"
                  variant="tonal"
              >
                Forgot Password?
              </v-btn>
            </div>
            <div class="d-flex align-center justify-center w-100">
              <v-btn
                  @click="state = REGISTERSTATE"
                  class="mt-2 w-66"
                  size="small"
                  variant="tonal"
              >
                Create an Account
              </v-btn>
            </div>
            <p class="copyright-text text-center mt-4">
              &copy; 2023-{{ currentYear }} {{ copyrightName }}. All rights reserved.
            </p>
          </v-form>
        </template>
        <template v-else-if="state === REGISTERSTATE">
          <v-form @submit.prevent="register">
            <p class="text-center mb-5">Create a new account to access STEManager.</p>
            <v-text-field
                v-model="firstName"
                label="First Name"
                required
                autocomplete="given-name"
            />
            <v-text-field
                v-model="lastName"
                label="Last Name"
                required
                autocomplete="family-name"
            />
            <v-text-field
                v-model="username"
                label="Email"
                required
                autocomplete="email"
            />
            <v-text-field
                v-model="password"
                label="Password"
                required
                type="password"
                autocomplete="new-password"
            />
            <div class="d-flex align-center justify-center w-100">
              <v-btn
                  type="submit"
                  :disabled="loading || !firstName || !lastName || !username || !password"
                  class="w-50"
              >
                Register
              </v-btn>
            </div>
            <div class="d-flex align-center justify-center w-100">
              <v-btn
                  @click="state = INITIALLOGINSTATE"
                  class="mt-2 w-66"
                  size="small"
                  variant="tonal"
              >
                Back to Login
              </v-btn>
            </div>
            <p class="copyright-text text-center mt-4">
              &copy; 2024-{{ currentYear }} {{ copyrightName }}. All rights reserved.
            </p>
          </v-form>
        </template>

        <template v-else-if="state === FORGOTPASSWORDSTATE">
          <v-form>
            <p class="text-center mx-2">
              Forgot your password? Enter your email below and we'll send a reset link.
            </p>
            <v-text-field
                v-model="username"
                label="Email"
                required
                autocomplete="username"
            />
            <div class="d-flex justify-center">
              <v-btn @click="resetPassword">Send Reset Email</v-btn>
            </div>
            <p class="copyright-text text-center mt-4">
              &copy; 2023-{{ currentYear }} {{ copyrightName }}. All rights reserved.
            </p>
          </v-form>
        </template>

        <template v-else-if="state === FORGOTPASSWORDEMAILSENTSTATE">
          <v-form>
            <v-alert type="info">
              If that email matches our records, a reset link was sent.
            </v-alert>
            <v-spacer class="my-4" />
            <div class="d-flex justify-center">
              <v-btn @click="state = INITIALLOGINSTATE">Back to Login</v-btn>
            </div>
            <p class="copyright-text text-center mt-4">
              &copy; 2024-{{ currentYear }} {{ copyrightName }}. All rights reserved.
            </p>
          </v-form>
        </template>
      </v-card>
    </v-container>
  </div>
</template>

<style scoped>
.curved-corner-v-card {
  border-radius: 6px !important;
}
.background-div {
  background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/login-background.webp');
  background-size: cover;
  background-position: top;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}
.copyright-text {
  font-size: 8px;
}
</style>