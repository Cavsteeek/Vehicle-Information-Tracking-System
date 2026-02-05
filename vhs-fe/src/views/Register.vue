<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')

const handleRegister = async () => {
    if (!name.value || !email.value || !password.value) return
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
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
        <div class="w-96 p-8 bg-white shadow-xl rounded-2xl">
            <h1 class="text-2xl font-bold mb-6 text-center text-gray-800">Join the Fleet</h1>
            <p v-if="error" class="text-red-500 text-sm mb-4 text-center font-medium">{{ error }}</p>

            <div class="space-y-4">
                <input v-model="name" @keyup.enter="handleRegister" type="text" placeholder="Full Name"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition" />

                <input v-model="email" @keyup.enter="handleRegister" type="email" placeholder="Email Address"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition" />

                <input v-model="password" @keyup.enter="handleRegister" type="password" placeholder="Password"
                    class="w-full border p-3 rounded-lg outline-none focus:ring-2 focus:ring-black transition" />

                <button @click="handleRegister"
                    class="w-full bg-black text-white p-3 rounded-lg font-bold hover:bg-gray-800 transition shadow-lg active:scale-95">
                    Create Account
                </button>
            </div>

            <p class="mt-6 text-center text-sm text-gray-600">
                Already have an account?
                <router-link to="/login" class="text-black font-bold underline ml-1">Sign In</router-link>
            </p>
        </div>
    </div>
</template>