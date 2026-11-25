'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import type { ReactNode } from 'react';
import { AuthGate } from '@/components/auth-gate';
import { logout } from '@/lib/auth-api';
import { useAuthStore } from '@/stores/auth-store';

/**
 * Chrome for every authenticated route. The real session check lives in
 * AuthGate; this header only reflects the resolved state.
 */
export default function DashboardLayout({ children }: { children: ReactNode }) {
	const router = useRouter();
	const queryClient = useQueryClient();
	const user = useAuthStore((state) => state.user);

	const signOut = useMutation({
		mutationFn: logout,
		onSuccess: () => {
			queryClient.clear();
			router.replace('/login');
		},
	});

	return (
		<main className="min-h-full bg-paper text-ink">
			<header className="border-b-2 border-ink">
				<div className="mx-auto flex max-w-360 flex-wrap items-center justify-between gap-4 px-5 py-5 sm:px-8 lg:px-12">
					<Link href="/dashboard" className="flex items-center gap-3" aria-label="SkillProof dashboard">
						<span className="grid size-9 place-items-center border-2 border-ink bg-signal text-sm font-black">SP</span>
						<span className="text-lg font-bold tracking-tight">SkillProof</span>
					</Link>
					<nav className="flex items-center gap-5 text-sm font-semibold" aria-label="Account">
						{user ? (
							<>
								<span className="hidden text-ink/70 sm:inline">{user.display_name}</span>
								<span className="border-2 border-ink bg-white px-3 py-1 text-xs font-bold uppercase tracking-[0.12em]">
									{user.role}
								</span>
								<button
									type="button"
									onClick={() => signOut.mutate()}
									disabled={signOut.isPending}
									className="border-2 border-ink px-4 py-2 font-bold transition-colors hover:bg-ink hover:text-white disabled:opacity-50"
								>
									{signOut.isPending ? 'Signing out…' : 'Sign out'}
								</button>
							</>
						) : null}
					</nav>
				</div>
			</header>
			<section className="mx-auto max-w-360 px-5 py-10 sm:px-8 lg:px-12">
				<AuthGate>{children}</AuthGate>
			</section>
		</main>
	);
}