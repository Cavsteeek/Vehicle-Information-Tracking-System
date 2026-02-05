<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'

const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
    try {
        const res = await api.post('/auth/login', {
            email: email.value,
            password: password.value,
        })

        localStorage.setItem('token', res.data.access_token)
        router.push('/dashboard')
    } catch (err) {
        error.value = 'Invalid credentials'
    }
}
</script>

<template>
    <div class="min-h-screen flex items-center justify-center">
        <div class="w-96 p-6 border rounded">
            <h1 class="text-2xl font-bold mb-4">Login</h1>

            <p v-if="error" class="text-red-500 mb-2">{{ error }}</p>

            <input v-model="email" type="email" placeholder="Email" class="w-full border p-2 mb-3" />

            <input v-model="password" type="password" placeholder="Password" class="w-full border p-2 mb-4" />

            <button @click="login" class="w-full bg-black text-white p-2">
                Login
            </button>

            <p class="mt-4 text-sm">
                No account?
                <router-link to="/register" class="underline">Sign up</router-link>
            </p>
        </div>
    </div>
</template>
