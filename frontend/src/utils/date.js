/**
 * Formats any date string or Date object into Cambodia Country Time (UTC+7 / Asia/Phnom_Penh).
 * Examples:
 * - "Oct 23, 2026 02:18 AM UTC" -> "Oct 23, 2026 09:18 AM"
 * - "2026-10-23T02:18:00Z" -> "Oct 23, 2026 09:18 AM"
 */
export function formatCambodiaTime(dateInput) {
  if (!dateInput) return '--'
  let date
  if (dateInput instanceof Date) {
    date = dateInput
  } else if (typeof dateInput === 'string') {
    const trimmed = dateInput.trim()
    date = new Date(trimmed)
    if (isNaN(date.getTime())) {
      date = new Date(trimmed.replace(/\s+UTC$/i, ' GMT'))
    }
  } else {
    date = new Date(dateInput)
  }

  if (isNaN(date.getTime())) {
    return String(dateInput)
  }

  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Phnom_Penh',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  }).formatToParts(date)

  const getPart = (type) => parts.find((p) => p.type === type)?.value || ''
  const month = getPart('month')
  const day = getPart('day')
  const year = getPart('year')
  const hour = getPart('hour')
  const minute = getPart('minute')
  const dayPeriod = getPart('dayPeriod')

  return `${month} ${day}, ${year} ${hour}:${minute} ${dayPeriod}`
}
