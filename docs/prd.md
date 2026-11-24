# Product Requirements Document (PRD)
## SkillProof — Verified Skills & Project-Based Hiring Platform

**Document Version:** 1.0  
**Product Type:** Web-based SaaS Platform  
**Project Category:** Final Year Project (FYP) + Startup  
**Target Market:** University students, software engineering graduates, universities, and software companies  
**Proposed Technology Stack:** Next.js, TypeScript, Django REST Framework, PostgreSQL, Redis, Celery, Docker

---

# 1. Executive Summary

SkillProof is a skills verification and project-based hiring platform designed to bridge the gap between academic qualifications, self-reported technical skills, and actual software engineering capabilities.

Traditional recruitment systems primarily depend on resumes, degrees, certificates, and keyword matching. These methods often fail to provide reliable evidence of a candidate's practical abilities.

SkillProof introduces an evidence-based assessment model in which students demonstrate their technical competencies through practical coding challenges, software development projects, automated testing, code quality analysis, and verified project contributions.

The platform generates structured skill profiles containing assessment scores, competency breakdowns, project evidence, and verification confidence.

Employers can use these profiles to identify candidates based on demonstrated capabilities rather than relying exclusively on resume claims.

Universities can use SkillProof to monitor student employability, identify skill gaps, and evaluate the effectiveness of their software engineering programs.

The initial product will focus on software engineering skills, particularly backend development, frontend development, databases, and software testing.

The long-term vision is to establish SkillProof as a trusted skills verification infrastructure for technical hiring.

---

# 2. Problem Statement

## 2.1 Current Problems

Students frequently face difficulties when applying for internships and entry-level software engineering positions.

Common problems include:

- Students lack professional experience despite possessing practical development skills.
- Resumes often contain self-reported skills that are difficult to verify.
- Academic grades do not always reflect practical software engineering ability.
- Employers spend considerable time screening candidates.
- Traditional coding assessments evaluate isolated problem-solving rather than complete engineering capabilities.
- GitHub repositories do not always provide sufficient evidence of individual contributions.
- Universities lack centralized tools to measure students' practical employability skills.

## 2.2 Problem Definition

There is a need for a reliable, evidence-based platform that evaluates practical software engineering competencies and connects verified candidates with suitable internship and employment opportunities.

## 2.3 Proposed Solution

SkillProof will provide:

1. Practical technical assessments.
2. Automated assessment execution.
3. Code quality and testing analysis.
4. Project contribution verification.
5. Evidence-based skill profiles.
6. Employer candidate discovery.
7. University employability analytics.

The platform will emphasize transparent assessment criteria, measurable evidence, and explainable skill scores.

---

# 3. Product Vision

To become a trusted platform where technical skills are demonstrated, verified, and connected to real career opportunities.

## 3.1 Mission

Help students prove what they can build and help employers discover talent based on actual capabilities.

## 3.2 Product Philosophy

SkillProof will follow these principles:

- Skills should be demonstrated, not merely claimed.
- Assessment results should be supported by evidence.
- Candidates should understand how their skills are evaluated.
- Employers should be able to inspect assessment details.
- Verification should be fair, transparent, and consistent.
- Students should benefit from assessments even when they are not selected for a job.

---

# 4. Product Goals and Objectives

## 4.1 Primary Goals

- Provide students with a credible way to demonstrate technical skills.
- Reduce uncertainty during entry-level technical recruitment.
- Help employers identify suitable candidates efficiently.
- Provide universities with measurable employability insights.
- Develop a scalable assessment and verification platform.

## 4.2 Secondary Goals

- Encourage practical software engineering learning.
- Improve student portfolios with verified evidence.
- Reduce dependence on certificate-based skill claims.
- Support project-based recruitment and internship placement.

## 4.3 Non-Goals for the Initial Release

The MVP will not attempt to:

- Replace traditional university degrees.
- Guarantee employment or internship placement.
- Verify every professional skill across all industries.
- Provide a complete freelance marketplace.
- Support every programming language and framework.
- Automatically make final hiring decisions.
- Guarantee that all submitted code was written without AI assistance.

---

# 5. Target Users and Personas

## 5.1 Student

**Description:** A university student or recent graduate seeking internships or entry-level technical employment.

**Goals:**

- Demonstrate practical skills.
- Build a credible technical profile.
- Identify weaknesses in technical abilities.
- Discover suitable internships.
- Improve employability.

**Pain Points:**

- Limited professional experience.
- Difficulty proving skills through resumes.
- Lack of structured practical assessment.
- Difficulty competing with experienced candidates.

## 5.2 Employer

**Description:** A software company, startup, or technical recruiter seeking entry-level developers.

**Goals:**

- Discover qualified candidates.
- Reduce screening time.
- Evaluate candidates consistently.
- Identify candidates with relevant technical skills.

**Pain Points:**

- Inflated resumes.
- Inconsistent candidate evaluation.
- Time-consuming technical screening.
- Difficulty verifying project contributions.

## 5.3 University

**Description:** A university department, career development office, or academic institution.

**Goals:**

- Monitor student technical competencies.
- Identify skill gaps.
- Improve graduate employability.
- Track assessment participation and outcomes.

**Pain Points:**

- Limited practical competency data.
- Difficulty evaluating industry readiness.
- Lack of centralized employability analytics.

## 5.4 Platform Administrator

**Description:** A SkillProof administrator responsible for platform operations.

**Goals:**

- Maintain platform integrity.
- Manage users and organizations.
- Monitor assessment quality.
- Resolve disputes and misuse.

---

# 6. Product Scope

## 6.1 MVP Modules

The initial release will include the following modules:

1. Authentication and Authorization
2. Student Profile Management
3. Employer and Organization Management
4. Skill Assessment Management
5. Coding Submission System
6. Automated Evaluation Engine
7. Code Quality Analysis
8. Evidence-Based Skill Scoring
9. Verified Skill Passport
10. Employer Candidate Search
11. Internship Listings and Applications
12. University Analytics
13. Administration and Moderation

## 6.2 Future Modules

Potential future features include:

- AI-assisted assessment generation.
- Collaborative team project verification.
- Live technical interview assistance.
- Advanced anti-cheating mechanisms.
- Additional programming languages.
- Industry-specific skill assessments.
- Professional certification partnerships.
- Mobile application.
- International hiring integrations.

---

# 7. Functional Requirements

## FR-01: Authentication and Authorization

The system shall provide secure authentication for all users.

### Requirements

- Users shall register using email and password.
- Users shall verify their email address.
- Users shall log in and log out securely.
- The system shall support access and refresh tokens.
- Users shall have role-based permissions.
- Users shall be able to reset forgotten passwords.
- The system shall prevent unauthorized access to protected resources.

### User Roles

- Student
- Employer
- University
- Administrator

### Acceptance Criteria

- A registered user can authenticate successfully.
- An unverified account cannot access restricted functionality.
- Users cannot access resources belonging to unauthorized organizations.
- Expired access tokens cannot be used to access protected endpoints.

---

## FR-02: Student Profile Management

The system shall allow students to create and maintain professional technical profiles.

### Profile Information

- Full name
- Profile picture
- University
- Degree program
- Graduation year
- Technical skills
- Projects
- GitHub profile
- LinkedIn profile
- Resume
- Assessment history

### Requirements

- Students shall edit their profile information.
- Students shall select skills they want to demonstrate.
- Students shall add projects to their profile.
- Students shall control the visibility of selected profile information.
- Students shall view their assessment results.

### Acceptance Criteria

- A student can create and update a profile.
- Verified skills are displayed separately from self-reported skills.
- Employers can view public profiles according to visibility settings.

---

## FR-03: Employer and Organization Management

The system shall allow employers to create company profiles and manage recruitment activities.

### Requirements

- Employers shall register an organization.
- Employers shall provide company information.
- Employers shall create and manage internship listings.
- Employers shall search verified student profiles.
- Employers shall shortlist candidates.
- Employers shall review assessment evidence.

### Acceptance Criteria

- Employers can access only authorized organization resources.
- Employer accounts cannot modify student assessment results.
- Candidate searches return profiles matching selected criteria.

---

## FR-04: Skill Assessment Management

The system shall provide practical assessments for evaluating technical competencies.

### Assessment Categories

- Python
- Django and Django REST Framework
- JavaScript and TypeScript
- React and Next.js
- Database Design and SQL
- Software Testing
- Git and Collaboration
- Software Engineering Fundamentals

### Assessment Types

- Coding challenges
- API development tasks
- Database design tasks
- Debugging challenges
- Code review tasks
- Project-based assessments

### Requirements

- Administrators shall create assessments.
- Assessments shall contain descriptions and requirements.
- Assessments shall define evaluation criteria.
- Assessments shall support difficulty levels.
- Assessments shall include test cases where applicable.
- Students shall view available assessments.
- Students shall submit solutions within defined constraints.

### Acceptance Criteria

- An assessment can be created and published.
- Students can access published assessments.
- Assessment instructions and evaluation criteria are available.
- Unpublished assessments cannot be accessed by unauthorized students.

---

## FR-05: Coding Submission System

The system shall allow students to submit solutions to practical coding assessments.

### Requirements

- Students shall upload code or connect a supported repository.
- The system shall validate submission formats.
- The system shall store submission metadata.
- The system shall track submission status.
- Students shall receive evaluation results.
- The system shall maintain assessment history.

### Submission Statuses

- Pending
- Queued
- Running
- Completed
- Failed

### Acceptance Criteria

- Valid submissions enter the evaluation queue.
- Invalid submissions are rejected with an explanation.
- Students can view the status of their submissions.
- Submission records remain associated with the correct student and assessment.

---

## FR-06: Automated Evaluation Engine

The system shall automatically evaluate submitted code using predefined assessment criteria.

### Evaluation Components

- Functional correctness
- Test case execution
- Input validation
- Error handling
- Edge-case handling
- Performance constraints
- Security checks where applicable

### Requirements

- Code shall execute inside an isolated environment.
- Execution shall have CPU and memory limits.
- Execution shall have a maximum time limit.
- Network access shall be restricted by default.
- Test results shall be stored.
- The engine shall calculate normalized evaluation scores.

### Acceptance Criteria

- Correct solutions pass relevant test cases.
- Incorrect solutions receive appropriate failure results.
- Execution timeouts are handled safely.
- Resource limits are enforced.
- Student code cannot directly access platform secrets or production databases.

---

## FR-07: Code Quality Analysis

The system shall analyze submitted code for maintainability and engineering quality.

### Metrics

- Code complexity
- Code duplication
- Maintainability indicators
- Test coverage
- Coding conventions
- Potential security issues

### Requirements

- The system shall integrate suitable static analysis tools.
- Analysis results shall be stored with the submission.
- Students shall receive explanations of detected issues.
- Employers shall be able to review relevant quality metrics.

### Acceptance Criteria

- Code quality reports are generated for supported submissions.
- Reports identify measurable issues.
- Unsupported code formats produce an appropriate status.
- Quality scores are based on documented criteria.

---

## FR-08: Evidence-Based Skill Scoring

The system shall generate structured skill scores using assessment evidence.

### Proposed Evaluation Dimensions

| Dimension | Initial Weight |
|---|---:|
| Functional Correctness | 30% |
| Problem Solving | 20% |
| Code Quality | 15% |
| Testing | 15% |
| Security and Best Practices | 10% |
| Project Contribution Evidence | 10% |

The weights are configurable and subject to research evaluation.

### Requirements

- The system shall calculate scores for individual competencies.
- Scores shall be based on documented evaluation rules.
- The system shall store evidence supporting each score.
- The system shall display assessment dates.
- The system shall distinguish verified and self-reported skills.
- The system shall calculate verification confidence separately from skill scores.

### Acceptance Criteria

- Every verified skill has associated evidence.
- Users can inspect the criteria behind a score.
- Skill scores can be updated after new assessments.
- Verification confidence reflects evidence quantity and quality.

---

## FR-09: Verified Skill Passport

The system shall generate a shareable profile containing verified technical competencies.

### Requirements

- Students shall view their skill passport.
- Students shall share a public profile link.
- Employers shall inspect verified skills.
- Each skill shall display relevant evidence.
- The profile shall display assessment dates.
- Students shall be able to control profile visibility.

### Acceptance Criteria

- A public profile displays only permitted information.
- Verified skills are distinguishable from self-reported skills.
- Employers can inspect assessment evidence.
- Revoked or invalid verification records are no longer displayed as active.

---

## FR-10: GitHub Project Contribution Verification

The system shall integrate with GitHub to analyze software project activity.

### Requirements

- Students shall connect their GitHub accounts through OAuth.
- The system shall retrieve authorized repository information.
- The system shall analyze commits, pull requests, and code changes.
- The system shall identify repository contribution patterns.
- Students shall select repositories for profile inclusion.
- The system shall distinguish contribution evidence from verified competency.

### Acceptance Criteria

- Repository access requires appropriate authorization.
- The system does not expose private repository data without permission.
- Contribution metrics are presented with clear limitations.
- Repository activity alone cannot automatically establish a verified skill.

---

## FR-11: Employer Candidate Search

The system shall allow employers to search for candidates based on demonstrated competencies.

### Search Filters

- Technical skill
- Verified skill score
- Assessment level
- University
- Graduation year
- Project experience
- Internship availability

### Requirements

- Employers shall search public or authorized candidate profiles.
- The system shall rank candidates according to relevant criteria.
- Employers shall view candidate evidence.
- Employers shall shortlist candidates.
- Employers shall save search criteria.

### Acceptance Criteria

- Search results reflect selected filters.
- Candidate rankings are based on documented criteria.
- Employers cannot access private student information without authorization.

---

## FR-12: Internship and Job Application Management

The system shall support internship listings and candidate applications.

### Requirements

- Employers shall create internship listings.
- Students shall browse available opportunities.
- Students shall apply using their SkillProof profile.
- Employers shall review applications.
- Employers shall update application statuses.
- Students shall receive application status updates.

### Application Statuses

- Submitted
- Under Review
- Shortlisted
- Interview
- Accepted
- Rejected
- Withdrawn

### Acceptance Criteria

- Students can apply to eligible listings.
- Employers can review applications.
- Application status changes are recorded.
- Unauthorized users cannot modify application records.

---

## FR-13: University Analytics

The system shall provide universities with insights into student competencies.

### Analytics

- Assessment participation
- Skill distribution
- Competency gaps
- Assessment completion rates
- Student progress
- Employability readiness indicators

### Requirements

- Universities shall view authorized student data.
- The system shall generate aggregate reports.
- Reports shall support filtering by academic program.
- Student privacy shall be respected.

### Acceptance Criteria

- Universities can access only authorized institutional data.
- Reports accurately reflect stored assessment records.
- Individual student data is not exposed without appropriate permissions.

---

## FR-14: Administration and Moderation

The system shall provide administrative tools for platform management.

### Requirements

- Manage users and organizations.
- Manage assessments.
- Review reported profiles.
- Handle disputes.
- Monitor submissions.
- Suspend accounts when necessary.
- View platform activity logs.

### Acceptance Criteria

- Administrative actions are logged.
- Unauthorized users cannot access administrative endpoints.
- Assessment and moderation changes are traceable.

---

# 8. Non-Functional Requirements

## 8.1 Performance

- Standard API requests should complete within 500 ms under normal load, excluding external services and heavy operations.
- Candidate search should return results within 2 seconds for the initial target dataset.
- Coding assessments shall execute asynchronously.
- The platform shall support concurrent submissions through background workers.

## 8.2 Security

- Passwords shall be securely hashed.
- Authentication shall use secure token handling.
- Role-based access control shall be enforced.
- Sensitive information shall be encrypted in transit.
- File uploads shall be validated.
- Code execution shall be isolated.
- Rate limiting shall protect sensitive endpoints.
- Secrets shall not be stored in source code.

## 8.3 Reliability

- The platform shall maintain submission records.
- Background tasks shall support retry mechanisms.
- Failed evaluations shall not corrupt assessment records.
- Database backups shall be maintained.
- Critical operations shall be logged.

## 8.4 Scalability

- The architecture shall support horizontal scaling of background workers.
- Assessment execution shall be separated from the main API server.
- Database queries shall be optimized.
- Redis shall support task coordination and caching where appropriate.

## 8.5 Usability

- The interface shall be responsive.
- Student dashboards shall provide clear assessment progress.
- Skill reports shall be understandable to non-technical recruiters.
- Error messages shall explain corrective actions.

## 8.6 Maintainability

- The backend shall follow modular architecture.
- APIs shall be documented.
- Automated tests shall cover critical functionality.
- The codebase shall follow consistent coding standards.

---

# 9. System Architecture

## 9.1 Proposed Architecture

The platform will use a modular, service-oriented architecture within a manageable FYP scope.

### Frontend Layer

**Technology:** Next.js, TypeScript, Tailwind CSS

Responsibilities:

- Student dashboard
- Employer dashboard
- University dashboard
- Assessment interface
- Skill passport
- Candidate search
- Internship management

### Backend Layer

**Technology:** Django REST Framework

Responsibilities:

- Authentication
- User and organization management
- Assessment management
- Submission processing
- Skill scoring
- Candidate matching
- Application management

### Database Layer

**Technology:** PostgreSQL

Responsibilities:

- User records
- Organization records
- Assessments
- Submissions
- Evaluation results
- Skill profiles
- Applications
- Audit logs

### Background Processing

**Technology:** Celery and Redis

Responsibilities:

- Assessment execution scheduling
- Code analysis
- GitHub synchronization
- Report generation
- Notification processing

### Isolated Execution Layer

**Technology:** Docker-based isolated workers

Responsibilities:

- Execute student code
- Run automated tests
- Enforce resource limits
- Return evaluation results

The execution environment shall be separated from the main application infrastructure.

---

# 10. Proposed Database Entities

The following entities will form the initial data model.

| Entity | Purpose |
|---|---|
| User | Authentication and identity |
| StudentProfile | Student-specific information |
| EmployerProfile | Employer information |
| University | Institutional information |
| Organization | Company or institution |
| Skill | Technical competency |
| Assessment | Assessment definition |
| AssessmentTask | Individual assessment task |
| Submission | Student submission |
| TestCase | Automated evaluation test |
| EvaluationResult | Assessment outcome |
| SkillEvidence | Evidence supporting a skill |
| SkillVerification | Verified competency record |
| GitHubRepository | Connected project |
| Internship | Internship listing |
| Application | Student application |
| Shortlist | Employer candidate shortlist |
| AuditLog | Administrative and security events |

---

# 11. Research and FYP Contribution

## 11.1 Research Title

**SkillProof: An Evidence-Based Software Engineering Skill Verification and Candidate Matching Platform**

## 11.2 Research Problem

Traditional technical recruitment often relies on self-reported skills, academic qualifications, and isolated coding assessments.

These approaches may not adequately represent practical software engineering competencies.

## 11.3 Proposed Research Contribution

The project will develop an evidence-weighted competency model that combines:

- Automated functional assessment
- Code quality metrics
- Testing performance
- Software engineering best practices
- Project contribution evidence
- Verification confidence

The model will generate competency profiles that provide more detailed information than a single coding assessment score.

## 11.4 Research Questions

1. Can evidence-based skill profiles provide more useful candidate information than self-reported resumes?
2. Does combining multiple assessment dimensions improve competency evaluation?
3. Can verification confidence help distinguish strong evidence from limited assessment evidence?
4. Can skill-based candidate matching reduce irrelevant candidate recommendations?

## 11.5 Evaluation Methodology

The system may be evaluated using:

- Student assessment submissions
- Expert-reviewed code samples
- Automated test results
- Software engineering evaluator feedback
- Candidate matching experiments
- Comparison with baseline scoring models

## 11.6 Evaluation Metrics

| Metric | Purpose |
|---|---|
| Test Pass Rate | Functional correctness |
| Precision | Accuracy of positive skill classifications |
| Recall | Ability to identify demonstrated competencies |
| Inter-Rater Agreement | Consistency between human evaluators |
| Ranking Quality | Relevance of candidate recommendations |
| Assessment Completion Rate | Platform usability |
| User Satisfaction | Student and employer feedback |

The research shall avoid claiming that SkillProof guarantees hiring success or perfectly measures a person's ability.

---

# 12. Success Metrics

## 12.1 MVP Metrics

The initial pilot will aim to measure:

- 100 registered students
- 5 participating employers or industry evaluators
- 10 practical assessments
- 200 completed assessment submissions
- 80% assessment completion rate
- 70% of participating students receiving at least one verified skill
- At least 3 employers using candidate search during the pilot

These are proposed pilot targets, not current platform results.

## 12.2 Product Success Metrics

- Number of verified student profiles
- Number of completed assessments
- Employer candidate search activity
- Internship applications submitted
- Employer shortlist rate
- Student return rate
- Assessment reliability
- University participation

## 12.3 Startup Success Metrics

- Number of paying organizations
- Monthly recurring revenue
- Customer retention
- Cost per assessment
- Employer conversion rate
- University renewal rate

---

# 13. Risks and Mitigation

## 13.1 Assessment Cheating

**Risk:** Students may copy code or use unauthorized assistance.

**Mitigation:**

- Use randomized assessment variants.
- Include code explanation or debugging tasks.
- Track suspicious submission patterns.
- Use plagiarism detection where appropriate.
- Allow human review.

AI-assisted coding shall not automatically be considered cheating unless the assessment explicitly prohibits it.

## 13.2 Inaccurate Skill Scores

**Risk:** Automated scoring may misrepresent a student's actual competency.

**Mitigation:**

- Use transparent scoring criteria.
- Separate skill scores from confidence.
- Validate scoring against human evaluations.
- Allow assessment appeals.
- Avoid relying exclusively on AI-generated judgments.

## 13.3 Limited Employer Adoption

**Risk:** Employers may not trust a new verification platform.

**Mitigation:**

- Begin with local software companies.
- Invite employers to contribute assessment requirements.
- Provide transparent evidence reports.
- Run a controlled pilot.

## 13.4 Privacy and Data Protection

**Risk:** Student information or private repositories may be exposed.

**Mitigation:**

- Use consent-based data access.
- Apply role-based permissions.
- Minimize collected information.
- Provide profile visibility controls.
- Secure GitHub integration.
- Maintain audit logs.

## 13.5 Technical Complexity

**Risk:** Secure code execution and automated evaluation may exceed the available FYP development time.

**Mitigation:**

- Begin with a limited set of programming languages.
- Use established sandboxing solutions.
- Support a small number of assessment types.
- Keep the MVP modular.

---

# 14. Development Roadmap

## Phase 1 — Foundation

- Requirements finalization
- UI/UX design
- Database design
- Authentication
- Role-based access control
- Student and employer profiles

## Phase 2 — Assessment Platform

- Assessment management
- Coding submissions
- Background execution
- Automated test cases
- Submission history

## Phase 3 — Verification Engine

- Code quality analysis
- Skill scoring
- Evidence management
- Confidence calculation
- Skill passport

## Phase 4 — Hiring Features

- Employer candidate search
- Internship listings
- Application management
- Shortlisting

## Phase 5 — Research and Evaluation

- Dataset preparation
- Model evaluation
- Scoring validation
- Performance testing
- User feedback

## Phase 6 — Startup Pilot

- Recruit initial students
- Partner with local software companies
- Conduct pilot assessments
- Collect employer feedback
- Validate pricing and business model

---

# 15. Future Enhancements

After the MVP, SkillProof may expand into:

- AI-generated practical assessments
- Adaptive assessment difficulty
- Team project contribution verification
- Advanced skill recommendation engine
- University curriculum mapping
- Company-specific assessment templates
- Industry-recognized skill credentials
- Freelance project matching
- Remote technical interview workflows
- International employer partnerships

---

# 16. Conclusion

SkillProof aims to transform technical recruitment from a resume-centered process into an evidence-based competency verification system.

By combining practical assessments, automated evaluation, code quality analysis, project contribution evidence, and skill-based candidate matching, the platform will help students demonstrate their abilities and help employers make more informed recruitment decisions.

The initial FYP will focus on building a functional MVP and evaluating the proposed evidence-based competency model.

The long-term startup vision is to develop SkillProof into a scalable SaaS platform serving universities, software companies, technical recruiters, and early-career developers.

**Final Product Vision:** A platform where every technical skill can be demonstrated, evaluated, and supported by verifiable evidence.