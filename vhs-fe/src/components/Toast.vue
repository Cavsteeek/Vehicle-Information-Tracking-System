<script setup>
import { useToast } from '../composables/useToast'

const { toasts, removeToast } = useToast()

const getToastClasses = (type) => {
    const baseClasses = 'px-4 sm:px-6 py-3 sm:py-4 rounded-lg font-bold text-sm sm:text-base shadow-lg flex items-center justify-between gap-3 animate-in fade-in slide-in-from-top-4 duration-300'

    switch (type) {
        case 'success':
            return `${baseClasses} bg-green-500 text-white`
        case 'error':
            return `${baseClasses} bg-red-500 text-white`
        case 'warning':
            return `${baseClasses} bg-yellow-500 text-white`
        case 'info':
            return `${baseClasses} bg-blue-500 text-white`
        default:
            return `${baseClasses} bg-gray-800 text-white`
    }
}

const getIcon = (type) => {
    switch (type) {
        case 'success':
            return '✓'
        case 'error':
            return '✕'
        case 'warning':
            return '⚠'
        case 'info':
            return 'ℹ'
        default:
            return '•'
    }
}
</script>

<template>
    <div class="fixed top-4 right-4 z-[9999] space-y-2 pointer-events-none">
        <transition-group name="toast" tag="div">
            <div v-for="toast in toasts" :key="toast.id" :class="getToastClasses(toast.type)"
                class="pointer-events-auto">
                <div class="flex items-center gap-3">
                    <span class="text-lg font-black">{{ getIcon(toast.type) }}</span>
                    <span>{{ toast.message }}</span>
                </div>
                <button @click="removeToast(toast.id)" class="hover:opacity-70 transition ml-2 flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd"
                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                            clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
        </transition-group>
    </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
    transition: all 0.3s ease;
}

.toast-enter-from {
    transform: translateX(30px);
    opacity: 0;
}

.toast-leave-to {
    transform: translateX(30px);
    opacity: 0;
}
</style>
