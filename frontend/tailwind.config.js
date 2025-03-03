/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f5f7ff',
                    100: '#ebf0fe',
                    200: '#d6e0fd',
                    300: '#b3c6fb',
                    400: '#8aa3f8',
                    500: '#6180f4',
                    600: '#3d5eeb',
                    700: '#2e48d9',
                    800: '#2839b6',
                    900: '#253494',
                },
                secondary: {
                    50: '#f8f9fa',
                    100: '#f1f3f5',
                    200: '#e9ecef',
                    300: '#dee2e6',
                    400: '#ced4da',
                    500: '#adb5bd',
                    600: '#868e96',
                    700: '#495057',
                    800: '#343a40',
                    900: '#212529',
                },
            },
            fontFamily: {
                sans: ['Inter var', 'sans-serif'],
            },
        },
    },
    plugins: [],
} 