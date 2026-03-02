# OGD India Pincode Data Extraction & Population Process

**Version:** 1.0
**Date:** March 3, 2026
**Status:** Ready for Execution
**Data Source:** India Open Government Data (OGD) Platform

---

## Table of Contents

1. [Overview](#overview)
2. [Data Source](#data-source)
3. [Extraction Steps](#extraction-steps)
4. [Transformation Process](#transformation-process)
5. [Data Quality Validation](#data-quality-validation)
6. [Loading Instructions](#loading-instructions)
7. [Verification & Rollback](#verification--rollback)

---

## Overview

This document describes the process for extracting pincode data from the OGD platform, transforming it into a hierarchical structure (Country → State → District → City → PinCode), and loading it into the `State_City_PinCode_Master` table.

### Key Features

- **Data Source:** India's official Open Government Data platform
- **Coverage:** 28 States + 7 UTs, 800+ Districts, 5,000+ Cities, 19,000+ PinCodes
- **Hierarchical Structure:** Proper geographic hierarchy with sequential ID assignment
- **City Names:** Uses proper city/division names, not post office names
- **Quality Assurance:** Pre and post-load validation with detailed error reporting

---

## Data Source

### OGD Platform Details

| Property | Value |
|----------|-------|
| **Platform** | Open Government Data (OGD) - India |
| **Resource Name** | All India Pincode Directory |
| **URL** | https://www.data.gov.in/resource/all-india-pincode-directory-till-last-month |
| **Format** | CSV |
| **Update Frequency** | Monthly |
| **License** | Open Data License - India (ODL) |
| **Accuracy** | Government-backed (India Post official data) |

### Source CSV Column Structure

| Column | Type | Description |
|--------|------|-------------|
| `StateName` | VARCHAR | Name of State/UT |
| `DistrictName` | VARCHAR | Name of District |
| `DivisionName` | VARCHAR | Postal Division (used as City) |
| `Pincode` | INTEGER | 6-digit postal code |
| `CircleName` | VARCHAR | Postal Circle |
| `RegionName` | VARCHAR | Postal Region |
| `OfficeName` | VARCHAR | Post Office Name |
| `OfficeType` | VARCHAR | Type of office |
| `DeliveryStatus` | VARCHAR | Delivery status |

---

## Extraction Steps

### Step 1: Download OGD CSV File

**Method A: Direct Web Download**

```bash
# Option 1: Using curl
curl -o pin_code_data.csv \
  "https://www.data.gov.in/files/ogdpv2dms/s3fs-public/dataurl03122020/pincode.csv"

# Option 2: Using wget
wget https://www.data.gov.in/files/ogdpv2dms/s3fs-public/dataurl03122020/pincode.csv \
  -O pin_code_data.csv
```

**Method B: Using OGD API**

```bash
# OGD provides a webservice endpoint
curl -X GET "https://data.gov.in/api/datastore/sql?sql=SELECT * FROM 'c7f26fb2-f1de-4ddb-a149-ab0ba8c3c698'" \
  -H "Content-Type: application/json" > pincode_api_data.json
```

**Method C: Manual Download**

1. Visit [OGD Resource Page](https://www.data.gov.in/resource/all-india-pincode-directory-till-last-month)
2. Click "Download" button
3. Select CSV format
4. Save as `pin_code_data.csv` in `Data Extraction/` folder

### Step 2: Verify Downloaded File

```bash
# Check file exists and has data
ls -lh pin_code_data.csv

# Preview first few rows
head -20 pin_code_data.csv

# Count total records
wc -l pin_code_data.csv

# Check file encoding
file pin_code_data.csv
```

**Expected Results:**
- File size: ~30-40 MB
- Total rows: ~190,000+
- Encoding: UTF-8
- Columns: ~8-10

### Step 3: Place File in Correct Location

```bash
# Navigate to project directory
cd medostel-api-backend/Data\ Extraction/

# Move or copy downloaded file
cp ~/Downloads/pincode.csv ./pin_code_data.csv

# Verify placement
ls -la pin_code_data.csv
```

---

## Transformation Process

### Python Script: `pin_code_data_transformer.py`

This script performs the data transformation and hierarchical ID assignment.

#### Prerequisites

```bash
# Install required Python packages
pip install pandas

# Verify Python version
python3 --version  # Requires Python 3.8+
```

#### Execution

```bash
# Navigate to Data Extraction directory
cd medostel-api-backend/Data\ Extraction/

# Run transformation script
python3 pin_code_data_transformer.py

# Monitor output for progress
```

#### What the Script Does

1. **Loads OGD CSV** - Reads `pin_code_data.csv` with error handling
2. **Validates Structure** - Checks for required columns
3. **Extracts Unique Entities** - Identifies all states, districts, cities
4. **Assigns Hierarchical IDs:**
   - StateID: 0001-0035 (sequential, 28 states + 7 UTs)
   - DistrictID: 0001-N per state (resets per state)
   - CityID: 0001-N per district (resets per district)
   - PinCode: 6-digit (unchanged from source)
5. **Removes Duplicates** - Keeps one record per pincode
6. **Generates CSV Output** - Creates `cleaned_data.csv`
7. **Creates Report** - Generates `data_transformation_report.txt`

#### Output Files

After execution, three files are created:

1. **cleaned_data.csv** (~30 MB)
   - Column order: pinCode, stateId, stateName, districtId, districtName, cityId, cityName, countryName, status, createdDate, updatedDate
   - Ready for database insertion
   - ~19,000 records (unique pincodes only)

2. **data_transformation_report.txt** (~5 KB)
   - Transformation statistics
   - Error logs (if any)
   - Data coverage details
   - Validation status

3. **Console Output**
   - Progress indicators
   - Record counts by geographic level
   - Error summary

### Sample Transformation Output

```
================================================================================
OGD PINCODE DATA TRANSFORMATION PIPELINE
================================================================================

Loading OGD CSV from: pin_code_data.csv
✓ Loaded 192456 records from OGD

✓ All required columns found

✓ Geographic Entities Extracted:
  - States/UTs: 35
  - Districts: 847
  - Unique Cities: 5234
  - Unique PinCodes: 19156
  - Total Records: 192456

Transforming 19156 unique pincode records...
✓ Transformed 19156 records successfully

✓ Hierarchy integrity validated (no inconsistencies)

Writing cleaned data to: cleaned_data.csv
✓ Wrote 19156 records to cleaned_data.csv

Generating validation report: data_transformation_report.txt
✓ Validation report generated

================================================================================
✓ TRANSFORMATION COMPLETED SUCCESSFULLY
================================================================================

Output Files:
  • cleaned_data.csv - Ready for database insertion
  • data_transformation_report.txt - Transformation details

Next Steps:
  1. Review data_transformation_report.txt
  2. Run load_pincode_data.sql to insert data into database
  3. Verify data integrity with validation queries
```

---

## Data Quality Validation

### Pre-Transformation Validation

The script validates:

- ✅ Required columns exist (StateName, DistrictName, Pincode, DivisionName)
- ✅ File can be read (proper encoding)
- ✅ Data types are correct
- ✅ No corrupted records

### During-Transformation Validation

For each record:

- ✅ Pincode is numeric and 5-6 digits (100000-999999)
- ✅ State name is not empty
- ✅ District name is not empty
- ✅ City/Division name is not empty
- ✅ No duplicate pincodes (one record per pincode)

### Post-Transformation Validation

- ✅ All StateIDs are sequential (0001-0035)
- ✅ All DistrictIDs are unique per state
- ✅ All CityIDs are unique per district
- ✅ No orphaned geographic relationships
- ✅ Total record count consistency

### Sample Report Output

```
================================================================================
OGD Data Transformation Report
================================================================================

TRANSFORMATION STATISTICS
Total Records Processed: 192456
Unique Pincodes Found: 19156
Final Record Count: 19156

GEOGRAPHIC COVERAGE
States/UTs: 35
Districts: 847
Cities: 5234
PinCodes: 19156

VALIDATION ERRORS: 0
VALIDATION STATUS: All records passed validation ✓
```

---

## Loading Instructions

### Prerequisites

1. **Database Setup**
   ```bash
   # Ensure migration_step1_1.sql has been executed
   psql -U postgres -d medostel -f migration_step1_1.sql
   ```

2. **Verify Table Structure**
   ```bash
   psql -U postgres -d medostel -c "\d State_City_PinCode_Master"
   ```

3. **Verify Cleaned Data**
   ```bash
   # Check file exists
   ls -lh cleaned_data.csv

   # Verify header
   head -1 cleaned_data.csv
   ```

### Loading Methods

#### Method 1: Using PostgreSQL COPY (Fastest)

```bash
# Create temporary copy of cleaned data in database server accessible location
cp cleaned_data.csv /tmp/cleaned_data.csv

# Execute load script
psql -U postgres -d medostel << EOF
\COPY State_City_PinCode_Master (pinCode, stateId, stateName, districtId, districtName, cityId, cityName, countryName, status, createdDate, updatedDate)
FROM '/tmp/cleaned_data.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ',');
EOF
```

#### Method 2: Using Python Script

```python
#!/usr/bin/env python3
import psycopg2
import csv
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    dbname="medostel",
    user="postgres",
    password="your_password",
    host="localhost"
)
cursor = conn.cursor()

print(f"Loading data at {datetime.now().isoformat()}...")

# Open and read CSV
with open('cleaned_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    batch = []
    batch_size = 1000

    for idx, row in enumerate(reader, 1):
        # Skip if pincode already exists (ON CONFLICT handling)
        batch.append((
            int(row['pinCode']),
            int(row['stateId']),
            row['stateName'],
            int(row['districtId']),
            row['districtName'],
            int(row['cityId']),
            row['cityName'],
            row['countryName'],
            row['status'],
            row['createdDate'],
            row['updatedDate']
        ))

        # Batch insert every N records
        if len(batch) >= batch_size:
            cursor.executemany("""
                INSERT INTO State_City_PinCode_Master
                (pinCode, stateId, stateName, districtId, districtName,
                 cityId, cityName, countryName, status, createdDate, updatedDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (pinCode) DO NOTHING
            """, batch)
            conn.commit()
            batch = []

            if idx % 5000 == 0:
                print(f"  Loaded {idx} records...")

    # Insert remaining batch
    if batch:
        cursor.executemany("""
            INSERT INTO State_City_PinCode_Master
            (pinCode, stateId, stateName, districtId, districtName,
             cityId, cityName, countryName, status, createdDate, updatedDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (pinCode) DO NOTHING
        """, batch)
        conn.commit()

cursor.close()
conn.close()

print(f"Data loading completed at {datetime.now().isoformat()}")
```

#### Method 3: Using SQL File with Manual COPY

```bash
# Edit load_pincode_data.sql and add COPY command
# Then execute:
psql -U postgres -d medostel -f load_pincode_data.sql
```

### Load Monitoring

```bash
# Monitor load progress (in separate terminal)
watch -n 5 'psql -U postgres -d medostel -c "SELECT COUNT(*) as loaded_records FROM State_City_PinCode_Master;"'
```

**Expected Load Time:** 5-15 minutes (depending on system)

---

## Verification & Rollback

### Post-Load Verification

```sql
-- Check total records
SELECT COUNT(*) FROM State_City_PinCode_Master;

-- Verify geographic coverage
SELECT
    COUNT(DISTINCT stateId) as states,
    COUNT(DISTINCT districtId) as districts,
    COUNT(DISTINCT cityId) as cities,
    COUNT(*) as pincodes
FROM State_City_PinCode_Master;

-- Sample records
SELECT * FROM State_City_PinCode_Master
ORDER BY stateId, districtId, cityId, pinCode
LIMIT 20;

-- Verify state IDs are sequential
SELECT DISTINCT stateId, stateName
FROM State_City_PinCode_Master
ORDER BY stateId;

-- Check for NULL values
SELECT COUNT(*) as invalid_records
FROM State_City_PinCode_Master
WHERE districtId IS NULL OR districtName IS NULL;
```

### Troubleshooting

**Issue: "Column count mismatch"**
- Solution: Verify cleaned_data.csv column order matches INSERT statement

**Issue: "Invalid integer value"**
- Solution: Check that numeric columns (stateId, districtId, cityId, pinCode) contain valid integers

**Issue: "Duplicate key value"**
- Solution: Use `ON CONFLICT DO NOTHING` to skip duplicates

**Issue: "File not found"**
- Solution: Verify file path and permissions

### Rollback Procedure

If data loading fails and you need to rollback:

```sql
-- Option 1: Restore from backup table
BEGIN TRANSACTION;

-- Clear current data
DELETE FROM State_City_PinCode_Master;

-- Restore from backup
INSERT INTO State_City_PinCode_Master
SELECT * FROM State_City_PinCode_Master_Backup_Step1_1;

COMMIT;

-- Verify restoration
SELECT COUNT(*) FROM State_City_PinCode_Master;
```

```sql
-- Option 2: Full schema rollback
BEGIN TRANSACTION;

-- Drop columns
ALTER TABLE State_City_PinCode_Master
DROP COLUMN IF EXISTS districtId,
DROP COLUMN IF EXISTS districtName;

-- Drop indexes
DROP INDEX IF EXISTS idx_district_id;
DROP INDEX IF EXISTS idx_district_name;
DROP INDEX IF EXISTS idx_state_district;
DROP INDEX IF EXISTS idx_district_city;
DROP INDEX IF EXISTS idx_state_district_city;
DROP INDEX IF EXISTS idx_district_status;

COMMIT;
```

---

## Useful Query Examples

### Query by State
```sql
SELECT DISTINCT districtId, districtName
FROM State_City_PinCode_Master
WHERE stateId = 1  -- Maharashtra
ORDER BY districtId;
```

### Query by District
```sql
SELECT DISTINCT cityId, cityName
FROM State_City_PinCode_Master
WHERE districtId = 1
ORDER BY cityId;
```

### Query by City
```sql
SELECT pinCode
FROM State_City_PinCode_Master
WHERE cityId = 1 AND districtId = 1
ORDER BY pinCode;
```

### Get All Pincodes for City
```sql
SELECT pinCode
FROM State_City_PinCode_Master
WHERE cityName = 'Mumbai' AND districtName = 'Mumbai'
ORDER BY pinCode;
```

---

## Summary

| Step | Task | Tool | Time |
|------|------|------|------|
| 1 | Download OGD CSV | curl/browser | 10 min |
| 2 | Verify file | bash commands | 2 min |
| 3 | Run transformation | Python script | 5 min |
| 4 | Review report | text editor | 5 min |
| 5 | Run migration | psql | 2 min |
| 6 | Load data | Python/psql | 10 min |
| 7 | Verify load | SQL queries | 3 min |
| **Total** | | | **37 min** |

---

**Next Steps:**
1. Follow extraction steps above
2. Execute Python transformation script
3. Review `data_transformation_report.txt`
4. Execute `load_pincode_data.sql`
5. Verify with provided SQL queries
6. Update APIs to support new district fields (Phase 3)

---

**Status:** ✅ Ready for Execution
**Last Updated:** March 3, 2026
