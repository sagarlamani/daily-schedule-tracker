import { useEffect, useRef } from 'react'

export const useMobileFocus = () => {
  const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null)

  useEffect(() => {
    const handleFocus = () => {
      // Small delay to ensure the keyboard has appeared
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          })
        }
      }, 300)
    }

    const element = inputRef.current
    if (element) {
      element.addEventListener('focus', handleFocus)
      return () => element.removeEventListener('focus', handleFocus)
    }
  }, [])

  return inputRef
}

// Specific hooks for different input types
export const useTextAreaFocus = () => {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const handleFocus = () => {
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          })
        }
      }, 300)
    }

    const element = textareaRef.current
    if (element) {
      element.addEventListener('focus', handleFocus)
      return () => element.removeEventListener('focus', handleFocus)
    }
  }, [])

  return textareaRef
}

export const useInputFocus = () => {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const handleFocus = () => {
      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
          })
        }
      }, 300)
    }

    const element = inputRef.current
    if (element) {
      element.addEventListener('focus', handleFocus)
      return () => element.removeEventListener('focus', handleFocus)
    }
  }, [])

  return inputRef
} 