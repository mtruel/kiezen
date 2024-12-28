import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import SongItem from "./components/SongItem.vue";

createApp(App).mount('#app')
export default {
    components: { SongItem },
    methods: {
        handlePlayClick(song: typeof SongItem) {
            console.log('Play clicked:', song)
        },
    },
}