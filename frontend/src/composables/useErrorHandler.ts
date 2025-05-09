import { ref } from 'vue'

export function useErrorHandler() {
  const error = ref<string | null>(null)

  const handleError = (err: unknown, defaultMessage: string) => {
    error.value = defaultMessage
    console.error(`Error: ${defaultMessage}`, err)
  }

  const clearError = () => {
    error.value = null
  }

  return {
    error,
    handleError,
    clearError
  }
} 