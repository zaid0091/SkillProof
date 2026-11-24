# Feature Ticket List (FTL)

## SkillProof — Verified Skills and Project-Based Hiring Platform

**Document Type:** Feature Ticket List  
**Project:** SkillProof  
**Version:** 1.0  
**Status:** Proposed Backlog  
**Development Methodology:** Agile / Scrum  
**Prepared For:** Final Year Project (FYP)

---

## 1. Introduction

### 1.1 Purpose

This document defines the development backlog for the SkillProof platform.

The Feature Ticket List breaks the platform's requirements into manageable development tasks that can be implemented, tested, and reviewed during development.

Each ticket contains:

- Ticket ID
- Feature or task title
- User story or technical description
- Priority
- Estimated effort
- Acceptance criteria
- Dependencies

### 1.2 Priority Definitions

| Priority | Meaning |
|---|---|
| P0 — Critical | Required for the core platform to function |
| P1 — High | Required for the MVP or essential user workflows |
| P2 — Medium | Important but can be implemented after core functionality |
| P3 — Low | Optional enhancement or future improvement |

### 1.3 Story Point Estimation

Story points represent relative development effort.

| Story Points | Estimated Complexity |
|---|---|
| 1 | Very small task |
| 2 | Small task |
| 3 | Moderate task |
| 5 | Complex task |
| 8 | Very complex task |
| 13 | Large task requiring breakdown |

Story points are estimates, not fixed development hours.

---

# 2. Epic Overview

| Epic ID | Epic Name |
|---|---|
| EP-01 | Project Setup and Infrastructure |
| EP-02 | Authentication and Access Control |
| EP-03 | Student Profile Management |
| EP-04 | Assessment Management |
| EP-05 | Submission and Code Evaluation |
| EP-06 | Skill Verification and Evidence |
| EP-07 | Employer and Hiring Management |
| EP-08 | University Analytics |
| EP-09 | GitHub Integration |
| EP-10 | Notifications and System Administration |
| EP-11 | Testing, Security, and Deployment |

---

# 3. Feature Tickets

## EP-01: Project Setup and Infrastructure

### SP-001 — Initialize Frontend Project

**Priority:** P0  
**Story Points:** 3

**Description:**

As a developer, I want to initialize the SkillProof frontend so that the user interface can be developed using the approved technology stack.

**Technology:**

- Next.js
- React
- TypeScript
- Tailwind CSS

**Acceptance Criteria:**

- Next.js project is initialized.
- TypeScript is configured.
- Tailwind CSS is configured.
- App Router is enabled.
- Initial project structure is created.
- The application runs successfully in development mode.

---

### SP-002 — Initialize Backend Project

**Priority:** P0  
**Story Points:** 3

**Description:**

As a developer, I want to initialize the Django backend so that the platform's APIs and business logic can be implemented.

**Technology:**

- Django
- Django REST Framework
- PostgreSQL

**Acceptance Criteria:**

- Django project is created.
- Django REST Framework is installed.
- PostgreSQL connection is configured.
- Environment variables are used for configuration.
- Initial Django applications are created.
- Backend runs successfully.

**Dependency:** SP-001 is not required; frontend and backend setup can proceed independently.

---

### SP-003 — Configure Development Environment

**Priority:** P0  
**Story Points:** 3

**Description:**

Configure a consistent development environment for frontend and backend development.

**Acceptance Criteria:**

- Environment variables are documented.
- `.env.example` files are created.
- Development database is configured.
- Git repository is initialized.
- `.gitignore` excludes secrets and generated files.
- Setup instructions are documented.

---

### SP-004 — Configure Redis and Celery

**Priority:** P0  
**Story Points:** 5

**Description:**

Configure asynchronous task processing for assessment evaluation and background operations.

**Acceptance Criteria:**

- Redis is configured as the message broker.
- Celery is configured in Django.
- A test background task executes successfully.
- Task failures are logged.
- Worker startup instructions are documented.

---

## EP-02: Authentication and Access Control

### SP-005 — Implement User Registration

**Priority:** P0  
**Story Points:** 5

**User Story:**

As a new user, I want to create an account so that I can access SkillProof.

**Acceptance Criteria:**

- User can register with a valid email and password.
- Password is securely hashed.
- Duplicate email registration is rejected.
- Required fields are validated.
- Registration response does not expose sensitive information.

---

### SP-006 — Implement User Login and JWT Authentication

**Priority:** P0  
**Story Points:** 5

**User Story:**

As a registered user, I want to log in securely so that I can access my account.

**Acceptance Criteria:**

- Valid credentials authenticate successfully.
- Invalid credentials are rejected.
- Access and refresh tokens are handled securely.
- Protected APIs reject unauthenticated requests.
- Authentication errors are returned consistently.

---

### SP-007 — Implement Role-Based Access Control

**Priority:** P0  
**Story Points:** 8

**Description:**

Implement permissions for Student, Employer, University, and Administrator roles.

**Acceptance Criteria:**

- Users have assigned roles.
- Backend permissions are enforced.
- Unauthorized actions return appropriate errors.
- Users cannot assign themselves privileged roles.
- Role changes are recorded.

---

### SP-008 — Implement Password Recovery

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- User can request password recovery.
- Recovery link or token expires.
- Token cannot be reused.
- Password is securely updated.
- User receives a confirmation notification.

---

### SP-009 — Implement Protected Frontend Routes

**Priority:** P0  
**Story Points:** 5

**Acceptance Criteria:**

- Unauthenticated users cannot access protected dashboards.
- Students access student routes.
- Employers access employer routes.
- Universities access university routes.
- Administrators access admin routes.
- Backend authorization remains independently enforced.

**Dependency:** SP-006, SP-007.

---

## EP-03: Student Profile Management

### SP-010 — Create Student Profile

**Priority:** P0  
**Story Points:** 5

**User Story:**

As a student, I want to create my professional profile so that employers can understand my background.

**Acceptance Criteria:**

- Student can add name and profile information.
- Student can add education details.
- Student can add technical interests.
- Profile information is saved.
- Profile can be updated by its owner.

---

### SP-011 — Manage Technical Skills

**Priority:** P1  
**Story Points:** 3

**Acceptance Criteria:**

- Student can add self-reported skills.
- Student can update skill information.
- Self-reported skills are clearly distinguished from verified skills.
- Student cannot manually assign verified scores.

---

### SP-012 — Generate Public Skill Profile

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- Student can enable or disable public profile visibility.
- Public profile displays approved information.
- Private information is excluded.
- Verified skills and evidence are displayed accurately.

**Dependency:** SP-010, SP-025.

---

## EP-04: Assessment Management

### SP-013 — Create Assessment Management Module

**Priority:** P0  
**Story Points:** 5

**Description:**

Create the backend module for managing practical assessments.

**Acceptance Criteria:**

- Assessment model is created.
- Assessment includes title, description, difficulty, and duration.
- Assessment includes required skills.
- Assessment status is supported.
- Database migrations are completed.

---

### SP-014 — Create Assessment Listing Page

**Priority:** P0  
**Story Points:** 3

**Acceptance Criteria:**

- Students can view published assessments.
- Assessment cards display relevant information.
- Draft assessments are hidden from students.
- Loading and empty states are implemented.

**Dependency:** SP-013.

---

### SP-015 — Create Assessment Details Page

**Priority:** P0  
**Story Points:** 5

**Acceptance Criteria:**

- Student can view assessment instructions.
- Required skills are displayed.
- Constraints and submission rules are displayed.
- Sample inputs and outputs are displayed where applicable.
- Restricted test cases are not exposed.

---

### SP-016 — Implement Assessment Administration

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Authorized administrators can create assessments.
- Assessments can be edited.
- Assessments can be published or unpublished.
- Invalid assessment data is rejected.
- Changes are recorded where appropriate.

---

## EP-05: Submission and Code Evaluation

### SP-017 — Implement Assessment Submission API

**Priority:** P0  
**Story Points:** 8

**User Story:**

As a student, I want to submit my solution so that my technical skills can be evaluated.

**Acceptance Criteria:**

- Student can submit an assessment solution.
- Submission ownership is verified.
- Submission limits are enforced.
- Submission is stored securely.
- Submission status is initialized correctly.

---

### SP-018 — Implement Submission History

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- Student can view their submissions.
- Submission history displays assessment information.
- Submission status is displayed.
- Students cannot access another student's private submissions.

---

### SP-019 — Configure Isolated Evaluation Worker

**Priority:** P0  
**Story Points:** 13

**Description:**

Implement an isolated environment for executing submitted code.

**Acceptance Criteria:**

- Submitted code executes outside the Django API process.
- Worker uses restricted execution privileges.
- CPU and memory limits are enforced.
- Execution timeout is enforced.
- Network access is restricted.
- Worker cannot access production secrets.
- Evaluation environment is cleaned after execution.

---

### SP-020 — Implement Automated Test Evaluation

**Priority:** P0  
**Story Points:** 13

**Description:**

Evaluate submitted solutions against assessment test cases.

**Acceptance Criteria:**

- Evaluation task is queued through Celery.
- Worker executes the submission.
- Test results are collected.
- Passed and failed tests are recorded.
- Evaluation status is updated.
- Evaluation failures are handled safely.

**Dependency:** SP-004, SP-017, SP-019.

---

### SP-021 — Implement Code Quality Analysis

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Supported static analysis tools are integrated.
- Code quality findings are collected.
- Findings are associated with submissions.
- Evaluation results include relevant quality metrics.
- Tool failures do not expose sensitive system information.

---

### SP-022 — Display Evaluation Results

**Priority:** P0  
**Story Points:** 5

**Acceptance Criteria:**

- Student can view completed evaluation results.
- Overall score is displayed.
- Functional correctness is displayed.
- Code quality findings are displayed.
- Evaluation status is updated.
- Results cannot be modified by students.

**Dependency:** SP-020, SP-021.

---

## EP-06: Skill Verification and Evidence

### SP-023 — Implement Skill Scoring Engine

**Priority:** P0  
**Story Points:** 8

**Description:**

Calculate skill scores using assessment and project evidence.

**Acceptance Criteria:**

- Scores are calculated by trusted backend logic.
- Scoring criteria are configurable.
- Evaluation data is used as input.
- Score calculation is reproducible.
- Students cannot modify calculated scores.

---

### SP-024 — Implement Skill Verification Status

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- Skills can have verification statuses.
- Verification is based on approved evidence.
- Unverified skills are clearly identified.
- Verification status is generated by backend rules.

---

### SP-025 — Create Skill Evidence Records

**Priority:** P0  
**Story Points:** 8

**Acceptance Criteria:**

- Evidence records are associated with users and skills.
- Evidence identifies its source.
- Evidence includes relevant assessment information.
- Evidence timestamps are recorded.
- Evidence cannot be altered by unauthorized users.

---

### SP-026 — Create Skill Passport Dashboard

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Student can view verified skills.
- Skill scores are displayed.
- Evidence is linked to relevant skills.
- Verification confidence is distinguished from skill level.
- Dashboard is responsive.

**Dependency:** SP-023, SP-024, SP-025.

---

## EP-07: Employer and Hiring Management

### SP-027 — Create Employer Organization

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- Employer can create an organization profile.
- Organization information is validated.
- Organization ownership is recorded.
- Organization members are authorized.

---

### SP-028 — Implement Candidate Search

**Priority:** P1  
**Story Points:** 8

**User Story:**

As an employer, I want to search candidates by verified skills so that I can identify suitable applicants.

**Acceptance Criteria:**

- Employer can search eligible candidate profiles.
- Search supports skill filters.
- Verification status can be filtered.
- Private student information is protected.
- Search results respect organization permissions.

---

### SP-029 — Implement Internship Management

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Employer can create internship opportunities.
- Employer can edit opportunities.
- Employer can publish or close opportunities.
- Opportunity ownership is verified.
- Public listings show only published opportunities.

---

### SP-030 — Implement Internship Applications

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Students can apply for internships.
- Duplicate applications are prevented.
- Employers can view authorized applications.
- Application status can be updated.
- Students can view their application status.

**Dependency:** SP-029.

---

## EP-08: University Analytics

### SP-031 — Create University Organization Module

**Priority:** P2  
**Story Points:** 5

**Acceptance Criteria:**

- University organization records are supported.
- Authorized members can be assigned.
- Institutional data is isolated.
- University permissions are enforced.

---

### SP-032 — Implement Student Progress Analytics

**Priority:** P2  
**Story Points:** 8

**Acceptance Criteria:**

- Authorized university users can view student progress.
- Assessment completion statistics are displayed.
- Verified skill distribution is displayed.
- Data is restricted to authorized institutions.

---

### SP-033 — Implement Analytics Dashboard

**Priority:** P2  
**Story Points:** 8

**Acceptance Criteria:**

- Dashboard displays approved analytics.
- Charts use backend-provided data.
- Loading and error states are supported.
- Charts are responsive.
- Data is not misleading or improperly aggregated.

---

## EP-09: GitHub Integration

### SP-034 — Implement GitHub OAuth Connection

**Priority:** P2  
**Story Points:** 8

**Acceptance Criteria:**

- Student can connect a GitHub account.
- OAuth flow is handled securely.
- Required permissions are requested.
- Integration status is displayed.
- Student can disconnect the account.

---

### SP-035 — Retrieve Project Contribution Data

**Priority:** P2  
**Story Points:** 8

**Acceptance Criteria:**

- Authorized GitHub data is retrieved through the backend.
- Relevant repository information is collected.
- Contribution records are associated with the student.
- API errors and rate limits are handled.
- GitHub activity is treated as supplementary evidence.

**Dependency:** SP-034.

---

## EP-10: Notifications and System Administration

### SP-036 — Implement Notification System

**Priority:** P2  
**Story Points:** 5

**Acceptance Criteria:**

- Users receive relevant platform notifications.
- Notifications are associated with recipients.
- Notification status is tracked.
- Unauthorized users cannot access another user's notifications.

---

### SP-037 — Implement Email Notifications

**Priority:** P2  
**Story Points:** 5

**Acceptance Criteria:**

- Account verification emails are supported.
- Password recovery emails are supported.
- Assessment completion notifications are supported.
- Internship application notifications are supported.
- Email failures are logged appropriately.

---

### SP-038 — Implement User Administration

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Administrators can view user accounts.
- Administrators can suspend accounts.
- Administrators can reactivate accounts.
- Role changes are restricted.
- Administrative actions are audited.

---

### SP-039 — Implement Security Audit Logging

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- Important security events are recorded.
- Logs include timestamps and relevant actors.
- Sensitive credentials are excluded.
- Audit logs are protected from unauthorized modification.
- Authorized administrators can review logs.

---

## EP-11: Testing, Security, and Deployment

### SP-040 — Implement Backend Unit Tests

**Priority:** P0  
**Story Points:** 8

**Acceptance Criteria:**

- Models are tested.
- Business logic is tested.
- Permission rules are tested.
- Scoring logic is tested.
- Critical API behavior is covered.

---

### SP-041 — Implement Frontend Component Tests

**Priority:** P1  
**Story Points:** 5

**Acceptance Criteria:**

- Reusable components are tested.
- Form validation is tested.
- Loading and error states are tested.
- Critical UI behavior is verified.

---

### SP-042 — Implement End-to-End Testing

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Registration and login workflows are tested.
- Assessment submission is tested.
- Evaluation result viewing is tested.
- Candidate search is tested.
- Unauthorized access scenarios are tested.

---

### SP-043 — Perform Security Testing

**Priority:** P0  
**Story Points:** 8

**Acceptance Criteria:**

- Authentication vulnerabilities are tested.
- Authorization bypass attempts are tested.
- Cross-organization access is tested.
- Input validation is tested.
- Code execution isolation is tested.
- Security findings are documented.

---

### SP-044 — Configure Production Deployment

**Priority:** P1  
**Story Points:** 8

**Acceptance Criteria:**

- Frontend and backend deployment configurations are created.
- Production environment variables are configured.
- HTTPS is enabled.
- Database migrations are documented.
- Redis and Celery workers are deployed.
- Application logs and monitoring are configured.

---

# 4. Recommended MVP Development Order

The following sequence prioritizes a working end-to-end skill verification workflow before advanced hiring and analytics features.

| Phase | Tickets | Objective |
|---|---|---|
| Phase 1 | SP-001 to SP-004 | Project setup and infrastructure |
| Phase 2 | SP-005 to SP-009 | Authentication and access control |
| Phase 3 | SP-010 to SP-016 | Student profiles and assessments |
| Phase 4 | SP-017 to SP-022 | Submission and automated evaluation |
| Phase 5 | SP-023 to SP-026 | Skill scoring and evidence |
| Phase 6 | SP-027 to SP-030 | Employer and internship features |
| Phase 7 | SP-040 to SP-044 | Testing, security, and deployment |
| Phase 8 | SP-031 to SP-039 | University analytics, GitHub, notifications, and administration |

The final phase may be adjusted depending on the FYP timeline and available resources.

---

# 5. MVP Definition

The minimum viable product shall include:

- User registration and login
- Role-based access control
- Student profile management
- Assessment creation and listing
- Assessment submission
- Isolated code execution
- Automated test evaluation
- Code quality analysis
- Skill scoring
- Evidence-based skill passport
- Basic employer candidate search
- Internship listing and applications
- Security testing
- Deployment

The MVP must demonstrate the complete workflow:

**Student registers → completes an assessment → submits code → receives automated evaluation → obtains verified skill evidence → displays the skill passport → becomes discoverable to authorized employers.**

This workflow represents the core innovation and research contribution of SkillProof.

---

# 6. Definition of Done

A feature ticket shall be considered complete when:

- The feature is implemented.
- Required acceptance criteria are satisfied.
- Backend validation is implemented where applicable.
- Authorization rules are verified.
- Relevant tests pass.
- Errors are handled appropriately.
- Code is reviewed.
- Documentation is updated.
- The feature works in the development environment.

For security-critical features, successful security testing is also required before the ticket can be marked complete.

---

# 7. Conclusion

This Feature Ticket List converts the SkillProof requirements and architecture into an actionable development backlog.

The tickets provide a structured approach to implementing the platform in manageable stages while maintaining alignment with the PRD, Technical Architecture Document, Security and Access Control Specification, and Frontend and Integration Specification.

The development team can use this backlog to plan sprints, assign responsibilities, track progress, and evaluate the completion of the SkillProof MVP.