<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
    if (!email.value || !password.value) return
    try {
        const res = await api.post('/auth/login', {
            email: email.value,
            password: password.value,
        })
        localStorage.setItem('token', res.data.access_token)
        router.push('/dashboard')
    } catch (err) {
        error.value = 'Invalid email or password'
    }
}
</script>

<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="w-96 p-8 bg-white shadow-xl rounded-2xl">
            <h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Login</h1>
            <p v-if="error" class="text-red-500 text-sm mb-4 text-center font-medium">{{ error }}</p>

            <form @submit.prevent="handleLogin" class="space-y-4">
                <input v-model="email" name="email" type="email" autocomplete="email" placeholder="Email"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition" />

                <input v-model="password" name="password" type="password" autocomplete="current-password"
                    placeholder="Password"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition" />

                <button type="submit"
                    class="w-full bg-black text-white p-3 rounded-lg font-bold hover:bg-gray-800 transition shadow-lg active:scale-95">
                    Sign In
                </button>
            </form>

            <p class="mt-6 text-center text-sm text-gray-600">
                New here?
                <router-link to="/register" class="text-black font-bold underline ml-1">Create an account</router-link>
            </p>
        </div>
    </div>
</template>