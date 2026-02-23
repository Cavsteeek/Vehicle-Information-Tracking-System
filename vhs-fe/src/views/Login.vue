<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false) // Spinner state

const handleLogin = async () => {
    if (!email.value || !password.value) return

    error.value = ''
    loading.value = true // Start spinner

    try {
        const res = await api.post('/auth/login', {
            email: email.value,
            password: password.value,
        })
        localStorage.setItem('token', res.data.access_token)
        router.push('/dashboard')
    } catch (err) {
        // Capture the specific error from FastAPI (401 vs 403)
        if (err.response && err.response.data && err.response.data.detail) {
            error.value = err.response.data.detail
        } else {
            error.value = 'An unexpected error occurred. Please try again.'
        }
    } finally {
        loading.value = false // Stop spinner
    }
}
</script>

<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="w-96 p-8 bg-white shadow-xl rounded-2xl">
            <h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Login</h1>

            <p v-if="error"
                class="text-red-500 text-sm mb-4 text-center font-medium bg-red-50 p-2 rounded border border-red-200">
                {{ error }}
            </p>

            <form @submit.prevent="handleLogin" class="space-y-4">
                <input v-model="email" name="email" type="email" autocomplete="email" placeholder="Email"
                    :disabled="loading"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition disabled:bg-gray-50 disabled:cursor-not-allowed" />

                <input v-model="password" name="password" type="password" autocomplete="current-password"
                    placeholder="Password" :disabled="loading"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition disabled:bg-gray-50 disabled:cursor-not-allowed" />

                <button type="submit" :disabled="loading"
                    class="w-full bg-black text-white p-3 rounded-lg font-bold hover:bg-gray-800 transition shadow-lg active:scale-95 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center">

                    <svg v-if="loading" class="animate-spin h-5 w-5 text-white mr-2" xmlns="http://www.w3.org/2000/svg"
                        fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                        </circle>
                        <path class="opacity-75" fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                        </path>
                    </svg>

                    <span>{{ loading ? 'Signing in...' : 'Sign In' }}</span>

                </button>
            </form>

            <p class="mt-6 text-center text-sm text-gray-600">
                New here?
                <router-link to="/register" class="text-black font-bold underline ml-1">Create an account</router-link>
            </p>
        </div>
    </div>
</template>
