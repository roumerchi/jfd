import axios from "axios";

export default class AuthService {
    static async login(username, password) {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/token/', {username, password})
            return response.data;
        } catch (e) {
            console.log(e)
        }
    }
    static async verifyAccessTokenApi(token) {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/token/verify/', {token: token})
            return response.data;
        } catch (e) {
            console.log(e)
        }
    }
    static async refreshAccessTokenApi(token) {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {refresh: token})
            return response.data;
        } catch (e) {
            console.log(e)
        }
    }
}