/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./views/**/*.{ejs,html}", "./public/**/*.js"],
  theme: {
    container: {
      center: true,
    },
    extend: {
      fontFamily: {
        'sans': ['"Courier New"', 'Courier', 'monospace'],
    },
  },
  plugins: [],
}
}
