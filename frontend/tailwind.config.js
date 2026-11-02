/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Kantumruy Pro"', 'sans-serif'],
        mono: ['"Kantumruy Pro"', 'sans-serif'],
        serif: ['"Kantumruy Pro"', 'sans-serif'],
      },
      colors: {
        navy: {
          50: '#f1f5fa',
          100: '#e2eaf3',
          600: '#27466d',
          800: '#16365c',
          900: '#102a49',
        },
        'accent-orange': '#f28c28',
        'accent-green': '#16a34a',
        'accent-red': '#dc2626',
      },
      boxShadow: {
        '2xs': '0 1px 2px rgb(15 23 42 / 0.06)',
        xs: '0 1px 3px rgb(15 23 42 / 0.08)',
        card: '0 4px 18px rgb(15 23 42 / 0.06)',
        'card-hover': '0 10px 30px rgb(15 23 42 / 0.1)',
      },
    },
  },
  plugins: [],
}