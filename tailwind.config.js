/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: [
    './templates/base.html',     // Add your HTML files here
  ],
  darkMode: false,         // Set to 'media' or 'class' to enable dark mode
  theme: {
    extend: {
      colors: {
        // Add your custom colors here
        primary: '#007BFF',
        secondary: '#6C757D',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    // Add any additional plugins here
    require('@tailwindcss/forms')
  ],
}
