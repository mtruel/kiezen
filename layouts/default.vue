<script lang="ts" setup>
const playingSong = usePlayingSong();

</script>

<template>
  <div class="DefaultLayout">
    <UCard class="fixed bottom-0 z-10 mx-auto w-full items-center">
      <template #header >
        <div class="flex justify-between max-w-[1460px]">
          <h1>Kiezen</h1>
          <p> current time {{ playingSong.elapsedTime }}/{{ playingSong.totalTime }} </p>
          <UMeter :max="playingSong.totalTime" :value="playingSong.elapsedTime"/>
          <p>Kiezen is a simple app for DJs</p>
        </div>
      </template>
    </UCard>
    <slot/>
  </div>
</template>

<style scoped>

</style>


