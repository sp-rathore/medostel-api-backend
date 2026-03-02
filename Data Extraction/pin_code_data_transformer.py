#!/usr/bin/env python3
# ============================================================================
# OGD India Pincode Data Transformer
# ============================================================================
# Purpose: Extract OGD pincode data, assign hierarchical IDs, and generate
#          insert-ready CSV for State_City_PinCode_Master table
#
# Input: OGD CSV with columns: officename, pincode, districtname, statename, etc.
# Output: cleaned_data.csv with columns for database insertion
#
# Author: Medostel Project
# Date: March 3, 2026
# ============================================================================

import pandas as pd
import csv
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    'input_file': 'pin_code_data.csv',  # OGD CSV (download separately)
    'output_file': 'cleaned_data.csv',
    'validation_report': 'data_transformation_report.txt',
    'country_id': 1,  # Always 1 for India
    'country_name': 'India',
    'default_status': 'Active',
    'city_preference': 'divisionname',  # Use divisionname for city (not post office name)
}

# ============================================================================
# DATA STRUCTURES FOR HIERARCHICAL ID ASSIGNMENT
# ============================================================================

class HierarchicalIDAssigner:
    """Manages hierarchical ID assignment for geographic entities."""

    def __init__(self):
        self.state_ids = {}  # {state_name: state_id}
        self.district_ids = defaultdict(dict)  # {state_id: {district_name: district_id}}
        self.city_ids = defaultdict(dict)  # {district_id: {city_name: city_id}}

        self.state_counter = 0
        self.district_counters = defaultdict(int)  # {state_id: counter}
        self.city_counters = defaultdict(int)  # {district_id: counter}

    def get_or_create_state_id(self, state_name: str) -> int:
        """Get existing or create new State ID (sequential: 0001, 0002, ..., 0035)."""
        if state_name not in self.state_ids:
            self.state_counter += 1
            self.state_ids[state_name] = str(self.state_counter).zfill(4)
        return self.state_ids[state_name]

    def get_or_create_district_id(self, state_id: str, district_name: str) -> str:
        """Get existing or create new District ID (per state: 0001-N)."""
        district_key = (state_id, district_name)
        if district_name not in self.district_ids[state_id]:
            self.district_counters[state_id] += 1
            self.district_ids[state_id][district_name] = str(self.district_counters[state_id]).zfill(4)
        return self.district_ids[state_id][district_name]

    def get_or_create_city_id(self, district_id: str, city_name: str) -> str:
        """Get existing or create new City ID (per district: 0001-N)."""
        if city_name not in self.city_ids[district_id]:
            self.city_counters[district_id] += 1
            self.city_ids[district_id][city_name] = str(self.city_counters[district_id]).zfill(4)
        return self.city_ids[district_id][city_name]


class OGDDataTransformer:
    """Transforms OGD pincode data to database-ready format."""

    def __init__(self, config: Dict):
        self.config = config
        self.id_assigner = HierarchicalIDAssigner()
        self.records = []
        self.validation_errors = []
        self.data_statistics = {}

    def load_ogd_csv(self, file_path: str) -> pd.DataFrame:
        """Load OGD CSV file with error handling."""
        try:
            print(f"Loading OGD CSV from: {file_path}")
            df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
            print(f"✓ Loaded {len(df)} records from OGD")
            return df
        except FileNotFoundError:
            raise Exception(f"CSV file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")

    def validate_required_columns(self, df: pd.DataFrame) -> bool:
        """Validate that required columns exist in CSV."""
        required_columns = [
            'statename',
            'districtname',
            'pincode',
            'divisionname'  # Used for city name
        ]

        df_cols_lower = [col.lower() for col in df.columns]
        missing = [col for col in required_columns if col not in df_cols_lower]

        if missing:
            raise Exception(f"Missing required columns: {missing}\nAvailable: {df.columns.tolist()}")

        print(f"✓ All required columns found")
        return True

    def extract_unique_geographic_entities(self, df: pd.DataFrame) -> Dict:
        """Extract unique states, districts, and cities."""
        # Normalize column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        # Extract unique entities
        unique_states = df['statename'].unique()
        unique_districts = df.groupby('statename')['districtname'].unique()
        unique_cities = df.groupby('districtname')['divisionname'].unique()
        unique_pincodes = df['pincode'].nunique()

        statistics = {
            'total_states': len(unique_states),
            'total_districts': df['districtname'].nunique(),
            'total_cities': df['divisionname'].nunique(),
            'total_pincodes': unique_pincodes,
            'total_records': len(df)
        }

        print(f"\n✓ Geographic Entities Extracted:")
        print(f"  - States/UTs: {statistics['total_states']}")
        print(f"  - Districts: {statistics['total_districts']}")
        print(f"  - Unique Cities: {statistics['total_cities']}")
        print(f"  - Unique PinCodes: {statistics['total_pincodes']}")
        print(f"  - Total Records: {statistics['total_records']}")

        return statistics

    def transform_data(self, df: pd.DataFrame) -> List[Dict]:
        """Transform OGD data to database format with hierarchical IDs."""

        # Normalize columns
        df.columns = [col.lower() for col in df.columns]

        # Clean and deduplicate: keep one record per pincode
        df_unique = df.drop_duplicates(subset=['pincode'], keep='first')

        print(f"\nTransforming {len(df_unique)} unique pincode records...")

        records = []
        seen_pincodes = set()

        for idx, row in df_unique.iterrows():
            try:
                pincode = int(row['pincode'])

                # Skip invalid pincodes
                if pincode < 100000 or pincode > 999999:
                    self.validation_errors.append(
                        f"Invalid pincode range: {pincode} (Row {idx+1})"
                    )
                    continue

                # Skip duplicate pincodes
                if pincode in seen_pincodes:
                    self.validation_errors.append(
                        f"Duplicate pincode: {pincode} (Row {idx+1})"
                    )
                    continue

                seen_pincodes.add(pincode)

                # Extract and clean fields
                state_name = str(row['statename']).strip() if pd.notna(row['statename']) else None
                district_name = str(row['districtname']).strip() if pd.notna(row['districtname']) else None
                city_name = str(row['divisionname']).strip() if pd.notna(row['divisionname']) else None

                # Validate required fields
                if not all([state_name, district_name, city_name]):
                    self.validation_errors.append(
                        f"Missing geographic data (Row {idx+1}): "
                        f"State={state_name}, District={district_name}, City={city_name}"
                    )
                    continue

                # Assign hierarchical IDs
                state_id = self.id_assigner.get_or_create_state_id(state_name)
                district_id = self.id_assigner.get_or_create_district_id(state_id, district_name)
                city_id = self.id_assigner.get_or_create_city_id(district_id, city_name)

                # Create record
                record = {
                    'pinCode': pincode,
                    'stateId': int(state_id),
                    'stateName': state_name,
                    'districtId': int(district_id),
                    'districtName': district_name,
                    'cityId': int(city_id),
                    'cityName': city_name,
                    'countryName': self.config['country_name'],
                    'status': self.config['default_status'],
                    'createdDate': datetime.utcnow().isoformat() + 'Z',
                    'updatedDate': datetime.utcnow().isoformat() + 'Z'
                }

                records.append(record)

            except ValueError as e:
                self.validation_errors.append(f"Value error (Row {idx+1}): {str(e)}")
                continue
            except Exception as e:
                self.validation_errors.append(f"Unexpected error (Row {idx+1}): {str(e)}")
                continue

        print(f"✓ Transformed {len(records)} records successfully")
        self.records = records
        return records

    def validate_hierarchy_integrity(self) -> bool:
        """Validate that all hierarchical relationships are valid."""
        print("\nValidating hierarchy integrity...")

        errors = 0
        state_districts = defaultdict(set)
        district_cities = defaultdict(set)

        for record in self.records:
            state_key = record['stateId']
            district_key = (record['stateId'], record['districtId'])
            city_key = (record['districtId'], record['cityId'])

            state_districts[state_key].add(record['stateName'])
            district_cities[district_key].add((record['districtName'], record['cityName']))

        # Check for inconsistencies
        for state_id, state_names in state_districts.items():
            if len(state_names) > 1:
                print(f"⚠ Warning: State ID {state_id} has multiple names: {state_names}")
                errors += 1

        if errors == 0:
            print("✓ Hierarchy integrity validated (no inconsistencies)")
        else:
            print(f"⚠ Found {errors} potential inconsistencies")

        return errors == 0

    def write_cleaned_csv(self, output_file: str) -> bool:
        """Write cleaned data to CSV file ready for database insertion."""
        try:
            print(f"\nWriting cleaned data to: {output_file}")

            # Write header
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'pinCode', 'stateId', 'stateName', 'districtId', 'districtName',
                    'cityId', 'cityName', 'countryName', 'status', 'createdDate', 'updatedDate'
                ])
                writer.writeheader()
                writer.writerows(self.records)

            print(f"✓ Wrote {len(self.records)} records to {output_file}")
            return True

        except Exception as e:
            print(f"✗ Error writing CSV: {str(e)}")
            return False

    def generate_validation_report(self, report_file: str):
        """Generate comprehensive validation report."""
        print(f"\nGenerating validation report: {report_file}")

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("OGD Data Transformation Report\n")
            f.write("=" * 80 + "\n\n")

            f.write("TRANSFORMATION STATISTICS\n")
            f.write("-" * 80 + "\n")
            for key, value in self.data_statistics.items():
                f.write(f"{key}: {value}\n")

            f.write(f"\nFinal Record Count: {len(self.records)}\n")

            # Geographic coverage
            states = set(r['stateId'] for r in self.records)
            districts = set((r['stateId'], r['districtId']) for r in self.records)
            cities = set((r['districtId'], r['cityId']) for r in self.records)
            pincodes = set(r['pinCode'] for r in self.records)

            f.write(f"\nGEOGRAPHIC COVERAGE\n")
            f.write("-" * 80 + "\n")
            f.write(f"States/UTs: {len(states)}\n")
            f.write(f"Districts: {len(districts)}\n")
            f.write(f"Cities: {len(cities)}\n")
            f.write(f"PinCodes: {len(pincodes)}\n")

            # Validation errors
            if self.validation_errors:
                f.write(f"\nVALIDATION ERRORS ({len(self.validation_errors)})\n")
                f.write("-" * 80 + "\n")
                for error in self.validation_errors[:100]:  # Limit to first 100
                    f.write(f"• {error}\n")
                if len(self.validation_errors) > 100:
                    f.write(f"\n... and {len(self.validation_errors) - 100} more errors\n")
            else:
                f.write(f"\nVALIDATION STATUS: All records passed validation ✓\n")

            f.write(f"\nTransformation completed: {datetime.now().isoformat()}\n")

        print(f"✓ Validation report generated")

    def execute(self, input_file: str) -> bool:
        """Execute full transformation pipeline."""
        print("\n" + "=" * 80)
        print("OGD PINCODE DATA TRANSFORMATION PIPELINE")
        print("=" * 80)

        try:
            # Load data
            df = self.load_ogd_csv(input_file)

            # Validate
            self.validate_required_columns(df)

            # Extract statistics
            self.data_statistics = self.extract_unique_geographic_entities(df)

            # Transform
            self.transform_data(df)

            # Validate hierarchy
            self.validate_hierarchy_integrity()

            # Write output
            self.write_cleaned_csv(self.config['output_file'])

            # Generate report
            self.generate_validation_report(self.config['validation_report'])

            print("\n" + "=" * 80)
            print("✓ TRANSFORMATION COMPLETED SUCCESSFULLY")
            print("=" * 80)
            print(f"\nOutput Files:")
            print(f"  • {self.config['output_file']} - Ready for database insertion")
            print(f"  • {self.config['validation_report']} - Transformation details")
            print("\nNext Steps:")
            print("  1. Review data_transformation_report.txt")
            print("  2. Run load_pincode_data.sql to insert data into database")
            print("  3. Verify data integrity with validation queries")

            return True

        except Exception as e:
            print(f"\n✗ TRANSFORMATION FAILED: {str(e)}")
            return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Create transformer instance
    transformer = OGDDataTransformer(CONFIG)

    # Execute transformation
    success = transformer.execute(CONFIG['input_file'])

    # Exit with appropriate code
    exit(0 if success else 1)
