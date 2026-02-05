<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = () => {
    // 1. Clear the session
    localStorage.removeItem('token')

    // 2. Redirect to login
    // The router.beforeEach guard in your router.js will now 
    // block access to /dashboard because the token is gone.
    router.push('/login')
}
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <nav class="bg-white shadow-sm px-8 py-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-gray-800">VPMS</h1>

            <button @click="handleLogout"
                class="flex items-center gap-2 text-gray-600 hover:text-red-600 font-medium transition">
                <span>Logout</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
            </button>
        </nav>

        <main class="max-w-7xl mx-auto py-12 px-4">
            <div class="text-center mb-12">
                <p class="text-gray-500 max-w-2xl mx-auto">

                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            </div>
        </main>
    </div>
</template>