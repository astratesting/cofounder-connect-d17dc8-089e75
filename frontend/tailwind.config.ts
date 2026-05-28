import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef8ff',
          100: '#d9efff',
          500: '#2478ff',
          600: '#155eea',
          900: '#0c1b3a'
        }
      },
      boxShadow: {
        glow: '0 24px 80px rgba(36, 120, 255, 0.18)'
      }
    }
  },
  plugins: [forms]
};

export default config;
