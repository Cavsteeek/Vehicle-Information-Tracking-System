<script setup>
import { ref, reactive } from 'vue'
import api from '../api/http'

const emit = defineEmits(['close', 'refresh'])

const loading = ref(false)
const error = ref('')

const form = reactive({
    name: '',
    description: ''
})

const handleSubmit = async () => {
    loading.value = true
    error.value = ''
    try {
        await api.post('/vessel-docs/vessels', form)
        emit('refresh')
        emit('close')
    } catch (err) {
        const detail = err.response?.data?.detail
        error.value = Array.isArray(detail) ? detail[0].msg : detail || "Error"
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="emit('close')"></div>

        <div
            class="relative bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
            <div class="p-8">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-black text-gray-800">Register Vessel</h2>
                    <button @click="emit('close')" class="text-gray-400 hover:text-black">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <p v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm font-bold">{{ error }}</p>

                <form @submit.prevent="handleSubmit" class="space-y-6">
                    <div class="space-y-1">
                        <label class="text-xs font-black uppercase text-gray-500 ml-1">Vessel Name</label>
                        <input v-model="form.name" required placeholder="e.g. MV Ocean Star"
                            class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                    </div>
                    <div class="space-y-1">
                        <label class="text-xs font-black uppercase text-gray-500 ml-1">Description (Optional)</label>
                        <textarea v-model="form.description" placeholder="Brief description..."
                            class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition resize-none"
                            rows="3"></textarea>
                    </div>

                    <button type="submit" :disabled="loading"
                        class="w-full bg-black text-white py-3 rounded-xl font-black hover:bg-gray-800 transition disabled:opacity-50">
                        <span v-if="loading">Registering...</span>
                        <span v-else>Register Vessel</span>
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>