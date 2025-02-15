import type { UseFetchOptions } from 'nuxt/app'

export function useFetchFastAPI<T>(
    url: string | (() => string),
    options: UseFetchOptions<T> = {},
) {
    return useFetch(`http://127.0.0.1:8000${url}`, {
        ...options,
        $fetch: useNuxtApp().$customFetch,
    })
}
