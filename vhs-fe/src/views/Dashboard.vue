<script setup>
import { ref, onMounted, computed } from 'vue'
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
const searchQuery = ref('')

// --- COMPUTED SEARCH LOGIC ---
const filteredVehicles = computed(() => {
    if (!searchQuery.value) return vehicles.value

    const query = searchQuery.value.toLowerCase()
    return vehicles.value.filter(v =>
        v.registration_number.toLowerCase().includes(query) ||
        v.vehicle_type.toLowerCase().includes(query)
    )
})

// --- DATA FETCHING ---
const fetchData = async () => {
    try {
        loading.value = true
        const userRes = await api.get('/vehicles/whoami')
        userEmail.value = userRes.data.email

        const vehicleRes = await api.get('/vehicles/')
        vehicles.value = vehicleRes.data
    } catch (err) {
        if (err.response?.status === 401) router.push('/login')
    } finally {
        loading.value = false
    }
}

// --- ACTIONS ---
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
        await fetchData()
        showDeleteModal.value = false
    } catch (err) {
        alert("Failed to delete vehicle")
    } finally {
        deleteLoading.value = false
        vehicleToDelete.value = null
    }
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
            </button>
        </nav>

        <main class="max-w-7xl mx-auto py-8 px-6">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-6">
                <div>
                    <h2 class="text-3xl font-black text-gray-900">Fleet Overview</h2>
                    <p class="text-gray-500 font-medium">Monitoring {{ vehicles.length }} active vehicles.</p>
                </div>

                <div class="flex w-full md:w-auto gap-4">
                    <div class="relative flex-1 md:w-64">
                        <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </span>
                        <input v-model="searchQuery" type="text" placeholder="Search by plate or model..."
                            class="w-full bg-white border-none shadow-sm pl-12 pr-4 py-3 rounded-xl focus:ring-2 focus:ring-black transition outline-none font-bold text-sm" />
                    </div>

                    <button @click="showAddModal = true"
                        class="bg-black text-white px-6 py-3 rounded-xl font-bold hover:bg-gray-800 transition shadow-lg flex items-center gap-2 whitespace-nowrap">
                        Add Vehicle
                    </button>
                </div>
            </div>

            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
            </div>

            <div v-else-if="filteredVehicles.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <VehicleCard v-for="vehicle in filteredVehicles" :key="vehicle.id" :vehicle="vehicle"
                    @renew="handleRenew" @delete="confirmDelete(vehicle)" />
            </div>

            <div v-else class="bg-white rounded-3xl p-20 text-center shadow-sm border-2 border-dashed border-gray-200">
                <h3 class="text-xl font-bold text-gray-800">
                    {{ searchQuery ? 'No matches found' : 'No vehicles tracked yet' }}
                </h3>
                <p class="text-gray-500 mb-8">
                    {{ searchQuery ? `Try a different plate number or vehicle name.` : `Start by adding your first
                    vehicle to the monitor.` }}
                </p>
                <button v-if="searchQuery" @click="searchQuery = ''" class="text-black font-black underline">Clear
                    Search</button>
                <button v-else @click="showAddModal = true" class="text-black font-black underline">Register
                    Vehicle</button>
            </div>
        </main>
    </div>

    <AddVehicleModal v-if="showAddModal" @close="showAddModal = false" @refresh="fetchData" />
    <UpdateExpiryModal v-if="showUpdateModal" :doc="selectedDoc" @close="showUpdateModal = false"
        @refresh="fetchData" />
    <DeleteConfirmModal v-if="showDeleteModal" :vehicleNumber="vehicleToDelete?.registration_number"
        :loading="deleteLoading" @close="showDeleteModal = false" @confirm="handleDelete" />
</template>