<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'
import VehicleCard from '../components/VehicleCard.vue'
import AddVehicleModal from '../components/AddVehicleModal.vue'
import UpdateExpiryModal from '../components/UpdateExpiryModal.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'

const router = useRouter()
const vehicles = ref([])
const userEmail = ref('')
const loading = ref(true)

// Fetch User Info and Vehicle List
const fetchData = async () => {
    try {
        loading.value = true
        // 1. Get current user email
        const userRes = await api.get('/vehicles/whoami')
        userEmail.value = userRes.data.email

        // 2. Get all vehicles
        const vehicleRes = await api.get('/vehicles/')
        vehicles.value = vehicleRes.data
    } catch (err) {
        console.error("Fetch error:", err)
        // If unauthorized, the interceptor or guard usually handles this, 
        // but we can fallback to login.
        if (err.response?.status === 401) router.push('/login')
    } finally {
        loading.value = false
    }
}

const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/login')
}

const showAddModal = ref(false)
const showUpdateModal = ref(false)
const selectedDoc = ref(null)
const showDeleteModal = ref(false)
const vehicleToDelete = ref(null)
const deleteLoading = ref(false)

const confirmDelete = (vehicle) => {
    vehicleToDelete.value = vehicle
    showDeleteModal.value = true
}

const handleDelete = async () => {
    if (!vehicleToDelete.value) return

    deleteLoading.value = true
    try {
        await api.delete(`/vehicles/${vehicleToDelete.value.id}`)
        await fetchData() // Refresh the list
        showDeleteModal.value = false
    } catch (err) {
        alert("Failed to delete vehicle")
    } finally {
        deleteLoading.value = false
        vehicleToDelete.value = null
    }
}

const openAddModal = () => {
    showAddModal.value = true
}

const closeAddModal = () => {
    showAddModal.value = false
}

const handleRenew = (doc) => {
    selectedDoc.value = doc
    showUpdateModal.value = true
}

onMounted(fetchData)
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <nav class="bg-white shadow-sm px-8 py-4 flex justify-between items-center sticky top-0 z-50">
            <div class="flex items-center gap-4">
                <h1 class="text-xl font-black text-gray-800 tracking-tighter">VPMS</h1>
                <div class="h-6 w-[1px] bg-gray-200"></div>
                <span class="text-sm font-medium text-gray-500">{{ userEmail }}</span>
            </div>

            <button @click="handleLogout"
                class="flex items-center gap-2 text-gray-600 hover:text-red-600 font-bold text-sm transition uppercase tracking-wider">
                <span>Logout</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
            </button>
        </nav>

        <main class="max-w-7xl mx-auto py-8 px-6">
            <div class="flex justify-between items-end mb-10">
                <div>
                    <h2 class="text-3xl font-black text-gray-900">Fleet Overview</h2>
                    <p class="text-gray-500 font-medium">Monitoring {{ vehicles.length }} active vehicles.</p>
                </div>

                <button @click="openAddModal"
                    class="bg-black text-white px-6 py-3 rounded-xl font-bold hover:bg-gray-800 transition shadow-lg active:scale-95 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd"
                            d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                            clip-rule="evenodd" />
                    </svg>
                    Add Vehicle
                </button>
            </div>

            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
            </div>

            <div v-else-if="vehicles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <VehicleCard v-for="vehicle in vehicles" :key="vehicle.id" :vehicle="vehicle" @renew="handleRenew"
                    @delete="confirmDelete(vehicle)" />
            </div>

            <div v-else class="bg-white rounded-3xl p-20 text-center shadow-sm border-2 border-dashed border-gray-200">
                <div class="bg-gray-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-300" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                    </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-800">No vehicles tracked yet</h3>
                <p class="text-gray-500 mb-8">Start by adding your first vehicle to the monitor.</p>
                <button @click="openAddModal" class="text-black font-black underline hover:text-gray-600 transition">
                    Register Vehicle
                </button>
            </div>
        </main>
    </div>
    <AddVehicleModal v-if="showAddModal" @close="closeAddModal" @refresh="fetchData" />
    <UpdateExpiryModal v-if="showUpdateModal" :doc="selectedDoc" @close="showUpdateModal = false"
        @refresh="fetchData" />
    <DeleteConfirmModal v-if="showDeleteModal" :vehicleNumber="vehicleToDelete?.registration_number"
        :loading="deleteLoading" @close="showDeleteModal = false" @confirm="handleDelete" />
</template>