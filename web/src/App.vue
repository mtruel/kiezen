<script setup lang="ts">
import { ref } from 'vue'
import SongList from './components/SongList.vue'
import AddSongForm from './components/AddSongForm.vue'

const activeTab = ref('songs')
</script>

<template>
  <div class="app">
    <header>
      <h1>Kiezen - DJ Song Manager</h1>
    </header>

    <main>
      <div class="layout">
        <div class="form-column">
          <AddSongForm />
        </div>
        <div class="content-column">
          <SongList />
        </div>
      </div>
    </main>
  </div>
</template>

<style>
.app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

main {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

.form-column {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.content-column {
  min-width: 0; /* Prevents overflow in grid */
}
</style>
