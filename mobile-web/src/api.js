import axios from 'axios';

class ApiClient {
  constructor() {
    this.baseURL = 'http://localhost:8000';
  }

  setBaseURL(url) {
    this.baseURL = url;
  }

  async getJobs() {
    const response = await axios.get(`${this.baseURL}/api/jobs`);
    return response.data;
  }

  async getJob(id) {
    const response = await axios.get(`${this.baseURL}/api/jobs/${id}`);
    return response.data;
  }

  async getRooms(jobId) {
    const response = await axios.get(`${this.baseURL}/api/rooms`, {
      params: { job_id: jobId },
    });
    return response.data;
  }

  async uploadRoom(jobId, roomName, roomNumber, imageBlob) {
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('room_name', roomName);
    formData.append('room_number', roomNumber.toString());
    formData.append('image', imageBlob, 'room.jpg');

    const response = await axios.post(`${this.baseURL}/api/rooms`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 seconds for AI processing
    });
    return response.data;
  }

  async healthCheck() {
    try {
      const response = await axios.get(`${this.baseURL}/health`, {
        timeout: 5000,
      });
      return response.status === 200;
    } catch {
      return false;
    }
  }
}

export default new ApiClient();
