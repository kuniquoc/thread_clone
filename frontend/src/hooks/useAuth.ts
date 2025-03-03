import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '@/services/api';
import type { User } from '@/types';

interface AuthState {
    token: string | null;
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: { email: string; password: string }) => Promise<void>;
    register: (data: { username: string; email: string; password: string; fullName: string }) => Promise<void>;
    logout: () => void;
}

export const useAuth = create<AuthState>()(
    persist(
        (set) => ({
            token: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,

            login: async (credentials) => {
                set({ isLoading: true });
                try {
                    // Convert to form data format
                    const formData = new URLSearchParams();
                    formData.append('username', credentials.email); // OAuth2 uses username field for email
                    formData.append('password', credentials.password);

                    const { data: tokenData } = await api.post('/api/v1/auth/login', formData, {
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                    });

                    // Store token first
                    const token = tokenData.access_token;
                    localStorage.setItem('token', token);

                    // Update axios default headers
                    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

                    // Get user profile
                    const { data: userData } = await api.get('/api/v1/users/me');

                    set({
                        token,
                        user: userData,
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            register: async (userData) => {
                set({ isLoading: true });
                try {
                    // Format the data to match the backend schema
                    const registerData = {
                        email: userData.email,
                        username: userData.username,
                        password: userData.password,
                        full_name: userData.fullName // Match backend field name
                    };

                    // Register the user
                    await api.post('/api/v1/auth/register', registerData);

                    // Login after successful registration
                    await useAuth.getState().login({
                        email: userData.email,
                        password: userData.password
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            logout: () => {
                localStorage.removeItem('token');
                // Clear auth header
                delete api.defaults.headers.common['Authorization'];
                set({ token: null, user: null, isAuthenticated: false, isLoading: false });
            },
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({
                token: state.token,
                user: state.user,
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);

// Authentication API
export const authApi = {
    login: async (email: string, password: string) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const { data: tokenData } = await api.post('/api/v1/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        // Set token in auth header
        api.defaults.headers.common['Authorization'] = `Bearer ${tokenData.access_token}`;

        // Get user data
        const { data: userData } = await api.get('/api/v1/users/me');

        return {
            token: tokenData.access_token,
            user: userData
        };
    },

    register: async (data: {
        email: string;
        password: string;
        username: string;
        fullName: string;
    }) => {
        const registerData = {
            email: data.email,
            username: data.username,
            password: data.password,
            full_name: data.fullName
        };
        return await api.post('/api/v1/auth/register', registerData);
    },

    getCurrentUser: async () => {
        const response = await api.get('/api/v1/users/me');
        return response.data;
    },
}; 