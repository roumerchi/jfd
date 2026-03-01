import axios from "axios";
import {PORT} from "../hooks/useApiInterceptors";

export default class AuthService {
    static async login(username, password) {
        try {
            const response = await axios.post(`http://127.0.0.1:${PORT}/api/token/`, {username, password})
            return response.data;
        } catch (e) {
            throw e;
        }
    }
    static async verifyAccessTokenApi(token) {
        try {
            const response = await axios.post(`http://127.0.0.1:${PORT}/api/token/verify/`, {token: token})
            return response.data;
        } catch (e) {
            console.log(e)
        }
    }
    static async refreshAccessTokenApi(token) {
        try {
            const response = await axios.post(`http://127.0.0.1:${PORT}/api/token/refresh/`, {refresh: token})
            return response.data;
        } catch (e) {
            console.log(e)
        }
    }
}