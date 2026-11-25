'use client';

import { RoleDashboard } from '@/components/role-dashboard';

export default function EmployerDashboard() {
	return (
		<RoleDashboard
			role="employer"
			title="Employer dashboard"
			blurb="Hire on evidence. Search candidates by verified skills, inspect the work behind each claim, and run your internship pipeline."
			panels={[
				{
					phase: 'Phase 7',
					title: 'Candidate search',
					detail: 'Filter by verified skills and competency levels, with transparent matching factors instead of opaque ranking.',
				},
				{
					phase: 'Phase 7',
					title: 'Shortlists',
					detail: 'Collect candidates into shared shortlists and review the supporting evidence for every skill claim.',
				},
				{
					phase: 'Phase 7',
					title: 'Internships & applications',
					detail: 'Publish internship listings, receive applications, and track each application through its stages.',
				},
			]}
		/>
	);
}