import { ref } from 'vue'

export function useLoadingState() {
  const isLoading = ref(false)

  const withLoading = async <T>(fn: () => Promise<T>): Promise<T> => {
    try {
      isLoading.value = true
      return await fn()
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    withLoading
  }
} 