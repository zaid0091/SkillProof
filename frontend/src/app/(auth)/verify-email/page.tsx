'use client';

import { useMutation } from '@tanstack/react-query';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Suspense, useEffect } from 'react';
import { Alert, AuthShell, Button } from '@/components/auth-ui';
import { apiErrorMessage } from '@/lib/api';
import { verifyEmail } from '@/lib/auth-api';

function VerifyEmailPanel() {
	const searchParams = useSearchParams();
	const token = searchParams.get('token') ?? '';

	const mutation = useMutation({
		mutationFn: () => verifyEmail(token),
	});

	useEffect(() => {
		if (token) mutation.mutate();
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [token]);

	return (
		<AuthShell
			title="Email verification"
			subtitle="Verification unlocks sensitive actions on your account."
			footer={
				<>
					Continue to{' '}
					<Link className="font-bold underline" href="/login">
						sign in
					</Link>
				</>
			}
		>
			{!token ? (
				<Alert>
					This page needs the verification link from your email. Open the link directly, or request a new one after
					signing in.
				</Alert>
			) : mutation.isPending || mutation.isIdle ? (
				<div role="status" className="text-sm font-bold text-ink/60">
					Verifying your email…
				</div>
			) : mutation.isError ? (
				<Alert>
					{apiErrorMessage(mutation.error, 'This verification link is invalid or has expired.')}
					{' '}
					Sign in and use “Resend email” to get a fresh link.
				</Alert>
			) : (
				<Alert tone="success">
					{mutation.data?.detail ?? 'Email address verified.'} Your account is fully active.
				</Alert>
			)}
			<div className="mt-6">
				<Link href="/login">
					<Button variant="secondary">Go to sign in</Button>
				</Link>
			</div>
		</AuthShell>
	);
}

export default function VerifyEmailPage() {
	return (
		<Suspense fallback={<div className="p-10 text-center text-sm font-bold text-ink/60">Loading…</div>}>
			<VerifyEmailPanel />
		</Suspense>
	);
}