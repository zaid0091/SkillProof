# SkillProof — Detailed Build Plan

**Document Version:** 1.0  
**Status:** Proposed implementation plan  
**Purpose:** Define the ordered implementation strategy for building the SkillProof MVP without contradicting the Product Requirements Document (PRD), Technical Architecture Document (TAD), Frontend and Integration Specification (FIS), Feature Ticket List (FTL), or Security and Access Control Specification (SACS).

---

# 1. Build Objectives

The implementation shall produce a secure, verifiable, and demonstrable end-to-end workflow:

**Student registers → completes an assessment → submits code → receives isolated automated evaluation → obtains skill evidence → displays a verified skill passport → becomes discoverable to authorized employers.**

The build must prioritize:

1. Security and tenant isolation.
2. The complete assessment and evaluation workflow.
3. Transparent evidence-based skill scoring.
4. Student, employer, university, and administrator role support.
5. Deployment-ready infrastructure.
6. Automated testing and auditable changes.
7. Measured MVP scope rather than speculative future expansion.

The initial supported execution language is Python. Additional languages may be introduced only after the core pipeline is stable.

---

# 2. Scope Boundaries

## 2.1 In Scope for the MVP

- User registration, verification, login, logout, password recovery, and JWT authentication.
- Student, employer, university, and administrator roles.
- Role-based and object-level authorization.
- Student profile and public profile visibility controls.
- Organization membership and employer profiles.
- Assessment creation, publication, listing, details, and administration.
- Code submission, submission history, status tracking, and cancellation.
- Isolated Python code execution with resource limits.
- Automated test execution and code-quality analysis.
- Evidence-based skill scoring and verification confidence.
- Public and protected skill passports.
- Basic employer candidate search and shortlisting.
- Internship listing, application, status update, and application history workflows.
- University aggregate analytics.
- GitHub OAuth and contribution evidence as a supplementary feature.
- Notifications, administrative moderation, audit logs, testing, monitoring, and deployment.

## 2.2 Deferred until after MVP stabilization

- AI-generated assessments.
- Adaptive assessment difficulty.
- Live interviews.
- Team project verification.
- Additional first-class programming languages.
- Advanced anti-cheating systems.
- Mobile applications.
- AI candidate ranking.
- Full freelance marketplace.
- International hiring integrations.
- Professional certification partnerships.

## 2.3 Explicit Non-Goals

The MVP shall not:

- Guarantee employment or internship placement.
- Automatically make hiring decisions.
- Replace university degrees.
- Claim to prove all technical skills.
- Treat GitHub activity alone as verified competency.
- Automatically assume that AI-assisted code is cheating.
- Make job recommendations without transparent matching factors.

---

# 3. Technology Decisions

## 3.1 Approved Core Stack

| Area | Technology |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | Django, Django REST Framework |
| Database | PostgreSQL |
| Cache and broker | Redis |
| Async tasks | Celery |
| Code execution | Docker-based isolated workers |
| Python test execution | pytest |
| Python quality analysis | Ruff/Pylint and Radon |
| Coverage analysis | Coverage.py |
| File storage | S3-compatible object storage |
| Authentication | SimpleJWT with secure refresh-token handling |
| Frontend state | Zustand where appropriate |
| API state/caching | TanStack Query |
| Forms | React Hook Form and Zod |
| Charts | Recharts |
| Icons | Lucide React |
| Testing | pytest, Vitest, React Testing Library, and Playwright |

## 3.2 Architecture Pattern

Use a modular Django monolith for application logic. Use separate Celery and execution workers for expensive or untrusted operations.

Do not introduce microservices until a measured bottleneck justifies independent deployment and scaling.

## 3.3 Repository Structure

The final workspace should contain separate frontend and backend applications unless a monorepo arrangement is explicitly chosen during setup.

```text
SkillProof/
├── frontend/
├── backend/
├── infrastructure/
├── docs/
├── scripts/
└── README.md
```

---

# 4. Implementation Strategy

## 4.1 Development Principles

- Backend authorization is always authoritative.
- Frontend route guards improve usability but provide no security boundary.
- Every assessment result shall retain its source evidence.
- Submission and verification records shall remain immutable to ordinary users.
- Data mutations shall use database transactions where consistency is required.
- State transitions shall be explicit and validated.
- Public APIs shall expose only safe, permitted fields.
- Files and source code shall be stored with least-necessary access.
- Scoring and matching logic shall be documented and reproducible.
- External integrations shall be replaceable and isolated.

## 4.2 Delivery Principle

The application shall be developed vertically wherever practical. A phase is not complete merely when its backend or frontend exists in isolation; it is complete only when the relevant workflow can be used securely through the application.

## 4.3 Definition of Done

A feature is complete when:

- It satisfies its documented acceptance criteria.
- Relevant backend validation and permissions are implemented.
- Frontend loading, empty, success, validation, and error states are handled.
- Ownership and organization isolation are tested.
- Unit and integration tests cover critical behavior.
- Security-sensitive behavior receives security tests.
- Migrations are safe and documented.
- API contracts are documented.
- Operational and environment requirements are recorded.
- Code has been reviewed and no unresolved high-severity issues remain.

---

# 5. Phase 1 — Project Foundation and Infrastructure

**Objective:** Establish both applications, local infrastructure, configuration conventions, and repository quality gates.

**Associated backlog:** SP-001, SP-002, SP-003, SP-004

## 5.1 Frontend Foundation

Build:

- Next.js App Router project.
- TypeScript configuration.
- Tailwind CSS configuration.
- Base public and dashboard route structure.
- Reusable application layout and UI primitives.
- Environment variable conventions.
- Centralized API client foundation.
- Global loading, error, empty, and notification patterns.

Required UI primitive families:

- Button, input, textarea, select, and checkbox.
- Cards and panels.
- Badges and status indicators.
- Modal and confirmation dialog.
- Data table and pagination.
- Loading spinner and skeleton.
- Toast notification.
- Error and empty-state components.

## 5.2 Backend Foundation

Build:

- Django project configured for environment-based settings.
- Django REST Framework setup.
- PostgreSQL connection.
- Initial domain applications.
- Common permissions, exceptions, validators, and utilities.
- Structured API error responses.
- Initial health and readiness endpoints.
- CORS, HTTPS, and security configuration.
- Centralized logging configuration.

Backend modules should follow the proposed domain structure:

- `accounts`
- `organizations`
- `profiles`
- `skills`
- `assessments`
- `submissions`
- `evaluations`
- `evidence`
- `github_integration`
- `hiring`
- `analytics`
- `notifications`
- `audit`

## 5.3 Infrastructure Foundation

Configure:

- PostgreSQL.
- Redis.
- Celery worker.
- Celery beat if scheduled tasks are needed.
- Object storage integration or local development substitute.
- Docker Compose for development.
- `.env.example` files.
- Secrets exclusion through `.gitignore`.
- Setup and shutdown documentation.

Create a smoke-test background task to prove that the API, Redis, and worker communicate successfully.

## 5.4 Exit Criteria

- Frontend and backend start independently.
- PostgreSQL migrations can run successfully.
- Redis and Celery execute a test task.
- Secrets are environment-configured.
- Base route structure and API health endpoints work.
- CI runs at least baseline lint and test commands.

---

# 6. Phase 2 — Authentication and Role Management

**Objective:** Implement a secure identity and authorization foundation for every later workflow.

**Associated backlog:** SP-005, SP-006, SP-007, SP-008, SP-009

## 6.1 Account Model

Implement:

- UUID-based users.
- Unique email addresses.
- Secure password storage.
- Account status.
- Email verification status.
- Role assignment owned by the backend.
- Account creation and update timestamps.
- Account audit events.

## 6.2 Registration and Verification

Implement:

- Email/password registration.
- Password policy validation.
- Duplicate-email rejection.
- Email-verification tokens.
- Time-limited verification links.
- Appropriate public registration responses.

Restrict sensitive operations until email verification is complete, while deciding consistently which read-only actions remain available.

## 6.3 Login and Token Handling

Implement:

- Short-lived access tokens.
- Longer-lived refresh tokens.
- Refresh-token rotation or revocation.
- Secure logout and token invalidation.
- Refresh failure handling.
- Protected endpoint authentication checks.
- Consistent unauthorized and forbidden responses.

For the web frontend:

- Access tokens remain in memory where practical.
- Refresh tokens use secure HttpOnly cookies.
- Secure and appropriate SameSite cookie settings are used in production.
- Concurrent refresh requests are coordinated.

## 6.4 Password Recovery

Implement:

- Verified email lookup.
- Time-limited, single-use reset tokens.
- Password update confirmation.
- Existing session/refresh-token invalidation after reset.
- Non-disclosing recovery responses.

## 6.5 RBAC

Implement four primary roles:

- Student.
- Employer.
- University.
- Administrator.

The backend shall additionally enforce:

- Object ownership.
- Organization membership.
- Organization membership role.
- Resource-specific permissions.
- Active account and verified-email state where required.

## 6.6 Frontend Protection

Implement:

- Authentication state.
- Login and registration pages.
- Role-based navigation.
- Protected route middleware or layout checks.
- Appropriate unauthorized/forbidden states.
- Automatic redirect after token expiration or logout.

## 6.7 Exit Criteria

- Each role can authenticate and reach only its permitted routes.
- Cross-role API access is denied.
- Role values cannot be assigned through an ordinary registration request.
- Password recovery and email verification are usable and secure.
- Authentication events are audited.
- Refresh and logout behavior is reliable.

---

# 7. Phase 3 — Profiles and Organization Management

**Objective:** Establish data ownership and multi-tenant organizational boundaries.

**Associated backlog:** SP-010, SP-011, SP-012, SP-027, SP-031

## 7.1 Student Profiles

Fields include:

- Full name.
- Profile picture.
- University.
- Degree program.
- Graduation year.
- Biography or professional summary.
- Technical interests.
- GitHub and LinkedIn links.
- Resume metadata.
- Profile visibility settings.

Implement:

- Profile creation.
- Profile update.
- Public and private field presentation.
- Owner-only editing.
- Public profile access by username or share identifier.
- Clear separation of self-reported and verified skills.

## 7.2 Organization Records

Implement:

- Company/university organization type.
- Organization profile fields.
- Organization membership records.
- Membership roles and statuses.
- Invitations or approval workflow if used.
- Organization ownership transfer procedures.

## 7.3 Employer and University Features

Employer profile support shall allow:

- Organization management.
- Organization member management.
- Authorized hiring operations.

University support shall allow:

- University organization details.
- Authorized member management.
- Authorized institutional reporting.

## 7.4 Data Isolation

Every organization query shall enforce membership.

The backend shall reject:

- Employer access to another employer's records.
- University access to another university's students or analytics.
- User-supplied organization identifiers that bypass membership checks.

## 7.5 Exit Criteria

- Student profiles are owner-editable.
- Public visibility excludes private fields.
- Organization membership is represented safely.
- Cross-organization access tests pass.
- Employer and university role boundaries are distinct.

---

# 8. Phase 4 — Assessment Management

**Objective:** Create and publish practical assessments before implementing submissions.

**Associated backlog:** SP-013, SP-014, SP-015, SP-016

## 8.1 Assessment Domain Model

Assessment fields:

- Title.
- Description.
- Required skill.
- Difficulty.
- Duration/time limit.
- Draft/published status.
- Creator/administrator.
- Creation and update timestamps.

Assessment task fields:

- Instructions.
- Task type.
- Evaluation configuration.
- Submission constraints.
- Restricted test configuration.

## 8.2 Initial Assessment Catalog

The MVP should begin with a controlled Python-only catalog. Suggested first categories:

- Python fundamentals.
- Django REST API development.
- Database design and SQL.
- Software testing.
- Debugging.
- Code review.

Each assessment shall define:

- Public requirements.
- Submission rules.
- Example inputs and outputs where useful.
- Public evaluation dimensions.
- Restricted tests that remain private.

## 8.3 Administration Workflow

Administrators or authorized assessment owners shall:

- Create assessments.
- Add assessment tasks.
- Configure test and quality criteria.
- Save drafts.
- Validate configuration.
- Publish assessments.
- Unpublish assessments.
- Audit changes.

## 8.4 Student Experience

Build:

- Assessment listing page.
- Filtering and sorting.
- Assessment detail page.
- Required skills and constraints.
- Loading and empty states.
- Clear entry to the submission workflow.

## 8.5 Exit Criteria

- Authorized users can create and publish assessments.
- Draft assessments are inaccessible to ordinary students.
- Required skill associations and evaluation configuration validate.
- Assessment listing and details are usable.
- Assessment changes are auditable.

---

# 9. Phase 5 — Secure Submission and Evaluation Pipeline

**Objective:** Implement the core technical innovation: a reliable, isolated, asynchronous code evaluation workflow.

**Associated backlog:** SP-017, SP-018, SP-019, SP-020, SP-021, SP-022

## 9.1 Submission API

Submission fields:

- Student owner.
- Assessment.
- Source type.
- Source location or file reference.
- Submitted timestamp.
- Status.
- Attempt metadata.
- Evaluation metadata.

Submission states:

```text
Pending → Queued → Running → Completed
                         → Failed
                         → Cancelled
```

Every transition shall be validated. Pending shall never transition directly to Completed.

## 9.2 Submission Validation

Before queueing:

- Verify assessment eligibility and publication status.
- Verify student ownership and account status.
- Enforce attempt and deadline limits.
- Validate file size and format.
- Reject archive types or files outside the permitted format.
- Store only authorized source artifacts.
- Generate a submission identifier that is not used for direct object access without permission.

## 9.3 Submission Storage

Use object storage or a controlled file subsystem for source artifacts.

The backend shall:

- Store source location metadata.
- Authorize every download.
- Use temporary access links only if needed.
- Apply retention policies.
- Prevent ordinary users from accessing restricted assessment test files.

## 9.4 Celery Integration

A submission workflow shall:

1. Validate the submission.
2. Create a database record.
3. Store source metadata.
4. Mark the submission queued.
5. Publish a task with the submission identifier.
6. Return accepted status to the frontend.

Worker failures shall:

- Update the submission safely.
- Avoid corrupting earlier records.
- Be retried only for recoverable conditions.
- Become permanently failed after retry limits.
- Be logged without exposing secrets or source code.

## 9.5 Isolated Execution

Each execution environment shall have:

- A separate container/image.
- Non-root execution.
- CPU limits.
- Memory limits.
- Strict timeout.
- Process limits.
- Restricted filesystem access.
- No production database access.
- No Redis administrative access.
- No application secrets.
- Restricted or disabled network access.
- Temporary workspace.
- Automatic cleanup.

Standard Docker isolation shall be treated as insufficient for a strong production threat model. Evaluate stronger sandboxing before deployment if available.

## 9.6 Evaluation Steps

The worker shall:

- Retrieve authorized submission metadata.
- Reconstruct the permitted execution workspace.
- Install or use predefined dependencies.
- Run assessment tests.
- Capture pass/fail and timeout data.
- Run supported static analysis.
- Calculate coverage if configured.
- Collect normalized metrics.
- Return a structured result object.
- Destroy the environment.

The Django API must not execute untrusted code.

## 9.7 Code Quality Analysis

For supported Python submissions collect:

- Complexity indicators.
- Duplication indicators.
- Maintainability indicators.
- Test coverage.
- Coding convention findings.
- Potential security or best-practice findings.

Tool crashes or unsupported formats shall produce appropriate status information rather than silently changing the score.

## 9.8 Evaluation Results

Store:

- Submission identifier.
- Functional score.
- Quality score.
- Testing score.
- Security/best-practice score.
- Total score.
- Execution status.
- Test-level details.
- Tool-specific findings.
- Completion timestamp.
- Evaluation schema/version.

Students and employers shall read results only according to permissions. Ordinary users shall not modify them.

## 9.9 Frontend Workflow

Build:

- Submission interface.
- File/repository submission control.
- Submission validation feedback.
- Status polling until completion.
- Pending, queued, running, completed, failed, and cancelled visual states.
- Submission history.
- Evaluation result detail page.
- Retry/cancel behavior where permitted.

If WebSockets are later added, polling shall remain as a fallback.

## 9.10 Exit Criteria

- A valid submission enters the queue and completes end to end.
- Invalid submissions are rejected without queueing.
- Resource limits and timeout behavior work.
- Production secrets are inaccessible to submitted code.
- Test failures and worker failures are represented safely.
- Submission owners only can access private submission records.
- Evaluation results are read-only to students and employers.

---

# 10. Phase 6 — Evidence and Skill Verification

**Objective:** Convert evaluation results into explainable skill records and confidence.

**Associated backlog:** SP-023, SP-024, SP-025, SP-026

## 10.1 Scoring Dimensions

The initial configurable weighted model:

| Dimension | Weight |
|---|---:|
| Functional correctness | 30% |
| Problem solving | 20% |
| Code quality | 15% |
| Testing | 15% |
| Security and best practices | 10% |
| Project contribution evidence | 10% |

The weight configuration shall be versioned so previous verification records remain reproducible.

## 10.2 Normalization

All dimensions shall be normalized to the same scale before aggregation.

The formula is:

$$
S = \sum_{i=1}^{n} w_i s_i
$$

Where:

- $S$ is the competency score.
- $w_i$ is the configured dimension weight.
- $s_i$ is the normalized evidence dimension score.

## 10.3 Evidence Records

Evidence types may include:

- Coding assessment.
- Project assessment.
- Code review.
- Human evaluation.
- Debugging task.
- GitHub contribution.

Each record shall retain:

- Student.
- Skill.
- Evidence type.
- Source identifier.
- Score.
- Confidence inputs.
- Creation timestamp.
- Scoring model version.
- Revocation status.

## 10.4 Verification Confidence

Skill score and verification confidence shall remain separate values.

Confidence inputs may include:

- Number of completed assessments.
- Difficulty.
- Evidence diversity.
- Evidence recency.
- Consistency across submissions.
- Human evaluator confirmation.

Confidence shall not be labeled a probability unless statistically calibrated.

## 10.5 Verification Workflow

After successful evaluation:

1. Store the evaluation result.
2. Create or update evidence records.
3. Recalculate the skill score.
4. Recalculate confidence.
5. Update the verification record.
6. Retain prior values for audit/history if needed.

A verification record shall become inactive or revoked when evidence is revoked or invalidated.

## 10.6 Skill Passport

Build:

- Verified skills view.
- Skill score and confidence display.
- Evidence source links.
- Assessment history.
- Last verification date.
- Visibility controls.
- Public and authenticated views.
- Clear distinction between claimed and verified skills.

## 10.7 Exit Criteria

- Every verified skill has evidence.
- Scores are reproducible with a named scoring-model version.
- Confidence is separate and explainable.
- Revocation removes active verification.
- Public profiles omit private evidence and information.

---

# 11. Phase 7 — Employer Hiring Features

**Objective:** Add candidate discovery and internship application workflows after the verification pipeline is stable.

**Associated backlog:** SP-027, SP-028, SP-029, SP-030

## 11.1 Candidate Search

Search filters:

- Technical skill.
- Verified score.
- Assessment level.
- University.
- Graduation year.
- Project evidence.
- Internship availability.

Candidate search shall:

- Return public or explicitly authorized profiles.
- Exclude private student fields.
- Expose evidence and matching factors.
- Support pagination and sorting.
- Display backend ranking rather than frontend-calculated ranking.

The MVP matching score shall remain transparent:

$$
M = \sum_{i=1}^{n} r_i v_i
$$

Where:

- $M$ is the normalized matching score.
- $r_i$ is the required-skill importance.
- $v_i$ is the candidate's verified competency.

Protected characteristics shall not be used in ranking.

## 11.2 Shortlisting

Build:

- Employer shortlist creation.
- Organization ownership verification.
- Candidate add/remove operations.
- Shortlist review by authorized organization users.
- Audit entries for shortlist changes.

## 11.3 Internship Listings

Employer capabilities:

- Create internships.
- Add title and description.
- Specify required skills.
- Specify location and deadline.
- Publish or close a listing.
- Edit organization-owned listings.

Students shall see only published opportunities.

## 11.4 Applications

Application states:

- Submitted.
- Under Review.
- Shortlisted.
- Interview.
- Accepted.
- Rejected.
- Withdrawn.

Implement:

- Duplicate application prevention.
- Eligible-listing checks.
- Student application history.
- Employer application review.
- Valid state transitions.
- Student status updates.
- Application audit history.

## 11.5 Exit Criteria

- Search and matching respect profile visibility.
- Another organization cannot access private applications or shortlists.
- Application state transitions are valid and audited.
- Students can apply and track applications.
- Employers can manage listings and review authorized candidates.

---

# 12. Phase 8 — GitHub Integration

**Objective:** Add supplementary project-contribution evidence without conflating activity with verification.

**Associated backlog:** SP-034, SP-035

## 12.1 OAuth Workflow

Implement:

- GitHub authorization initiation.
- State/PKCE protection if supported.
- Callback validation.
- Permission explanation.
- Secure token storage.
- Integration status.
- Disconnect and revocation workflow.

OAuth secrets and access tokens shall remain backend-only.

## 12.2 Repository Synchronization

Retrieve only authorized repository data:

- Commits.
- Pull requests.
- Code-review activity.
- Repository participation.
- Files and test/documentation changes where permitted.

Handle:

- GitHub API outages.
- Rate limits.
- Revoked OAuth access.
- Repository visibility changes.
- Partial synchronization.

## 12.3 Evidence Presentation

GitHub evidence shall:

- Be student-approved before profile inclusion.
- Remain supplementary.
- Include source, repository, and timestamp context.
- Clearly explain limitations.
- Never establish a verified skill independently.

## 12.4 Exit Criteria

- OAuth authorization and revocation work safely.
- Private repository data is never exposed without permission.
- GitHub API failures are recoverable.
- Project contribution evidence cannot be self-added as an automatic verified skill.

---

# 13. Phase 9 — University Analytics and Administration

**Objective:** Provide institutional and platform-management capabilities while preserving privacy.

**Associated backlog:** SP-031, SP-032, SP-033, SP-036, SP-037, SP-038, SP-039

## 13.1 University Analytics

Provide:

- Assessment participation.
- Completion rates.
- Skill distribution.
- Competency gaps.
- Student progress.
- Employability readiness indicators.
- Program-level filtering.

The analytics engine shall:

- Filter by authorized institution and program.
- Prefer aggregate results.
- Apply a minimum reporting population where necessary.
- Avoid exposing individuals without authorization.
- Use backend-provided chart data.

## 13.2 Notifications

Implement:

- In-app notification records.
- Recipient ownership.
- Read/unread state.
- Assessment completion notifications.
- Application status notifications.
- Email verification and password recovery.
- Notification delivery retry and failure logging.

## 13.3 User and Assessment Administration

Administrators shall manage:

- User status.
- Role assignments within policy limits.
- Organization records.
- Assessment availability.
- Reported profiles.
- Disputes.
- Security-related account restrictions.

## 13.4 Audit Logging

Log:

- Login success/failure.
- Password changes.
- Role changes.
- Organization membership changes.
- Assessment publication changes.
- Submission evaluation events.
- Verification and revocation changes.
- Application status changes.
- Administrative actions.
- Unauthorized-access attempts.

Logs shall exclude passwords, access tokens, source code, and unnecessary private data.

## 13.5 Exit Criteria

- Universities see only authorized institutional data.
- Student-level access within university analytics is controlled.
- Notifications reach the correct recipient.
- Administrative actions are audited.
- Suspended accounts lose protected access.

---

# 14. Phase 10 — Testing, Hardening, and Deployment

**Objective:** Demonstrate that the MVP is secure, reliable, testable, and deployable.

**Associated backlog:** SP-040, SP-041, SP-042, SP-043, SP-044

## 14.1 Unit Testing

Backend unit tests shall cover:

- Registration and authentication.
- Password policy.
- Permission and ownership checks.
- Scoring calculations.
- Confidence updates.
- Submission state transitions.
- Application state transitions.
- Matching calculations.
- Organization isolation.

Frontend unit tests shall cover:

- Reusable components.
- Form validation.
- Loading and error states.
- Status rendering.
- Public/private evidence presentation.

## 14.2 Integration Testing

Test:

- Login and refresh workflows.
- Email verification and password recovery.
- Assessment creation and publication.
- Submission queue and worker result processing.
- Scoring and verification updates.
- Candidate search.
- Internship application lifecycle.
- GitHub callback and synchronization.
- University analytics access.

## 14.3 End-to-End Testing

At minimum, Playwright shall cover:

- Student registration and login.
- Profile creation.
- Assessment submission.
- Evaluation completion.
- Verified skill passport.
- Public profile visibility.
- Employer candidate search.
- Internship application and status review.
- Unauthorized route access.
- University analytics access.

## 14.4 Security Testing

Test:

- Token expiration and revocation.
- Object-level authorization bypass.
- Cross-employer isolation.
- Cross-university isolation.
- Student/private submission access.
- Unauthorized evaluation modification.
- Malicious file upload types.
- SQL injection and XSS prevention.
- CSRF protection.
- Rate limiting.
- Worker isolation and resource limits.
- Access to host filesystem and secrets.
- Network restriction.
- Security logs and sensitive-data exclusion.

## 14.5 Performance Testing

Measure:

- API response times below 500 ms under normal load for standard operations.
- Candidate search below 2 seconds for the pilot dataset.
- Concurrent submission handling.
- Queue depth and task duration.
- Worker retry behavior.
- Database query counts and slow queries.
- Frontend build size and route performance.

## 14.6 Deployment

Prepare:

- Separate development, testing, staging, and production environments.
- Managed PostgreSQL.
- Managed Redis or equivalent.
- Containerized Next.js frontend.
- Containerized Django API.
- Separate Celery workers.
- Separate isolated evaluation workers.
- Object storage.
- HTTPS reverse proxy/CDN.
- Environment-specific secrets.
- Database migration procedure.
- Backup and restore procedures.
- Monitoring and structured logging.
- Worker health and queue monitoring.

## 14.7 Production Readiness Checklist

Before production:

- HTTPS and secure cookies are verified.
- Refresh-token revocation is enabled.
- RBAC and object-level permissions are tested.
- Assessment sandbox limits are tested.
- Database backup and restore are tested.
- Secrets are not in source control.
- Public profile fields are explicitly allowlisted.
- Restricted test cases are inaccessible.
- Audit logs contain no credentials or unnecessary source content.
- Error monitoring is configured.
- API and worker metrics are visible.
- Incident response contacts and procedures exist.

## 14.8 Exit Criteria

- Critical test suites pass.
- Security tests pass before production.
- Staging and production configurations are separated.
- Deployment is repeatable.
- Logs and metrics are usable.
- Backup and rollback procedures are documented.
- The MVP workflow can be demonstrated from registration through candidate discovery.

---

# 15. Phase 11 — Pilot Validation and Research Evaluation

**Objective:** Evaluate the platform and evidence model with real or controlled pilot participants.

## 15.1 Pilot Preparation

Prepare:

- 10 practical assessments.
- 100–500 student pilot cohort.
- 5–20 participating employers or evaluators.
- Public and institutional consent processes.
- Privacy and data-retention notices.
- Recruitment materials.
- User feedback questionnaires.
- Candidate-matching experiments.
- Expert code-review samples.

## 15.2 Research Measurements

Measure:

- Test pass rate.
- Assessment completion rate.
- Skill verification rate.
- Precision and recall against expert-reviewed competencies.
- Inter-rater agreement.
- Candidate ranking quality.
- Student satisfaction.
- Employer satisfaction.
- Employer candidate search activity.
- Employer shortlist rate.
- University participant adoption.

## 15.3 Evaluation Limitations

The platform shall not claim:

- Guaranteed hiring performance.
- Perfect ability measurement.
- Human-independent skill certainty.
- Correlation with future success without sufficient study.

## 15.4 Pilot Outputs

Produce:

- Scoring-model evaluation report.
- Reliability findings.
- UX findings.
- Security and performance report.
- Employer adoption observations.
- University analytics usability report.
- Prioritized recommendations for the next release.

---

# 16. Sprint Planning Guidance

The feature backlog can be divided into 2–3 week iterations.

## Recommended Sprint Sequence

| Sprint | Primary Output |
|---|---|
| 1 | Frontend/backend initialization and Docker development environment |
| 2 | PostgreSQL, Redis, Celery, health checks, and CI baseline |
| 3 | Registration, login, email verification, and token handling |
| 4 | Roles, RBAC, protected routes, and password recovery |
| 5 | Student and organization profiles |
| 6 | Assessment models and administration |
| 7 | Assessment listing and details |
| 8 | Submission API and worker queue |
| 9 | Sandbox execution and test runner |
| 10 | Static analysis and evaluation results |
| 11 | Scoring engine and evidence records |
| 12 | Public skill passport |
| 13 | Employer search and internship management |
| 14 | Applications and shortlisting |
| 15 | University analytics or GitHub integration |
| 16 | Notifications and administration |
| 17 | Security hardening |
| 18 | End-to-end testing and deployment |
| 19 | Pilot and research evaluation |

This is a planning sequence, not a fixed calendar commitment. Sprints may overlap for frontend/backend ownership and testing.

---

# 17. Critical Dependencies

The build should respect these dependencies:

- Authentication precedes protected features.
- RBAC precedes organization and object-level workflows.
- Profiles precede public passport features.
- Assessment management precedes submission features.
- Submission storage precedes isolated execution.
- Celery setup precedes evaluation queueing.
- Isolated execution precedes automated test scoring.
- Evaluation results precede evidence and verification.
- Organization membership precedes employer/university resource isolation.
- Candidate search precedes ranking validation.
- Security testing precedes production deployment.

---

# 18. Risk Register and Mitigations

## 18.1 Secure Code Execution

**Risk:** Untrusted code could access secrets or host resources.

**Mitigation:**

- Separate execution worker.
- Non-root containers.
- Resource limits.
- Restricted filesystem/network.
- Production secret separation.
- Sandbox security testing.
- Evaluate stronger sandbox technologies.

## 18.2 Scoring Accuracy

**Risk:** Automated scoring could misrepresent competency.

**Mitigation:**

- Transparent dimensions and weights.
- Separate confidence.
- Versioned scoring models.
- Human evaluator review.
- Appeals and revocation.
- Pilot validation.

## 18.3 Cheating and Copying

**Risk:** Students may reuse code or unauthorized solutions.

**Mitigation:**

- Randomized assessment variants.
- Debugging and explanation tasks.
- Submission-pattern monitoring.
- Human review.
- Plagiarism detection where appropriate.
- Explicit assessment policies.

## 18.4 Employer Adoption

**Risk:** Employers may not trust a new platform.

**Mitigation:**

- Begin with local partners.
- Make evidence inspectable.
- Invite employer assessment requirements.
- Controlled pilot.
- Avoid false hiring guarantees.

## 18.5 Privacy Exposure

**Risk:** Student or organization data may leak.

**Mitigation:**

- RBAC and object-level permissions.
- Public field allowlists.
- Tenant isolation tests.
- Consent-based GitHub access.
- Audit logging.
- Data minimization and retention controls.

## 18.6 Scope Creep

**Risk:** Future features could delay the core workflow.

**Mitigation:**

- Freeze MVP scope.
- Prioritize P0/P1 tickets.
- Defer university and GitHub features if core stability requires it.
- Measure before architectural expansion.

## 18.7 Infrastructure Complexity

**Risk:** Delivery could exceed FYP resources.

**Mitigation:**

- Modular monolith.
- Docker Compose development environment.
- Limited language support.
- Controlled assessment catalog.
- Managed production services where practical.

---

# 19. Team Workstream Organization

A small team may divide work into these workstreams:

## Frontend Workstream

- Public pages and authentication.
- Role dashboards.
- Assessment and submission UI.
- Skill passport.
- Employer and application UI.
- University analytics.
- Component tests and E2E testing.

## Backend Workstream

- Accounts and permissions.
- Profiles and organizations.
- Assessments and submissions.
- Scoring and evidence.
- Hiring and applications.
- GitHub integration.
- Analytics and notifications.

## Infrastructure and Security Workstream

- Docker Compose and deployments.
- Redis/Celery.
- Isolated execution.
- PostgreSQL and object storage.
- Monitoring, audit logs, and backups.
- Security testing.

## QA and Research Workstream

- Test planning.
- API and E2E test suites.
- Pilot dataset.
- Expert evaluation.
- User research.
- Scoring validation.
- Performance and accessibility checks.

Workstreams should share API contract, data model, acceptance criteria, and security review ownership.

---

# 20. API and Contract Governance

Create one source of truth for API contracts:

- Versioned endpoint documentation.
- Typed frontend response models.
- Backend serializer schemas.
- Example success and error responses.
- Pagination and filtering conventions.
- Field visibility and permission documentation.
- State-transition documentation.

Breaking API changes should be versioned. Internal endpoint changes should update frontend types and integration tests simultaneously.

---

# 21. Data and Migration Strategy

Before implementation:

- Finalize core entities and relationships.
- Use migrations for every schema change.
- Prefer additive migrations during production rollout.
- Define foreign-key and uniqueness constraints.
- Index high-frequency filtering fields.
- Plan soft deletion or retention for sensitive records.
- Document record retention and revocation behavior.

The database should enforce:

- Unique emails.
- Valid membership roles.
- Valid assessment status transitions where enforceable.
- Valid application status transitions where enforceable.
- Referential integrity for submissions and evaluation records.

---

# 22. MVP Milestones

## Milestone A — Platform Foundation

- Applications run locally.
- PostgreSQL, Redis, and Celery operate.
- Authentication and RBAC work.

## Milestone B — End-to-End Assessment

- Assessment publication works.
- Submission queues.
- Code executes in isolation.
- Tests run and results are stored.

## Milestone C — Verification

- Evaluation feeds evidence.
- Scoring and confidence are displayed.
- Public/private skill passports work.

## Milestone D — Hiring

- Candidate search works.
- Internship listings and applications work.
- Shortlists and status updates work.

## Milestone E — Institutional and Production Readiness

- University analytics are available within permissions.
- GitHub evidence is available if included in the pilot.
- Administration, notifications, audit logs, and deployment are complete.

## Milestone F — Pilot

- The workflow is demonstrated in a controlled environment.
- Research metrics are collected.
- Employer, university, and student feedback inform the next roadmap.

---

# 23. Acceptance Criteria for the MVP

The MVP shall be accepted when:

1. A student can register, verify, log in, and create a profile.
2. A published assessment can be viewed only as permitted.
3. A student can submit valid Python code.
4. The submission is queued and evaluated safely.
5. The evaluation reports functional, quality, testing, and security findings.
6. A backend scoring process creates evidence and a skill verification record.
7. The student can view a public or private skill passport.
8. A public profile does not expose private submissions or personal fields.
9. An employer can search authorized candidates and evidence.
10. An employer can create and manage an internship listing.
11. A student can apply and track the application.
12. An employer can review and update authorized applications.
13. A university can view only permitted aggregate institutional analytics.
14. Administrators can manage users and view protected audit logs.
15. The entire workflow passes security, integration, end-to-end, and deployment checks.

---

# 24. Recommended MVP Sequencing

If time or resources become constrained, implementation priority should remain:

1. Project infrastructure.
2. Accounts and RBAC.
3. Profiles and organization isolation.
4. Assessments.
5. Submission and sandbox execution.
6. Automated test evaluation.
7. Code-quality reporting.
8. Scoring, evidence, and passport.
9. Candidate search and internships.
10. University analytics and GitHub integration.
11. Advanced notifications and administration.
12. Pilot research and refinement.

A partial but complete core workflow is more valuable than numerous partially implemented features.

---

# 25. Post-MVP Roadmap

After MVP stabilization, consider:

- Multi-language execution images.
- Adaptive difficulty.
- AI-assisted assessment authoring with human approval.
- Team project contribution verification.
- Stronger anti-cheating methods.
- Search and ranking infrastructure.
- Advanced analytics and curriculum mapping.
- Company-specific assessment templates.
- Industry-recognized credentials.
- Mobile applications.
- International employer integrations.
- Microservice extraction only for measured scaling needs.

---

# 26. Final Build Principle

Build the smallest complete, secure, evidence-producing system first. The core value is not the number of screens or integrations; it is the integrity of the full pipeline from submitted work to explainable, revocable, verified skill evidence.
