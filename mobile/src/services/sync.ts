/**
 * Offline Sync Service
 * Handles offline operations and syncs when online
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import { SyncOperation } from '../types';
import apiService from './api';

const SYNC_QUEUE_KEY = 'sync_queue';

class SyncService {
  private queue: SyncOperation[] = [];
  private isSyncing: boolean = false;

  async init(): Promise<void> {
    await this.loadQueue();
  }

  private async loadQueue(): Promise<void> {
    try {
      const queueData = await AsyncStorage.getItem(SYNC_QUEUE_KEY);
      if (queueData) {
        this.queue = JSON.parse(queueData);
      }
    } catch (error) {
      console.error('Failed to load sync queue:', error);
      this.queue = [];
    }
  }

  private async saveQueue(): Promise<void> {
    try {
      await AsyncStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(this.queue));
    } catch (error) {
      console.error('Failed to save sync queue:', error);
    }
  }

  /**
   * Add operation to sync queue
   */
  async addToQueue(
    operation_type: 'create' | 'update' | 'delete',
    entity_type: 'customer' | 'job' | 'room',
    entity_id: string,
    data: any
  ): Promise<void> {
    const operation: SyncOperation = {
      id: `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      operation_type,
      entity_type,
      entity_id,
      data,
      timestamp: new Date().toISOString(),
      synced: false,
    };

    this.queue.push(operation);
    await this.saveQueue();
  }

  /**
   * Process sync queue (upload pending operations)
   */
  async processQueue(): Promise<{ success: number; failed: number }> {
    if (this.isSyncing || this.queue.length === 0) {
      return { success: 0, failed: 0 };
    }

    this.isSyncing = true;
    let success = 0;
    let failed = 0;

    // Check if backend is reachable
    const isHealthy = await apiService.healthCheck();
    if (!isHealthy) {
      console.log('Backend not reachable, skipping sync');
      this.isSyncing = false;
      return { success: 0, failed: 0 };
    }

    const pendingOps = this.queue.filter((op) => !op.synced);

    for (const op of pendingOps) {
      try {
        await this.processOperation(op);
        op.synced = true;
        success++;
      } catch (error) {
        console.error(`Failed to sync operation ${op.id}:`, error);
        failed++;
      }
    }

    // Remove synced operations
    this.queue = this.queue.filter((op) => !op.synced);
    await this.saveQueue();

    this.isSyncing = false;
    return { success, failed };
  }

  private async processOperation(op: SyncOperation): Promise<void> {
    // This would need to be expanded based on actual backend endpoints
    // For now, this is a placeholder
    console.log(`Processing ${op.operation_type} ${op.entity_type} ${op.entity_id}`);

    // Example implementation:
    // if (op.entity_type === 'room' && op.operation_type === 'create') {
    //   await apiService.uploadRoom(...);
    // }
  }

  /**
   * Get pending operations count
   */
  getPendingCount(): number {
    return this.queue.filter((op) => !op.synced).length;
  }

  /**
   * Clear all synced operations
   */
  async clearSynced(): Promise<void> {
    this.queue = this.queue.filter((op) => !op.synced);
    await this.saveQueue();
  }

  /**
   * Clear all operations (dangerous!)
   */
  async clearAll(): Promise<void> {
    this.queue = [];
    await this.saveQueue();
  }
}

export default new SyncService();
