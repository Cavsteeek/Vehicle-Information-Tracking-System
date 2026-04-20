<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/http'
import VesselCard from '../components/VesselCard.vue'
import AddVesselModal from '../components/AddVesselModal.vue'
import AddVesselDocModal from '../components/AddVesselDocModal.vue'
import CreateUserModal from '../components/CreateUserModal.vue'
import UpdateExpiryModal from '../components/UpdateExpiryModal.vue'

const router = useRouter()
const vessels = ref([])
const loading = ref(true)
const userRole = ref(localStorage.getItem('role') || '')
const userEmail = ref('')

const showAddModal = ref(false)
const showCreateUserModal = ref(false)
const showAddDocModal = ref(false)
const showUpdateModal = ref(false)
const selectedDoc = ref(null)
const selectedVessel = ref(null)

const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 6

const filteredVessels = computed(() => {
    if (!searchQuery.value) return vessels.value
    const q = searchQuery.value.toLowerCase()
    return vessels.value.filter(v => v.name.toLowerCase().includes(q))
})

const pagedVessels = computed(() => {
    return filteredVessels.value.slice(0, currentPage.value * itemsPerPage)
})

const hasMore = computed(() => pagedVessels.value.length < filteredVessels.value.length)

const fetchVessels = async () => {
    loading.value = true
    try {
        const userRes = await api.get('/vehicles/whoami')
        userEmail.value = userRes.data.email
        const res = await api.get('/vessel-docs/vessels')
        vessels.value = res.data
    } catch (err) {
        if (err.response?.status === 401) router.push('/login')
    } finally {
        loading.value = false
    }
}

const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    router.push('/login')
}

const handleRenew = (doc) => {
    selectedDoc.value = doc
    showUpdateModal.value = true
}

const handleAddDoc = (vessel) => {
    selectedVessel.value = vessel
    showAddDocModal.value = true
}

const handleDelete = async (doc) => {
    if (!doc) return
    try {
        await api.delete(`/vessel-docs/${doc.id}`)
        await fetchVessels()
    } catch (err) {
        alert('Failed to delete document')
    }
}

onMounted(async () => {
    // Restrict access: vessel-only users cannot access vehicle dashboard, redirect them
    // Allow: admin, vessel, multi_dept users
    if (!['vessel', 'admin', 'multi_dept'].includes(userRole.value)) {
        router.push('/dashboard')
        return
    }
    await fetchVessels()
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
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path fill-rule="evenodd"
                            d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                            clip-rule="evenodd" />
                    </svg>
                    <span class="hidden sm:inline">Create User</span>
                    <span class="sm:hidden">User</span>
                </button>
                <button v-if="userRole === 'admin' || userRole === 'multi_dept'" @click="router.push('/dashboard')"
                    class="px-2 sm:px-4 py-2 text-xs sm:text-sm font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition">
                    <span class="hidden sm:inline">Vehicle Dashboard</span>
                    <span class="sm:hidden">Vehicles</span>
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
                    <h2 class="text-2xl sm:text-3xl font-black text-gray-900">Vessel Overview</h2>
                    <p class="text-gray-500 font-medium text-sm sm:text-base">Monitoring {{ vessels.length }} active
                        vessel(s).</p>
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
                        <input v-model="searchQuery" type="text" placeholder="Search by name..."
                            class="w-full bg-white border-none shadow-sm pl-10 sm:pl-12 pr-10 py-3 rounded-xl focus:ring-2 focus:ring-black transition outline-none font-bold text-sm" />
                    </div>
                    <button @click="showAddModal = true"
                        class="bg-black text-white px-4 sm:px-6 py-3 rounded-xl font-bold hover:bg-gray-800 transition shadow-lg flex items-center gap-2 whitespace-nowrap active:scale-95 text-sm sm:text-base">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5" viewBox="0 0 20 20"
                            fill="currentColor">
                            <path fill-rule="evenodd"
                                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                                clip-rule="evenodd" />
                        </svg>
                        <span class="hidden sm:inline">Add Vessel</span>
                        <span class="sm:hidden">Add</span>
                    </button>
                </div>
            </div>

            <div v-if="loading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-black"></div>
            </div>

            <div v-else-if="pagedVessels.length > 0"
                class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
                <VesselCard v-for="vessel in pagedVessels" :key="vessel.id" :vessel="vessel" @renew="handleRenew"
                    @addDoc="handleAddDoc" @delete="handleDelete" @refresh="fetchVessels" />
            </div>

            <div v-else class="bg-white rounded-3xl p-20 text-center shadow-sm border-2 border-dashed border-gray-200">
                <h3 class="text-xl font-bold text-gray-800">No vessels registered yet</h3>
                <p class="text-gray-500 mb-8">Start by registering your first vessel.</p>
                <button @click="showAddModal = true" class="text-black font-black underline">Register Vessel</button>
            </div>

            <div v-if="!loading && hasMore" class="mt-12 flex justify-center">
                <button @click="currentPage++"
                    class="bg-white text-black px-8 py-3 rounded-xl font-black shadow-sm border border-gray-200">Show
                    More</button>
            </div>
        </main>

        <AddVesselModal v-if="showAddModal" @close="showAddModal = false" @refresh="fetchVessels" />
        <CreateUserModal v-if="showCreateUserModal" @close="showCreateUserModal = false" @refresh="fetchVessels" />
        <AddVesselDocModal v-if="showAddDocModal" :vessel="selectedVessel" @close="showAddDocModal = false"
            @refresh="fetchVessels" />
        <UpdateExpiryModal v-if="showUpdateModal" :doc="selectedDoc" mode="vessel" @close="showUpdateModal = false"
            @refresh="fetchVessels" />
    </div>
</template>
