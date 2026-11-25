'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import Link from 'next/link';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Alert, AuthShell, Button, Field, SelectInput, TextInput } from '@/components/auth-ui';
import { apiErrorDetails, apiErrorMessage } from '@/lib/api';
import { register as registerAccount, type RegisterInput } from '@/lib/auth-api';

const schema = z.object({
	full_name: z.string().max(150, 'Keep the name under 150 characters.').optional(),
	email: z.email('Enter a valid email address.'),
	password: z
		.string()
		.min(10, 'Use at least 10 characters.')
		.regex(/[a-zA-Z]/, 'Include at least one letter.')
		.regex(/[0-9]/, 'Include at least one number.'),
	role: z.enum(['student', 'employer', 'university']),
});

type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
	const [done, setDone] = useState(false);

	const mutation = useMutation({
		mutationFn: (values: FormValues) =>
			registerAccount({
				email: values.email,
				password: values.password,
				full_name: values.full_name ?? '',
				role: values.role,
			} satisfies RegisterInput),
		onSuccess: () => setDone(true),
	});

	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<FormValues>({
		resolver: zodResolver(schema),
		defaultValues: { full_name: '', email: '', password: '', role: 'student' },
	});

	const details = apiErrorDetails(mutation.error);
	const fieldError = (name: keyof FormValues) => {
		const fromApi = details?.[name];
		if (Array.isArray(fromApi) && typeof fromApi[0] === 'string') return fromApi[0];
		return undefined;
	};

	if (done) {
		return (
			<AuthShell
				title="Check your email"
				subtitle="Your account is created. Open the verification link we sent to activate sensitive features."
				footer={
					<>
						Already verified?{' '}
						<Link className="font-bold underline" href="/login">
							Sign in
						</Link>
					</>
				}
			>
				<Alert tone="success">
					A verification link is on its way to <strong>{mutation.data?.user.email}</strong>. The link expires in
					72 hours and works once.
				</Alert>
			</AuthShell>
		);
	}

	return (
		<AuthShell
			title="Create your account"
			subtitle="Project-based verification starts with an account type. You can only choose a non-privileged type here."
			footer={
				<>
					Already have an account?{' '}
					<Link className="font-bold underline" href="/login">
						Sign in
					</Link>
				</>
			}
		>
			<form className="grid gap-5" onSubmit={handleSubmit((values) => mutation.mutate(values))} noValidate>
				{mutation.isError ? <Alert>{apiErrorMessage(mutation.error, 'Registration failed.')}</Alert> : null}
				<Field label="Full name" error={errors.full_name?.message ?? fieldError('full_name')}>
					<TextInput
						autoComplete="name"
						placeholder="Ada Lovelace"
						aria-label="Full name"
						{...register('full_name')}
					/>
				</Field>
				<Field label="Email" error={errors.email?.message ?? fieldError('email')}>
					<TextInput
						type="email"
						autoComplete="email"
						placeholder="you@example.com"
						aria-label="Email"
						{...register('email')}
					/>
				</Field>
				<Field
					label="Password"
					hint="At least 10 characters, with letters and numbers."
					error={errors.password?.message ?? fieldError('password')}
				>
					<TextInput type="password" autoComplete="new-password" aria-label="Password" {...register('password')} />
				</Field>
				<Field label="Account type" error={errors.role?.message ?? fieldError('role')}>
					<SelectInput aria-label="Account type" {...register('role')}>
						<option value="student">Student</option>
						<option value="employer">Employer</option>
						<option value="university">University</option>
					</SelectInput>
				</Field>
				<Button type="submit" disabled={isSubmitting || mutation.isPending}>
					{mutation.isPending ? 'Creating account…' : 'Create account'}
				</Button>
			</form>
		</AuthShell>
	);
}