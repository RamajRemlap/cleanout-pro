/**
 * Global State Management using Zustand
 */

import { create } from 'zustand';
import { Job, Room, Customer } from '../types';

interface AppState {
  // Current job being worked on
  currentJob: Job | null;
  setCurrentJob: (job: Job | null) => void;

  // Current customer
  currentCustomer: Customer | null;
  setCurrentCustomer: (customer: Customer | null) => void;

  // Rooms for current job
  rooms: Room[];
  setRooms: (rooms: Room[]) => void;
  addRoom: (room: Room) => void;
  updateRoom: (id: string, room: Partial<Room>) => void;
  removeRoom: (id: string) => void;

  // Offline mode
  isOffline: boolean;
  setOffline: (offline: boolean) => void;

  // Sync status
  pendingSyncCount: number;
  setPendingSyncCount: (count: number) => void;

  // Loading states
  isLoading: boolean;
  setLoading: (loading: boolean) => void;

  // Clear all state
  clearState: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  currentJob: null,
  currentCustomer: null,
  rooms: [],
  isOffline: false,
  pendingSyncCount: 0,
  isLoading: false,

  // Actions
  setCurrentJob: (job) => set({ currentJob: job }),
  setCurrentCustomer: (customer) => set({ currentCustomer: customer }),

  setRooms: (rooms) => set({ rooms }),
  addRoom: (room) => set((state) => ({ rooms: [...state.rooms, room] })),
  updateRoom: (id, updates) =>
    set((state) => ({
      rooms: state.rooms.map((room) =>
        room.id === id ? { ...room, ...updates } : room
      ),
    })),
  removeRoom: (id) =>
    set((state) => ({
      rooms: state.rooms.filter((room) => room.id !== id),
    })),

  setOffline: (offline) => set({ isOffline: offline }),
  setPendingSyncCount: (count) => set({ pendingSyncCount: count }),
  setLoading: (loading) => set({ isLoading: loading }),

  clearState: () =>
    set({
      currentJob: null,
      currentCustomer: null,
      rooms: [],
      isOffline: false,
      pendingSyncCount: 0,
      isLoading: false,
    }),
}));
