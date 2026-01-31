import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const uploadHumming = async (audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'humming.wav');
    
    try {
        const response = await axios.post(`${API_BASE_URL}/upload-humming`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Upload failed';
    }
};

export const getSongs = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/songs`);
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Failed to fetch songs';
    }
};

export const healthCheck = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/health`);
        return response.data;
    } catch (error) {
        throw error.response?.data?.error || 'Health check failed';
    }
};