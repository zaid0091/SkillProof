'use client';

import { RoleDashboard } from '@/components/role-dashboard';

export default function StudentDashboard() {
	return (
		<RoleDashboard
			role="student"
			title="Student dashboard"
			blurb="Your verified skills start here. Complete assessments, submit real work, and collect evidence that employers can inspect."
			panels={[
				{
					phase: 'Phase 4',
					title: 'Assessments',
					detail: 'Browse published, role-relevant assessments and see formats, difficulty, and time limits before you start.',
				},
				{
					phase: 'Phase 5',
					title: 'Submissions & evaluation',
					detail: 'Submit solutions, follow the isolated run status, and inspect test, quality, and security results.',
				},
				{
					phase: 'Phase 6',
					title: 'Skill passport',
					detail: 'Turn evaluation results into verified skill records with the evidence and confidence behind each claim.',
				},
			]}
		/>
	);
}