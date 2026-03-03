# PHASE 1.1: PRE-MIGRATION ANALYSIS

**Status:** IN PROGRESS
**Date Started:** 2026-03-03
**Phase:** 1.1 of 4
**Duration:** 2-4 hours

---

## EXECUTIVE SUMMARY

This document provides a comprehensive analysis of the changes required to migrate the `user_master` table from its current schema to the new enhanced schema. The analysis identifies:
- **Column changes:** 4 modifications, 2 additions, 0 removals
- **Data compatibility issues:** 5 identified (medium risk)
- **Foreign key changes:** 3 new foreign keys
- **Constraint additions:** Composite unique constraint, email validation, mobile validation
- **Migration complexity:** Medium (requires data type conversion and validation)

---

## SECTION 1: SCHEMA COMPARISON

### 1.1 Current Schema (As of 2026-03-03)

**Table Name:** `user_master` | **Owner:** postgres | **Schema:** public

| Column | Current Type | Current Nullable | Current Default | Current Constraints |
|--------|--------------|-----------------|-----------------|-------------------|
| userid | varchar(100) | NOT NULL | - | PRIMARY KEY |
| firstname | varchar(50) | NOT NULL | - | - |
| lastname | varchar(50) | NOT NULL | - | - |
| currentrole | integer | NOT NULL | - | FK → user_role_master(roleid) |
| organisation | varchar(100) | YES | - | - |
| emailid | varchar(100) | NOT NULL | - | UNIQUE |
| mobilenumber | varchar(15) | NOT NULL | - | UNIQUE |
| address1 | varchar(255) | YES | - | - |
| address2 | varchar(255) | YES | - | - |
| statename | varchar(100) | YES | - | - |
| cityname | varchar(100) | YES | - | - |
| pincode | varchar(10) | YES | - | - |
| status | varchar(20) | NOT NULL | 'Active' | CHECK (status IN ('Active', 'Inactive')) |
| createddate | timestamp | YES | CURRENT_TIMESTAMP | - |
| updateddate | timestamp | YES | CURRENT_TIMESTAMP | - |

**Current Indexes:**
- `user_master_pkey` (PRIMARY KEY on userid)
- `idx_user_created_date` (btree on createddate)
- `idx_user_email` (btree on emailid)
- `idx_user_mobile` (btree on mobilenumber)
- `idx_user_role` (btree on currentrole)
- `idx_user_status` (btree on status)
- `user_master_emailid_key` (UNIQUE on emailid)
- `user_master_mobilenumber_key` (UNIQUE on mobilenumber)

**Current Foreign Keys:**
- `currentrole` → user_role_master(roleid) with ON UPDATE CASCADE, ON DELETE SET NULL

**Current Referenced By:**
- report_history(userid)
- user_login(userid)

---

### 1.2 New Schema (Target)

**Table Name:** `user_master` | **Schema:** public

| Column | New Type | New Nullable | New Default | New Constraints |
|--------|----------|-------------|-------------|-----------------|
| userId | varchar(100) | NOT NULL | - | PRIMARY KEY |
| firstName | varchar(50) | NOT NULL | - | - |
| lastName | varchar(50) | NOT NULL | - | - |
| currentRole | varchar(50) | NOT NULL | - | FK → user_role_master(roleId) |
| emailId | varchar(255) | NOT NULL | - | UNIQUE, CHECK email regex |
| mobileNumber | numeric(10) | NOT NULL | - | UNIQUE, CHECK (1000000000-9999999999) |
| organisation | varchar(255) | YES | - | - |
| address1 | varchar(255) | YES | - | - |
| address2 | varchar(255) | YES | - | - |
| stateId | integer | YES | - | FK → state_city_pincode_master(stateId) |
| stateName | varchar(100) | YES | - | - |
| districtId | integer | YES | - | FK → state_city_pincode_master(districtId) |
| cityId | integer | YES | - | FK → state_city_pincode_master(cityId) |
| cityName | varchar(100) | YES | - | - |
| pinCode | integer | YES | - | FK → state_city_pincode_master(pinCode) |
| commentLog | varchar(255) | YES | - | - |
| status | varchar(50) | YES | 'Active' | CHECK (status IN ('active', 'pending', 'deceased', 'inactive')) |
| createdDate | timestamp | YES | CURRENT_TIMESTAMP | - |
| updatedDate | timestamp | YES | CURRENT_TIMESTAMP | - |

**New Unique Constraints:**
- emailId (individual)
- mobileNumber (individual)
- COMPOSITE: (emailId, mobileNumber) combination

**New Check Constraints:**
- emailId: `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$`
- mobileNumber: `>= 1000000000 AND <= 9999999999`
- status: 'active', 'pending', 'deceased', 'inactive'

**New Foreign Keys:**
- currentRole → user_role_master(roleId)
- stateId → state_city_pincode_master(stateId)
- districtId → state_city_pincode_master(districtId)
- cityId → state_city_pincode_master(cityId)
- pinCode → state_city_pincode_master(pinCode)

---

## SECTION 2: COLUMN CHANGE ANALYSIS

### 2.1 Column Modifications (Data Compatibility Issues)

#### Change 1: Column Name Case Conversion
| Field | Current | New | Issue |
|-------|---------|-----|-------|
| **userid** | `userid` | `userId` | Case change - not a data issue, pure rename |
| **firstname** | `firstname` | `firstName` | Case change - not a data issue, pure rename |
| **lastname** | `lastname` | `lastName` | Case change - not a data issue, pure rename |
| **currentrole** | `currentrole` | `currentRole` | Case change + type change |
| **emailid** | `emailid` | `emailId` | Case change + length change |
| **mobilenumber** | `mobilenumber` | `mobileNumber` | Case change + type change |
| **organisation** | `organisation` | `organisation` | No change |
| **address1** | `address1` | `address1` | No change |
| **address2** | `address2` | `address2` | No change |
| **statename** | `statename` | `stateName` | Case change - not a data issue |
| **cityname** | `cityname` | `cityName` | Case change - not a data issue |
| **pincode** | `pincode` | `pinCode` | Case change + type change |
| **status** | `status` | `status` | No change in name |
| **createddate** | `createddate` | `createdDate` | Case change - not a data issue |
| **updateddate** | `updateddate` | `updatedDate` | Case change - not a data issue |

---

#### Change 2: currentrole - Type Conversion (integer → varchar(50))

**Current:** `currentrole INTEGER`
**New:** `currentRole VARCHAR(50)`
**Impact Level:** HIGH

**Data Compatibility Analysis:**
- Current data: Integer role IDs (e.g., 1, 2, 3, etc.)
- Expected new data: Role names (e.g., 'admin', 'user', 'doctor', etc.)

**Issues:**
1. Current integer values (1, 2, 3) won't match new VARCHAR values
2. Need to lookup mapping from user_role_master table

**Migration Strategy:**
```sql
-- STEP 1: Create temporary column for role names
ALTER TABLE user_master ADD COLUMN currentRole_temp VARCHAR(50);

-- STEP 2: Populate from user_role_master lookup
UPDATE user_master um
SET currentRole_temp = urm.roleName
FROM user_role_master urm
WHERE um.currentrole = urm.roleid;

-- STEP 3: Verify data integrity
SELECT COUNT(*) FROM user_master WHERE currentRole_temp IS NULL;
-- Should return 0

-- STEP 4: Drop old column and rename
ALTER TABLE user_master DROP COLUMN currentrole CASCADE;
ALTER TABLE user_master RENAME COLUMN currentRole_temp TO currentRole;
```

**Risk:** ⚠️ **HIGH**
- If user_role_master.roleName doesn't exist, need to verify structure first
- If any users have non-existent role IDs, migration will fail

**Dependency Check Required:** ✅ REQUIRED

---

#### Change 3: emailid - Length & Validation Change (varchar(100) → varchar(255) + regex check)

**Current:** `emailid VARCHAR(100) NOT NULL UNIQUE`
**New:** `emailId VARCHAR(255) NOT NULL UNIQUE` + email regex validation
**Impact Level:** LOW-MEDIUM

**Data Compatibility Analysis:**
- Current data: Email addresses (max 100 chars)
- New constraint: Email addresses (max 255 chars) + regex validation

**Issues:**
1. Current max length is 100 chars - new is 255 chars (expansion, no data loss)
2. Need to validate all existing emails match regex pattern

**Migration Strategy:**
```sql
-- STEP 1: Verify all existing emails match the pattern
SELECT emailid, COUNT(*) as invalid_count
FROM user_master
WHERE emailid !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
GROUP BY emailid;

-- STEP 2: If any invalid emails found, review and fix manually or apply cleanup logic
-- Example: Remove or flag invalid emails for manual review

-- STEP 3: Rename and extend column
ALTER TABLE user_master RENAME COLUMN emailid TO emailId;
ALTER TABLE user_master ALTER COLUMN emailId TYPE VARCHAR(255);
```

**Risk:** ⚠️ **MEDIUM**
- Some existing emails might not match strict regex pattern
- Need to audit and clean data before migration

**Data Validation Required:** ✅ REQUIRED

---

#### Change 4: mobilenumber - Type Conversion (varchar(15) → numeric(10) + validation check)

**Current:** `mobilenumber VARCHAR(15) NOT NULL UNIQUE`
**New:** `mobileNumber NUMERIC(10) NOT NULL UNIQUE` + validation (1000000000-9999999999)
**Impact Level:** HIGH

**Data Compatibility Analysis:**
- Current data: String format mobile numbers (max 15 chars)
- New constraint: Numeric values (exactly 10 digits, range 1000000000-9999999999)

**Issues:**
1. **Type conversion:** VARCHAR to NUMERIC requires careful casting
2. **Format validation:** Current data might include:
   - Country codes: +91 (India)
   - Dashes: 98-7654-3210
   - Spaces: 98 7654 3210
   - Extensions: 9876543210 ext 123
   - Non-numeric characters
3. **Length mismatch:** VARCHAR(15) might contain non-10-digit numbers

**Migration Strategy:**
```sql
-- STEP 1: Audit current mobile number formats
SELECT
    mobilenumber,
    LENGTH(mobilenumber) as length,
    REGEXP_MATCHES(mobilenumber, '[0-9]+', 'g') as digits,
    COUNT(*) as count
FROM user_master
GROUP BY mobilenumber
ORDER BY length DESC;

-- STEP 2: Create temporary column
ALTER TABLE user_master ADD COLUMN mobileNumber_temp NUMERIC(10);

-- STEP 3: Extract and convert numeric portion
UPDATE user_master
SET mobileNumber_temp = (
    REGEXP_REPLACE(mobilenumber, '[^0-9]', '', 'g')::NUMERIC
)
WHERE mobilenumber ~ '[0-9]{10}';

-- STEP 4: Verify conversion success
SELECT COUNT(*) FROM user_master WHERE mobileNumber_temp IS NULL;
-- Should be 0 or identify problematic records

-- STEP 5: Validate range (10 digits, 1000000000-9999999999)
SELECT COUNT(*) FROM user_master
WHERE mobileNumber_temp < 1000000000 OR mobileNumber_temp > 9999999999;

-- STEP 6: Drop old column and rename
ALTER TABLE user_master DROP COLUMN mobilenumber CASCADE;
ALTER TABLE user_master RENAME COLUMN mobileNumber_temp TO mobileNumber;
```

**Risk:** ⚠️⚠️ **CRITICAL**
- Data loss possible if format conversion fails
- Non-standard formats will be lost
- Need comprehensive audit before proceeding
- Some mobile numbers might not be valid 10-digit Indian numbers

**Data Cleanup Required:** ✅ REQUIRED
**Manual Review Required:** ✅ REQUIRED

---

#### Change 5: pincode - Type Conversion (varchar(10) → integer)

**Current:** `pincode VARCHAR(10)`
**New:** `pinCode INTEGER`
**Impact Level:** MEDIUM

**Data Compatibility Analysis:**
- Current data: String format PIN codes (max 10 chars)
- New constraint: Integer format (up to 2,147,483,647)

**Issues:**
1. Type conversion from VARCHAR to INTEGER
2. Current data might include:
   - Non-numeric characters
   - Leading zeros (which will be lost in INTEGER)
   - Alphanumeric PIN codes

**Migration Strategy:**
```sql
-- STEP 1: Audit PIN code formats
SELECT
    pincode,
    LENGTH(pincode) as length,
    REGEXP_MATCHES(pincode, '[^0-9]') as non_digits,
    COUNT(*) as count
FROM user_master
WHERE pincode IS NOT NULL
GROUP BY pincode
ORDER BY length DESC;

-- STEP 2: Create temporary column
ALTER TABLE user_master ADD COLUMN pinCode_temp INTEGER;

-- STEP 3: Convert numeric PIN codes only
UPDATE user_master
SET pinCode_temp = (pincode::INTEGER)
WHERE pincode ~ '^[0-9]+$';

-- STEP 4: Verify conversion
SELECT COUNT(*) FROM user_master WHERE pinCode_temp IS NULL AND pincode IS NOT NULL;

-- STEP 5: Drop old column and rename
ALTER TABLE user_master DROP COLUMN pincode CASCADE;
ALTER TABLE user_master RENAME COLUMN pinCode_temp TO pinCode;
```

**Risk:** ⚠️ **MEDIUM**
- Leading zeros in PIN codes will be lost
- Non-numeric PIN codes will fail conversion
- Some data might become NULL if format is invalid

**Data Validation Required:** ✅ REQUIRED

---

### 2.2 Column Additions (New Columns)

#### Addition 1: stateId (NEW)
- **Type:** INTEGER
- **Nullable:** YES
- **Default:** NULL
- **Purpose:** Foreign key to state_city_pincode_master
- **Migration:** Initialize as NULL (no existing data)
- **Data Population:** Manual/batch update later

#### Addition 2: districtId (NEW)
- **Type:** INTEGER
- **Nullable:** YES
- **Default:** NULL
- **Purpose:** Foreign key to state_city_pincode_master
- **Migration:** Initialize as NULL (no existing data)
- **Data Population:** Manual/batch update later

#### Addition 3: cityId (NEW)
- **Type:** INTEGER
- **Nullable:** YES
- **Default:** NULL
- **Purpose:** Foreign key to state_city_pincode_master
- **Migration:** Initialize as NULL (no existing data)
- **Data Population:** Manual/batch update later

#### Addition 4: commentLog (NEW)
- **Type:** VARCHAR(255)
- **Nullable:** YES
- **Default:** NULL
- **Purpose:** Track recent changes/audit log
- **Migration:** Initialize as NULL for existing records
- **Data Population:** Manual annotation or auto-generate migration comment

**Migration Strategy:**
```sql
-- All new columns initialize to NULL
ALTER TABLE user_master ADD COLUMN stateId INTEGER;
ALTER TABLE user_master ADD COLUMN districtId INTEGER;
ALTER TABLE user_master ADD COLUMN cityId INTEGER;
ALTER TABLE user_master ADD COLUMN commentLog VARCHAR(255);

-- Optional: Add initial comment for all existing records
UPDATE user_master
SET commentLog = 'Migrated from legacy schema on 2026-03-03'
WHERE commentLog IS NULL;
```

---

### 2.3 Column Removals (None)
✅ No columns are being removed from the schema.

---

## SECTION 3: DATA COMPATIBILITY ISSUES (DETAILED)

### Issue #1: Mobile Number Format Standardization
**Severity:** 🔴 CRITICAL
**Affected Column:** mobilenumber → mobileNumber
**Status:** UNRESOLVED - Requires Data Audit

**Description:**
Current mobile numbers are stored as VARCHAR(15) with various formats:
- Standard 10-digit: 9876543210
- With country code: +919876543210
- With dashes: 98-7654-3210
- With spaces: 98 7654 3210
- With extensions: 9876543210 x123

**Impact:**
- Conversion to NUMERIC(10) will fail for non-standard formats
- Leading zeros (unlikely in Indian numbers but possible) will be lost
- Data loss if format cleanup is not done properly

**Resolution:**
1. ✅ Query to identify all formats (see Section 2.1 Migration Strategy)
2. ❓ Decision required: Keep only valid 10-digit numbers?
3. ❓ Decision required: How to handle non-standard formats? (Delete, Archive, Convert)

**Action Required Before Migration:** ✅ YES

---

### Issue #2: Email Address Format Validation
**Severity:** 🟡 MEDIUM
**Affected Column:** emailid → emailId
**Status:** UNRESOLVED - Requires Data Audit

**Description:**
New schema enforces regex validation: `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$`

Some existing emails might fail this validation:
- Emails with special characters beyond [A-Za-z0-9._%+-]
- International domain names (IDN)
- Non-standard TLDs

**Impact:**
- Data validation failure during migration
- Need to identify and clean problematic email addresses

**Resolution:**
1. ✅ Query to identify invalid emails (see Section 2.1 Migration Strategy)
2. ❓ Decision required: Reject or modify invalid emails?

**Action Required Before Migration:** ✅ YES

---

### Issue #3: Role Name Mapping Dependency
**Severity:** 🔴 CRITICAL
**Affected Column:** currentrole → currentRole
**Status:** UNRESOLVED - Requires Dependency Verification

**Description:**
Type conversion from INTEGER (role ID) to VARCHAR(role name) requires:
- Mapping table: user_role_master
- Must have consistent roleId → roleName relationship
- All current role IDs must exist in user_role_master

**Impact:**
- Migration failure if user_role_master structure is different
- Data loss if user_role_master.roleName doesn't exist
- Orphaned role IDs will result in NULL values

**Resolution:**
1. ✅ Verify user_role_master table structure
2. ✅ Verify all current role IDs exist in user_role_master
3. ✅ Identify role name field name (might be roleName, role_name, name, etc.)

**Action Required Before Migration:** ✅ YES - CRITICAL

---

### Issue #4: PIN Code Type Conversion
**Severity:** 🟡 MEDIUM
**Affected Column:** pincode → pinCode
**Status:** UNRESOLVED - Requires Data Audit

**Description:**
Conversion from VARCHAR(10) to INTEGER:
- Loses leading zeros (if any)
- Fails for non-numeric PIN codes
- Loses extended formats (e.g., postal codes with letters)

**Impact:**
- Data loss for non-numeric PIN codes
- Loss of leading zeros

**Resolution:**
1. ✅ Query to identify PIN code formats
2. ❓ Decision required: Keep only numeric PIN codes?

**Action Required Before Migration:** ✅ YES

---

### Issue #5: Status Field Value Changes
**Severity:** 🟡 MEDIUM
**Affected Column:** status
**Status:** UNRESOLVED - Requires Data Update

**Description:**
Current schema allows: 'Active', 'Inactive'
New schema allows: 'active', 'pending', 'deceased', 'inactive'

**Issues:**
- Case mismatch: 'Active' vs 'active'
- New status values: 'pending', 'deceased' (no existing data)
- Need to standardize case

**Impact:**
- CHECK constraint will fail for 'Active' (capital A)
- Existing 'Inactive' won't match 'inactive' (case sensitive)

**Resolution:**
```sql
-- STEP 1: Convert to lowercase
UPDATE user_master
SET status = LOWER(status)
WHERE status IS NOT NULL;

-- STEP 2: Verify conversion
SELECT DISTINCT status FROM user_master;
-- Should show: 'active', 'inactive' (lowercase)
```

**Action Required Before Migration:** ✅ YES

---

## SECTION 4: DEPENDENT TABLE VERIFICATION

### 4.1 user_role_master Table

**Purpose:** Reference table for currentRole foreign key
**Status:** ⏳ REQUIRES VERIFICATION

**Required Checks:**
- [ ] Table exists in database
- [ ] Has field: roleId (INTEGER) or similar
- [ ] Has field: roleName (VARCHAR) or similar
- [ ] All current user_master.currentrole values exist in user_role_master.roleId
- [ ] Naming convention: roleId vs role_id vs roleid

**Verification Query:**
```sql
-- Check table structure
\d user_role_master

-- Check column names
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'user_role_master';

-- Verify current role IDs exist
SELECT DISTINCT currentrole FROM user_master
WHERE currentrole NOT IN (SELECT roleid FROM user_role_master);
-- Should return 0 rows
```

**Action Required Before Migration:** ✅ YES

---

### 4.2 state_city_pincode_master Table

**Purpose:** Reference table for stateId, districtId, cityId, pinCode foreign keys
**Status:** ⏳ REQUIRES VERIFICATION

**Required Checks:**
- [ ] Table exists in database
- [ ] Has columns: stateId, districtId, cityId, pinCode
- [ ] Column data types match (all INTEGER)
- [ ] Primary key structure
- [ ] Naming convention: stateId vs state_id vs stateid

**Verification Query:**
```sql
-- Check table structure
\d state_city_pincode_master

-- Check column names and types
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'state_city_pincode_master';

-- Check row count
SELECT COUNT(*) FROM state_city_pincode_master;
```

**Action Required Before Migration:** ✅ YES

---

### 4.3 Referenced Tables

**report_history:**
- Foreign key: userid → user_master.userid
- Impact: NONE (rename is backward compatible with constraints)

**user_login:**
- Foreign key: userid → user_master.userid
- Impact: NONE (rename is backward compatible with constraints)

---

## SECTION 5: DATA VALIDATION QUERIES

### 5.1 Pre-Migration Audit

```sql
-- 1. Count total records
SELECT COUNT(*) as total_users FROM user_master;

-- 2. Check NULL values by column
SELECT
    SUM(CASE WHEN userid IS NULL THEN 1 ELSE 0 END) as null_userid,
    SUM(CASE WHEN firstname IS NULL THEN 1 ELSE 0 END) as null_firstname,
    SUM(CASE WHEN lastname IS NULL THEN 1 ELSE 0 END) as null_lastname,
    SUM(CASE WHEN currentrole IS NULL THEN 1 ELSE 0 END) as null_currentrole,
    SUM(CASE WHEN emailid IS NULL THEN 1 ELSE 0 END) as null_emailid,
    SUM(CASE WHEN mobilenumber IS NULL THEN 1 ELSE 0 END) as null_mobilenumber,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END) as null_status
FROM user_master;

-- 3. Check status values
SELECT DISTINCT status, COUNT(*) FROM user_master GROUP BY status;

-- 4. Check email format (regex)
SELECT COUNT(*) as invalid_emails FROM user_master
WHERE emailid !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$';

-- 5. Check mobile number format
SELECT COUNT(*) as non_numeric_mobile FROM user_master
WHERE mobilenumber !~ '^[0-9]+$';

-- 6. Check for duplicate emails
SELECT emailid, COUNT(*) FROM user_master
GROUP BY emailid HAVING COUNT(*) > 1;

-- 7. Check for duplicate mobile numbers
SELECT mobilenumber, COUNT(*) FROM user_master
GROUP BY mobilenumber HAVING COUNT(*) > 1;

-- 8. Check role IDs exist in user_role_master
SELECT DISTINCT currentrole FROM user_master
WHERE currentrole NOT IN (SELECT roleid FROM user_role_master);

-- 9. Check for orphaned foreign keys
SELECT COUNT(*) as orphaned_records FROM user_master um
WHERE NOT EXISTS (
    SELECT 1 FROM user_role_master urm
    WHERE um.currentrole = urm.roleid
);

-- 10. Check PIN code format
SELECT pincode, COUNT(*) FROM user_master
WHERE pincode IS NOT NULL
GROUP BY pincode
ORDER BY LENGTH(pincode) DESC;
```

---

## SECTION 6: DATA MIGRATION STRATEGY

### 6.1 Overall Migration Approach

**Strategy:** SAFE MIGRATION WITH INTERMEDIATE COLUMNS
- Create new columns with new names and types
- Migrate and transform data
- Validate all data in parallel
- Drop old columns only after successful validation
- Maintain ability to rollback

**Key Principles:**
1. ✅ Non-destructive (create before drop)
2. ✅ Reversible (keep old columns until verification)
3. ✅ Validatable (run checks before final conversion)
4. ✅ Auditable (log all transformations)

### 6.2 Phase-by-Phase Migration Plan

#### Phase A: Backup & Validation (Pre-Migration)
1. Full database backup
2. Run all validation queries (Section 5.1)
3. Generate audit report
4. Get approval to proceed
5. Create staging environment copy for dry-run

#### Phase B: Add New Columns (No Data Loss)
1. Add all new columns with NULL defaults
2. Add stateId, districtId, cityId, commentLog
3. Verify schema change successful

#### Phase C: Transform & Migrate Data
1. **Case normalization:** Convert column names to camelCase (rename)
2. **Mobile number conversion:** Extract digits, validate range
3. **Email validation:** Verify regex match, flag invalid
4. **Role name mapping:** Join with user_role_master, convert to names
5. **PIN code conversion:** Convert to integer, validate

#### Phase D: Validation & Verification
1. Row count before/after should match
2. No unexpected NULLs introduced
3. All foreign keys resolvable
4. All CHECK constraints validatable
5. Run comprehensive validation queries

#### Phase E: Add Constraints & Indexes
1. Add CHECK constraints for email, mobile, status
2. Add composite UNIQUE constraint (emailId, mobileNumber)
3. Create indexes
4. Create foreign keys

#### Phase F: Cleanup & Finalize
1. Drop old columns
2. Rename temporary columns to final names
3. Verify all foreign keys and dependencies
4. Update statistics
5. Run final validation

---

## SECTION 7: IDENTIFIED RISKS & BLOCKERS

### Risk 1: user_role_master Structure Unknown
**Status:** 🔴 BLOCKING
**Priority:** CRITICAL
**Impact:** Cannot proceed with currentRole conversion without verification

**Required Action:**
```bash
# Need to verify:
1. Check user_role_master table exists
2. Identify role ID column name (roleid, role_id, roleId?)
3. Identify role name column name (roleName, role_name, name?)
4. Verify all current role IDs exist in the table
```

### Risk 2: Mobile Number Format Variety
**Status:** 🟡 WARNING
**Priority:** HIGH
**Impact:** Data loss if formats not standardized

**Required Action:**
- Audit all mobile number formats
- Decide on cleanup strategy
- Test conversion logic with sample data

### Risk 3: Email Validation Strict Regex
**Status:** 🟡 WARNING
**Priority:** MEDIUM
**Impact:** Some emails might fail validation

**Required Action:**
- Query invalid email addresses
- Review and manually fix outliers
- Ensure regex pattern covers all valid existing emails

### Risk 4: Status Field Case Sensitivity
**Status:** 🟡 WARNING
**Priority:** MEDIUM
**Impact:** CHECK constraint will fail for existing 'Active'/'Inactive'

**Required Action:**
- Convert all status values to lowercase before applying constraints
- Verify no other status values exist

### Risk 5: PIN Code Data Loss
**Status:** 🟡 WARNING
**Priority:** MEDIUM
**Impact:** Leading zeros lost, non-numeric codes rejected

**Required Action:**
- Audit PIN code formats
- Decide on approach for non-numeric PIN codes
- Document data loss

---

## SECTION 8: RECOMMENDATIONS

### 8.1 Pre-Migration Checklist

Before proceeding to Phase 1.2 (Migration Script Creation):

- [ ] **Backup current database** - Full backup on production
- [ ] **Verify user_role_master** - Structure, columns, data integrity
- [ ] **Verify state_city_pincode_master** - Structure, columns, data integrity
- [ ] **Run validation queries** - Identify data quality issues
- [ ] **Audit mobile numbers** - Document format variations
- [ ] **Audit emails** - Identify regex validation failures
- [ ] **Get stakeholder approval** - Sign off on migration approach
- [ ] **Schedule downtime** - Plan migration window
- [ ] **Prepare rollback plan** - Document rollback procedures
- [ ] **Test on staging** - Do dry-run migration first
- [ ] **Document exceptions** - List any data that will be lost/changed

### 8.2 Data Cleanup Actions (Recommended)

**High Priority:**
1. Standardize status values to lowercase ('active', 'inactive')
2. Validate and clean email addresses
3. Standardize mobile number format to 10-digit numeric

**Medium Priority:**
1. Populate stateId, districtId, cityId from existing stateName, cityName data
2. Add meaningful commentLog values for existing records

**Low Priority:**
1. Validate PIN codes against official postal code database

### 8.3 Dependency Verification Script

```bash
#!/bin/bash
# Script to verify all dependencies before migration

echo "=== USER_MASTER PRE-MIGRATION VERIFICATION ==="
echo ""

# Check user_role_master exists
psql -d medostel -c "
    SELECT 'user_role_master' as table_name,
           EXISTS(SELECT 1 FROM information_schema.tables
                  WHERE table_name = 'user_role_master') as exists;
"

# Check state_city_pincode_master exists
psql -d medostel -c "
    SELECT 'state_city_pincode_master' as table_name,
           EXISTS(SELECT 1 FROM information_schema.tables
                  WHERE table_name = 'state_city_pincode_master') as exists;
"

# Count total users
psql -d medostel -c "SELECT COUNT(*) as total_users FROM user_master;"

# Check status values
psql -d medostel -c "SELECT DISTINCT status FROM user_master;"

echo ""
echo "=== END VERIFICATION ==="
```

---

## SECTION 9: NEXT STEPS

### Immediate Actions (Today - 2026-03-03)

1. ✅ **Verify user_role_master structure**
   - Run: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user_role_master';`
   - Document column names and identify mapping fields

2. ✅ **Verify state_city_pincode_master structure**
   - Run: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'state_city_pincode_master';`
   - Document column names

3. ✅ **Run validation audit queries** (Section 5.1)
   - Generate data quality report
   - Identify exceptions

4. ✅ **Get approval to proceed** with Phase 1.2

### Next Phase (Phase 1.2)

Once all verifications and approvals are in place:
- Create comprehensive migration SQL script
- Create backup and rollback scripts
- Create validation scripts
- Document all transformation logic

---

## SUMMARY TABLE

| Item | Current | New | Change Type | Risk | Action |
|------|---------|-----|-------------|------|--------|
| userid | PK | PK | Rename | Low | Auto-rename |
| firstname | varchar(50) | varchar(50) | Rename | Low | Auto-rename |
| lastname | varchar(50) | varchar(50) | Rename | Low | Auto-rename |
| currentrole | int → | varchar(50) | Type + Lookup | HIGH | Verify mapping |
| emailid | varchar(100) | varchar(255) + regex | Length + Validation | MED | Audit emails |
| mobilenumber | varchar(15) | numeric(10) + check | Type + Validation | HIGH | Audit & clean |
| organisation | varchar(100) | varchar(255) | Length expand | Low | Auto-resize |
| address1 | varchar(255) | varchar(255) | No change | None | No action |
| address2 | varchar(255) | varchar(255) | No change | None | No action |
| statename | varchar(100) | varchar(100) | Rename | Low | Auto-rename |
| cityname | varchar(100) | varchar(100) | Rename | Low | Auto-rename |
| pincode | varchar(10) | int | Type + rename | MED | Audit & convert |
| status | varchar(20) | varchar(50) | Case change | MED | Normalize case |
| createddate | timestamp | timestamp | Rename | Low | Auto-rename |
| updateddate | timestamp | timestamp | Rename | Low | Auto-rename |
| stateId | - | int | NEW | Low | NULL init |
| districtId | - | int | NEW | Low | NULL init |
| cityId | - | int | NEW | Low | NULL init |
| commentLog | - | varchar(255) | NEW | Low | NULL init |

---

## DOCUMENT METADATA

| Field | Value |
|-------|-------|
| Phase | 1.1 - Pre-Migration Analysis |
| Status | IN PROGRESS |
| Created | 2026-03-03 |
| Last Updated | 2026-03-03 |
| Duration Est. | 2-4 hours |
| Blockers | 3 (user_role_master, mobile audit, email audit) |
| Risks Identified | 5 HIGH/CRITICAL |
| Next Phase | 1.2 - Migration Script Creation |
| Approval Status | ⏳ PENDING |

---

**Document Prepared By:** Claude Code (AI Assistant)
**Status:** Ready for Review
**Location:** Implementation Guide folder

---

## APPENDIX A: VERIFICATION COMMANDS

Run these queries to gather all required information:

```sql
-- 1. Database state
SELECT version();
SELECT current_database();

-- 2. User_role_master verification
\d user_role_master
SELECT * FROM user_role_master LIMIT 5;

-- 3. State_city_pincode_master verification
\d state_city_pincode_master
SELECT * FROM state_city_pincode_master LIMIT 5;

-- 4. Current user_master info
SELECT COUNT(*) FROM user_master;
SELECT * FROM user_master LIMIT 1;

-- 5. Data quality audit (full)
-- (See Section 5.1 for complete queries)
```

