<script setup>
import { ref, reactive } from 'vue'
import api from '../api/http'

const emit = defineEmits(['close', 'refresh'])

const loading = ref(false)
const error = ref('')

// The form structure matching your Backend VehicleCreate schema
const form = reactive({
    registration_number: '',
    type: 'Truck', // Default
    owner: '',
    purchase_date: new Date().toISOString().split('T')[0],
    remark: '',
    documents: [
        { document_type: 'Insurance', expiry_date: '', reminder_start_days: 21 },
        { document_type: 'Road Worthiness', expiry_date: '', reminder_start_days: 21 }
    ]
})

const addDocumentRow = () => {
    form.documents.push({ document_type: '', expiry_date: '', reminder_start_days: 21 })
}

const removeDocumentRow = (index) => {
    form.documents.splice(index, 1)
}

const handleSubmit = async () => {
    loading.value = true
    error.value = ''
    try {
        await api.post('/vehicles/', form)
        emit('refresh')
        emit('close')
    } catch (err) {
        error.value = err.response?.data?.detail || "Failed to create vehicle"
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="emit('close')"></div>

        <div
            class="relative bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
            <div class="p-8 max-h-[90vh] overflow-y-auto">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-black text-gray-800">Register Vehicle</h2>
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
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="space-y-1">
                            <label class="text-xs font-black uppercase text-gray-500 ml-1">Reg Number</label>
                            <input v-model="form.registration_number" required placeholder="ABC-123-XY"
                                class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                        </div>
                        <div class="space-y-1">
                            <label class="text-xs font-black uppercase text-gray-500 ml-1">Vehicle Type</label>
                            <select v-model="form.type"
                                class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black bg-white">
                                <option>Truck</option>
                                <option>Van</option>
                                <option>Car</option>
                                <option>Motorcycle</option>
                            </select>
                        </div>
                        <div class="space-y-1">
                            <label class="text-xs font-black uppercase text-gray-500 ml-1">Owner Name</label>
                            <input v-model="form.owner" required placeholder="John Doe"
                                class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                        </div>
                        <div class="space-y-1">
                            <label class="text-xs font-black uppercase text-gray-500 ml-1">Purchase Date</label>
                            <input v-model="form.purchase_date" type="date"
                                class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition" />
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between items-center mb-3">
                            <label class="text-xs font-black uppercase text-gray-500 ml-1">Documents & Expiries</label>
                            <button type="button" @click="addDocumentRow"
                                class="text-xs font-black text-blue-600 hover:underline">+ Add More</button>
                        </div>
                        <div class="space-y-3">
                            <div v-for="(doc, index) in form.documents" :key="index"
                                class="flex gap-2 items-center bg-gray-50 p-3 rounded-2xl">
                                <input v-model="doc.document_type" placeholder="Doc Type"
                                    class="flex-1 bg-transparent border-b border-gray-300 outline-none focus:border-black py-1 text-sm font-bold" />
                                <input v-model="doc.expiry_date" type="date" required
                                    class="bg-transparent border-b border-gray-300 outline-none focus:border-black py-1 text-sm font-bold" />
                                <button v-if="form.documents.length > 1" type="button" @click="removeDocumentRow(index)"
                                    class="text-red-400 hover:text-red-600">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                                        fill="currentColor">
                                        <path fill-rule="evenodd"
                                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                            clip-rule="evenodd" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>

                    <button type="submit" :disabled="loading"
                        class="w-full bg-black text-white p-4 rounded-2xl font-black hover:bg-gray-800 transition shadow-xl active:scale-95 disabled:bg-gray-400">
                        {{ loading ? 'Registering...' : 'Register Vehicle' }}
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>