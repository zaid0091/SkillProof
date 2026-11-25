import { create } from 'zustand';
import type { AuthUser } from '@/lib/auth-api';

export type AuthStatus = 'unknown' | 'loading' | 'authenticated' | 'anonymous';

type AuthState = {
	user: AuthUser | null;
	status: AuthStatus;
	setUser: (user: AuthUser) => void;
	setLoading: () => void;
	clear: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
	user: null,
	status: 'unknown',
	setUser: (user) => set({ user, status: 'authenticated' }),
	setLoading: () => set({ status: 'loading' }),
	clear: () => set({ user: null, status: 'anonymous' }),
}));