import axios from 'axios'

const localApiHost = typeof window !== 'undefined' ? window.location.hostname : 'localhost'
const isLocalDev = typeof window !== 'undefined' && (window.location.port === '5173' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
const fallbackBaseUrl = isLocalDev && window.location.port === '5173' ? `http://${localApiHost}:8000/api` : '/api'

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

export const accountService = {
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
    return apiClient.get('/accounts/session')
  },
  getUserEnrollments(params = {}) {
    return apiClient.get('/accounts/enrollments', { params })
  },
  updateProfile(payload) {
    return apiClient.put('/accounts/profile', payload)
  },
  uploadAvatar(file) {
    const formData = new FormData()
    formData.append('avatar', file)
    return apiClient.post('/accounts/avatar', formData, {
      headers: { 'Content-Type': undefined },
    })
  },
  logout() {
    return apiClient.post('/accounts/logout')
  },
  createStoreOrder(payload) {
    return apiClient.post('/accounts/orders', payload)
  },
  getUserOrders() {
    return apiClient.get('/accounts/orders')
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
  getDatabaseStats() {
    return apiClient.get('/admin/database/stats')
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
