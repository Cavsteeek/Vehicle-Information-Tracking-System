<script setup>
import { ref } from 'vue'
import api from '../api/http'

const props = defineProps({
    doc: Object // The document we are updating
})

const emit = defineEmits(['close', 'refresh'])

const newDate = ref(props.doc?.expiry_date || '')
const loading = ref(false)

const handleUpdate = async () => {
    loading.value = true
    try {
        await api.put(`/vehicles/documents/${props.doc.id}`, {
            new_expiry_date: newDate.value
        })
        emit('refresh')
        emit('close')
    } catch (err) {
        alert("Update failed")
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="fixed inset-0 z-[110] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="emit('close')"></div>

        <div class="relative bg-white w-full max-w-sm rounded-3xl shadow-2xl p-8">
            <h2 class="text-xl font-black mb-2 uppercase tracking-tight">Update Expiry</h2>
            <p class="text-gray-500 text-sm mb-6 font-medium">{{ doc.document_type }}</p>

            <div class="space-y-4">
                <div class="space-y-1">
                    <label class="text-[10px] font-black uppercase text-gray-400 ml-1">New Expiry Date</label>
                    <input v-model="newDate" type="date"
                        class="w-full border-2 border-gray-100 p-3 rounded-xl outline-none focus:border-black transition font-bold" />
                </div>

                <div class="flex gap-3">
                    <button @click="emit('close')"
                        class="flex-1 bg-gray-100 text-gray-600 p-3 rounded-xl font-bold hover:bg-gray-200 transition">
                        Cancel
                    </button>
                    <button @click="handleUpdate" :disabled="loading"
                        class="flex-1 bg-black text-white p-3 rounded-xl font-bold hover:bg-gray-800 transition shadow-lg">
                        {{ loading ? 'Saving...' : 'Save' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>