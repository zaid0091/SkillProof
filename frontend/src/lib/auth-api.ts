import { api, setAccessToken } from './api';

export type Role = 'student' | 'employer' | 'university' | 'administrator';

export type AuthUser = {
	id: string;
	email: string;
	full_name: string;
	display_name: string;
	role: Role;
	is_verified: boolean;
	date_joined: string;
};

export type RegisterInput = {
	email: string;
	password: string;
	full_name?: string;
	role?: Exclude<Role, 'administrator'>;
};

const HOME_BY_ROLE: Record<Role, string> = {
	student: '/dashboard/student',
	employer: '/dashboard/employer',
	university: '/dashboard/university',
	administrator: '/dashboard/admin',
};

export function dashboardPathFor(role: Role): string {
	return HOME_BY_ROLE[role] ?? '/dashboard';
}

// --- API calls ---------------------------------------------------------------

export async function register(input: RegisterInput): Promise<{ user: AuthUser; detail: string }> {
	const { data } = await api.post('/auth/register/', input);
	return data;
}

export async function login(email: string, password: string): Promise<AuthUser> {
	const { data } = await api.post<{ access: string; user: AuthUser }>('/auth/login/', {
		email,
		password,
	});
	setAccessToken(data.access);
	return data.user;
}

export async function logout(): Promise<void> {
	try {
		await api.post('/auth/logout/');
	} finally {
		setAccessToken(null);
	}
}

export async function fetchMe(): Promise<AuthUser> {
	const { data } = await api.get<{ user: AuthUser }>('/auth/me/');
	return data.user;
}

export async function verifyEmail(token: string): Promise<{ user: AuthUser; detail: string }> {
	const { data } = await api.post('/auth/verify-email/', { token });
	return data;
}

export async function resendVerification(): Promise<{ detail: string }> {
	const { data } = await api.post('/auth/resend-verification/');
	return data;
}

export async function requestPasswordReset(email: string): Promise<{ detail: string }> {
	const { data } = await api.post('/auth/password-reset/', { email });
	return data;
}

export async function confirmPasswordReset(token: string, newPassword: string): Promise<{ detail: string }> {
	const { data } = await api.post('/auth/password-reset/confirm/', {
		token,
		new_password: newPassword,
	});
	return data;
}