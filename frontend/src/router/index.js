import { createRouter, createWebHistory } from 'vue-router'
import { accountService } from '../services/api'

const ExploreCoursesView = () => import('../views/ExploreCoursesView.vue')
const QuestionsView = () => import('../views/QuestionsView.vue')
const AccountAccessView = () => import('../views/AccountAccessView.vue')
const AdminContentView = () => import('../views/AdminContentView.vue')
const CourseDetailView = () => import('../views/CourseDetailView.vue')
const CourseEnrollmentView = () => import('../views/CourseEnrollmentView.vue')
const ScanToPayView = () => import('../views/ScanToPayView.vue')
const PaymentSuccessfulView = () => import('../views/PaymentSuccessfulView.vue')
const PaymentExpiredView = () => import('../views/PaymentExpiredView.vue')
const AboutView = () => import('../views/AboutView.vue')
const ContactView = () => import('../views/ContactView.vue')
const ProfileInformationView = () => import('../views/ProfileInformationView.vue')
const TermsOfUseView = () => import('../views/TermsOfUseView.vue')
const PrivacyPolicyView = () => import('../views/PrivacyPolicyView.vue')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/questions' },
    { path: '/questions', name: 'questions', component: QuestionsView },
    { path: '/courses', name: 'courses', component: ExploreCoursesView },
    { path: '/account', name: 'account', component: AccountAccessView },
    { path: '/admin', name: 'admin', component: AdminContentView },
    { path: '/courses/:id', name: 'CourseDetail', component: CourseDetailView, props: true, alias: ['/course/:id'] },
    { path: '/enroll/:id', name: 'CourseEnrollment', component: CourseEnrollmentView, props: true, alias: ['/enrollment/:id'] },
    { path: '/payment/:enrollmentId', name: 'ScanToPay', component: ScanToPayView },
    {
      path: '/payment/success/:enrollmentId',
      name: 'PaymentSuccessful',
      component: PaymentSuccessfulView,
      alias: ['/receipt/:enrollmentId'],
    },
    {
      path: '/payment/expired/:enrollmentId',
      name: 'PaymentExpired',
      component: PaymentExpiredView,
    },
    { path: '/about', name: 'about', component: AboutView },
    { path: '/contact', name: 'contact', component: ContactView },
    { path: '/profile', name: 'profile', component: ProfileInformationView },
    { path: '/terms', name: 'terms', component: TermsOfUseView },
    { path: '/privacy', name: 'privacy', component: PrivacyPolicyView },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.afterEach((to) => {
  try {
    if (typeof window === 'undefined') return
    if (to.path.startsWith('/admin')) return
    let visitorId = localStorage.getItem('aerobyte_visitor_id')
    if (!visitorId) {
      visitorId = 'v_' + Math.random().toString(36).substring(2, 10) + Date.now().toString(36)
      localStorage.setItem('aerobyte_visitor_id', visitorId)
    }
    const emailQuery = to.query?.email ? String(to.query.email).trim() : ''
    fetch('/api/track-visit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        path: to.fullPath,
        visitor_id: visitorId,
        referrer: document.referrer || '',
        user_email: emailQuery || undefined,
      }),
    }).catch(() => {})
  } catch {
    // ignore
  }
})

router.beforeEach(async (to, from, next) => {
  if (to.name === 'CourseEnrollment') {
    try {
      const { data } = await accountService.getSession()
      if (!data?.authenticated) {
        return next({
          path: '/account',
          query: {
            mode: 'register',
            redirect: to.fullPath,
          },
        })
      }
    } catch {
      return next({
        path: '/account',
        query: {
          mode: 'register',
          redirect: to.fullPath,
        },
      })
    }
  }
  next()
})

export default router
