import apiClient from "../hooks/useApiInterceptors";

export default class ContactsService {
    static async getContacts(page = 1, ordering = '') {
        const params = new URLSearchParams();
        params.set('page', page);
        if (ordering) params.set('ordering', ordering);
        const response = await apiClient.get(`/contacts/?${params.toString()}`);
        return response.data;
    }
    static async createContact(data) {
        const response = await apiClient.post(`/contacts/`, data);
        return response.data
    }
    static async bulkImport(file) {
        const formData = new FormData();
        formData.append('file', file);
        const response = await apiClient.post('/contacts/bulk/', formData, {headers: {'Content-Type': undefined}})
        return response.data;
    }
    static async removeContacts(pk) {
        const response = await apiClient.delete(`/contacts/${pk}/`);
        return response.data
    }
}