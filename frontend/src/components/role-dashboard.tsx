'use client';

import type { ReactNode } from 'react';
import { AuthGate } from '@/components/auth-gate';
import type { Role } from '@/lib/auth-api';
import { useAuthStore } from '@/stores/auth-store';

export type RolePanel = {
	title: string;
	detail: string;
	phase: string;
};

/**
 * Shared role dashboard body. Every role page wraps its content in
 * AuthGate(requiredRole), so cross-role views render an explicit access-denied
 * state instead of someone else's data.
 */
export function RoleDashboard({
	role,
	title,
	blurb,
	panels,
}: {
	role: Role;
	title: string;
	blurb: string;
	panels: RolePanel[];
	children?: ReactNode;
}) {
	const user = useAuthStore((state) => state.user);

	return (
		<AuthGate requiredRole={role}>
			<section className="border-2 border-ink bg-white">
				<div className="border-b-2 border-ink px-6 py-6 sm:px-10">
					<h1 className="text-3xl font-black tracking-tight">{title}</h1>
					<p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink/70">{blurb}</p>
				</div>

				<div className="grid gap-px bg-ink/15 sm:grid-cols-2 lg:grid-cols-3">
					{panels.map((panel) => (
						<article key={panel.title} className="bg-white px-6 py-6">
							<p className="text-xs font-bold uppercase tracking-[0.14em] text-blue">{panel.phase}</p>
							<h2 className="mt-3 text-lg font-black">{panel.title}</h2>
							<p className="mt-2 text-sm leading-relaxed text-ink/60">{panel.detail}</p>
						</article>
					))}
				</div>

				<dl className="grid gap-px border-t-2 border-ink bg-ink/15 sm:grid-cols-3">
					<div className="bg-paper px-6 py-5">
						<dt className="text-xs font-bold uppercase tracking-[0.14em] text-ink/55">Signed in as</dt>
						<dd className="mt-2 text-sm font-semibold">{user?.display_name ?? '—'}</dd>
					</div>
					<div className="bg-paper px-6 py-5">
						<dt className="text-xs font-bold uppercase tracking-[0.14em] text-ink/55">Account type</dt>
						<dd className="mt-2 text-sm font-semibold">{user?.role ?? '—'}</dd>
					</div>
					<div className="bg-paper px-6 py-5">
						<dt className="text-xs font-bold uppercase tracking-[0.14em] text-ink/55">Email status</dt>
						<dd className="mt-2 text-sm font-semibold">
							{user?.is_verified ? 'Verified' : 'Not verified yet'}
						</dd>
					</div>
				</dl>
			</section>
		</AuthGate>
	);
}