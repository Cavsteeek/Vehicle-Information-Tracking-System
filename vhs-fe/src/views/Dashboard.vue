<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'
import VehicleCard from '../components/VehicleCard.vue'
import AddVehicleModal from '../components/AddVehicleModal.vue'
import CreateUserModal from '../components/CreateUserModal.vue'
import UpdateExpiryModal from '../components/UpdateExpiryModal.vue'
import DeleteConfirmModal from '../components/DeleteConfirmModal.vue'

const router = useRouter()
const vehicles = ref([])
const userEmail = ref('')
const userRole = ref(localStorage.getItem('role') || '')
const loading = ref(true)

// --- SEARCH & PAGINATION ---
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

watch(searchQuery, () => {
    currentPage.value = 1
})

const allFilteredResults = computed(() => {
    if (!searchQuery.value) return vehicles.value
    const query = searchQuery.value.toLowerCase()
    return vehicles.value.filter(v =>
        v.registration_number.toLowerCase().includes(query) ||
        v.vehicle_type.toLowerCase().includes(query)
    )
})

const filteredVehicles = computed(() => {
    return allFilteredResults.value.slice(0, currentPage.value * itemsPerPage)
})

const hasMore = computed(() => {
    return filteredVehicles.value.length < allFilteredResults.value.length
})

const remainingCount = computed(() => {
    return allFilteredResults.value.length - filteredVehicles.value.length
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
    localStorage.removeItem('role')
    router.push('/login')
}

const showAddModal = ref(false)
const showCreateUserModal = ref(false)
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

onMounted(async () => {
    await fetchData()
})
</script>

<template>
    <div class="min-h-screen bg-gray-100">
        <nav
            class="bg-white shadow-sm px-4 sm:px-6 lg:px-8 py-3 sm:py-4 flex justify-between items-center sticky top-0 z-50">
            <div class="flex items-center gap-2 sm:gap-4">
                <h1 class="text-lg sm:text-xl font-black text-gray-800 tracking-tighter">VPMS</h1>
                <div class="h-4 sm:h-6 w-[1px] bg-gray-200"></div>
                <span class="text-xs sm:text-sm font-medium text-gray-500 truncate max-w-[120px] sm:max-w-none">{{
                    userEmail }} - {{ userRole }}</span>
            </div>

            <div class="flex items-center gap-2 sm:gap-4 md:gap-6">
                <button v-if="userRole === 'admin'" @click="showCreateUserModal = true"
                    class="px-2 sm:px-4 py-2 text-xs sm:text-sm font-bold text-white bg-green-600 hover:bg-green-700 rounded-lg transition flex items-center gap-1 sm:gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4" viewBox="0 0 20 20"
                        fill="currentColor">
                        <path fill-rule="evenodd"
                            d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                            clip-rule="evenodd" />
                    </svg>
                    <span class="hidden sm:inline">New User</span>
                    <span class="sm:hidden">New User</span>
                </button>
                <button v-if="userRole === 'admin' || userRole === 'multi_dept'"
                    @click="router.push('/vessel-dashboard')"
                    class="px-2 sm:px-4 py-2 text-xs sm:text-sm font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition">
                    <span class="hidden sm:inline">Vessel Dashboard</span>
                    <span class="sm:hidden">Vessels</span>
                </button>
                <button @click="handleLogout"
                    class="flex items-center gap-1 sm:gap-2 text-gray-600 hover:text-red-600 font-bold text-xs sm:text-sm transition uppercase tracking-wider">
                    <span class="hidden sm:inline">Logout</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                </button>
            </div>
        </nav>

        <main class="max-w-7xl mx-auto py-6 sm:py-8 px-4 sm:px-6">
            <div
                class="flex flex-col lg:flex-row justify-between items-start lg:items-end mb-8 sm:mb-10 gap-4 sm:gap-6">
                <div class="w-full lg:w-auto">
                    <h2 class="text-2xl sm:text-3xl font-black text-gray-900">Fleet Overview</h2>
                    <p class="text-gray-500 font-medium text-sm sm:text-base">Monitoring {{ vehicles.length }} active
                        vehicle(s).</p>
                </div>

                <div class="flex flex-col sm:flex-row w-full lg:w-auto gap-3 sm:gap-4">
                    <div class="relative flex-1 sm:w-64 lg:w-80">
                        <span
                            class="absolute left-3 sm:left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </span>
                        <input v-model="searchQuery" type="text" placeholder="Search by plate or model..."
                            class="w-full bg-white border-none shadow-sm pl-10 sm:pl-12 pr-10 py-3 rounded-xl focus:ring-2 focus:ring-black transition outline-none font-bold text-sm" />

                        <button v-if="searchQuery" @click="searchQuery = ''"
                            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-300 hover:text-black transition">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5" viewBox="0 0 20 20"
                                fill="currentColor">
                                <path fill-rule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                                    clip-rule="evenodd" />
                            </svg>
                        </button>
                    </div>

                    <button @click="showAddModal = true"
                        class="bg-black text-white px-4 sm:px-6 py-3 rounded-xl font-bold hover:bg-gray-800 transition shadow-lg flex items-center gap-2 whitespace-nowrap active:scale-95 text-sm sm:text-base">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5" viewBox="0 0 20 20"
                            fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                                clip-rule="evenodd" />
                        </svg>
                        <span class="hidden sm:inline">Add Vehicle</span>
                        <span class="sm:hidden">Add</span>
                    </button>
                </div>
            </div>

            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
            </div>

            <div v-else-if="filteredVehicles.length > 0">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
                    <VehicleCard v-for="vehicle in filteredVehicles" :key="vehicle.id" :vehicle="vehicle"
                        @renew="handleRenew" @delete="confirmDelete(vehicle)" />
                </div>

                <div v-if="hasMore" class="mt-12 flex justify-center">
                    <button @click="currentPage++"
                        class="group bg-white text-black px-8 py-3 rounded-xl font-black shadow-sm border border-gray-200 hover:bg-gray-50 transition active:scale-95 flex items-center gap-3">
                        <span>Show More</span>
                        <span
                            class="bg-gray-100 text-gray-500 text-[10px] px-2 py-1 rounded-md group-hover:bg-black group-hover:text-white transition">
                            {{ remainingCount }}
                        </span>
                    </button>
                </div>
            </div>

            <div v-else class="bg-white rounded-3xl p-20 text-center shadow-sm border-2 border-dashed border-gray-200">
                <h3 class="text-xl font-bold text-gray-800">
                    {{ searchQuery ? `No matches found` : `No vehicles tracked yet` }}
                </h3>
                <p class="text-gray-500 mb-8">
                    {{ searchQuery
                        ? `Try a different plate number or vehicle name.`
                        : `Start by adding your first vehicle to the monitor.`
                    }}
                </p>
                <button v-if="searchQuery" @click="searchQuery = ''" class="text-black font-black underline">
                    Clear Search
                </button>
                <button v-else @click="showAddModal = true" class="text-black font-black underline">
                    Register Vehicle
                </button>
            </div>
        </main>
    </div>

    <AddVehicleModal v-if="showAddModal" @close="showAddModal = false" @refresh="fetchData" />
    <CreateUserModal v-if="showCreateUserModal" @close="showCreateUserModal = false" @refresh="fetchData" />
    <UpdateExpiryModal v-if="showUpdateModal" :doc="selectedDoc" @close="showUpdateModal = false"
        @refresh="fetchData" />
    <DeleteConfirmModal v-if="showDeleteModal" :vehicleNumber="vehicleToDelete?.registration_number"
        :loading="deleteLoading" @close="showDeleteModal = false" @confirm="handleDelete" />
</template>