import axios from 'axios';
import {useAuth} from "../context";

export const PORT = process.env.BACKEND_PORT || 8000
const apiClient = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL ? `${process.env.REACT_APP_BASE_URL}/api/` : `http://127.0.0.1:8000/api/`,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const useApiInterceptors = () => {
    const authContext = useAuth();

    if (!authContext) return;

    const { logout, refreshAccessToken, tokensRef} = authContext;

    apiClient.interceptors.request.use((config) => {
        if (tokensRef?.access) {
            config.headers.Authorization = `Bearer ${tokensRef.access}`;
        }
        return config;
    }, (error) => {
        return Promise.reject(error);
    });

    apiClient.interceptors.response.use(
        (config) => {
            return config;
        },
        async (error) => {
            const originalRequest = error.config;
            if (error.response.status === 401 &&  error.config && !error.config._retry) {
                originalRequest._retry = true;
                try {
                    const accessToken = await refreshAccessToken();
                    apiClient.defaults.headers.common.Authorization = `Bearer ${accessToken}`;
                    originalRequest.headers.Authorization = `Bearer ${accessToken}`;
                    console.log('refreshing')
                    return apiClient(originalRequest);
                } catch (e) {
                    console.error('Refreshing token error', e);
                    logout();
                }
            }
            throw error;
        }
    );
    return apiClient;
};

export default apiClient;
