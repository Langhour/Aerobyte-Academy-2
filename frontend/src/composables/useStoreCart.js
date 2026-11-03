import { ref, computed } from 'vue'

const CART_STORAGE_KEY = 'aerobyte_store_cart'
const FAVS_STORAGE_KEY = 'aerobyte_store_favs'

// Load initial cart
let initialCart = []
try {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem(CART_STORAGE_KEY)
    if (saved) initialCart = JSON.parse(saved)
  }
} catch {
  initialCart = []
}

// Load initial favorites
let initialFavs = []
try {
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem(FAVS_STORAGE_KEY)
    if (saved) initialFavs = JSON.parse(saved)
  }
} catch {
  initialFavs = []
}

const isCartOpen = ref(false)
const cartItems = ref(initialCart)
const favorites = ref(new Set(initialFavs))
const selectedDeliveryMethod = ref('pickup')
const toastMessage = ref('')
let toastTimer = null

function persistCart() {
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cartItems.value))
    }
  } catch {}
}

function persistFavorites() {
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(FAVS_STORAGE_KEY, JSON.stringify([...favorites.value]))
    }
  } catch {}
}

export function showToast(message, duration = 2500) {
  toastMessage.value = message
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, duration)
}

export function useStoreCart() {
  function addToCart(product, quantity = 1, selectedVariant = null) {
    const itemKey = selectedVariant ? `${product.id}-${selectedVariant}` : product.id
    const existing = cartItems.value.find(item => item.cartKey === itemKey || (item.id === product.id && !item.cartKey && !selectedVariant))

    if (existing) {
      existing.quantity += quantity
    } else {
      cartItems.value.push({
        ...product,
        cartKey: itemKey,
        selectedVariant: selectedVariant || null,
        quantity: Math.max(1, quantity)
      })
    }
    persistCart()
    showToast(`Added ${product.name} to shopping bag`)
  }

  function updateCartQuantity(productIdOrKey, newQty) {
    if (newQty <= 0) {
      removeFromCart(productIdOrKey)
      return
    }
    const item = cartItems.value.find(i => (i.cartKey && i.cartKey === productIdOrKey) || i.id === productIdOrKey)
    if (item) {
      item.quantity = newQty
      persistCart()
    }
  }

  function removeFromCart(productIdOrKey) {
    cartItems.value = cartItems.value.filter(i => (i.cartKey ? i.cartKey !== productIdOrKey : i.id !== productIdOrKey))
    persistCart()
  }

  function clearCart() {
    cartItems.value = []
    persistCart()
  }

  function toggleFavorite(productId) {
    if (favorites.value.has(productId)) {
      favorites.value.delete(productId)
      showToast('Removed from wishlist')
    } else {
      favorites.value.add(productId)
      showToast('Saved to your wishlist')
    }
    persistFavorites()
  }

  function isFavorite(productId) {
    return favorites.value.has(productId)
  }

  const totalCartItemsCount = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const cartSubtotalUsd = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + item.priceUsd * item.quantity, 0)
  })

  const deliveryFeeUsd = computed(() => {
    if (selectedDeliveryMethod.value === 'phnom-penh') return 1.50
    if (selectedDeliveryMethod.value === 'province') return 2.50
    return 0.00
  })

  const cartTotalUsd = computed(() => {
    return cartSubtotalUsd.value + deliveryFeeUsd.value
  })

  const cartTelegramCheckoutLink = computed(() => {
    if (cartItems.value.length === 0) return 'https://t.me/aerobyte_academy'
    const lines = [
      '🛒 *New Aero Store Order Request*',
      '--------------------------------',
      ...cartItems.value.map(item => `• ${item.name}${item.selectedVariant ? ` (${item.selectedVariant})` : ''} x${item.quantity} = $${(item.priceUsd * item.quantity).toFixed(2)}`),
      '--------------------------------',
      `Subtotal: $${cartSubtotalUsd.value.toFixed(2)}`,
      `Delivery: ${deliveryFeeUsd.value === 0 ? 'Free Lab Pickup' : `$${deliveryFeeUsd.value.toFixed(2)}`}`,
      `Total: $${cartTotalUsd.value.toFixed(2)} (≈ ${(cartTotalUsd.value * 4100).toLocaleString()} KHR)`,
      '',
      'Please confirm availability and dispatch!'
    ]
    return `https://t.me/aerobyte_academy?text=${encodeURIComponent(lines.join('\n'))}`
  })

  return {
    isCartOpen,
    cartItems,
    favorites,
    selectedDeliveryMethod,
    toastMessage,
    addToCart,
    updateCartQuantity,
    removeFromCart,
    clearCart,
    toggleFavorite,
    isFavorite,
    totalCartItemsCount,
    cartSubtotalUsd,
    deliveryFeeUsd,
    cartTotalUsd,
    cartTelegramCheckoutLink,
    showToast
  }
}
