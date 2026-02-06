<script setup>
const props = defineProps({
    vehicleNumber: String,
    loading: Boolean
})
const emit = defineEmits(['close', 'confirm'])
</script>

<template>
    <div class="fixed inset-0 z-[120] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="emit('close')"></div>

        <div
            class="relative bg-white w-full max-w-sm rounded-3xl shadow-2xl p-8 text-center animate-in fade-in zoom-in duration-200">
            <div class="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
            </div>

            <h2 class="text-xl font-black text-gray-900 mb-2 uppercase">Delete Vehicle?</h2>
            <p class="text-gray-500 text-sm mb-8 font-medium">
                Are you sure you want to remove <span class="text-black font-bold">{{ vehicleNumber }}</span>? This
                action cannot be undone.
            </p>

            <div class="flex gap-3">
                <button @click="emit('close')"
                    class="flex-1 bg-gray-100 text-gray-600 p-4 rounded-2xl font-black hover:bg-gray-200 transition uppercase text-xs tracking-widest">
                    Cancel
                </button>
                <button @click="emit('confirm')" :disabled="loading"
                    class="flex-1 bg-red-600 text-white p-4 rounded-2xl font-black hover:bg-red-700 transition shadow-lg shadow-red-200 uppercase text-xs tracking-widest disabled:opacity-50">
                    {{ loading ? 'Deleting...' : 'Delete' }}
                </button>
            </div>
        </div>
    </div>
</template>