<script setup>
import { ref } from 'vue'
import { useToast } from '../composables/useToast'
import api from '../api/http'

const props = defineProps({
    vessel: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['close', 'refresh'])
const { error: showError } = useToast()

const title = ref('')
const expiry_date = ref('')
const issued_date = ref('')
const loading = ref(false)
const error = ref('')

const submit = async () => {
    if (!title.value || !expiry_date.value) {
        error.value = 'Title and expiry date are required'
        showError('Title and expiry date are required')
        return
    }

    loading.value = true
    error.value = ''
    try {
        await api.post('/vessel-docs/', {
            vessel_id: props.vessel.id,
            title: title.value,
            expiry_date: expiry_date.value,
            issued_date: issued_date.value || null
        })
        emit('refresh')
        emit('close')
    } catch (err) {
        const errorMsg = err.response?.data?.detail || 'Error creating document'
        error.value = errorMsg
        showError(errorMsg)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="emit('close')"></div>
        <div class="relative bg-white w-full max-w-md rounded-3xl shadow-2xl p-8">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-black text-gray-800">Add Vessel Document</h2>
                <button @click="emit('close')" class="text-gray-400 hover:text-black">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <p v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm font-bold">{{ error }}</p>
            <form @submit.prevent="submit" class="space-y-4">
                <div>
                    <label class="text-xs font-black uppercase text-gray-500 ml-1">Title</label>
                    <input v-model="title" required
                        class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                </div>
                <div>
                    <label class="text-xs font-black uppercase text-gray-500 ml-1">Expiry Date</label>
                    <input v-model="expiry_date" type="date" required
                        class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                </div>
                <div>
                    <label class="text-xs font-black uppercase text-gray-500 ml-1">Issued Date</label>
                    <input v-model="issued_date" type="date"
                        class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                </div>
                <button type="submit" :disabled="loading"
                    class="w-full bg-black text-white p-3 rounded-xl font-bold hover:bg-gray-800 transition">{{ loading
                        ? 'Saving...' : 'Save Document' }}</button>
            </form>
        </div>
    </div>
</template>
