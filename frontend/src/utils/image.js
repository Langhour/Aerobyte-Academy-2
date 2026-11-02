/**
 * Resolves an image URL so it can be reliably loaded across different origins,
 * localhost vs 127.0.0.1, relative uploads, and production environments (e.g. Render).
 */
export function resolveImageUrl(url) {
  if (!url || typeof url !== 'string') return ''
  const trimmed = url.trim()
  if (!trimmed) return ''

  // Data URLs and Blobs (preview images)
  if (trimmed.startsWith('data:') || trimmed.startsWith('blob:')) {
    return trimmed
  }

  const isBrowser = typeof window !== 'undefined'
  const currentHost = isBrowser ? window.location.hostname : 'localhost'
  const isLocalHost = currentHost === 'localhost' || currentHost === '127.0.0.1'

  // If already an absolute HTTP/HTTPS URL
  if (/^https?:\/\//i.test(trimmed)) {
    try {
      const parsed = new URL(trimmed)

      // In production (not localhost):
      if (!isLocalHost) {
        // If pointing to localhost/127.0.0.1, strip host and use relative path
        if (parsed.hostname === 'localhost' || parsed.hostname === '127.0.0.1') {
          return parsed.pathname + parsed.search
        }
        // If pointing to a production host with the internal API port, strip it
        if (parsed.port === '8000' || parsed.port === '8010') {
          return parsed.pathname + parsed.search
        }
      } else {
        // In local development:
        if (
          (parsed.hostname === 'localhost' || parsed.hostname === '127.0.0.1') &&
          parsed.port === '8000' &&
          currentHost !== parsed.hostname
        ) {
          return `${window.location.protocol}//${currentHost}:8000${parsed.pathname}${parsed.search}`
        }
      }
    } catch {
      // Ignore URL parse error and return trimmed
    }
    return trimmed
  }

  // If it's a relative path starting with /uploads or uploads
  const cleanPath = trimmed.startsWith('/') ? trimmed : `/${trimmed}`
  if (cleanPath.startsWith('/uploads/')) {
    if (import.meta.env.VITE_BACKEND_URL) {
      return `${import.meta.env.VITE_BACKEND_URL.replace(/\/+$/, '')}${cleanPath}`
    }
    // In both Vite dev (proxied to 8000) and production (served by FastAPI/static),
    // root-relative /uploads/... is the most reliable cross-device URL.
    return cleanPath
  }

  return cleanPath
}

/**
 * Checks whether an input string looks like a local Windows/Unix disk path
 * (e.g. C:\Users\... or file:///...) which browsers cannot display directly.
 */
export function isLocalFilePath(url) {
  if (!url || typeof url !== 'string') return false
  const trimmed = url.trim()
  return (
    trimmed.startsWith('file:') ||
    /^[a-zA-Z]:[\\/]/.test(trimmed) ||
    trimmed.startsWith('\\\\')
  )
}
