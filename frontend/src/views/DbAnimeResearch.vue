<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Watchlist Anime</h1>

    <!-- Navigazione tra ricerca e lista completa -->
    <div class="flex gap-2 mb-6">
      <button @click="fetchAllAnime" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        Mostra tutti gli anime
      </button>
      <button @click="$router.push('/')"
              class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
        Vai alla Home
      </button>
    </div>

    <!-- Input ricerca -->
    <div class="flex gap-2 mb-6">
      <input v-model="query" type="text" placeholder="Cerca anime per nome o ID"
             class="border p-2 rounded w-full" />
      <button @click="searchDbAnime"
              class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
        Cerca
      </button>
    </div>

    <!-- Stato caricamento / errore -->
    <div v-if="loading" class="text-gray-500">Caricamento in corso...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <!-- Lista anime -->
    <div v-if="paginatedAnime.length > 0" class="space-y-4">
      <div v-for="anime in paginatedAnime" :key="anime.mal_id"
           class="p-4 border rounded-lg bg-gray-100 flex justify-between items-center">
        <div class="flex gap-4 items-center">
          <img :src="anime.image" alt="Anime Image" class="w-20 rounded shadow" />
          <div>
            <h2 class="font-semibold text-lg">{{ anime.name }}</h2>
            <p><strong>Voto personale:</strong> {{ anime.voto_personale || 'N/D' }}</p>
            <p><strong>Visto:</strong> {{ anime.visto_nonvisto ? 'Sì' : 'No' }}</p>
            <p><strong>Media voto:</strong> {{ anime.media_voto || 'N/D' }}</p>
          </div>
        </div>

        <!-- Pulsante elimina -->
        <button @click="deleteAnime(anime.mal_id)"
                class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700">
          Elimina
        </button>
      </div>
    </div>

    <!-- Paginazione -->
    <div v-if="totalPages > 1" class="flex gap-2 mt-4">
      <button v-for="page in totalPages" :key="page" @click="currentPage = page"
              :class="page === currentPage ? 'bg-blue-600 text-white px-3 py-1 rounded' : 'bg-gray-300 px-3 py-1 rounded hover:bg-gray-400'">
        {{ page }}
      </button>
    </div>

    <div v-if="paginatedAnime.length === 0 && !loading && !error" class="text-gray-500">
      Nessun risultato trovato.
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const query = ref('')
const animeList = ref([])
const loading = ref(false)
const error = ref('')
const currentPage = ref(1)
const perPage = 10 // anime per pagina

// --- Calcolo paginazione ---
const totalPages = computed(() => Math.ceil(animeList.value.length / perPage))
const paginatedAnime = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return animeList.value.slice(start, start + perPage)
})

// --- Ricerca anime per query ---
const searchDbAnime = async () => {
  if (!query.value.trim()) {
    error.value = 'Inserisci un ID o nome anime.'
    return
  }

  loading.value = true
  error.value = ''
  animeList.value = []

  try {
    const res = await axios.get(`http://localhost:8000/anime/search?query=${encodeURIComponent(query.value)}`)
    animeList.value = res.data
    currentPage.value = 1
  } catch (err) {
    console.error(err)
    error.value = 'Errore durante la ricerca nel DB.'
  } finally {
    loading.value = false
  }
}

// --- Prendi tutti gli anime ---
const fetchAllAnime = async () => {
  loading.value = true
  error.value = ''
  animeList.value = []

  try {
    const res = await axios.get(`http://localhost:8000/anime/all`)
    animeList.value = res.data
    currentPage.value = 1
  } catch (err) {
    console.error(err)
    error.value = 'Errore nel recupero di tutti gli anime.'
  } finally {
    loading.value = false
  }
}

// --- Elimina anime dal DB ---
const deleteAnime = async (mal_id) => {
  try {
    await axios.delete(`http://localhost:8000/anime/${mal_id}`)
    animeList.value = animeList.value.filter(a => a.mal_id !== mal_id)
  } catch (err) {
    console.error(err)
    error.value = 'Errore durante la cancellazione dell\'anime.'
  }
}
</script>
