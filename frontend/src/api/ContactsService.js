import apiClient from "../hooks/useApiInterceptors";

export default class ContactsService {
    static async getContacts(pk) {
        const response = await apiClient.get(`/contacts/`)
        return response.data
    }
    static async createContact(pk) {
        const response = await apiClient.get(`/contacts/`);
        return response.data
    }
    static async getContact(pk) {
        const response = await apiClient.get(`/contacts/${pk}/`)
        return response.data
    }
    static async removeContacts(pk) {
        const response = await apiClient.get(`/contacts/${pk}/`);
        return response.data
    }
}