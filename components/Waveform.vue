<script lang="ts" setup>
import WaveSurfer from 'wavesurfer.js'
import Hover from 'wavesurfer.js/dist/plugins/hover.esm.js'
import {usePlayingSong} from "~/composables/states";

const waveform = ref<HTMLElement| null>(null)
let waveSurfer: WaveSurfer

const props = defineProps({id: {required: true, type: Number}});

onMounted(() => {
  waveSurfer = WaveSurfer.create({
    container: waveform.value as HTMLElement,
    waveColor: 'rgb(33,146,86)',
    progressColor: 'rgb(37,147,162)',
    url: `/api/v1/file/${props.id}`,
    plugins: [
      Hover.create({
        lineColor: '#ff0000',
        lineWidth: 2,
        labelBackground: '#555',
        labelColor: '#fff',
        labelSize: '11px',
      }),
    ],
    height: 64,
    // width: 300,
    normalize: true,
    dragToSeek: true,
    barWidth: 3,
    barGap: 1,
    barRadius: 2,
    barAlign: "bottom"
  });
  waveSurfer.on('click', () => {
    handlePlay();
  });
});

onUnmounted(() => {
  if (waveSurfer) waveSurfer.destroy();
  if (interval) clearInterval(interval);
});

const isPlaying = ref(false);

const playingSong = usePlayingSong();
watch(() => playingSong.value.id, (newId) => {
  if (isPlaying.value) {
    if (newId !== props.id) {
      handlePause()
    }
  }
})


const updateElapsedTime = () => {
  playingSong.value.elapsedTime = waveSurfer.getCurrentTime();
  console.log(playingSong.value.elapsedTime);
};


let interval: NodeJS.Timeout | null = null;

function handlePlay() {
  waveSurfer.play();
  isPlaying.value = waveSurfer.isPlaying();
  playingSong.value.id = props.id;
  playingSong.value.totalTime = waveSurfer.getDuration();
  updateElapsedTime();
  if (interval) clearInterval(interval);
  interval = setInterval(updateElapsedTime, 1000);
  // useState('interval', () => interval);
  // playingSong.value.waveformPeaks = waveSurfer.exportPeaks();
}

function handlePause() {
  waveSurfer.pause();
  isPlaying.value = waveSurfer.isPlaying();
  if (interval) clearInterval(interval);
}
</script>

<template>
  <div class="inline-flex flex-grow">
    <UButton v-if="isPlaying" icon="heroicons:pause-16-solid" @click="handlePause"/>
    <UButton v-else icon="heroicons:play-16-solid" @click="handlePlay"/>
    <div ref="waveform" class="min-w-80 flex-grow"/>
  </div>
</template>
