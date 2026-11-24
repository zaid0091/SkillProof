# SkillProof — Project Phases and Implementation Plan

**Document Version:** 1.0  
**Status:** Proposed implementation roadmap  
**Project:** SkillProof — Verified Skills and Project-Based Hiring Platform  
**Primary Sources:** PRD, TAD, FIS, FTL, SACS, and Build Plan

---

# 1. Purpose

This document organizes SkillProof development into ordered phases. It defines the objective, scope, deliverables, dependencies, validation activities, and exit criteria for each stage.

The recommended sequence is:

1. Build a secure platform foundation.
2. Implement authentication and role management.
3. Add profiles and organizational data isolation.
4. Add assessment management.
5. Implement submission and isolated code evaluation.
6. Implement evidence and skill verification.
7. Add employer hiring workflows.
8. Integrate GitHub contribution evidence.
9. Add university analytics and administration.
10. Complete testing, security hardening, and deployment.
11. Run a controlled pilot and research evaluation.

The MVP shall demonstrate this complete journey:

**Student registration → assessment submission → isolated evaluation → verified skill evidence → public skill passport → employer discovery.**

---

# 2. Delivery Rules

## 2.1 MVP Priorities

- P0 features are required for the platform foundation and core workflow.
- P1 features are required for an effective MVP.
- P2 features are important but may follow after the core workflow is stable.
- P3 features are deferred enhancements.

## 2.2 Cross-Cutting Requirements

Every phase must preserve:

- Backend authorization as the security boundary.
- Role-based and object-level permissions.
- Organization and tenant isolation.
- Auditability of important changes.
- Secure handling of credentials and private data.
- Reproducible scoring and verification.
- API validation and consistent error responses.
- Frontend loading, empty, success, and error states.
- Automated tests for critical behavior.

## 2.3 Phase Completion Rule

A phase is complete only when:

- Its deliverables satisfy the acceptance criteria.
- Relevant backend and frontend functionality works together.
- Security-sensitive behavior is tested.
- Database migrations are complete.
- API contracts and setup documentation are updated.
- No unresolved high-severity issue remains.

---

# 3. Phase Overview

| Phase | Name | Main Objective | Primary Outcome |
|---|---|---|---|
| 1 | Project Foundation | Create frontend, backend, database, workers, and local infrastructure | Development environment is runnable |
| 2 | Authentication and RBAC | Implement secure users and role-based authorization | Protected role-specific access |
| 3 | Profiles and Organizations | Implement student, employer, and university records | Secure profile and tenant foundation |
| 4 | Assessment Management | Create and publish practical assessments | Students can view published assessments |
| 5 | Submission and Evaluation | Queue, isolate, execute, and score submissions | End-to-end code evaluation |
| 6 | Skill Verification | Convert evaluation results into evidence and confidence | Verified skill passport |
| 7 | Employer and Hiring | Add candidate discovery and applications | Employer-to-student hiring workflow |
| 8 | GitHub Integration | Collect supplementary project evidence | Consent-based repository evidence |
| 9 | Analytics and Administration | Provide institutional analytics and moderation | University and administrator capabilities |
| 10 | Testing and Deployment | Harden, test, monitor, and deploy the platform | Production-ready MVP |
| 11 | Pilot and Research | Evaluate the platform with participants | Evidence model and UX findings |

---

# Phase 1 — Project Foundation and Infrastructure

## Objective

Create the runnable development foundation for the frontend, backend, database, caching, asynchronous workers, and local services.

## Scope

### Frontend

- Initialize Next.js with the App Router.
- Configure React and TypeScript.
- Configure Tailwind CSS.
- Create the initial route structure.
- Add reusable UI primitives and layout components.
- Configure environment variables.
- Establish the centralized API client.
- Add global loading, error, empty, and notification patterns.

### Backend

- Initialize Django and Django REST Framework.
- Configure environment-based settings.
- Configure PostgreSQL.
- Create domain applications for accounts, organizations, profiles, assessments, submissions, evaluations, evidence, hiring, analytics, notifications, and audit.
- Add common exceptions, permissions, validators, and utilities.
- Add consistent API error handling and health endpoints.

### Infrastructure

- Configure Redis.
- Configure Celery and Celery worker startup.
- Create Docker Compose development services.
- Configure object-storage access or a safe local substitute.
- Create `.env.example` files.
- Exclude secrets and generated files from Git.
- Document setup and shutdown commands.

### Quality Gates

- Configure baseline backend linting and testing.
- Configure frontend linting and component testing.
- Configure CI for builds and tests.

## Main Deliverables

- Running Next.js application.
- Running Django application.
- Working PostgreSQL migrations.
- Working Redis/Celery test task.
- Documented local setup process.
- Initial repository structure.

## Dependencies

- None; frontend and backend initialization may proceed independently.

## Backlog Tickets

- SP-001 — Initialize Frontend Project.
- SP-002 — Initialize Backend Project.
- SP-003 — Configure Development Environment.
- SP-004 — Configure Redis and Celery.

## Exit Criteria

- Both applications start locally.
- Environment variables are not committed as secrets.
- Database migrations run successfully.
- Redis and Celery execute a test task.
- API health endpoints respond successfully.
- The frontend can reach a versioned backend endpoint.

---

# Phase 2 — Authentication and Role-Based Access

## Objective

Create a secure account system and enforce permissions for Student, Employer, University, and Administrator roles.

## Scope

### Account Registration

- Email and password registration.
- Secure password hashing.
- Duplicate-email rejection.
- Email verification.
- Role assignment under backend control.

### Login and Sessions

- Short-lived access tokens.
- Limited-lifetime refresh tokens.
- Secure refresh-token rotation or revocation.
- Logout and session invalidation.
- Password recovery.
- Time-limited, single-use recovery tokens.

### Authorization

- Role definitions and permissions.
- Authentication checks on protected APIs.
- Object-level permission checks.
- Organization membership authorization.
- Denial of privileged role assignment by ordinary users.
- Audit events for role and security changes.

### Frontend Protection

- Login and registration pages.
- Role-specific navigation.
- Protected routes.
- Access-denied states.
- Automatic logout or redirect after invalid authentication.
- Coordinated refresh-token handling.

## Main Deliverables

- Registration and verification workflow.
- Login and logout workflow.
- Password recovery workflow.
- Role and permission system.
- Protected frontend routes.

## Dependencies

- Phase 1 infrastructure.
- PostgreSQL and API foundation.

## Backlog Tickets

- SP-005 — Implement User Registration.
- SP-006 — Implement User Login and JWT Authentication.
- SP-007 — Implement Role-Based Access Control.
- SP-008 — Implement Password Recovery.
- SP-009 — Implement Protected Frontend Routes.

## Exit Criteria

- Valid credentials authenticate successfully.
- Expired or invalid tokens are rejected.
- Unverified accounts cannot perform restricted operations.
- Users cannot assign themselves privileged roles.
- Frontend protection cannot bypass backend authorization.
- Password recovery cannot reveal whether an email is registered.

---

# Phase 3 — Profiles and Organization Management

## Objective

Implement ownership, public profile visibility, organization membership, and multi-tenant boundaries.

## Scope

### Student Profile

- Name and profile picture.
- University and degree program.
- Graduation year.
- Biography and technical interests.
- GitHub and LinkedIn links.
- Resume metadata.
- Public/private visibility settings.
- Self-reported technical skills.

### Organizations

- Company and university organization records.
- Organization membership.
- Membership role and status.
- Membership invitation or approval if implemented.
- Organization-level record ownership.

### Employer Profile

- Organization profile.
- Organization member management.
- Hiring-role authorization.

### University Profile

- Institutional profile.
- Authorized members.
- Institutional data boundaries.

### Security and Isolation

- Student owner-only profile editing.
- Public field allowlisting.
- Organization membership verification.
- Organization-filtered database queries.
- Prevention of cross-organization resource access.

## Main Deliverables

- Student profile creation and editing.
- Public profile visibility support.
- Organization creation and membership.
- Employer and university authorization boundaries.

## Dependencies

- Phase 2 authentication and RBAC.

## Backlog Tickets

- SP-010 — Create Student Profile.
- SP-011 — Manage Technical Skills.
- SP-027 — Create Employer Organization.
- SP-031 — Create University Organization Module.

## Exit Criteria

- Students can create and update their own profiles.
- Public profiles exclude private fields.
- Self-reported skills are clearly separate from verified skills.
- Cross-organization API access is denied.
- University and employer membership data are isolated.

---

# Phase 4 — Assessment Management

## Objective

Provide the data model and workflows required to create, publish, and present practical assessments.

## Scope

### Assessment Model

- Title and description.
- Required skill.
- Difficulty and duration.
- Draft/published status.
- Creator and audit metadata.
- Supported task types.

### Assessment Tasks

- Instructions and requirements.
- Submission constraints.
- Evaluation configuration.
- Public sample cases.
- Restricted test cases.

### Assessment Administration

- Create and edit assessments.
- Create assessment tasks and test configurations.
- Publish or unpublish assessments.
- Reject invalid configurations.
- Audit assessment changes.

### Student Assessment Experience

- Assessment listing.
- Filtering and sorting.
- Assessment details.
- Public requirements and constraints.
- No exposure of restricted tests.

### Initial Assessment Categories

The initial catalog should focus on Python and limited software engineering categories:

- Python fundamentals.
- Django REST API development.
- Database design and SQL.
- Software testing.
- Debugging.
- Code review.

## Main Deliverables

- Assessment backend model and API.
- Assessment administration interface.
- Published assessment listing.
- Assessment detail workflow.

## Dependencies

- Phase 2 authentication and RBAC.
- Phase 3 organizations, if assessment ownership is restricted to organization roles.

## Backlog Tickets

- SP-013 — Create Assessment Management Module.
- SP-014 — Create Assessment Listing Page.
- SP-015 — Create Assessment Details Page.
- SP-016 — Implement Assessment Administration.

## Exit Criteria

- Authorized administrators can create and publish assessments.
- Draft assessments are inaccessible to ordinary students.
- Restricted test cases remain private.
- Assessment instructions and constraints are clear.
- Assessment changes are validated and audited.

---

# Phase 5 — Submission and Isolated Code Evaluation

## Objective

Implement the core technical workflow that securely executes student code and produces evaluation results.

## Scope

### Submission Lifecycle

States:

```text
Pending → Queued → Running → Completed
                         → Failed
                         → Cancelled
```

Implement explicit validation for state transitions.

### Submission Management

- Assessment owner and student validation.
- Source upload or repository submission.
- File size and format validation.
- Attempt limits and deadlines.
- Submission history.
- Submission status and cancellation.
- Owner-only private submission access.

### Asynchronous Queue

- Create a submission record.
- Store submission metadata.
- Mark submission queued.
- Dispatch a Celery evaluation task.
- Retry recoverable task failures.
- Convert permanent failures into failed status.
- Avoid task retry loops.

### Execution Isolation

Each submitted solution shall execute in an environment with:

- Separate worker process or container.
- Non-root execution.
- CPU, memory, process, and timeout limits.
- Restricted filesystem access.
- Restricted or disabled network access.
- No production database credentials.
- No Redis administrative access.
- No application secrets.
- Automatic cleanup.

### Test and Quality Evaluation

- Execute assessment test cases.
- Record passed and failed tests.
- Capture timeouts and execution failures.
- Analyze code complexity.
- Measure test coverage where supported.
- Detect coding and security findings.
- Normalize evaluation dimensions.

### Evaluation Results

Store:

- Functional score.
- Code-quality score.
- Testing score.
- Security/best-practice score.
- Overall score.
- Execution status.
- Test-level findings.
- Tool findings.
- Evaluation timestamp and scoring schema version.

## Main Deliverables

- Submission API and frontend workflow.
- Celery evaluation queue.
- Isolated Docker execution worker.
- Automated test runner.
- Code-quality analysis.
- Evaluation result presentation.

## Dependencies

- Phase 1 Redis and Celery setup.
- Phase 2 authentication.
- Phase 4 assessments.

## Backlog Tickets

- SP-017 — Implement Assessment Submission API.
- SP-018 — Implement Submission History.
- SP-019 — Configure Isolated Evaluation Worker.
- SP-020 — Implement Automated Test Evaluation.
- SP-021 — Implement Code Quality Analysis.
- SP-022 — Display Evaluation Results.

## Exit Criteria

- A valid submission completes end to end.
- Invalid submissions are rejected safely.
- Resource limits and timeouts are enforced.
- Submitted code cannot access platform secrets or host resources.
- Test failures are recorded correctly.
- Worker failures do not corrupt submission records.
- Results are read-only for ordinary users.

---

# Phase 6 — Evidence and Skill Verification

## Objective

Convert evaluation and project evidence into transparent skill scores and verification records.

## Scope

### Scoring Dimensions

| Dimension | Initial Weight |
|---|---:|
| Functional correctness | 30% |
| Problem solving | 20% |
| Code quality | 15% |
| Testing | 15% |
| Security and best practices | 10% |
| Project contribution evidence | 10% |

Weights shall be configurable and versioned.

### Evidence Records

Evidence sources may include:

- Coding assessments.
- Project assessments.
- Code review.
- Debugging tasks.
- Human evaluation.
- GitHub project activity.

Evidence records shall retain their source, score, timestamp, confidence inputs, and model version.

### Verification Confidence

Confidence shall be stored separately from skill score.

Possible confidence inputs:

- Number of completed assessments.
- Assessment difficulty.
- Evidence diversity.
- Evidence recency.
- Score consistency.
- Human evaluator confirmation.

Confidence shall not be described as a statistically calibrated probability unless validated.

### Skill Passport

- Verified skill list.
- Skill score.
- Verification confidence.
- Evidence source.
- Assessment history.
- Last verification date.
- Public visibility control.
- Clear separation of claimed and verified skills.

### Revocation

The system shall support:

- Invalidating evidence.
- Revoking verification records.
- Removing revoked records from active public display.
- Auditing revocation actions.

## Main Deliverables

- Configurable scoring engine.
- Skill evidence records.
- Verification status records.
- Student skill passport.
- Public profile evidence display.

## Dependencies

- Phase 5 evaluation results.
- Phase 3 profile data.

## Backlog Tickets

- SP-023 — Implement Skill Scoring Engine.
- SP-024 — Implement Skill Verification Status.
- SP-025 — Create Skill Evidence Records.
- SP-026 — Create Skill Passport Dashboard.

## Exit Criteria

- Every verified skill references evidence.
- Skill score and confidence are separate values.
- Scoring is reproducible for a named model version.
- Students cannot modify scores or evidence manually.
- Revoked records no longer appear active.
- Public evidence respects profile visibility.

---

# Phase 7 — Employer and Hiring Workflows

## Objective

Enable employers to discover candidates and manage internship applications.

## Scope

### Candidate Search

- Filter by technical skill.
- Filter by verified score.
- Filter by assessment level.
- Filter by university and graduation year.
- Filter by project evidence.
- Filter by internship availability.
- Rank authorized public profiles using documented factors.
- Expose a summary of matching evidence.

Matching shall avoid protected characteristics and shall not claim guaranteed hiring performance.

### Employer Shortlists

- Create organization shortlists.
- Add and remove candidates.
- Restrict access to organization members.
- Audit shortlist modifications.

### Internship Listings

- Create and edit listings.
- Add skills and requirements.
- Set location and application deadline.
- Publish or close listings.
- Verify organization ownership.

### Applications

Supported statuses:

- Submitted.
- Under Review.
- Shortlisted.
- Interview.
- Accepted.
- Rejected.
- Withdrawn.

The system shall prevent duplicate applications and validate state transitions.

### Student Application Experience

- Browse published listings.
- Apply using an authorized SkillProof profile.
- View application history.
- Withdraw or track an eligible application.

### Employer Application Experience

- Review authorized applications.
- View permitted candidate evidence.
- Update application status.
- Receive status-change audit records.

## Main Deliverables

- Employer candidate search.
- Candidate evidence pages.
- Internship management.
- Application workflow.
- Shortlisting.

## Dependencies

- Phase 3 organization isolation.
- Phase 6 skill evidence and passport.

## Backlog Tickets

- SP-027 — Create Employer Organization.
- SP-028 — Implement Candidate Search.
- SP-029 — Implement Internship Management.
- SP-030 — Implement Internship Applications.

## Exit Criteria

- Employer search excludes private data.
- Candidate rankings use backend-calculated factors.
- Employers cannot access another organization's applications.
- Duplicate applications are rejected.
- Application state transitions are valid and audited.

---

# Phase 8 — GitHub Integration

## Objective

Add consent-based GitHub project evidence as supplementary information.

## Scope

### OAuth Connection

- GitHub OAuth initiation.
- Authorization callback validation.
- Required permission explanation.
- Secure token storage.
- Connection status.
- Account disconnect and token revocation.

### Repository Data

Retrieve only authorized repository information:

- Commits.
- Pull requests.
- Code review activity.
- Repository participation.
- Permitted file and test/documentation contributions.

### Synchronization

- Repository selection.
- Incremental or scheduled synchronization.
- GitHub API outage handling.
- API rate-limit handling.
- Revoked authorization handling.
- Repository visibility-change handling.

### Evidence Presentation

- Student approval before profile inclusion.
- Repository source context.
- Contribution timestamp and metrics.
- Clear limitations.
- Supplementary evidence status.

GitHub activity shall never independently establish a verified technical skill.

## Main Deliverables

- GitHub connection interface.
- OAuth backend integration.
- Repository synchronization worker.
- Project contribution evidence records.

## Dependencies

- Phase 2 authentication.
- Phase 3 profiles.
- Phase 6 evidence model.

## Backlog Tickets

- SP-034 — Implement GitHub OAuth Connection.
- SP-035 — Retrieve Project Contribution Data.

## Exit Criteria

- OAuth secrets and tokens are backend-only.
- Private repositories require explicit permission.
- API failures do not corrupt evidence records.
- Students can disconnect and revoke integration access.
- GitHub activity remains clearly identified as supplementary evidence.

---

# Phase 9 — University Analytics and Administration

## Objective

Provide institutional insights and administrative controls with privacy and audit safeguards.

## Scope

### University Analytics

- Assessment participation.
- Completion rates.
- Verified skill distribution.
- Competency gaps.
- Student progress.
- Employability readiness indicators.
- Program-level filtering.
- Aggregate institutional reporting.

Individual data shall be exposed only when the authorized university role permits it.

### Notifications

- In-app notifications.
- Account verification emails.
- Password recovery emails.
- Assessment completion notifications.
- Internship application notifications.
- Read/unread status.
- Delivery failure logging.

### Platform Administration

- View and suspend accounts.
- Reactivate accounts.
- Restricted role changes.
- Manage organizations.
- Manage assessments.
- Review reports and disputes.
- Review audit logs.

### Audit Logging

Record:

- Login attempts.
- Password changes.
- Role and membership changes.
- Assessment publication changes.
- Submission evaluation events.
- Verification and revocation changes.
- Application status changes.
- Administrative actions.
- Unauthorized access attempts.

Audit logs shall never store passwords or access tokens.

## Main Deliverables

- University dashboard.
- Aggregate analytics.
- Notification system.
- Email notifications.
- User administration.
- Security audit log review.

## Dependencies

- Phase 2 authorization.
- Phase 3 organization isolation.
- Phase 5 submissions.
- Phase 6 verification.

## Backlog Tickets

- SP-031 — Create University Organization Module.
- SP-032 — Implement Student Progress Analytics.
- SP-033 — Implement Analytics Dashboard.
- SP-036 — Implement Notification System.
- SP-037 — Implement Email Notifications.
- SP-038 — Implement User Administration.
- SP-039 — Implement Security Audit Logging.

## Exit Criteria

- University analytics are limited to authorized institutions.
- Individual student records remain protected.
- Notifications reach only their intended recipients.
- Suspended accounts lose protected access.
- Administrative actions are traceable.

---

# Phase 10 — Testing, Security, and Deployment

## Objective

Harden the platform and establish repeatable testing and production deployment.

## Scope

### Unit Tests

- Models and database constraints.
- Authentication and password handling.
- Permission and ownership logic.
- Scoring and verification calculations.
- Submission state transitions.
- Application state transitions.
- Matching calculations.

### Integration Tests

- Authentication and refresh workflows.
- Assessment submission and result processing.
- Evaluation status updates.
- GitHub integration callbacks.
- Internship application workflows.
- University analytics authorization.

### End-to-End Tests

Test:

- Student registration and login.
- Assessment submission.
- Evaluation result review.
- Skill passport access.
- Public profile visibility.
- Employer candidate search.
- Internship application review.
- Unauthorized route access.

### Security Tests

Test:

- Authentication bypass.
- Expired and revoked tokens.
- Object-level authorization bypass.
- Cross-organization access.
- Evaluation record modification.
- Malicious file uploads.
- SQL injection and XSS.
- CSRF and rate limits.
- Code-execution isolation.
- Host and secret access from submitted code.

### Performance Tests

Measure:

- Standard API response times.
- Candidate search latency.
- Submission throughput.
- Worker queue duration.
- Database query performance.
- Frontend build and route performance.

### Deployment

- Separate development, testing, staging, and production environments.
- Managed or controlled PostgreSQL.
- Managed or controlled Redis.
- Containerized frontend and backend.
- Separate Celery and evaluation workers.
- Object storage.
- HTTPS reverse proxy/CDN.
- Monitoring and structured logging.
- Database backup and restore.
- Migration and rollback procedure.

## Main Deliverables

- Complete test suites.
- Security hardening report.
- Repeatable deployment configuration.
- Monitoring and audit visibility.
- Production readiness checklist.

## Dependencies

- All MVP features.

## Backlog Tickets

- SP-040 — Implement Backend Unit Tests.
- SP-041 — Implement Frontend Component Tests.
- SP-042 — Implement End-to-End Testing.
- SP-043 — Perform Security Testing.
- SP-044 — Configure Production Deployment.

## Exit Criteria

- Critical test suites pass.
- Security testing is complete before production.
- Staging configuration is separate from production.
- HTTPS and secure cookies are enabled.
- Backup and rollback procedures are tested.
- Logs and metrics are usable.
- The complete MVP workflow is demonstrable.

---

# Phase 11 — Pilot and Research Evaluation

## Objective

Validate the platform, scoring model, user experience, and candidate-matching hypothesis using a controlled pilot.

## Scope

### Pilot Setup

- Prepare a controlled assessment catalog.
- Recruit participating students.
- Recruit employers or expert evaluators.
- Recruit authorized university users if included.
- Define consent and retention policies.
- Prepare feedback surveys.
- Prepare expert-reviewed code samples.

### Pilot Targets

Proposed initial targets:

- 100 registered students.
- 5 participating employers or evaluators.
- 10 practical assessments.
- 200 completed submissions.
- 80% assessment completion rate.
- 70% of participating students with at least one verified skill.
- At least 3 employers using candidate search.

These targets are planning goals, not current results.

### Research Metrics

- Test pass rate.
- Assessment completion rate.
- Precision and recall against expert review.
- Inter-rater agreement.
- Candidate ranking quality.
- Student satisfaction.
- Employer satisfaction.
- University analytics usefulness.
- Employer shortlist rate.
- Student return rate.

### Evaluation Boundaries

The pilot shall avoid claiming:

- Guaranteed hiring success.
- Perfect ability measurement.
- Human-independent competence certainty.
- Correlation with future job performance without sufficient evidence.

## Main Deliverables

- Pilot findings report.
- Scoring and confidence evaluation.
- Candidate ranking evaluation.
- UX findings.
- Security and performance observations.
- Prioritized post-pilot backlog.

## Dependencies

- Production or staging deployment.
- Stable assessment and verification workflow.
- Consent, privacy, and reporting process.

## Exit Criteria

- Pilot users can complete the defined workflow.
- Required metrics are collected and documented.
- Major usability issues are prioritized.
- Scoring model limitations are recorded.
- A post-pilot roadmap is approved.

---

# 4. Recommended Development Order

If resources are limited, implement in this order:

1. Frontend and backend foundations.
2. Authentication and RBAC.
3. Student profiles and organizations.
4. Assessment management.
5. Submission and isolated execution.
6. Automated test and quality evaluation.
7. Scoring and evidence.
8. Skill passport.
9. Employer search and internships.
10. University analytics and GitHub integration.
11. Administration and notifications.
12. Security testing and deployment.
13. Pilot evaluation.

A complete, secure core workflow is preferable to many partially implemented features.

---

# 5. Suggested Sprint Mapping

| Sprint | Deliverable |
|---|---|
| 1 | Frontend/backend setup and local infrastructure |
| 2 | Database, Redis/Celery, CI, and health checks |
| 3 | Registration, login, email verification |
| 4 | RBAC, protected routes, password recovery |
| 5 | Student and organization profiles |
| 6 | Assessment models and administration |
| 7 | Assessment listing and details |
| 8 | Submission API and queue |
| 9 | Sandbox execution and test runner |
| 10 | Static analysis and evaluation results |
| 11 | Scoring engine and evidence |
| 12 | Public skill passport |
| 13 | Employer search and internships |
| 14 | Applications and shortlisting |
| 15 | University analytics or GitHub integration |
| 16 | Notifications and user administration |
| 17 | Security hardening |
| 18 | End-to-end testing and deployment |
| 19 | Pilot and research evaluation |

Sprint durations and ownership may be adjusted, but the dependency order should remain stable.

---

# 6. Critical Phase Dependencies

```text
Foundation
    → Authentication/RBAC
    → Profiles/Organizations
    → Assessment Management
    → Submission Queue
    → Isolated Evaluation
    → Evidence and Verification
    → Skill Passport
    → Candidate Search and Internships
    → University Analytics/GitHub
    → Testing and Deployment
    → Pilot Research
```

No downstream feature should bypass the backend authorization, submission integrity, or evidence model established in earlier phases.

---

# 7. Phase-Gate Summary

| Gate | Required Result |
|---|---|
| Gate 1 | Applications, database, Redis, and Celery run locally |
| Gate 2 | Authentication, roles, and protected routes work securely |
| Gate 3 | Profiles and organizations enforce ownership and isolation |
| Gate 4 | Published assessments are accessible to authorized students |
| Gate 5 | Submissions execute safely and produce stored results |
| Gate 6 | Evidence produces skill and confidence records |
| Gate 7 | Employers can search, shortlist, list, and manage applications |
| Gate 8 | GitHub evidence is consent-based and supplementary |
| Gate 9 | University analytics and administration preserve privacy |
| Gate 10 | Tests, security controls, monitoring, and deployment are ready |
| Gate 11 | Pilot data supports measured post-MVP decisions |

---

# 8. Deferred Enhancements

The following shall not block MVP delivery:

- AI-generated assessments.
- Adaptive assessment difficulty.
- Live technical interviews.
- Team project verification.
- Advanced anti-cheating systems.
- Additional supported languages.
- Mobile application.
- AI candidate ranking.
- Freelance marketplace.
- International hiring integrations.
- Professional certification partnerships.
- Microservice decomposition.

Microservices and major architecture changes shall follow measured bottlenecks rather than speculative scaling needs.

---

# 9. Final Outcome

At the end of the implementation phases, SkillProof shall provide a secure, demonstrable MVP where:

- Students demonstrate technical ability through practical work.
- Evaluation occurs asynchronously in isolation.
- Assessment evidence supports transparent skill scores.
- Verification confidence is separate from competency level.
- Students control an evidence-based public profile.
- Employers can discover and review qualified candidates.
- Universities can inspect authorized aggregate employability data.
- Administrative actions are controlled and audited.
- The full workflow can be tested, measured, deployed, and used in a pilot.
