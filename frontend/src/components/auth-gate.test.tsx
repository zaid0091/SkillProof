import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { ReactNode } from 'react';
import type { AuthUser } from '@/lib/auth-api';
import { AuthGate } from './auth-gate';

const mocks = vi.hoisted(() => ({
	replace: vi.fn(),
	fetchMe: vi.fn(),
	resendVerification: vi.fn(),
}));

vi.mock('next/navigation', () => ({
	useRouter: () => ({ replace: mocks.replace }),
	usePathname: () => '/dashboard/student',
}));

vi.mock('@/lib/auth-api', () => ({
	fetchMe: mocks.fetchMe,
	resendVerification: mocks.resendVerification,
	dashboardPathFor: (role: string) => `/dashboard/${role}`,
}));

const student: AuthUser = {
	id: 'u-1',
	email: 'ada@example.com',
	full_name: 'Ada Lovelace',
	display_name: 'Ada',
	role: 'student',
	is_verified: true,
	date_joined: '2026-01-01T00:00:00Z',
};

function renderGate(children: ReactNode, requiredRole?: AuthUser['role']) {
	const client = new QueryClient();
	return render(
		<QueryClientProvider client={client}>
			<AuthGate requiredRole={requiredRole}>{children}</AuthGate>
		</QueryClientProvider>,
	);
}

beforeEach(() => {
	vi.clearAllMocks();
});

describe('AuthGate', () => {
	it('shows a session check while the session resolves', () => {
		mocks.fetchMe.mockReturnValue(new Promise(() => undefined));

		renderGate(<p>Protected content</p>);

		expect(screen.getByRole('status')).toHaveTextContent(/checking your session/i);
		expect(screen.queryByText('Protected content')).not.toBeInTheDocument();
	});

	it('redirects to login when the session is invalid', async () => {
		mocks.fetchMe.mockRejectedValue(new Error('401'));

		renderGate(<p>Protected content</p>);

		await waitFor(() =>
			expect(mocks.replace).toHaveBeenCalledWith('/login?next=%2Fdashboard%2Fstudent'),
		);
		expect(screen.queryByText('Protected content')).not.toBeInTheDocument();
	});

	it('renders children for the matching role', async () => {
		mocks.fetchMe.mockResolvedValue(student);

		renderGate(<p>Protected content</p>, 'student');

		expect(await screen.findByText('Protected content')).toBeInTheDocument();
	});

	it('renders an access-denied state for a different role', async () => {
		mocks.fetchMe.mockResolvedValue(student);

		renderGate(<p>Protected content</p>, 'employer');

		expect(await screen.findByRole('heading', { name: /access denied/i })).toBeInTheDocument();
		expect(screen.queryByText('Protected content')).not.toBeInTheDocument();
	});

	it('warns unverified accounts and offers to resend the verification email', async () => {
		mocks.fetchMe.mockResolvedValue({ ...student, is_verified: false });

		renderGate(<p>Protected content</p>, 'student');

		expect(await screen.findByText(/not verified yet/i)).toBeInTheDocument();
		expect(screen.getByRole('button', { name: /resend email/i })).toBeInTheDocument();
	});
});