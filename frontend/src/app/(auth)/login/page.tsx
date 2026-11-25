'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Alert, AuthShell, Button, Field, TextInput } from '@/components/auth-ui';
import { apiErrorMessage } from '@/lib/api';
import { dashboardPathFor, login } from '@/lib/auth-api';
import { useAuthStore } from '@/stores/auth-store';

const schema = z.object({
	email: z.email('Enter a valid email address.'),
	password: z.string().min(1, 'Enter your password.'),
});

type FormValues = z.infer<typeof schema>;

function LoginForm() {
	const router = useRouter();
	const searchParams = useSearchParams();
	const setUser = useAuthStore((state) => state.setUser);
	const queryClient = useQueryClient();
	const next = searchParams.get('next');

	const mutation = useMutation({
		mutationFn: (values: FormValues) => login(values.email, values.password),
		onSuccess: (user) => {
			setUser(user);
			queryClient.setQueryData(['auth', 'me'], user);
			router.replace(next && next.startsWith('/') ? next : dashboardPathFor(user.role));
		},
	});

	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<FormValues>({
		resolver: zodResolver(schema),
		defaultValues: { email: '', password: '' },
	});

	return (
		<AuthShell
			title="Sign in"
			subtitle="Access your verified skill workspace."
			footer={
				<>
					New to SkillProof?{' '}
					<Link className="font-bold underline" href="/register">
						Create an account
					</Link>
				</>
			}
		>
			<form className="grid gap-5" onSubmit={handleSubmit((values) => mutation.mutate(values))} noValidate>
				{mutation.isError ? <Alert>{apiErrorMessage(mutation.error, 'Sign in failed.')}</Alert> : null}
				<Field label="Email" error={errors.email?.message}>
					<TextInput
						type="email"
						autoComplete="email"
						placeholder="you@example.com"
						aria-label="Email"
						{...register('email')}
					/>
				</Field>
				<Field label="Password" error={errors.password?.message}>
					<TextInput type="password" autoComplete="current-password" aria-label="Password" {...register('password')} />
				</Field>
				<Button type="submit" disabled={isSubmitting || mutation.isPending}>
					{mutation.isPending ? 'Signing in…' : 'Sign in'}
				</Button>
				<Link href="/forgot-password" className="text-sm font-semibold text-blue underline">
					Forgot your password?
				</Link>
			</form>
		</AuthShell>
	);
}

export default function LoginPage() {
	return (
		<Suspense fallback={<div className="p-10 text-center text-sm font-bold text-ink/60">Loading…</div>}>
			<LoginForm />
		</Suspense>
	);
}