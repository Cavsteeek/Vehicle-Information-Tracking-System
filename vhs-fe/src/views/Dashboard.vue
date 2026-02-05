<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'

const router = useRouter()
const email = ref('')

onMounted(async () => {
    try {
        const res = await api.get('/vehicles/whoami')
        email.value = res.data.email
    } catch {
        router.push('/login')
    }
})

const logout = () => {
    localStorage.removeItem('token')
    router.push('/login')
}
</script>

<template>
    <div class="p-6">
        <h1 class="text-2xl font-bold">Dashboard</h1>
        <p class="mt-2">Logged in as: {{ email }}</p>

        <button @click="logout" class="mt-4 bg-red-600 text-white px-4 py-2">
            Logout
        </button>
    </div>
</template>
