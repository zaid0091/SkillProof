# Security and Access Control Specification (SACS)

## SkillProof — Verified Skills and Project-Based Hiring Platform

**Document Type:** Security and Access Control Specification  
**Project:** SkillProof  
**Version:** 1.0  
**Status:** Proposed  
**Prepared For:** Final Year Project (FYP)

---

## 1. Introduction

### 1.1 Purpose

The purpose of this Security and Access Control Specification is to define the security policies, authentication mechanisms, authorization rules, data protection requirements, and access control procedures for the SkillProof platform.

SkillProof is a project-based skill verification and hiring platform that allows students to demonstrate their technical abilities through practical assessments, verified project contributions, and evidence-based skill profiles.

Since the platform stores personal information, assessment results, source code submissions, skill verification records, and hiring-related data, appropriate security controls are required to protect users and maintain the integrity of the platform.

### 1.2 Scope

This specification covers:

- User authentication and account security
- Role-based access control
- Permission management
- Organization and university data isolation
- Student assessment and submission security
- Automated code evaluation security
- API security
- Data privacy and protection
- Audit logging and monitoring
- Security testing and incident handling

### 1.3 Security Objectives

The primary security objectives are:

1. **Confidentiality:** Ensure that sensitive information is accessible only to authorized users.
2. **Integrity:** Prevent unauthorized modification of assessments, submissions, evaluation results, and verification records.
3. **Availability:** Ensure that the platform remains accessible to legitimate users.
4. **Authentication:** Verify the identity of users accessing the system.
5. **Authorization:** Restrict actions according to user roles and permissions.
6. **Accountability:** Maintain records of important security-related activities.
7. **Isolation:** Prevent one organization or user from accessing another organization's restricted information.

---

## 2. User Roles and Responsibilities

SkillProof will implement Role-Based Access Control (RBAC).

Each authenticated user will be assigned one or more roles. The permissions associated with those roles will determine which resources and operations the user can access.

### 2.1 Student

Students use the platform to build verified skill profiles and participate in practical assessments.

**Permissions:**

- Register and manage their own account.
- Create and update their student profile.
- View available assessments.
- Start and submit assessments.
- View their own submissions and evaluation results.
- View their verified skill profile.
- Connect their GitHub account.
- Apply for available internships.
- View their own application status.

**Restrictions:**

- Cannot access another student's private submissions.
- Cannot modify evaluation results.
- Cannot manually assign verified skill scores.
- Cannot access employer-only candidate information.
- Cannot access administrative functions.

### 2.2 Employer

Employers use the platform to discover candidates and manage internship opportunities.

**Permissions:**

- Create and manage an organization profile.
- Manage authorized organization members.
- Create and publish internship opportunities.
- Search eligible candidate profiles.
- View candidate skill evidence according to platform policies.
- Review internship applications.
- Update application statuses.
- View organization-related hiring analytics.

**Restrictions:**

- Cannot access private student information without authorization.
- Cannot modify student assessment results.
- Cannot access another employer's private organization data.
- Cannot modify platform-wide security settings.
- Cannot execute or download restricted assessment data.

### 2.3 University

Universities use SkillProof to monitor student skill development and assessment performance.

**Permissions:**

- Manage university organization details.
- Access authorized student progress information.
- View assessment completion statistics.
- View aggregated skill-development analytics.
- Manage authorized university members.

**Restrictions:**

- Cannot access students outside their authorized institution unless explicitly permitted.
- Cannot modify assessment evaluation results.
- Cannot access employer-private hiring records.
- Cannot modify platform administration settings.

### 2.4 Administrator

Administrators are responsible for managing the platform and maintaining its operational security.

**Permissions:**

- Manage user accounts.
- Assign and revoke platform roles.
- Suspend or reactivate accounts.
- Manage assessment availability.
- Configure platform-wide settings.
- Review security audit logs.
- Manage reported security incidents.
- Monitor system activity.

**Restrictions:**

- Administrative access must be limited to authorized personnel.
- Sensitive administrative actions must be logged.
- Administrator accounts must use stronger authentication controls.
- Administrators should not access private user data unless required for a legitimate operational or security purpose.

---

## 3. Authentication Specification

### 3.1 User Registration

The platform shall support secure user registration.

Registration requirements:

- Users must provide a valid email address.
- Passwords must satisfy the platform's password policy.
- Email verification shall be required before sensitive account operations.
- Users must select an appropriate account type during registration.
- Role assignment must be validated by the backend.
- Organization membership must require an invitation or authorized approval.

The backend must never trust a role or permission value submitted directly by the frontend.

### 3.2 Password Security

Passwords shall be securely hashed using Django's supported password-hashing framework.

Requirements:

- Passwords must never be stored in plaintext.
- Passwords must never be included in application logs.
- Password reset tokens must be securely generated.
- Password reset links must expire.
- Password reset tokens must be single-use.
- Password changes must invalidate relevant existing sessions or refresh tokens.

The platform should use Django's Argon2 password hasher where supported and appropriately configured.

### 3.3 JWT Authentication

SkillProof shall use JSON Web Tokens (JWT) for API authentication.

The authentication system will use:

- Access tokens for short-lived API authentication.
- Refresh tokens for obtaining new access tokens.
- Token expiration and rotation.
- Refresh-token revocation or blacklisting.

Access tokens should have a short lifetime, such as 5–15 minutes, subject to implementation and usability testing.

Refresh tokens should have a longer but limited lifetime and must be securely stored.

### 3.4 Token Storage

For the web application:

- Access tokens should preferably remain in memory.
- Refresh tokens should be stored in secure, HttpOnly cookies.
- Cookies should use the Secure flag in production.
- Cookies should use an appropriate SameSite policy.
- Cookie-based refresh endpoints must implement appropriate CSRF protection.

JWTs must not be exposed through URLs or stored in application logs.

### 3.5 Account Recovery

The platform shall provide a secure password recovery process.

The process must:

1. Accept the user's registered email address.
2. Generate a time-limited recovery token.
3. Send a recovery link through a verified email service.
4. Validate the token before allowing a password reset.
5. Invalidate the token after successful use.
6. Notify the user when the password is changed.

The system should avoid revealing whether an email address is registered during password recovery.

---

## 4. Authorization and Access Control

### 4.1 Role-Based Access Control

SkillProof shall use RBAC to manage access to protected resources.

The backend shall enforce permissions independently of the frontend.

Hiding a button or page in the frontend does not constitute an authorization control.

### 4.2 Permission Enforcement

Every protected API endpoint must verify:

- The user is authenticated.
- The user has the required role or permission.
- The requested resource belongs to the user's authorized scope.
- The requested operation is permitted for the resource's current state.

### 4.3 Object-Level Permissions

Object-level permissions shall be implemented to prevent unauthorized access to individual records.

Examples:

- A student can access only their own private submission records.
- An employer can access only organization-owned internship records.
- A university member can access only authorized institutional analytics.
- An administrator can access administrative resources according to assigned privileges.

The backend must verify ownership and organization membership for every relevant request.

### 4.4 Least Privilege Principle

Users shall receive only the permissions required to perform their assigned responsibilities.

The platform must avoid granting unnecessary administrative privileges.

Role changes and permission updates must be recorded in the audit log.

---

## 5. Organization and Tenant Isolation

SkillProof supports multiple organizations, including universities and employers.

The platform shall enforce logical tenant isolation.

### 5.1 Organization Data Isolation

Each organization-owned resource must be associated with an organization identifier.

Examples include:

- Organization profiles
- Internship opportunities
- Organization members
- Hiring records
- University analytics

Users must not access organization resources unless they have valid membership or explicitly granted access.

### 5.2 Backend Validation

Organization identifiers supplied by the frontend must not be trusted automatically.

The backend must:

- Validate organization membership.
- Verify the user's permissions within the organization.
- Apply organization-level filters to database queries.
- Prevent cross-organization record access.
- Validate ownership before updates or deletions.

### 5.3 Data Isolation Testing

The development team shall test that:

- Employer A cannot access Employer B's private records.
- University A cannot access University B's restricted analytics.
- Unauthorized users cannot modify organization-owned resources.
- Changing a record identifier in an API request does not bypass authorization.

---

## 6. API Security

### 6.1 HTTPS

All production communication between clients and the backend must use HTTPS.

Sensitive information, authentication tokens, and user data must not be transmitted over unencrypted connections.

### 6.2 Input Validation

All incoming API data must be validated using Django REST Framework serializers or equivalent backend validation mechanisms.

Validation shall cover:

- Required fields
- Data types
- Maximum field lengths
- File sizes
- Allowed file formats
- Identifier formats
- Business rules
- Request parameters

### 6.3 SQL Injection Prevention

The backend shall use Django ORM or parameterized queries.

Raw SQL must be avoided unless necessary and must use safe parameter binding.

### 6.4 Cross-Site Scripting (XSS)

The frontend and backend shall implement protections against XSS.

Requirements:

- Validate and sanitize user-generated content where appropriate.
- Avoid unsafe HTML rendering.
- Use framework-provided escaping.
- Apply a suitable Content Security Policy in production.
- Never render untrusted assessment output as executable HTML.

### 6.5 Cross-Site Request Forgery (CSRF)

CSRF protection shall be enabled for cookie-based authentication and other state-changing browser requests.

The backend shall validate CSRF tokens where required.

### 6.6 Rate Limiting

The platform shall apply rate limits to sensitive endpoints.

Examples:

- Login
- Registration
- Password recovery
- Token refresh
- Assessment submission
- Candidate search
- File uploads

Rate limits shall help reduce brute-force attacks, automated abuse, and excessive resource consumption.

### 6.7 Error Handling

API responses must not expose:

- Database credentials
- Internal server paths
- Secret keys
- Stack traces
- Sensitive configuration details

Detailed errors may be recorded in protected server logs for debugging.

---

## 7. Assessment and Code Submission Security

Since SkillProof evaluates user-submitted source code, code execution is a major security concern.

### 7.1 Submission Validation

The system shall validate assessment submissions before processing them.

Validation requirements:

- Verify assessment eligibility.
- Verify submission ownership.
- Check file size limits.
- Validate permitted file types.
- Reject prohibited file formats.
- Prevent unauthorized access to assessment test cases.
- Enforce submission deadlines and attempt limits.

### 7.2 Secure Code Execution

Student-submitted code must never execute directly inside the Django API server.

Code execution shall take place in isolated evaluation workers.

Each evaluation environment must:

- Run inside a restricted container or equivalent sandbox.
- Use a non-root execution user.
- Have limited CPU and memory resources.
- Have a strict execution timeout.
- Use a restricted filesystem.
- Avoid access to host credentials.
- Avoid access to application secrets.
- Restrict or disable network access.
- Be destroyed or cleaned after execution.

### 7.3 Evaluation Worker Isolation

The evaluation worker must be separated from the main application environment.

The worker shall not have unrestricted access to:

- The production database
- Redis administrative functions
- Environment secrets
- Other users' submissions
- Host filesystem resources

The application shall pass only the necessary assessment data to the worker.

### 7.4 Evaluation Result Integrity

Evaluation results must be generated by trusted backend processes.

Students and employers must not be able to directly modify:

- Test results
- Evaluation scores
- Verification status
- Skill evidence records

Evaluation results should include relevant metadata such as:

- Submission identifier
- Assessment identifier
- Evaluation status
- Score
- Evaluation timestamp
- Evaluation version

---

## 8. Data Protection and Privacy

### 8.1 Sensitive Data

The platform may store:

- User names and email addresses
- Student profiles
- Assessment submissions
- Evaluation results
- GitHub integration information
- Internship applications
- Organization information

Access to sensitive information must be restricted according to the user's role and authorization.

### 8.2 Data Minimization

SkillProof shall collect only the information necessary to provide its services.

The platform should avoid collecting unnecessary personal information.

### 8.3 Encryption

Sensitive data must be protected during transmission using HTTPS.

Where appropriate, sensitive information should also be encrypted at rest through database, storage, or infrastructure-level encryption.

### 8.4 GitHub Integration Security

GitHub integration shall use OAuth or an equivalent secure authorization mechanism.

Requirements:

- Request only necessary permissions.
- Store integration tokens securely.
- Never expose tokens to the frontend unnecessarily.
- Allow users to disconnect their GitHub account.
- Revoke or delete stored credentials when access is removed.
- Do not treat GitHub activity alone as proof of verified technical skill.

### 8.5 Data Retention

The platform shall define retention periods for:

- User accounts
- Assessment submissions
- Evaluation records
- Internship applications
- Audit logs

Users should be informed about how their data is used and retained.

Deletion or anonymization requests shall be handled according to applicable policies and institutional requirements.

---

## 9. Audit Logging and Monitoring

### 9.1 Audit Events

The platform shall record important security-related activities.

Examples include:

- Successful and failed login attempts
- Password changes
- Account suspension
- Role assignment or removal
- Organization membership changes
- Assessment publication
- Submission evaluation
- Verification status changes
- Administrative actions
- Unauthorized access attempts

### 9.2 Audit Log Requirements

Audit logs shall:

- Include timestamps.
- Identify the actor when available.
- Record the action performed.
- Identify the affected resource.
- Record the outcome.
- Avoid storing passwords, access tokens, or unnecessary sensitive data.

### 9.3 Log Protection

Audit logs must be accessible only to authorized personnel.

Users must not be able to modify or delete security audit records through ordinary application endpoints.

### 9.4 Monitoring

The platform should monitor:

- Repeated authentication failures
- Unusual API request patterns
- Excessive assessment submissions
- Evaluation worker failures
- Suspicious permission violations
- Unexpected administrative activity

---

## 10. Security Testing

Security testing shall be performed throughout development.

### 10.1 Authentication Testing

Verify that:

- Unauthenticated users cannot access protected endpoints.
- Expired access tokens are rejected.
- Invalid tokens are rejected.
- Revoked refresh tokens cannot be reused.
- Password recovery tokens expire and cannot be reused.

### 10.2 Authorization Testing

Verify that:

- Students cannot access other students' private submissions.
- Employers cannot access other organizations' private records.
- Universities cannot access unauthorized institutional data.
- Users cannot assign themselves administrative roles.
- Unauthorized users cannot modify evaluation results.

### 10.3 Input and API Testing

Test for:

- SQL injection
- XSS
- CSRF
- Invalid input
- Unauthorized file access
- Rate-limit bypass
- Insecure direct object references

### 10.4 Sandbox Testing

Verify that submitted code cannot:

- Access host files
- Read environment secrets
- Access the production database
- Consume unlimited CPU or memory
- Run indefinitely
- Access restricted network resources

### 10.5 Automated Security Checks

The development team should use appropriate tools, such as:

- Django security checks
- Dependency vulnerability scanners
- Static analysis tools
- API permission tests
- Container image scanners
- OWASP-based security testing checklists

---

## 11. Security Incident Handling

The platform shall define a basic security incident response process.

When a security incident is detected:

1. Identify and investigate the incident.
2. Determine the affected users and resources.
3. Restrict or disable compromised access.
4. Preserve relevant logs and evidence.
5. Apply corrective measures.
6. Restore affected services securely.
7. Document the incident and prevention measures.

Examples of incidents include:

- Unauthorized account access
- Exposure of private student data
- Compromised administrator credentials
- Malicious code execution attempts
- Cross-organization data access

---

## 12. Security Requirements Summary

| ID | Requirement | Priority |
|---|---|---|
| SEC-01 | The system shall authenticate users before granting protected API access. | High |
| SEC-02 | The system shall enforce role-based access control. | High |
| SEC-03 | The system shall enforce object-level permissions. | High |
| SEC-04 | The system shall isolate organization-owned data. | High |
| SEC-05 | The system shall securely hash user passwords. | High |
| SEC-06 | The system shall implement secure JWT handling and token expiration. | High |
| SEC-07 | The system shall protect production communication using HTTPS. | High |
| SEC-08 | The system shall validate all incoming API data. | High |
| SEC-09 | The system shall execute student code in isolated environments. | Critical |
| SEC-10 | The system shall prevent users from modifying evaluation results. | High |
| SEC-11 | The system shall securely store integration credentials. | High |
| SEC-12 | The system shall maintain security audit logs. | Medium |
| SEC-13 | The system shall apply rate limits to sensitive endpoints. | Medium |
| SEC-14 | The system shall perform security testing before production deployment. | High |
| SEC-15 | The system shall provide a security incident response procedure. | Medium |

---

## 13. Conclusion

The Security and Access Control Specification establishes the security foundation of the SkillProof platform.

By implementing secure authentication, role-based permissions, organization-level data isolation, protected APIs, isolated code execution, and comprehensive audit logging, SkillProof will reduce the risk of unauthorized access and protect the integrity of its skill verification process.

Security controls shall be implemented primarily within the backend and infrastructure layers, ensuring that access restrictions remain effective regardless of frontend behavior.

This specification will serve as a reference for the development, testing, deployment, and maintenance of the SkillProof platform.