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