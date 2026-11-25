'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, type ReactNode } from 'react';
import { Alert, Button } from '@/components/auth-ui';
import { apiErrorMessage } from '@/lib/api';
import { dashboardPathFor, fetchMe, resendVerification, type Role } from '@/lib/auth-api';
import { useAuthStore } from '@/stores/auth-store';

/**
 * Client-side route guard.
 *
 * This is a UX layer only: every protected resource is independently enforced
 * by the Django API (docs/sacs.md section 4.1 — hiding UI is not authorization).
 * It resolves the real session through GET /auth/me/, which also exercises the
 * silent refresh path.
 */

export function AccessDenied({ requiredRole }: { requiredRole?: Role }) {
	const user = useAuthStore((state) => state.user);
	const home = user ? dashboardPathFor(user.role) : '/dashboard';

	return (
		<div className="border-2 border-ink bg-white p-8">
			<h2 className="text-2xl font-black tracking-tight">Access denied</h2>
			<p className="mt-3 text-sm leading-relaxed text-ink/70">
				{requiredRole
					? `This area is for ${requiredRole} accounts. Your account role does not permit this view.`
					: 'Your account role does not permit this view.'}
			</p>
			<div className="mt-6">
				<Link href={home}>
					<Button variant="secondary">Go to your dashboard</Button>
				</Link>
			</div>
		</div>
	);
}

function VerificationBanner() {
	const user = useAuthStore((state) => state.user);
	const mutation = useMutation({
		mutationFn: resendVerification,
		onSuccess: () => {
			mutation.reset();
		},
	});

	if (!user || user.is_verified) return null;

	return (
		<div className="mb-6">
			<Alert tone="info">
				<div className="flex flex-wrap items-center justify-between gap-3">
					<span>
						Your email address is not verified yet. Reads work, but sensitive actions stay locked until you
						verify.
					</span>
					<div className="flex items-center gap-3">
						{mutation.isSuccess ? <span className="font-semibold">Verification email sent.</span> : null}
						{mutation.isError ? <span className="font-semibold text-signal">{apiErrorMessage(mutation.error)}</span> : null}
						<button
							type="button"
							onClick={() => mutation.mutate()}
							disabled={mutation.isPending}
							className="border-2 border-ink px-3 py-1.5 text-xs font-bold disabled:opacity-50"
						>
							{mutation.isPending ? 'Sending…' : 'Resend email'}
						</button>
					</div>
				</div>
			</Alert>
		</div>
	);
}

export function AuthGate({
	requiredRole,
	children,
}: {
	requiredRole?: Role;
	children: ReactNode;
}) {
	const router = useRouter();
	const pathname = usePathname();
	const queryClient = useQueryClient();
	const { setUser, clear, setLoading } = useAuthStore();

	const me = useQuery({
		queryKey: ['auth', 'me'],
		queryFn: fetchMe,
		retry: false,
		staleTime: 60_000,
	});

	useEffect(() => {
		if (me.isPending) setLoading();
	}, [me.isPending, setLoading]);

	useEffect(() => {
		if (me.data) setUser(me.data);
	}, [me.data, setUser]);

	useEffect(() => {
		if (me.isError) {
			clear();
			queryClient.clear();
			router.replace(`/login?next=${encodeURIComponent(pathname)}`);
		}
	}, [me.isError, clear, queryClient, router, pathname]);

	if (me.isPending || me.isError) {
		return (
			<div className="flex min-h-64 items-center justify-center text-sm font-bold text-ink/60" role="status">
				Checking your session…
			</div>
		);
	}

	if (requiredRole && me.data?.role !== requiredRole) {
		return <AccessDenied requiredRole={requiredRole} />;
	}

	return (
		<>
			<VerificationBanner />
			{children}
		</>
	);
}