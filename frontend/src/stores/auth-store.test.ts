import { describe, expect, it } from 'vitest';
import { useAuthStore } from './auth-store';
import type { AuthUser } from '@/lib/auth-api';

const user: AuthUser = {
	id: 'u-1',
	email: 'ada@example.com',
	full_name: 'Ada',
	display_name: 'Ada',
	role: 'student',
	is_verified: false,
	date_joined: '2026-01-01T00:00:00Z',
};

describe('auth store', () => {
	it('moves through loading, authenticated, and anonymous states', () => {
		const store = useAuthStore.getState();

		store.clear();
		expect(useAuthStore.getState().status).toBe('anonymous');
		expect(useAuthStore.getState().user).toBeNull();

		store.setLoading();
		expect(useAuthStore.getState().status).toBe('loading');

		store.setUser(user);
		expect(useAuthStore.getState().status).toBe('authenticated');
		expect(useAuthStore.getState().user?.email).toBe('ada@example.com');

		store.clear();
		expect(useAuthStore.getState().status).toBe('anonymous');
		expect(useAuthStore.getState().user).toBeNull();
	});
});