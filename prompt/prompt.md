# Prompt Tracking & Version Control

**Date**: 2026-03-03

1. Table name: User_Role_Master:
    -   change the schema. Roleid should be Integer starting with 1.
    -   Rest all is fine
    -   create a sql query script that contains
        -   create Alter query for user_role_master
        -   delete the current records, drop the current table and then alter the table
        -   create load query as below for the user_role_master
        INSERT INTO user_role_master (roleId, roleName, status, comments) VALUES
            (1, 'ADMIN', 'Active', 'System Administrator - Full system access and database management'),
            (2, 'DOCTOR','Active', 'Doctor or Physician - Can view and manage patient records and create medical reports'),
            (3, 'HOSPITAL','Active', 'Hospital administrator - manages hospital operations and staff'),
            (4, 'NURSE', 'Active', 'Can assist with patient records, blood work, and vitals'),
            (5, 'PARTNER','Active', 'Sales and marketing partner - manages partnerships and revenue'),
            (6, 'PATIENT', 'Active', 'Can view own medical reports and health history'),
            (7, 'RECEPTION', 'Active', 'Reception Staff - Can manage appointments, check-in/check-out, and scheduling'),
            (8, 'TECHNICIAN', 'Active', 'Lab Technician - Can create and upload laboratory test reports and results');
    - APIs will be created for both Select and CRUD operation (no Delete operation required)
        - Select API should be able to fetch data based on following inputs
            -   Role ID - select specific row for all columns
            -   Role Name - select specific row for all columns
            -   Status - select all roles rows for specific status
        -   PUT and POST APIs should be able to
            -   Insert a new Role, all column values need to be mandatorily provided except Roleid. Roleid should be an auto increment - max(roleid) + 1. Both createdDate and updatedDate should be the system date
            -   Update API can be for a 
                -   status change (valid status are Active, Inactive, Closed)
                -   comments change
                -   for any update request createdDate should not be changed and updatedDate should be the system date when the update operation is executed 
    - Create an overall plan and rewrite the Plan/API Development Plan.md that should comprise of updating
        - Agents/DB Dev Agent.md
        - Agents/API Dev Agent.md
        - Agents/API Unit Testing Agent.md
        - Agents/DBA Agent.md
        - DevOps /DBA/Databasespecs.md
        - DevOps /DBA/DEPLOYMENT_GUIDE.md
        - README.md
        - src/SQL files/create_Tables.sql
        - src/schemas/user_role.py
        - src/routes/v1/roles.py
    - Ensure that all respective dependent .md files and code is regenerated for this change.

## Overview
This document captures all prompts and tracks version changes that percolate to respective code and documents.

## Primary Sections

### 1. Prompt Log
- **Section**: Document all prompts executed
- **Purpose**: Track every instruction/request made to the system
- **Version Control**: Link to corresponding code/document changes

### 2. Code Changes
- **Section**: Track modifications to source code
- **Purpose**: Map prompts to code implementations
- **Impact**: Document how code evolved from prompts

### 3. Document Updates
- **Section**: Track documentation changes
- **Purpose**: Ensure docs stay synchronized with code changes
- **Versioning**: Maintain version history

### 4. Flow Impact Analysis
- **Section**: Track how changes propagate through the system
- **Purpose**: Understand dependencies and affected modules
- **Traceability**: Connect prompts → code → docs → flow

### 5. Version History
- **Section**: Maintain change history
- **Purpose**: Rollback capability and audit trail
- **Schema**: Date | Prompt | Changes | Affected Files

---

## Sections to Populate

### Active Prompts
- [ ] Prompt 1
- [ ] Prompt 2

### Pending Changes
- [ ] Change 1
- [ ] Change 2

### Completed Implementations
- [ ] Implementation 1
- [ ] Implementation 2

---

## Change Propagation Path

```
Prompt → Code Changes → Document Updates → Flow Validation
```

---

*Last Updated: 2026-03-03*
