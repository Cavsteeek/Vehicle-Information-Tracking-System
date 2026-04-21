import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export const useToast = () => {
    const addToast = (message, type = 'info', duration = 3000) => {
        const id = ++toastId
        const toast = {
            id,
            message,
            type // 'success', 'error', 'info', 'warning'
        }
        toasts.value.push(toast)

        if (duration > 0) {
            setTimeout(() => {
                removeToast(id)
            }, duration)
        }

        return id
    }

    const removeToast = (id) => {
        const index = toasts.value.findIndex(t => t.id === id)
        if (index > -1) {
            toasts.value.splice(index, 1)
        }
    }

    const success = (message, duration = 3000) => addToast(message, 'success', duration)
    const error = (message, duration = 4000) => addToast(message, 'error', duration)
    const info = (message, duration = 3000) => addToast(message, 'info', duration)
    const warning = (message, duration = 3500) => addToast(message, 'warning', duration)

    return {
        toasts,
        addToast,
        removeToast,
        success,
        error,
        info,
        warning
    }
}
