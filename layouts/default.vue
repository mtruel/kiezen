<script setup lang="ts">
const playingSong = usePlayingSong();

</script>

<template>
  <div class="DefaultLayout">
    <UCard>
      <template #header>
        <div class="flex justify-between">
          <h1>Kiezen</h1>
          <p> current time {{playingSong.elapsedTime}}/{{playingSong.totalTime}} </p>
          <UMeter :value="playingSong.elapsedTime" :max="playingSong.totalTime" />
          <p>Kiezen is a simple app for DJs</p>
        </div>
      </template>
    </UCard>
    <slot/>
  </div>
</template>

<style scoped>

</style>


