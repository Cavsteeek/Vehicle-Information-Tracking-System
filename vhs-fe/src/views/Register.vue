<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const register = async () => {
    try {
        await api.post('/auth/register', {
            name: name.value,
            email: email.value,
            password: password.value,
        })

        router.push('/login')
    } catch (err) {
        error.value = 'Email already registered'
    }
}
</script>

<template>
    <div class="min-h-screen flex items-center justify-center">
        <div class="w-96 p-6 border rounded">
            <h1 class="text-2xl font-bold mb-4">Sign Up</h1>

            <p v-if="error" class="text-red-500 mb-2">{{ error }}</p>

            <input v-model="name" type="text" placeholder="Full name" class="w-full border p-2 mb-3" />

            <input v-model="email" type="email" placeholder="Email" class="w-full border p-2 mb-3" />

            <input v-model="password" type="password" placeholder="Password" class="w-full border p-2 mb-4" />

            <button @click="register" class="w-full bg-black text-white p-2">
                Create account
            </button>

            <p class="mt-4 text-sm">
                Already have an account?
                <router-link to="/login" class="underline">Login</router-link>
            </p>
        </div>
    </div>
</template>
