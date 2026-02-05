<script setup>
import { computed } from 'vue'

const props = defineProps({
    vehicle: {
        type: Object,
        required: true
    }
})

// Color Logic: Returns a status object for a document
const getStatus = (expiryDate, reminderDays) => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const expiry = new Date(expiryDate)

    const diffTime = expiry - today
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays < 0) return { label: 'Expired', color: 'text-red-600 bg-red-50', border: 'border-red-200' }
    if (diffDays <= reminderDays) return { label: `${diffDays} days left`, color: 'text-orange-600 bg-orange-50', border: 'border-orange-200' }
    return { label: 'Active', color: 'text-green-600 bg-green-50', border: 'border-green-200' }
}

const emit = defineEmits(['renew'])
</script>

<template>
    <div class="bg-white shadow-xl rounded-2xl p-6 border border-gray-100 flex flex-col h-full">
        <div class="mb-4">
            <h3 class="text-xl font-black text-gray-800 uppercase tracking-tight">
                {{ vehicle.registration_number }}
            </h3>
            <span class="text-xs font-bold px-2 py-1 bg-gray-100 text-gray-500 rounded uppercase">
                {{ vehicle.vehicle_type }}
            </span>
        </div>

        <div class="space-y-3 flex-grow">
            <div v-for="doc in vehicle.documents" :key="doc.id"
                class="flex items-center justify-between p-3 rounded-xl border transition hover:shadow-sm"
                :class="getStatus(doc.expiry_date, 21).border">
                <div>
                    <p class="text-sm font-bold text-gray-700">{{ doc.document_type }}</p>
                    <p class="text-xs text-gray-500">Expires: {{ doc.expiry_date }}</p>
                </div>

                <div class="flex flex-col items-end gap-2">
                    <span class="text-[10px] font-black uppercase px-2 py-0.5 rounded-full"
                        :class="getStatus(doc.expiry_date, 21).color">
                        {{ getStatus(doc.expiry_date, 21).label }}
                    </span>
                    <button @click="emit('renew', doc)"
                        class="text-[11px] font-bold underline hover:text-blue-600 transition">
                        Update
                    </button>
                </div>
            </div>
        </div>

        <div class="mt-6 pt-4 border-t border-gray-50 flex justify-between items-center">
            <div class="flex flex-col">
                <span class="text-[11px] text-gray-400 font-bold uppercase tracking-wider">Owner</span>
                <span class="text-sm text-gray-800 font-black">{{ vehicle.owner }}</span>
                <span class="text-[10px] text-gray-400 font-medium mt-1">Purchased: {{ vehicle.purchase_date || 'N/A'
                    }}</span>
            </div>

            <button class="text-gray-300 hover:text-red-500 transition self-end pb-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
            </button>
        </div>
    </div>
</template>