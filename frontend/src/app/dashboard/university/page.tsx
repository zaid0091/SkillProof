'use client';

import { RoleDashboard } from '@/components/role-dashboard';

export default function UniversityDashboard() {
	return (
		<RoleDashboard
			role="university"
			title="University dashboard"
			blurb="See how your students develop demonstrable competencies, and report on outcomes with evidence instead of grades alone."
			panels={[
				{
					phase: 'Phase 9',
					title: 'Progress analytics',
					detail: 'Track assessment participation and competency development across cohorts and degree programs.',
				},
				{
					phase: 'Phase 9',
					title: 'Outcome reporting',
					detail: 'Aggregate skill verification outcomes for internal review and accreditation evidence.',
				},
				{
					phase: 'Phase 3',
					title: 'Organization management',
					detail: 'Manage institutional membership and control which staff can see which analytics.',
				},
			]}
		/>
	);
}