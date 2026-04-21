<script setup>
import { ref, reactive, watch } from 'vue'
import { useToast } from '../composables/useToast'
import api from '../api/http'

const emit = defineEmits(['close', 'refresh'])
const { error: showError } = useToast()

const loading = ref(false)
const error = ref('')
const step = ref(1) // Step 1: Basic info, Step 2: Documents

const presetType = ref('Truck')

const form = reactive({
    registration_number: '',
    type: '',
    owner: '',
    purchase_date: new Date().toISOString().split('T')[0],
    remark: '',
    documents: []
})

// Document Presets
const truckDocs = [
    'Vehicle License', 'Motor Vehicle Info Cert (CMRIS)', 'Proof of Ownership', 'Road Worthiness',
    'Hackney Carriage', 'Carrier Permit', 'Insurance (Genuine)'
]
const carDocs = [
    'Vehicle License', 'Motor Vehicle Info Cert (CMRIS)', 'Proof of Ownership', 'Road Worthiness',
    'Insurance (Genuine)',
]

// Function to apply presets
const applyPreset = (type) => {
    const docList = type === 'Truck' || type === 'Bus' ? truckDocs : carDocs
    form.documents = docList.map(name => ({
        document_type: name,
        expiry_date: '',
        reminder_start_days: 21
    }))
}

// Watch for preset changes to update the doc list automatically
watch(presetType, (newType) => {
    applyPreset(newType)
}, { immediate: true })

const canProceed = () => {
    return form.registration_number && form.type && form.owner
}

const canSubmit = () => {
    return form.documents.every(d => d.document_type && d.expiry_date)
}

const addDocumentRow = () => {
    form.documents.push({ document_type: '', expiry_date: '', reminder_start_days: 21 })
}

const removeDocumentRow = (index) => {
    form.documents.splice(index, 1)
}

const handleSubmit = async () => {
    if (!canSubmit()) return

    loading.value = true
    error.value = ''
    try {
        const payload = {
            ...form,
            purchase_date: form.purchase_date ? form.purchase_date : null
        }

        await api.post('/vehicles/', payload)
        emit('refresh')
        emit('close')
    } catch (err) {
        const detail = err.response?.data?.detail
        const errorMsg = Array.isArray(detail) ? detail[0].msg : detail || "Error"
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

        <div
            class="relative bg-white w-full max-w-2xl rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
            <!-- Header -->
            <div class="bg-gradient-to-r from-gray-900 to-gray-800 px-6 sm:px-8 py-6 flex justify-between items-center">
                <div>
                    <h2 class="text-xl sm:text-2xl font-black text-white">Register Vehicle</h2>
                    <p class="text-xs sm:text-sm text-gray-400 mt-1">Step {{ step }} of 2</p>
                </div>
                <button @click="emit('close')" class="text-gray-400 hover:text-white transition">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Progress bar -->
            <div class="h-1 bg-gray-200">
                <div class="h-full bg-black transition-all" :style="{ width: step === 1 ? '50%' : '100%' }"></div>
            </div>

            <!-- Content -->
            <div class="p-6 sm:p-8 max-h-[calc(90vh-180px)] overflow-y-auto">
                <p v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm font-bold">{{ error }}</p>

                <!-- STEP 1: Vehicle Info -->
                <div v-show="step === 1" class="space-y-6">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="space-y-2">
                            <label class="text-xs font-black uppercase text-gray-500">Reg Number *</label>
                            <input v-model="form.registration_number" required placeholder="ABC-123-XY"
                                class="w-full border-2 border-gray-200 p-3 rounded-xl outline-none focus:border-black focus:bg-gray-50 transition text-sm" />
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs font-black uppercase text-gray-500">Vehicle Type *</label>
                            <input v-model="form.type" required placeholder="e.g. Mack Titan 2024"
                                class="w-full border-2 border-gray-200 p-3 rounded-xl outline-none focus:border-black focus:bg-gray-50 transition text-sm" />
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs font-black uppercase text-gray-500">Owner Name *</label>
                            <input v-model="form.owner" required placeholder="John Doe"
                                class="w-full border-2 border-gray-200 p-3 rounded-xl outline-none focus:border-black focus:bg-gray-50 transition text-sm" />
                        </div>
                        <div class="space-y-2">
                            <label class="text-xs font-black uppercase text-gray-500">Purchase Date</label>
                            <input v-model="form.purchase_date" type="date"
                                class="w-full border-2 border-gray-200 p-3 rounded-xl outline-none focus:border-black focus:bg-gray-50 transition text-sm" />
                        </div>
                    </div>
                </div>

                <!-- STEP 2: Documents & Expiries -->
                <div v-show="step === 2" class="space-y-4">
                    <div class="bg-black/5 p-4 rounded-2xl border border-gray-200">
                        <label class="text-xs font-black uppercase text-gray-500 block mb-3">Vehicle Type
                            Template</label>
                        <div class="flex flex-wrap gap-2">
                            <label v-for="t in ['Truck', 'Car', 'Bus']" :key="t"
                                class="flex items-center gap-2 cursor-pointer px-3 py-2 rounded-lg transition"
                                :class="presetType === t ? 'bg-black text-white' : 'bg-white hover:bg-gray-100'">
                                <input type="radio" v-model="presetType" :value="t" class="accent-black" />
                                <span class="text-sm font-bold">{{ t }}</span>
                            </label>
                        </div>
                    </div>

                    <div class="space-y-3">
                        <div class="flex justify-between items-center">
                            <label class="text-xs font-black uppercase text-gray-500">Documents</label>
                            <button type="button" @click="addDocumentRow"
                                class="text-xs font-black text-blue-600 hover:underline">
                                + Add Custom
                            </button>
                        </div>
                        <div class="space-y-2 max-h-80 overflow-y-auto">
                            <div v-for="(doc, index) in form.documents" :key="index"
                                class="flex gap-2 items-center bg-gray-50 p-3 rounded-xl border border-gray-200 hover:border-gray-300 transition">
                                <input v-model="doc.document_type" placeholder="Doc Type" required
                                    class="flex-1 bg-transparent outline-none focus:font-bold text-sm py-1 min-w-0" />
                                <input v-model="doc.expiry_date" type="date" required
                                    class="bg-transparent outline-none text-sm py-1 w-32" />
                                <button type="button" @click="removeDocumentRow(index)"
                                    class="text-gray-300 hover:text-red-500 transition flex-shrink-0">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20"
                                        fill="currentColor">
                                        <path fill-rule="evenodd"
                                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                            clip-rule="evenodd" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="bg-gray-50 px-6 sm:px-8 py-4 border-t border-gray-200 flex gap-3 justify-end">
                <button @click="emit('close')"
                    class="px-4 py-2 text-sm font-bold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100 transition">
                    Cancel
                </button>
                <button v-if="step === 2" @click="step = 1"
                    class="px-4 py-2 text-sm font-bold text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition">
                    Back
                </button>
                <button v-if="step === 1" @click="step = 2" :disabled="!canProceed()"
                    class="px-4 py-2 text-sm font-bold text-white bg-black rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition">
                    Next
                </button>
                <button v-if="step === 2" @click="handleSubmit" :disabled="loading || !canSubmit()"
                    class="px-4 py-2 text-sm font-bold text-white bg-black rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition">
                    {{ loading ? 'Registering...' : 'Register' }}
                </button>
            </div>
        </div>
    </div>
</template>