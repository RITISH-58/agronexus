/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                olive: {
                    50: '#f8faf0',
                    100: '#eef2d9',
                    200: '#dce6b3',
                    300: '#c4d484',
                    400: '#a8be5a',
                    500: '#6B8E23',
                    600: '#5a7a1c',
                    700: '#4a6418',
                    800: '#3b5014',
                    900: '#2d3d10',
                },
                leaf: {
                    50: '#e8f5e9',
                    100: '#c8e6c9',
                    200: '#a5d6a7',
                    300: '#81c784',
                    400: '#66bb6a',
                    500: '#4CAF50',
                    600: '#43a047',
                    700: '#388e3c',
                    800: '#2e7d32',
                    900: '#1b5e20',
                },
                cream: {
                    50: '#FEFEF9',
                    100: '#FCFCF0',
                    200: '#F7F8F2',
                    300: '#F0F2E8',
                    400: '#E5E8D8',
                    500: '#D8DBC8',
                },
                wheat: {
                    50: '#fdf8f0',
                    100: '#f9edda',
                    200: '#f0d9b5',
                    300: '#D4A373',
                    400: '#c48f5c',
                    500: '#b07a45',
                    600: '#96643a',
                    700: '#7a5030',
                    800: '#5e3d26',
                    900: '#432b1c',
                },
                dark: '#1B1B1B',
                muted: '#6D6D6D',
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            borderRadius: {
                '2.5xl': '20px',
                '3xl': '24px',
                '4xl': '28px',
            },
            boxShadow: {
                'card': '0 4px 20px rgba(0,0,0,0.06)',
                'card-hover': '0 10px 30px rgba(0,0,0,0.10)',
                'glow-green': '0 0 20px rgba(76, 175, 80, 0.15)',
                'glow-gold': '0 0 20px rgba(212, 163, 115, 0.15)',
                'bottom-nav': '0 -4px 20px rgba(0,0,0,0.08)',
            },
            animation: {
                'fade-in': 'fadeIn 0.5s ease-out forwards',
                'fade-in-up': 'fadeInUp 0.6s ease-out forwards',
                'slide-up': 'slideUp 0.5s ease-out forwards',
                'slide-left': 'slideLeft 0.4s ease-out forwards',
                'scale-in': 'scaleIn 0.4s ease-out forwards',
                'shimmer': 'shimmer 1.5s infinite linear',
                'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'ripple': 'ripple 0.6s ease-out',
                'float': 'float 6s ease-in-out infinite',
                'wave-bar': 'waveBar 0.5s ease-in-out infinite alternate',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                fadeInUp: {
                    '0%': { opacity: '0', transform: 'translateY(24px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(20px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                slideLeft: {
                    '0%': { transform: 'translateX(30px)', opacity: '0' },
                    '100%': { transform: 'translateX(0)', opacity: '1' },
                },
                scaleIn: {
                    '0%': { transform: 'scale(0.9)', opacity: '0' },
                    '100%': { transform: 'scale(1)', opacity: '1' },
                },
                shimmer: {
                    '0%': { backgroundPosition: '-200% 0' },
                    '100%': { backgroundPosition: '200% 0' },
                },
                pulseSoft: {
                    '0%, 100%': { opacity: '1', transform: 'scale(1)' },
                    '50%': { opacity: '.85', transform: 'scale(1.04)' },
                },
                ripple: {
                    '0%': { transform: 'scale(0)', opacity: '0.5' },
                    '100%': { transform: 'scale(4)', opacity: '0' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-8px)' },
                },
                waveBar: {
                    '0%': { height: '12%' },
                    '100%': { height: '90%' },
                },
            },
        },
    },
    plugins: [],
}
