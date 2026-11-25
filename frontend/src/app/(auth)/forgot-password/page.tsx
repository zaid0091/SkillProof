'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Alert, AuthShell, Button, Field, TextInput } from '@/components/auth-ui';
import { apiErrorMessage } from '@/lib/api';
import { requestPasswordReset } from '@/lib/auth-api';

const schema = z.object({
	email: z.email('Enter a valid email address.'),
});

type FormValues = z.infer<typeof schema>;

export default function ForgotPasswordPage() {
	const mutation = useMutation({
		mutationFn: (values: FormValues) => requestPasswordReset(values.email),
	});

	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<FormValues>({ resolver: zodResolver(schema), defaultValues: { email: '' } });

	return (
		<AuthShell
			title="Reset your password"
			subtitle="Enter your account email and we will send a single-use reset link. The response is the same whether or not the account exists."
			footer={
				<>
					Remembered it?{' '}
					<Link className="font-bold underline" href="/login">
						Back to sign in
					</Link>
				</>
			}
		>
			{mutation.isSuccess ? (
				<Alert tone="success">
					If an account exists for that address, a reset link has been sent. The link expires in 60 minutes and
					works once.
				</Alert>
			) : (
				<form className="grid gap-5" onSubmit={handleSubmit((values) => mutation.mutate(values))} noValidate>
					{mutation.isError ? <Alert>{apiErrorMessage(mutation.error, 'Could not send the reset email.')}</Alert> : null}
					<Field label="Email" error={errors.email?.message}>
						<TextInput
							type="email"
							autoComplete="email"
							placeholder="you@example.com"
							aria-label="Email"
							{...register('email')}
						/>
					</Field>
					<Button type="submit" disabled={isSubmitting || mutation.isPending}>
						{mutation.isPending ? 'Sending…' : 'Send reset link'}
					</Button>
				</form>
			)}
		</AuthShell>
	);
}