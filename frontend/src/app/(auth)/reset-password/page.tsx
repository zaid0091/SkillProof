'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Alert, AuthShell, Button, Field, TextInput } from '@/components/auth-ui';
import { apiErrorMessage } from '@/lib/api';
import { confirmPasswordReset } from '@/lib/auth-api';

const schema = z
	.object({
		new_password: z
			.string()
			.min(10, 'Use at least 10 characters.')
			.regex(/[a-zA-Z]/, 'Include at least one letter.')
			.regex(/[0-9]/, 'Include at least one number.'),
		confirm_password: z.string(),
	})
	.refine((values) => values.new_password === values.confirm_password, {
		message: 'Both passwords must match.',
		path: ['confirm_password'],
	});

type FormValues = z.infer<typeof schema>;

function ResetPasswordForm() {
	const router = useRouter();
	const searchParams = useSearchParams();
	const token = searchParams.get('token') ?? '';

	const mutation = useMutation({
		mutationFn: (values: FormValues) => confirmPasswordReset(token, values.new_password),
		onSuccess: () => router.replace('/login?reset=1'),
	});

	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<FormValues>({
		resolver: zodResolver(schema),
		defaultValues: { new_password: '', confirm_password: '' },
	});

	if (!token) {
		return (
			<AuthShell title="Reset link missing" subtitle="This page needs the single-use link from your reset email.">
				<Alert>The reset link is missing or incomplete. Request a new link and open it directly.</Alert>
				<div className="mt-5">
					<Link href="/forgot-password">
						<Button variant="secondary">Request a new link</Button>
					</Link>
				</div>
			</AuthShell>
		);
	}

	return (
		<AuthShell
			title="Choose a new password"
			subtitle="This link works once. After the change, every other session is signed out."
			footer={
				<>
					Back to{' '}
					<Link className="font-bold underline" href="/login">
						sign in
					</Link>
				</>
			}
		>
			<form className="grid gap-5" onSubmit={handleSubmit((values) => mutation.mutate(values))} noValidate>
				{mutation.isError ? <Alert>{apiErrorMessage(mutation.error, 'Could not update the password.')}</Alert> : null}
				<Field
					label="New password"
					hint="At least 10 characters, with letters and numbers."
					error={errors.new_password?.message}
				>
					<TextInput type="password" autoComplete="new-password" aria-label="New password" {...register('new_password')} />
				</Field>
				<Field label="Confirm new password" error={errors.confirm_password?.message}>
					<TextInput
						type="password"
						autoComplete="new-password"
						aria-label="Confirm new password"
						{...register('confirm_password')}
					/>
				</Field>
				<Button type="submit" disabled={isSubmitting || mutation.isPending}>
					{mutation.isPending ? 'Updating…' : 'Update password'}
				</Button>
			</form>
		</AuthShell>
	);
}

export default function ResetPasswordPage() {
	return (
		<Suspense fallback={<div className="p-10 text-center text-sm font-bold text-ink/60">Loading…</div>}>
			<ResetPasswordForm />
		</Suspense>
	);
}