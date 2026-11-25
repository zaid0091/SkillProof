# Frontend and Integration Specification (FIS)

## SkillProof — Verified Skills and Project-Based Hiring Platform

**Document Type:** Frontend and Integration Specification  
**Project:** SkillProof  
**Version:** 1.0  
**Status:** Proposed  
**Prepared For:** Final Year Project (FYP)

---

## 1. Introduction

### 1.1 Purpose

The purpose of this Frontend and Integration Specification is to define the frontend architecture, user interface requirements, API communication standards, and integration mechanisms for the SkillProof platform.

SkillProof is a project-based skill verification and hiring platform that enables students to demonstrate technical skills through practical assessments, verified project contributions, and evidence-based skill profiles.

The frontend will provide an intuitive interface for students, employers, universities, and administrators to interact with the platform.

### 1.2 Scope

This specification covers:

- Frontend technology stack
- Frontend architecture
- User interface and navigation
- Role-based dashboards
- API communication
- Authentication integration
- Assessment and submission workflows
- Skill profile and evidence presentation
- Employer hiring functionality
- University analytics
- External service integration
- Error handling and loading states
- Frontend security
- Testing and deployment

### 1.3 Frontend Objectives

The frontend shall:

1. Provide a responsive and accessible user interface.
2. Support role-specific experiences.
3. Communicate securely with the Django REST Framework backend.
4. Display assessment results and verified skill evidence.
5. Provide clear feedback during asynchronous operations.
6. Maintain consistent design and navigation.
7. Support future feature expansion without major architectural changes.

---

## 2. Frontend Technology Stack

The frontend will use modern web technologies to provide a scalable and maintainable application.

| Technology | Purpose |
|---|---|
| Next.js | Frontend framework and application routing |
| React | Component-based UI development |
| TypeScript | Type safety and maintainability |
| Tailwind CSS | Styling and responsive layouts |
| Axios | HTTP communication with backend APIs |
| Zustand | Lightweight client-side state management |
| React Hook Form | Form handling |
| Zod | Frontend data validation |
| Recharts | Analytics and dashboard charts |
| Lucide React | UI icons |

### 2.1 Next.js

Next.js will be used to develop the frontend application.

It will provide:

- App Router-based navigation
- Reusable layouts
- Route-level loading and error handling
- Server and client component support
- Optimized rendering
- Application-level organization

Protected and interactive dashboard pages will primarily use client-side functionality where required.

### 2.2 TypeScript

TypeScript will be used to improve code reliability.

The frontend shall define reusable types and interfaces for:

- User accounts
- Student profiles
- Organizations
- Assessments
- Submissions
- Evaluation results
- Skill evidence
- Internship opportunities
- Applications

API responses should be typed consistently across the application.

### 2.3 Tailwind CSS

Tailwind CSS will be used for styling.

The design system shall define:

- Primary and secondary colors
- Typography
- Spacing
- Border styles
- Buttons
- Form controls
- Cards
- Navigation elements
- Status indicators

The interface shall maintain visual consistency across all user roles.

---

## 3. Frontend Architecture

### 3.1 Architectural Approach

The frontend shall follow a modular, component-based architecture.

Each major platform feature will have its own page, components, types, and API functions.

The frontend will communicate with the backend through a centralized API client.

### 3.2 Directory Structure

The proposed frontend structure is:

```text
skillproof-frontend/
│
├── app/
│   ├── (public)/
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── register/
│   │   └── assessments/
│   │
│   ├── (dashboard)/
│   │   ├── student/
│   │   ├── employer/
│   │   ├── university/
│   │   └── admin/
│   │
│   ├── layout.tsx
│   └── globals.css
│
├── components/
│   ├── ui/
│   ├── layout/
│   ├── forms/
│   ├── assessments/
│   ├── skills/
│   └── charts/
│
├── features/
│   ├── auth/
│   ├── profiles/
│   ├── assessments/
│   ├── submissions/
│   ├── evidence/
│   ├── hiring/
│   └── analytics/
│
├── lib/
│   ├── api/
│   ├── auth/
│   ├── validation/
│   └── utilities/
│
├── hooks/
├── stores/
├── types/
└── public/
```

### 3.3 Component Reusability

Common UI elements shall be implemented as reusable components.

Examples:

- Button
- Input
- Select
- Modal
- Badge
- Data table
- Pagination
- Loading spinner
- Confirmation dialog
- Toast notification
- Empty-state component

Reusable components shall reduce duplication and improve consistency.

---

## 4. User Interface and Navigation

### 4.1 Public Pages

The platform shall provide public pages for visitors.

These pages may include:

- Landing page
- About SkillProof
- Assessment overview
- Public verified skill profiles
- Login
- Registration
- Internship listings

Public pages must not expose private user or organization information.

### 4.2 Student Dashboard

The student dashboard shall provide access to:

- Profile overview
- Available assessments
- Active assessments
- Submission history
- Evaluation results
- Verified skill passport
- Skill evidence
- GitHub integration
- Internship opportunities
- Application history

The dashboard should display progress indicators and relevant assessment statistics.

### 4.3 Employer Dashboard

The employer dashboard shall provide access to:

- Organization profile
- Candidate search
- Candidate skill profiles
- Assessment evidence
- Internship management
- Application review
- Hiring analytics

Candidate information shall be displayed according to access permissions and privacy settings.

### 4.4 University Dashboard

The university dashboard shall provide access to:

- Institutional overview
- Authorized student records
- Assessment completion statistics
- Skill-development analytics
- Student progress reports
- Organization management

University analytics shall be restricted to authorized institutional users.

### 4.5 Administrator Dashboard

The administrator dashboard shall provide access to:

- User management
- Organization management
- Assessment management
- Platform statistics
- Security audit logs
- System monitoring
- Administrative configuration

Administrative interfaces shall be accessible only to authorized users.

---

## 5. Frontend Routing and Access Control

### 5.1 Route Organization

The frontend shall use Next.js App Router.

Routes shall be organized according to user roles and platform features.

Example routes:

| Route | Description |
|---|---|
| `/login` | User authentication |
| `/register` | User registration |
| `/student/dashboard` | Student overview |
| `/student/assessments` | Available assessments |
| `/student/submissions` | Submission history |
| `/student/skills` | Verified skill profile |
| `/employer/dashboard` | Employer overview |
| `/employer/candidates` | Candidate search |
| `/employer/applications` | Candidate application pipeline and status updates |
| `/employer/internships` | Internship management |
| `/university/dashboard` | University analytics |
| `/admin/dashboard` | Administrative overview |

### 5.2 Protected Routes

Protected routes shall require authentication.

The frontend shall redirect unauthenticated users to the login page.

Users attempting to access routes outside their assigned roles shall be redirected to an appropriate page or shown an access-denied message.

### 5.3 Backend Authorization

Frontend route protection is a usability feature, not a security boundary.

The Django REST Framework backend must independently validate authentication, roles, permissions, and resource ownership for every protected operation.

---

## 6. API Integration

### 6.1 Backend Communication

The frontend shall communicate with the backend through REST APIs developed using Django REST Framework.

The API base URL shall be configurable through environment variables.

Example:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

Production environments shall use HTTPS.

### 6.2 Centralized API Client

Axios shall be configured as the centralized HTTP transport, and TanStack Query shall provide API request state, caching, retries, and invalidation.

The API client shall provide:

- Base URL configuration
- Request timeout
- Common headers
- Authentication handling
- Error handling
- Response processing

Feature-specific API functions shall use this centralized client.

### 6.3 API Versioning

The backend API shall use versioned endpoints.

Example:

```text
/api/v1/auth/
/api/v1/profiles/
/api/v1/assessments/
/api/v1/submissions/
/api/v1/evidence/
/api/v1/hiring/
```

API versioning will help maintain compatibility as the platform evolves.

### 6.4 Request and Response Types

Frontend API functions shall use TypeScript interfaces or types.

Example:

```typescript
export interface Assessment {
  id: string;
  title: string;
  description: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  duration_minutes: number;
  status: "published" | "draft";
}
```

Response types shall match the backend API contract.

---

## 7. Authentication Integration

### 7.1 Login Workflow

The login workflow shall:

1. Collect the user's email and password.
2. Send credentials to the authentication API.
3. Receive authentication information.
4. Store authentication state securely.
5. Retrieve the user's profile and roles.
6. Redirect the user to the appropriate dashboard.

### 7.2 Token Refresh

The frontend shall support automatic access-token renewal.

When an access token expires:

1. The API client detects the unauthorized response.
2. A refresh request is sent to the backend.
3. The backend validates the refresh token.
4. A new access token is issued.
5. The original request is retried when appropriate.

If refresh fails, the user shall be logged out and redirected to the login page.

Concurrent refresh requests should be coordinated to prevent unnecessary token refresh operations.

### 7.3 Logout Workflow

The logout process shall:

- Request backend token revocation where supported.
- Clear client-side authentication state.
- Remove sensitive cached information.
- Redirect the user to a public page.

### 7.4 Authentication Security

The frontend shall:

- Avoid exposing refresh tokens to JavaScript.
- Avoid storing sensitive tokens in localStorage.
- Use secure cookie-based refresh-token handling where supported.
- Avoid including tokens in URLs.
- Handle authentication errors consistently.

---

## 8. Assessment and Submission Integration

### 8.1 Assessment Listing

Students shall be able to view available assessments.

Each assessment card shall display:

- Assessment title
- Description
- Difficulty level
- Required skills
- Estimated duration
- Available status

### 8.2 Assessment Details

The assessment detail page shall display:

- Instructions
- Requirements
- Constraints
- Sample inputs and outputs
- Submission rules
- Time limits
- Attempt limits

Restricted evaluation test cases must not be exposed to students.

### 8.3 Submission Workflow

The frontend shall support the following submission process:

1. Student selects an assessment.
2. Student reviews the instructions.
3. Student uploads or submits code.
4. Frontend validates basic submission requirements.
5. Submission is sent to the backend.
6. Backend creates a submission record.
7. Evaluation is queued.
8. Frontend displays the current evaluation status.
9. Final evaluation results are displayed when available.

### 8.4 Submission Status

The frontend shall support the following statuses:

- Pending
- Queued
- Running
- Completed
- Failed
- Cancelled

Status indicators shall use clear labels and visual representations.

### 8.5 Evaluation Results

The results page shall display:

- Overall score
- Functional correctness
- Code quality
- Test coverage
- Problem-solving performance
- Security or best-practice findings
- Verified skills
- Supporting evidence

The interface must clearly distinguish between a skill score and the confidence or strength of its verification evidence.

---

## 9. Skill Profile and Evidence Integration

### 9.1 Skill Passport

The student skill passport shall provide a structured view of verified skills.

It may include:

- Skill name
- Skill level or score
- Verification status
- Evidence source
- Assessment history
- Last verification date

### 9.2 Evidence Presentation

Evidence shall be presented in a transparent manner.

Examples include:

- Assessment results
- Completed practical tasks
- Code quality reports
- Test coverage
- Verified project contributions

The frontend shall not present unverified claims as verified achievements.

### 9.3 Public Profiles

Students may choose to make selected profile information public.

Public profiles shall exclude private information such as:

- Email addresses
- Private submissions
- Internal evaluation details
- Private internship applications

The backend shall determine which fields are permitted for public display.

---

## 10. Employer Hiring Integration

### 10.1 Candidate Search

Employers shall be able to search eligible candidates using supported filters.

Possible filters include:

- Technical skills
- Skill verification status
- Assessment completion
- Experience level
- Project contributions
- Availability

### 10.2 Candidate Profiles

Candidate profile pages shall display relevant skill evidence.

The frontend shall provide clear distinctions between:

- Self-reported skills
- Assessment-verified skills
- Project-based evidence
- External contribution records

### 10.3 Internship Management

Employers shall be able to:

- Create internship opportunities.
- Edit internship descriptions.
- Publish or close opportunities.
- View applications.
- Review candidate profiles.
- Update application statuses.

### 10.4 Application Status

The frontend shall support application statuses such as:

- Submitted
- Under Review
- Shortlisted
- Interview
- Rejected
- Accepted
- Withdrawn

Application status updates shall be reflected through API responses.

---

## 11. University Analytics Integration

### 11.1 Analytics Dashboard

The university dashboard shall present institutional skill-development information.

Possible visualizations include:

- Assessment completion rates
- Verified skill distribution
- Student progress
- Assessment performance trends
- Skill gaps
- Department-level summaries

### 11.2 Data Visualization

Recharts shall be used for suitable charts.

Charts must:

- Display accurate backend-provided data.
- Include labels and legends.
- Support responsive layouts.
- Avoid misleading visual representations.
- Respect user permissions.

### 11.3 Reporting

Authorized university users may generate reports containing approved institutional data.

Reports shall not expose information beyond the user's access permissions.

---

## 12. External Service Integration

### 12.1 GitHub Integration

SkillProof shall integrate with GitHub to support project contribution evidence.

The frontend shall provide:

- GitHub connection interface
- Connection status
- Permission explanation
- Repository selection where supported
- Contribution information
- Disconnect option

GitHub integration shall be handled through the backend.

The frontend must not directly expose OAuth secrets or privileged integration tokens.

### 12.2 Email Notifications

The platform may integrate with an email service for:

- Account verification
- Password recovery
- Assessment notifications
- Evaluation completion
- Internship application updates

Email delivery shall be handled by the backend or asynchronous notification workers.

### 12.3 Object Storage

Assessment files and approved evidence documents may be stored using object storage.

The frontend shall upload files through secure backend-authorized mechanisms.

File access must respect permissions and expiration policies where temporary links are used.

---

## 13. Real-Time and Asynchronous Integration

### 13.1 Assessment Status Updates

Assessment evaluation may take time.

The frontend shall support asynchronous status updates.

For the initial implementation, polling may be used to retrieve submission status.

Example endpoint:

```text
GET /api/v1/submissions/{id}/status/
```

### 13.2 WebSocket Integration

WebSockets may be introduced for real-time updates.

Potential use cases include:

- Evaluation progress
- Evaluation completion
- Notifications
- Application status updates

WebSocket connections must require authentication and enforce appropriate authorization.

### 13.3 Fallback Mechanism

If a real-time connection fails, the frontend shall fall back to polling or manual refresh where appropriate.

The user interface must not assume that an asynchronous operation has completed until the backend confirms its status.

---

## 14. Error Handling and User Feedback

### 14.1 Error Handling

The frontend shall handle common API errors consistently.

Examples:

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict
- 429 Too Many Requests
- 500 Internal Server Error

### 14.2 User Feedback

The interface shall provide:

- Loading indicators
- Success messages
- Validation errors
- Empty states
- Retry options
- Access-denied messages
- Network error notifications

### 14.3 Form Validation

Forms shall use React Hook Form and Zod where appropriate.

Frontend validation shall improve usability, while the backend remains responsible for authoritative validation.

### 14.4 Asynchronous Operations

For long-running operations, the frontend shall display progress or status information.

Examples include:

- Code evaluation
- File uploads
- Report generation
- GitHub synchronization

---

## 15. Frontend Security Requirements

The frontend shall follow the security principles defined in the Security and Access Control Specification.

Requirements include:

- Secure authentication state management
- Protected route handling
- Safe rendering of user-generated content
- Secure file uploads
- No exposure of backend secrets
- Appropriate CSRF handling
- HTTPS in production
- Permission-aware UI
- Secure error handling
- Dependency security checks

Frontend controls shall not replace backend authorization.

---

## 16. Responsive Design and Accessibility

### 16.1 Responsive Design

The frontend shall support:

- Desktop screens
- Laptop screens
- Tablets
- Mobile devices

The layout shall adapt to different screen sizes without losing important functionality.

### 16.2 Accessibility

The interface should follow WCAG 2.2 Level AA guidelines where practical.

Accessibility requirements include:

- Keyboard navigation
- Clear focus indicators
- Accessible form labels
- Appropriate color contrast
- Screen-reader-friendly controls
- Meaningful error messages
- Accessible charts and tables

---

## 17. Frontend Testing

### 17.1 Unit Testing

Reusable components and frontend utilities shall be tested.

Recommended tools:

- Vitest
- React Testing Library

### 17.2 Integration Testing

Integration tests shall verify:

- API communication
- Authentication workflows
- Form submission
- Dashboard data loading
- Assessment submission
- Error handling

### 17.3 End-to-End Testing

Playwright may be used for end-to-end testing.

Important test scenarios include:

- Student registration and login
- Assessment submission
- Evaluation result viewing
- Skill passport access
- Employer candidate search
- Internship application review
- University analytics access
- Unauthorized route access

---

## 18. Deployment and Environment Configuration

### 18.1 Development Environment

The frontend shall support local development using environment-specific configuration.

Example:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

### 18.2 Production Environment

Production deployment shall use:

- HTTPS
- Secure environment variables
- Production API URLs
- Appropriate cookie settings
- Optimized frontend builds
- Error monitoring
- Dependency checks

### 18.3 Environment Separation

The platform should maintain separate configurations for:

- Development
- Testing
- Staging
- Production

Production secrets must not be committed to source control.

---

## 19. Frontend and Integration Requirements Summary

| ID | Requirement | Priority |
|---|---|---|
| FE-01 | The frontend shall use Next.js, React, and TypeScript. | High |
| FE-02 | The frontend shall provide role-specific dashboards. | High |
| FE-03 | The frontend shall communicate with versioned REST APIs. | High |
| FE-04 | The frontend shall support secure authentication workflows. | High |
| FE-05 | The frontend shall display assessment submission statuses. | High |
| FE-06 | The frontend shall display evaluation results and skill evidence. | High |
| FE-07 | The frontend shall support employer candidate search. | High |
| FE-08 | The frontend shall support internship management. | High |
| FE-09 | The frontend shall provide university analytics. | Medium |
| FE-10 | The frontend shall integrate with GitHub through the backend. | Medium |
| FE-11 | The frontend shall handle API errors consistently. | High |
| FE-12 | The frontend shall provide responsive layouts. | High |
| FE-13 | The frontend shall implement protected routes. | High |
| FE-14 | The frontend shall support asynchronous evaluation updates. | High |
| FE-15 | The frontend shall undergo unit, integration, and end-to-end testing. | High |

---

## 20. Conclusion

The Frontend and Integration Specification defines the structure and behavior of the SkillProof user interface and its communication with the backend system.

By adopting a modular Next.js architecture, reusable React components, centralized API integration, secure authentication workflows, and role-specific dashboards, the frontend will provide a maintainable and user-friendly platform.

The integration design ensures that assessment evaluation, skill verification, GitHub contribution tracking, hiring workflows, and university analytics operate through consistent and secure interfaces.

This specification will serve as a reference for frontend development, API integration, testing, and deployment of the SkillProof platform.