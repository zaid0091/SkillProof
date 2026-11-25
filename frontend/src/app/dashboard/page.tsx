'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { dashboardPathFor } from '@/lib/auth-api';
import { useAuthStore } from '@/stores/auth-store';

/** /dashboard routes each role to its own home. */
export default function DashboardIndex() {
	const router = useRouter();
	const user = useAuthStore((state) => state.user);

	useEffect(() => {
		if (user) router.replace(dashboardPathFor(user.role));
	}, [user, router]);

	return (
		<div role="status" className="flex min-h-64 items-center justify-center text-sm font-bold text-ink/60">
			Opening your dashboard…
		</div>
	);
}