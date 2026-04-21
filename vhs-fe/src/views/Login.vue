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
        localStorage.setItem('role', res.data.role)

        if (res.data.role === 'admin' || res.data.role === 'logistics' || res.data.role === 'multi_dept') {
            router.push('/dashboard')
        } else if (res.data.role === 'vessel') {
            router.push('/vessel-dashboard')
        } else {
            router.push('/dashboard')
        }
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
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 px-4 py-8">
        <div class="w-full max-w-md">
            <!-- Logo/Brand Section -->
            <div class="text-center mb-8">
                <h1 class="text-3xl sm:text-4xl font-black text-gray-900 tracking-tighter">VPMS</h1>
            </div>

            <!-- Login Card -->
            <div class="bg-white shadow-xl rounded-3xl p-6 sm:p-8 border border-gray-100">


                <!-- Error Message -->
                <p v-if="error"
                    class="text-red-600 text-xs sm:text-sm mb-4 text-center font-bold bg-red-50 p-3 sm:p-4 rounded-xl border border-red-200">
                    {{ error }}
                </p>

                <!-- Form -->
                <form @submit.prevent="handleLogin" class="space-y-4">
                    <div class="space-y-2">
                        <label class="text-xs font-black uppercase text-gray-500">Email</label>
                        <input v-model="email" name="email" type="email" autocomplete="email"
                            placeholder="you@example.com" :disabled="loading"
                            class="w-full border-2 border-gray-200 p-3 rounded-xl outline-none focus:border-black focus:bg-gray-50 transition disabled:bg-gray-50 disabled:cursor-not-allowed text-sm" />
                    </div>

                    <div class="space-y-2">
                        <label class="text-xs font-black uppercase text-gray-500">Password</label>
                        <input v-model="password" name="password" type="password" autocomplete="current-password"
                            placeholder="Enter your password" :disabled="loading"
                            class="w-full border-2 border-gray-200 p-3 rounded-xl outline-none focus:border-black focus:bg-gray-50 transition disabled:bg-gray-50 disabled:cursor-not-allowed text-sm" />
                    </div>

                    <button type="submit" :disabled="loading"
                        class="w-full bg-black text-white p-3 sm:p-4 rounded-xl font-black hover:bg-gray-800 transition active:scale-95 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm sm:text-base">
                        <svg v-if="loading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                        </svg>
                        <span>{{ loading ? 'Signing in...' : 'Sign In' }}</span>
                    </button>
                </form>


            </div>
        </div>
    </div>
</template>
