<script setup lang="ts">
const {data: songs, status} = await useFetch(`/api/v1/songs`);
</script>

<template>
  <div>
    <ULink to="/page_two" class="underline text-cyan-500 italic">Go to page two</ULink>
    <ULink to="/upload" class="underline text-cyan-500 italic"> Go upload</ULink>
    <div v-if="status === 'pending'">
      <UProgress animation="carousel"/>
    </div>
    <div class="space-y-2">
      <Song
          v-for="song in songs"
          :key="song.id"
          :song="song"
      />
    </div>
  </div>
</template>

<style scoped>

</style>