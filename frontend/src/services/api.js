import axios from 'axios'

const fallbackBaseUrl = '/api'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || fallbackBaseUrl,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  paramsSerializer: {
    indexes: null
  }
})

export const courseService = {
  getCourses(params = {}) {
    return apiClient.get('/courses', { params })
  },
  getCourseById(idOrSlug) {
    return apiClient.get(`/courses/${idOrSlug}`)
  }
}

export const enrollmentService = {
  getFees() {
    return apiClient.get('/enrollments/fees')
  },
  validateCoupon(code, course_price) {
    return apiClient.post('/enrollments/validate-coupon', { code, course_price })
  },
  createEnrollment(payload) {
    return apiClient.post('/enrollments', payload)
  },
  getEnrollment(enrollmentId) {
    return apiClient.get(`/enrollments/${enrollmentId}`)
  },
  getMyEnrollments(params = {}) {
    return apiClient.get('/enrollments/my-history', { params })
  },
  updateStatus(enrollmentId, status) {
    return apiClient.post(`/enrollments/${enrollmentId}/status`, null, {
      params: { status }
    })
  }
}

export const authService = {
  sendCode(email) {
    return apiClient.post('/auth/send-code', { email })
  },
  verifyCode(email, code) {
    return apiClient.post('/auth/verify-code', { email, code })
  }
}

export const accountService = {
  sendCode(email) {
    return apiClient.post('/auth/send-code', { email })
  },
  verifyCode(email, code) {
    return apiClient.post('/auth/verify-code', { email, code })
  },
  register(payload) {
    return apiClient.post('/accounts/register', payload)
  },
  verifyEmail(payload) {
    return apiClient.post('/accounts/verify-email', payload)
  },
  verifyEmailToken(token) {
    return apiClient.post('/accounts/verify-email-token', { token })
  },
  resendVerification(email) {
    return apiClient.post('/accounts/resend-verification', { email })
  },
  login(payload) {
    return apiClient.post('/accounts/login', payload)
  },
  requestPasswordReset(email) {
    return apiClient.post('/accounts/password-reset/request', { email })
  },
  completePasswordReset(payload) {
    return apiClient.post('/accounts/password-reset/complete', payload)
  },
  getSession() {
    return apiClient.get('/accounts/session', {
      params: { _t: Date.now() },
      headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' }
    })
  },
  getUserEnrollments(params = {}) {
    return apiClient.get('/accounts/enrollments', { params })
  },
  updateProfile(payload) {
    return apiClient.put('/accounts/profile', payload)
  },
  async uploadAvatar(file, email = null) {
    let cleanEmail = email
    if (!cleanEmail) {
      try {
        const cached = JSON.parse(localStorage.getItem('aerobyte-profile-current') || '{}')
        cleanEmail = cached.email || ''
      } catch (_) {}
    }
    const formData = new FormData()
    formData.append('avatar', file)
    if (cleanEmail) {
      formData.append('email', cleanEmail)
    }

    const base = apiClient.defaults.baseURL || '/api'
    const endpoint = `${base.replace(/\/+$/, '')}/accounts/avatar`
    const res = await fetch(endpoint, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      const detail = data.detail
      const msg = Array.isArray(detail)
        ? (detail[0]?.msg || JSON.stringify(detail))
        : (typeof detail === 'string' ? detail : data.message || `Upload failed (${res.status})`)
      const err = new Error(msg)
      err.response = { status: res.status, data }
      throw err
    }
    return { data }
  },
  async logout() {
    const base = (apiClient.defaults.baseURL || '/api').replace(/\/+$/, '')
    const endpoints = ['/auth/logout', '/accounts/logout', '/logout']
    const promises = [
      apiClient.post('/auth/logout').catch(() => {}),
      apiClient.post('/accounts/logout').catch(() => {}),
      apiClient.get('/auth/logout').catch(() => {}),
      apiClient.get('/accounts/logout').catch(() => {}),
    ]
    if (typeof fetch !== 'undefined') {
      endpoints.forEach((ep) => {
        promises.push(
          fetch(`/api${ep}`, { method: 'POST', credentials: 'include' }).catch(() => {}),
          fetch(`/api${ep}`, { method: 'GET', credentials: 'include' }).catch(() => {}),
          fetch(`${base}${ep}`, { method: 'POST', credentials: 'include' }).catch(() => {}),
          fetch(`${base}${ep}`, { method: 'GET', credentials: 'include' }).catch(() => {})
        )
      })
    }
    await Promise.allSettled(promises)
    return { data: { authenticated: false } }
  },
  createStoreOrder(payload) {
    return apiClient.post('/accounts/orders', payload)
  },
  getUserOrders() {
    return apiClient.get('/accounts/orders')
  },
  getUserPrintOrders(params = {}) {
    return apiClient.get('/accounts/print-orders', { params })
  },
}

export function getGoogleSignInUrl() {
  const base = apiClient.defaults.baseURL || '/api'
  if (base.startsWith('http://') || base.startsWith('https://')) {
    return `${base}/auth/google/start`
  }
  return `/api/auth/google/start`
}

export function getGoogleAuthConfig() {
  return apiClient.get('/auth/google/config')
}

export function googleCredentialLogin(credential) {
  return apiClient.post('/auth/google/credential', { credential })
}

export function googleHandoffLogin(token) {
  return apiClient.post('/auth/google/handoff', { token })
}

export function googleDirectLogin(payload) {
  return apiClient.post('/auth/google/direct', payload)
}

export const adminService = {
  login(payload) {
    return apiClient.post('/admin/login', payload)
  },
  getSession() {
    return apiClient.get('/admin/session')
  },
  logout() {
    return apiClient.post('/admin/logout')
  },
  getCourses() {
    return apiClient.get('/admin/courses')
  },
  reorderCourses(courseIds) {
    return apiClient.put('/admin/courses/reorder', { course_ids: courseIds })
  },
  createCourse(payload) {
    return apiClient.post('/admin/courses', payload)
  },
  updateCourse(id, payload) {
    return apiClient.put(`/admin/courses/${encodeURIComponent(id)}`, payload)
  },
  deleteCourse(id) {
    return apiClient.delete(`/admin/courses/${encodeURIComponent(id)}`)
  },
  uploadImage(file) {
    const form = new FormData()
    form.append('image', file)
    return apiClient.post('/admin/images', form, {
      headers: { 'Content-Type': undefined },
    })
  },
  getOverview() {
    return apiClient.get('/admin/overview')
  },
  getEnrollments() {
    return apiClient.get('/admin/enrollments')
  },
  exportEnrollments() {
    return apiClient.get('/admin/enrollments/export', { responseType: 'blob' })
  },
  updateEnrollmentStatus(id, status) {
    return apiClient.put(`/admin/enrollments/${encodeURIComponent(id)}/status`, { status })
  },
  getPayments() {
    return apiClient.get('/admin/payments')
  },
  updatePaymentStatus(id, status) {
    return apiClient.put(`/admin/payments/${encodeURIComponent(id)}/status`, { status })
  },
  getCoupons() {
    return apiClient.get('/admin/coupons')
  },
  createCoupon(payload) {
    return apiClient.post('/admin/coupons', payload)
  },
  updateCoupon(code, payload) {
    return apiClient.put(`/admin/coupons/${encodeURIComponent(code)}`, payload)
  },
  deleteCoupon(code) {
    return apiClient.delete(`/admin/coupons/${encodeURIComponent(code)}`)
  },
  getSettings() {
    return apiClient.get('/admin/settings')
  },
  updateSettings(payload) {
    return apiClient.put('/admin/settings', payload)
  },
  getLogsAnalytics() {
    return apiClient.get('/admin/logs/analytics')
  },
  getLoginLogs(params) {
    return apiClient.get('/admin/logs/logins', { params })
  },
  getVisitLogs(params) {
    return apiClient.get('/admin/logs/visits', { params })
  },
  getUsers() {
    return apiClient.get('/admin/users')
  },
  updateUser(id, payload) {
    return apiClient.put(`/admin/users/${encodeURIComponent(id)}`, payload)
  },
  setUserPassword(id, password) {
    return apiClient.put(`/admin/users/${encodeURIComponent(id)}/password`, { password })
  },
  deleteUser(id) {
    return apiClient.delete(`/admin/users/${encodeURIComponent(id)}`)
  },
  getAllOrders(params) {
    return apiClient.get('/admin/orders', { params })
  },
  updateOrderStatus(orderId, status) {
    return apiClient.put(`/admin/orders/${encodeURIComponent(orderId)}/status`, { status })
  },
  getPrintOrders() {
    return apiClient.get('/admin/print-orders')
  },
  getPrintOrder(id) {
    return apiClient.get(`/admin/print-orders/${encodeURIComponent(id)}`)
  },
  updatePrintOrderStatus(id, status) {
    return apiClient.put(`/admin/print-orders/${encodeURIComponent(id)}/status`, { status })
  },
  updatePrintOrderPrice(id, price) {
    const cleanId = String(id || '').replace(/^#/, '')
    return apiClient.put(`/admin/print-orders/${encodeURIComponent(cleanId)}/price`, { price: Number(price) })
  },
  updatePrintOrderPaymentStatus(id, payment_status) {
    const cleanId = String(id || '').replace(/^#/, '')
    return apiClient.put(`/admin/print-orders/${encodeURIComponent(cleanId)}/payment-status`, { payment_status })
  },
  deletePrintOrder(id) {
    return apiClient.delete(`/admin/print-orders/${encodeURIComponent(id)}`)
  },
  getDatabaseStats() {
    return apiClient.get('/admin/database/stats')
  },
}

export const printOrderService = {
  submitOrder(formData) {
    return apiClient.post('/print-orders', formData, {
      headers: { 'Content-Type': undefined },
    })
  },
  getAdminOrders() {
    return apiClient.get('/admin/print-orders')
  },
  getAdminOrder(id) {
    return apiClient.get(`/admin/print-orders/${encodeURIComponent(id)}`)
  },
  updateStatus(id, status) {
    return apiClient.put(`/admin/print-orders/${encodeURIComponent(id)}/status`, { status })
  },
  updatePrice(id, price) {
    const cleanId = String(id || '').replace(/^#/, '')
    return apiClient.put(`/admin/print-orders/${encodeURIComponent(cleanId)}/price`, { price: Number(price) })
  },
  deleteOrder(id) {
    return apiClient.delete(`/admin/print-orders/${encodeURIComponent(id)}`)
  },
  getFileDownloadUrl(filename, originalName) {
    const base = apiClient.defaults.baseURL || '/api'
    const nameParam = originalName ? `?name=${encodeURIComponent(originalName)}` : ''
    return `${base}/print-orders/files/${encodeURIComponent(filename)}${nameParam}`
  },
  getMyOrders(params = {}) {
    return apiClient.get('/print-orders/my-orders', { params })
  },
  getOrder(id) {
    const cleanId = String(id || '').replace(/^#/, '')
    return apiClient.get(`/print-orders/${encodeURIComponent(cleanId)}`)
  },
  submitReview(id, reviewData) {
    return apiClient.post(`/print-orders/${encodeURIComponent(id)}/review`, reviewData)
  },
  getReviews(params = {}) {
    return apiClient.get('/print-orders/reviews', { params })
  },
}

export const analyticsService = {
  trackVisit(payload) {
    return apiClient.post('/track-visit', payload)
  },
}

export const siteSettingsService = {
  getPublicSettings() {
    return apiClient.get('/site-settings')
  },
}

export default apiClient
