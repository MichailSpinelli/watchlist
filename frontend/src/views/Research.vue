<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Ricerca Anime</h1>

    <button @click="$router.push('/research-db')">Vai al tuo db</button>
    <button @click="$router.push('/')">Vai alla Home</button>

    <!-- Input e pulsante ricerca -->
    <div class="flex gap-2 mb-6">
      <input
        v-model="query"
        type="text"
        placeholder="Inserisci ID o nome anime"
        class="border p-2 rounded w-full"
      />
      <button
        @click="searchAnime"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Cerca
      </button>
    </div>

    <!-- Stato caricamento / errore -->
    <div v-if="loading" class="text-gray-500">Caricamento in corso...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <!-- Risultato ricerca -->
    <div v-if="anime" class="bg-gray-100 p-4 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-2">{{ anime.title }}</h2>

      <div class="flex flex-col sm:flex-row gap-4">
        <img
          :src="anime.images?.jpg?.large_image_url"
          alt="Immagine Anime"
          class="w-40 rounded-lg shadow mb-4"
        />

        <div class="flex-1">
          <p><strong>Studio:</strong> {{ anime.studios?.[0]?.name || 'N/D' }}</p>
          <p><strong>Anno:</strong> {{ anime.year || 'N/D' }}</p>
          <p><strong>Media voto:</strong> {{ anime.score || 'N/D' }}</p>
          <p><strong>Classifica:</strong> {{ anime.rank || 'N/D' }}</p>
          <p><strong>Generi:</strong> {{ anime.genres?.map(g => g.name).join(', ') || 'N/D' }}</p>
        </div>
      </div>

      <!-- Sinossi -->
      <div class="mt-4">
        <h3 class="font-semibold mb-1">Sinossi</h3>
        <p class="text-gray-700 whitespace-pre-line">{{ anime.synopsis || 'Nessuna descrizione disponibile.' }}</p>
      </div>

      <!-- Trailer -->
      <div v-if="anime.trailer?.embed_url" class="mt-4">
        <h3 class="font-semibold mb-1">Trailer</h3>
        <iframe
          :src="anime.trailer.embed_url"
          width="100%"
          height="300"
          frameborder="0"
          allowfullscreen
          class="rounded-lg"
        ></iframe>
      </div>

      <!-- Aggiungi al DB -->
      <div class="mt-4 p-4 border rounded-lg bg-white">
        <h3 class="font-semibold mb-2">Aggiungi alla tua watchlist</h3>
        <div class="flex flex-col sm:flex-row gap-4 items-center mb-2">
          <label>
            Voto personale:
            <input type="number" v-model.number="mioVoto" min="0" max="10" class="border p-1 rounded w-20"/>
          </label>
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="visto"/>
            Visto
          </label>
        </div>
        <button
          @click="addToWatchlist"
          class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Aggiungi
        </button>
        <div v-if="successMsg" class="text-green-600 mt-2">{{ successMsg }}</div>
        <div v-if="addError" class="text-red-600 mt-2">{{ addError }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const query = ref('')
const anime = ref(null)
const loading = ref(false)
const error = ref('')

// Campi aggiunta watchlist
const mioVoto = ref(null)
const visto = ref(false)
const successMsg = ref('')
const addError = ref('')

const searchAnime = async () => {
  if (!query.value.trim()) {
    error.value = 'Inserisci un ID o nome anime.'
    return
  }

  anime.value = null
  error.value = ''
  loading.value = true
  successMsg.value = ''
  addError.value = ''

  try {
    let response
    if (!isNaN(query.value)) {
      // Ricerca per ID
      response = await axios.get(`https://api.jikan.moe/v4/anime/${query.value}`)
      anime.value = response.data.data
    } else {
      // Ricerca per nome
      response = await axios.get(`https://api.jikan.moe/v4/anime?q=${encodeURIComponent(query.value)}&limit=1`)
      if (response.data.data.length > 0) {
        anime.value = response.data.data[0]
      } else {
        error.value = 'Nessun anime trovato.'
      }
    }
  } catch (err) {
    console.error(err)
    error.value = 'Errore durante la ricerca.'
  } finally {
    loading.value = false
  }
}

const addToWatchlist = async () => {
  if (!anime.value) return
  addError.value = ''
  successMsg.value = ''

  // Payload da inviare al backend
  const payload = {
    mal_id: anime.value.mal_id,
    name: anime.value.title,
    trailer: anime.value.trailer?.embed_url || null,
    image: anime.value.images?.jpg?.large_image_url || null,
    episodi: anime.value.episodes || null,
    anno_uscita_fine: anime.value.year || null,
    media_voto: anime.value.score || null,
    voto_personale: mioVoto.value,
    visto_nonvisto: visto.value,
    classifica: anime.value.rank || null,
    votato_da: anime.value.scored_by || null,
    sinopsi: anime.value.synopsis || null,
    background: anime.value.background || null,
    genere_1: anime.value.genres?.[0]?.name || null,
    genere_2: anime.value.genres?.[1]?.name || null,
    genere_3: anime.value.genres?.[2]?.name || null,
    studio: anime.value.studios?.[0]?.name || null
  }

  try {
    const res = await axios.post('http://localhost:8000/anime', payload)
    successMsg.value = res.data.message
  } catch (err) {
    console.error(err)
    addError.value = 'Errore nell\'aggiunta alla watchlist.'
  }
}
</script>