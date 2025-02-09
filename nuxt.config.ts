// https://nuxt.com/docs/api/configuration/nuxt-config
const mountPath = process.env.mount || "./tmp/music"

export default defineNuxtConfig({
    devtools: {enabled: true},
    modules: ["@nuxt/ui", "@vueuse/nuxt", "@prisma/nuxt", "nuxt-file-storage"],
    compatibilityDate: "2025-01-11",
    nitro: {
        storage: {
            musicFiles: {
                driver: 'fs',
                base: mountPath,
            }
        }
    },
})