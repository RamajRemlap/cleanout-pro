import { create } from 'zustand';

export const useStore = create((set) => ({
  // API configuration
  apiUrl: 'http://localhost:8000',
  setApiUrl: (url) => set({ apiUrl: url }),

  // Current selections
  currentJob: null,
  setCurrentJob: (job) => set({ currentJob: job }),

  currentRoom: null,
  setCurrentRoom: (room) => set({ currentRoom: room }),

  // Data
  jobs: [],
  setJobs: (jobs) => set({ jobs }),

  rooms: [],
  setRooms: (rooms) => set({ rooms }),
  addRoom: (room) => set((state) => ({ rooms: [...state.rooms, room] })),

  // UI state
  loading: false,
  setLoading: (loading) => set({ loading }),

  error: null,
  setError: (error) => set({ error }),
}));
