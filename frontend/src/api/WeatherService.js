import apiClient from "../hooks/useApiInterceptors";

export default class WeatherService {
    static async getWeather(city) {
        const response = await apiClient.get(`/weather/?city=${city}`)
        return response.data
    }
}