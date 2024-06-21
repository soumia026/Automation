/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,jsx}"],
  theme: {
    extend: {
      colors: {
        beige: {
          400: '#F1EEDC',
          600: '#E5DDC5',
        },
        blue: {
          400: '#BED7DC',
          600: '#B3C8CF',
        },
      },
      backgroundImage: {
        'custom-gradient': 'linear-gradient(-45deg, #7eb0d2, #4f64bb,  #753ebd)',
      },
      fontFamily: {
        northStar: 'northStar',
      },
    },
  },
  plugins: [],
}