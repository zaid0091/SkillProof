import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode, SelectHTMLAttributes } from 'react';
import Link from 'next/link';
import clsx from 'clsx';

/** Shared neo-brutalist building blocks for the auth surfaces. */

export function AuthShell({
	title,
	subtitle,
	children,
	footer,
}: {
	title: string;
	subtitle?: string;
	children: ReactNode;
	footer?: ReactNode;
}) {
	return (
		<main className="min-h-full bg-paper text-ink">
			<header className="mx-auto flex max-w-360 items-center justify-between px-5 py-5 sm:px-8">
				<Link href="/" className="flex items-center gap-3" aria-label="SkillProof home">
					<span className="grid size-9 place-items-center border-2 border-ink bg-signal text-sm font-black">SP</span>
					<span className="text-lg font-bold tracking-tight">SkillProof</span>
				</Link>
			</header>
			<section className="mx-auto max-w-360 px-5 pb-16 sm:px-8">
				<div className="mx-auto max-w-150 border-2 border-ink bg-white p-6 sm:p-10">
					<h1 className="text-3xl font-black tracking-tight">{title}</h1>
					{subtitle ? <p className="mt-2 text-sm leading-relaxed text-ink/70">{subtitle}</p> : null}
					<div className="mt-8">{children}</div>
					{footer ? <div className="mt-8 border-t-2 border-ink pt-6 text-sm text-ink/70">{footer}</div> : null}
				</div>
			</section>
		</main>
	);
}

export function Field({
	label,
	error,
	hint,
	children,
}: {
	label: string;
	error?: string;
	hint?: string;
	children: ReactNode;
}) {
	return (
		<label className="block">
			<span className="block text-xs font-bold uppercase tracking-[0.12em] text-ink/55">{label}</span>
			<div className="mt-2">{children}</div>
			{hint && !error ? <span className="mt-1 block text-xs text-ink/55">{hint}</span> : null}
			{error ? <span className="mt-1 block text-xs font-semibold text-signal">{error}</span> : null}
		</label>
	);
}

export function TextInput({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
	return (
		<input
			{...props}
			className={clsx(
				'w-full border-2 border-ink bg-paper px-3 py-3 text-sm font-medium outline-none placeholder:text-ink/40 focus:border-blue',
				className,
			)}
		/>
	);
}

export function SelectInput({ className, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
	return (
		<select
			{...props}
			className={clsx(
				'w-full border-2 border-ink bg-paper px-3 py-3 text-sm font-medium outline-none focus:border-blue',
				className,
			)}
		/>
	);
}

export function Button({
	className,
	variant = 'primary',
	...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' }) {
	return (
		<button
			{...props}
			className={clsx(
				'flex min-h-11 w-full items-center justify-center gap-2 border-2 border-ink px-4 text-sm font-bold transition-colors disabled:cursor-not-allowed disabled:opacity-50',
				variant === 'primary' ? 'bg-ink text-white hover:bg-blue' : 'bg-white text-ink hover:bg-ink hover:text-white',
				className,
			)}
		/>
	);
}

export function Alert({ tone = 'error', children }: { tone?: 'error' | 'info' | 'success'; children: ReactNode }) {
	const tones = {
		error: 'border-signal bg-signal/10 text-ink',
		info: 'border-blue bg-blue/10 text-ink',
		success: 'border-ink bg-ink/5 text-ink',
	} as const;
	return (
		<div role={tone === 'error' ? 'alert' : 'status'} className={clsx('border-2 px-4 py-3 text-sm font-medium', tones[tone])}>
			{children}
		</div>
	);
}