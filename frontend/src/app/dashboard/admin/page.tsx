'use client';

import { RoleDashboard } from '@/components/role-dashboard';

export default function AdminDashboard() {
	return (
		<RoleDashboard
			role="administrator"
			title="Administration"
			blurb="Platform operations: moderation, support, and the security audit trail. Administrator accounts are only ever assigned by another administrator."
			panels={[
				{
					phase: 'Phase 9',
					title: 'User administration',
					detail: 'Suspend accounts, correct role assignments, and support users through verification and recovery issues.',
				},
				{
					phase: 'Phase 9',
					title: 'Moderation',
					detail: 'Review flagged content, assessment definitions, and disputed evaluation outcomes.',
				},
				{
					phase: 'Phase 2',
					title: 'Audit log',
					detail: 'Security events — logins, role changes, recovery flows — are recorded immutably and readable here.',
				},
			]}
		/>
	);
}