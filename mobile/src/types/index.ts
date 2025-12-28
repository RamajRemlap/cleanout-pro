/**
 * Core TypeScript types for CleanoutPro Mobile
 */

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  address: string;
  created_at: string;
}

export interface Job {
  id: string;
  customer_id: string;
  customer?: Customer;
  job_number: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  scheduled_date?: string;
  completion_date?: string;

  // Pricing
  base_estimate: number;
  ai_estimate: number;
  human_adjusted_estimate?: number;
  final_price: number;

  // Job details
  notes?: string;
  bin_rental?: string;
  stairs_flights?: number;
  difficult_access?: boolean;

  created_at: string;
  updated_at: string;
}

export interface Room {
  id: string;
  job_id: string;
  name: string;
  room_number: number;
  image_url?: string;

  // AI Classification
  ai_size_class?: 'small' | 'medium' | 'large' | 'extra_large';
  ai_workload_class?: 'light' | 'moderate' | 'heavy' | 'extreme';
  ai_confidence?: number;
  ai_reasoning?: string;
  ai_features?: Record<string, any>;

  // Human Overrides
  human_size_class?: 'small' | 'medium' | 'large' | 'extra_large';
  human_workload_class?: 'light' | 'moderate' | 'heavy' | 'extreme';
  human_override_reason?: string;

  // Final Classification
  final_size_class: 'small' | 'medium' | 'large' | 'extra_large';
  final_workload_class: 'light' | 'moderate' | 'heavy' | 'extreme';

  // Pricing
  estimated_cost: number;

  captured_at: string;
  processed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface SyncOperation {
  id: string;
  operation_type: 'create' | 'update' | 'delete';
  entity_type: 'customer' | 'job' | 'room';
  entity_id: string;
  data: any;
  timestamp: string;
  synced: boolean;
}

export type SizeClass = 'small' | 'medium' | 'large' | 'extra_large';
export type WorkloadClass = 'light' | 'moderate' | 'heavy' | 'extreme';
export type JobStatus = 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
