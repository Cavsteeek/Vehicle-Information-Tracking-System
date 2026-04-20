<script setup>
import { ref, reactive } from 'vue'
import api from '../api/http'

const emit = defineEmits(['close', 'refresh'])

const loading = ref(false)
const error = ref('')

const form = reactive({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'logistics'
})

const roles = [
    { value: 'logistics', label: 'Logistics Department' },
    { value: 'vessel', label: 'Vessel Department' },
    { value: 'multi_dept', label: 'Multi-Department (Both Dashboards)' },
    { value: 'admin', label: 'Administrator' }
]

const handleSubmit = async () => {
    error.value = ''

    // Validation
    if (!form.name.trim()) {
        error.value = 'Name is required'
        return
    }
    if (!form.email.trim()) {
        error.value = 'Email is required'
        return
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        error.value = 'Invalid email format'
        return
    }
    if (!form.password) {
        error.value = 'Password is required'
        return
    }
    if (form.password.length < 6) {
        error.value = 'Password must be at least 6 characters'
        return
    }
    if (form.password !== form.confirmPassword) {
        error.value = 'Passwords do not match'
        return
    }

    loading.value = true
    try {
        await api.post('/auth/users/create', {
            name: form.name,
            email: form.email,
            password: form.password,
            role: form.role
        })
        emit('refresh')
        emit('close')
    } catch (err) {
        error.value = err.response?.data?.detail || 'Failed to create user'
    } finally {
        loading.value = false
    }
}

const handleClose = () => {
    if (loading.value) return
    form.name = ''
    form.email = ''
    form.password = ''
    form.confirmPassword = ''
    form.role = 'logistics'
    error.value = ''
    emit('close')
}
</script>

<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-black text-gray-900">Create New User</h2>
                <button @click="handleClose" :disabled="loading"
                    class="text-gray-400 hover:text-gray-600 disabled:opacity-50">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p class="text-sm text-red-700 font-medium">{{ error }}</p>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <!-- Name -->
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Full Name</label>
                    <input v-model="form.name" type="text" placeholder="e.g., John Smith" :disabled="loading"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none disabled:bg-gray-50 disabled:cursor-not-allowed" />
                </div>

                <!-- Email -->
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Email</label>
                    <input v-model="form.email" type="email" placeholder="user@example.com" :disabled="loading"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none disabled:bg-gray-50 disabled:cursor-not-allowed" />
                </div>

                <!-- Password -->
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Password</label>
                    <input v-model="form.password" type="password" placeholder="Min. 6 characters" :disabled="loading"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none disabled:bg-gray-50 disabled:cursor-not-allowed" />
                </div>

                <!-- Confirm Password -->
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-1">Confirm Password</label>
                    <input v-model="form.confirmPassword" type="password" placeholder="Repeat password"
                        :disabled="loading"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent outline-none disabled:bg-gray-50 disabled:cursor-not-allowed" />
                </div>

                <!-- Role Selection -->
                <div>
                    <label class="block text-sm font-bold text-gray-700 mb-2">Assign Role</label>
                    <div class="space-y-2">
                        <label v-for="role in roles" :key="role.value"
                            class="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition"
                            :class="form.role === role.value ? 'bg-black bg-opacity-5 border-black' : ''">
                            <input type="radio" :value="role.value" v-model="form.role" :disabled="loading"
                                class="w-4 h-4 text-black cursor-pointer" />
                            <div class="ml-3">
                                <div class="font-bold text-gray-900 text-sm">{{ role.label }}</div>
                                <div v-if="role.value === 'multi_dept'" class="text-xs text-gray-500 mt-0.5">Can access
                                    both vehicle and vessel dashboards</div>
                                <div v-else-if="role.value === 'logistics'" class="text-xs text-gray-500 mt-0.5">Vehicle
                                    tracking department</div>
                                <div v-else-if="role.value === 'vessel'" class="text-xs text-gray-500 mt-0.5">Vessel
                                    tracking department</div>
                                <div v-else-if="role.value === 'admin'" class="text-xs text-gray-500 mt-0.5">Full system
                                    access and user management</div>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Buttons -->
                <div class="flex gap-3 pt-4">
                    <button type="button" @click="handleClose" :disabled="loading"
                        class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 font-bold rounded-lg hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed">
                        Cancel
                    </button>
                    <button type="submit" :disabled="loading"
                        class="flex-1 px-4 py-2 bg-black text-white font-bold rounded-lg hover:bg-gray-800 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
                        <span v-if="!loading">Create User</span>
                        <span v-else class="flex items-center gap-2">
                            <span
                                class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
                            Creating...
                        </span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
