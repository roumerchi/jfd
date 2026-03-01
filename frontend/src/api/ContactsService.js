import apiClient from "../hooks/useApiInterceptors";

export default class ContactsService {
    static async getContacts(page) {
        const response = await apiClient.get(`/contacts/?page=${page}`)
        return response.data
    }
    static async createContact(data) {
        const response = await apiClient.post(`/contacts/`, data);
        return response.data
    }
    static async removeContacts(pk) {
        const response = await apiClient.delete(`/contacts/${pk}/`);
        return response.data
    }
}