import {createContext, useContext, useRef, useState} from "react";
import AuthService from "../api/AuthService";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuth, setIsAuth] = useState(false);
    const tokensRef = useRef({ access: null });

    const login = async (username, password) => {
        try {
            const data = await AuthService.login(username, password);
            localStorage.setItem('token', data.refresh)
            tokensRef.current = { access: data.access, refresh: data.refresh };
            setIsAuth(true);
        } catch (e) {
            console.error("Login failed:", e);
        }
    };

    const logout = () => {
        setIsAuth(false);
        localStorage.removeItem('token')
    };

    const refreshAccessToken = async () => {
        try {
            const refreshToken = localStorage.getItem('token')
            const data = await AuthService.refreshAccessTokenApi(refreshToken);
            tokensRef.current = { access: data.access, refresh: refreshToken };
            return data.access
        } catch (e) {
            console.error("Token refreshing failed:", e);
            logout();
        }
    };

    return (
        <AuthContext.Provider value={{ isAuth, setIsAuth, login, logout, refreshAccessToken, tokensRef }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};