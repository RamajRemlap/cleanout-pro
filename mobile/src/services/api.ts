/**
 * API Service - Backend communication
 */

import axios, { AxiosInstance } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Customer, Job, Room } from '../types';

// Use localhost for Android emulator (10.0.2.2) or your machine IP
const API_BASE_URL = __DEV__
  ? 'http://10.0.2.2:8000'  // Android emulator
  : process.env.API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth token (future)
    this.client.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  // Customer endpoints
  async getCustomers(): Promise<Customer[]> {
    const response = await this.client.get('/api/customers');
    return response.data;
  }

  async getCustomer(id: string): Promise<Customer> {
    const response = await this.client.get(`/api/customers/${id}`);
    return response.data;
  }

  async createCustomer(customer: Partial<Customer>): Promise<Customer> {
    const response = await this.client.post('/api/customers', customer);
    return response.data;
  }

  // Job endpoints
  async getJobs(customerId?: string): Promise<Job[]> {
    const params = customerId ? { customer_id: customerId } : {};
    const response = await this.client.get('/api/jobs', { params });
    return response.data;
  }

  async getJob(id: string): Promise<Job> {
    const response = await this.client.get(`/api/jobs/${id}`);
    return response.data;
  }

  async createJob(job: Partial<Job>): Promise<Job> {
    const response = await this.client.post('/api/jobs', job);
    return response.data;
  }

  async updateJob(id: string, job: Partial<Job>): Promise<Job> {
    const response = await this.client.put(`/api/jobs/${id}`, job);
    return response.data;
  }

  // Room endpoints
  async getRooms(jobId?: string): Promise<Room[]> {
    const params = jobId ? { job_id: jobId } : {};
    const response = await this.client.get('/api/rooms', { params });
    return response.data;
  }

  async getRoom(id: string): Promise<Room> {
    const response = await this.client.get(`/api/rooms/${id}`);
    return response.data;
  }

  /**
   * Upload room image for AI classification
   *
   * @param jobId - Job ID
   * @param roomName - Room name (e.g., "Master Bedroom")
   * @param roomNumber - Room sequence number
   * @param imageUri - Local image file URI
   */
  async uploadRoom(
    jobId: string,
    roomName: string,
    roomNumber: number,
    imageUri: string
  ): Promise<Room> {
    const formData = new FormData();
    formData.append('job_id', jobId);
    formData.append('room_name', roomName);
    formData.append('room_number', roomNumber.toString());

    // Extract filename from URI
    const filename = imageUri.split('/').pop() || 'photo.jpg';
    const match = /\.(\w+)$/.exec(filename);
    const type = match ? `image/${match[1]}` : 'image/jpeg';

    formData.append('image', {
      uri: imageUri,
      name: filename,
      type,
    } as any);

    const response = await this.client.post('/api/rooms', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // AI classification can take 10-30s
    });

    return response.data;
  }

  async deleteRoom(id: string): Promise<void> {
    await this.client.delete(`/api/rooms/${id}`);
  }

  /**
   * Override room AI classification (human adjustment)
   */
  async overrideRoomClassification(
    id: string,
    override: {
      human_size_class?: string;
      human_workload_class?: string;
      human_override_reason?: string;
    }
  ): Promise<Room> {
    const response = await this.client.patch(`/api/rooms/${id}`, override);
    return response.data;
  }
}

export default new ApiService();
