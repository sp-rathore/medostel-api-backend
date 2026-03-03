#!/usr/bin/env python3
# ============================================================================
# OGD Batch Data Extractor - Fetches India Pincode Data in Batches
# ============================================================================
# Purpose: Download OGD pincode data in batches of 1000 records and merge
# Data Source: Open Government Data - India Pincode Directory
# ============================================================================

import pandas as pd
import requests
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from collections import defaultdict
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    'output_file': 'cleaned_data.csv',
    'batch_report': 'batch_extraction_report.txt',
    'country_id': 1,
    'country_name': 'India',
    'default_status': 'Active',
    'batch_size': 1000,
}

# OGD API Endpoint for pincode data
OGD_API_URL = "https://data.gov.in/api/datastore/sql?sql=SELECT * FROM 'c7f26fb2-f1de-4ddb-a149-ab0ba8c3c698' LIMIT {limit} OFFSET {offset}"

# Alternative: Direct CSV download
OGD_CSV_URL = "https://www.data.gov.in/files/ogdpv2dms/s3fs-public/dataurl03122020/pincode.csv"

# ============================================================================
# HIERARCHICAL ID ASSIGNER
# ============================================================================

class HierarchicalIDAssigner:
    """Manages hierarchical ID assignment for geographic entities."""

    def __init__(self):
        self.state_ids = {}
        self.district_ids = defaultdict(dict)
        self.city_ids = defaultdict(dict)
        
        self.state_counter = 0
        self.district_counters = defaultdict(int)
        self.city_counters = defaultdict(int)

    def get_or_create_state_id(self, state_name: str) -> str:
        """Get existing or create new State ID."""
        if state_name not in self.state_ids:
            self.state_counter += 1
            self.state_ids[state_name] = str(self.state_counter).zfill(4)
        return self.state_ids[state_name]

    def get_or_create_district_id(self, state_id: str, district_name: str) -> str:
        """Get existing or create new District ID (per state)."""
        if district_name not in self.district_ids[state_id]:
            self.district_counters[state_id] += 1
            self.district_ids[state_id][district_name] = str(self.district_counters[state_id]).zfill(4)
        return self.district_ids[state_id][district_name]

    def get_or_create_city_id(self, district_id: str, city_name: str) -> str:
        """Get existing or create new City ID (per district)."""
        if city_name not in self.city_ids[district_id]:
            self.city_counters[district_id] += 1
            self.city_ids[district_id][city_name] = str(self.city_counters[district_id]).zfill(4)
        return self.city_ids[district_id][city_name]

# ============================================================================
# BATCH OGD EXTRACTOR
# ============================================================================

class BatchOGDExtractor:
    """Extracts OGD pincode data in batches and transforms to database format."""

    def __init__(self, config: Dict):
        self.config = config
        self.id_assigner = HierarchicalIDAssigner()
        self.all_records = []
        self.processed_pincodes = set()
        self.batch_stats = []
        self.total_records_processed = 0
        self.start_time = datetime.now()

    def download_csv_data(self):
        """Download OGD CSV data directly."""
        print("\n" + "="*80)
        print("DOWNLOADING OGD PINCODE DATA")
        print("="*80)
        
        try:
            print(f"Downloading from: {OGD_CSV_URL}")
            response = requests.get(OGD_CSV_URL, timeout=300)
            response.raise_for_status()
            
            # Save to file
            csv_file = 'pin_code_data.csv'
            with open(csv_file, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(csv_file)
            print(f"✓ Downloaded successfully ({file_size:,} bytes)")
            print(f"✓ Saved to: {csv_file}")
            
            return csv_file
            
        except Exception as e:
            print(f"✗ Download failed: {str(e)}")
            print("\nFallback: Please download manually from:")
            print("https://www.data.gov.in/resource/all-india-pincode-directory-till-last-month")
            return None

    def process_batch(self, batch_df: pd.DataFrame, batch_num: int) -> Dict:
        """Process a single batch of records."""
        print(f"\nProcessing Batch {batch_num}...")
        
        batch_start = datetime.now()
        batch_records = 0
        batch_duplicates = 0
        
        try:
            for _, row in batch_df.iterrows():
                pincode = str(row.get('Pincode', '')).strip()
                
                # Skip if already processed
                if pincode in self.processed_pincodes:
                    batch_duplicates += 1
                    continue
                
                # Validate pincode
                if not pincode or not pincode.isdigit() or len(pincode) < 5:
                    continue
                
                # Extract geographic data
                state_name = str(row.get('StateName', '')).strip()
                district_name = str(row.get('DistrictName', '')).strip()
                city_name = str(row.get('DivisionName', '')).strip() or str(row.get('OfficeName', '')).strip()
                
                if not all([state_name, district_name, city_name]):
                    continue
                
                # Assign hierarchical IDs
                state_id = self.id_assigner.get_or_create_state_id(state_name)
                district_id = self.id_assigner.get_or_create_district_id(state_id, district_name)
                city_id = self.id_assigner.get_or_create_city_id(district_id, city_name)
                
                # Create record
                record = {
                    'pinCode': pincode,
                    'stateId': state_id,
                    'stateName': state_name,
                    'districtId': int(district_id),
                    'districtName': district_name,
                    'cityId': city_id,
                    'cityName': city_name,
                    'countryName': self.config['country_name'],
                    'status': self.config['default_status'],
                    'createdDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'updatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                self.all_records.append(record)
                self.processed_pincodes.add(pincode)
                batch_records += 1
                self.total_records_processed += 1
        
        except Exception as e:
            print(f"  ✗ Error processing batch: {str(e)}")
            return None
        
        batch_end = datetime.now()
        batch_time = (batch_end - batch_start).total_seconds()
        
        stats = {
            'batch_num': batch_num,
            'records_processed': batch_records,
            'duplicates': batch_duplicates,
            'time_seconds': batch_time,
        }
        
        self.batch_stats.append(stats)
        
        print(f"  ✓ Batch {batch_num}: {batch_records} new records (skipped {batch_duplicates} duplicates)")
        print(f"  ✓ Processing time: {batch_time:.2f}s")
        print(f"  ✓ Total so far: {len(self.all_records)} unique records")
        
        return stats

    def extract_and_transform(self):
        """Main extraction and transformation process."""
        print("\n" + "="*80)
        print("OGD BATCH DATA EXTRACTION & TRANSFORMATION")
        print("="*80)
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check for existing CSV file
        csv_file = 'pin_code_data.csv'
        if not os.path.exists(csv_file):
            print(f"\n✗ CSV file not found: {csv_file}")
            print("Attempting to download from OGD...")
            csv_file = self.download_csv_data()
            
            if not csv_file or not os.path.exists(csv_file):
                print("\n✗ Could not obtain OGD data. Exiting.")
                return False
        
        print(f"\n✓ Using CSV file: {csv_file}")
        file_size = os.path.getsize(csv_file)
        print(f"✓ File size: {file_size:,} bytes")
        
        # Load CSV in batches
        print(f"\nReading CSV file in batches of {self.config['batch_size']}...")
        
        try:
            batch_num = 0
            for chunk_df in pd.read_csv(csv_file, chunksize=self.config['batch_size'], encoding='utf-8'):
                batch_num += 1
                self.process_batch(chunk_df, batch_num)
            
            print(f"\n✓ All {batch_num} batches processed")
            
        except Exception as e:
            print(f"✗ Error reading CSV: {str(e)}")
            return False
        
        return True

    def save_cleaned_data(self) -> bool:
        """Save cleaned data to CSV file."""
        print("\n" + "="*80)
        print("SAVING CLEANED DATA")
        print("="*80)
        
        if not self.all_records:
            print("✗ No records to save")
            return False
        
        try:
            # Create DataFrame
            df = pd.DataFrame(self.all_records)
            
            # Ensure correct column order
            column_order = [
                'pinCode', 'stateId', 'stateName', 'districtId', 'districtName',
                'cityId', 'cityName', 'countryName', 'status', 'createdDate', 'updatedDate'
            ]
            df = df[column_order]
            
            # Save to CSV
            output_path = self.config['output_file']
            df.to_csv(output_path, index=False)
            
            file_size = os.path.getsize(output_path)
            print(f"✓ Saved to: {output_path}")
            print(f"✓ File size: {file_size:,} bytes")
            print(f"✓ Total records: {len(df)}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving data: {str(e)}")
            return False

    def generate_report(self):
        """Generate extraction report."""
        print("\n" + "="*80)
        print("GENERATING EXTRACTION REPORT")
        print("="*80)
        
        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()
        
        # Calculate statistics
        total_states = len(self.id_assigner.state_ids)
        total_districts = sum(len(d) for d in self.id_assigner.district_ids.values())
        total_cities = sum(len(c) for c in self.id_assigner.city_ids.values())
        
        report = f"""
================================================================================
OGD BATCH DATA EXTRACTION REPORT
================================================================================

EXTRACTION SUMMARY
{'─'*80}
Start Time:              {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time:                {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Total Duration:          {total_time:.2f} seconds ({total_time/60:.2f} minutes)

BATCH PROCESSING STATISTICS
{'─'*80}
Total Batches:           {len(self.batch_stats)}
Batch Size:              {self.config['batch_size']}
Total Records Processed: {self.total_records_processed}
Unique Records:          {len(self.all_records)}
Duplicates Skipped:      {self.total_records_processed - len(self.all_records)}

GEOGRAPHIC COVERAGE
{'─'*80}
States/UTs:              {total_states}
Districts:               {total_districts}
Cities:                  {total_cities}
Pin Codes:               {len(self.all_records)}

BATCH-WISE DETAILS
{'─'*80}
"""
        for stat in self.batch_stats:
            report += f"Batch {stat['batch_num']:3d}: {stat['records_processed']:6d} records ({stat['time_seconds']:6.2f}s, {stat['duplicates']} duplicates)\n"
        
        report += f"""
{'─'*80}
OUTPUT FILES
{'─'*80}
Cleaned Data:  {self.config['output_file']}
Report:        {self.config['batch_report']}

STATUS: ✓ EXTRACTION COMPLETED SUCCESSFULLY
================================================================================
"""
        
        # Save report
        with open(self.config['batch_report'], 'w') as f:
            f.write(report)
        
        print(report)
        return True

    def run(self):
        """Run complete extraction pipeline."""
        print("\n" + "="*80)
        print("MEDOSTEL - OGD BATCH DATA EXTRACTION PIPELINE")
        print("="*80)
        
        # Step 1: Extract and transform
        if not self.extract_and_transform():
            print("\n✗ Extraction failed")
            return False
        
        # Step 2: Save cleaned data
        if not self.save_cleaned_data():
            print("\n✗ Save failed")
            return False
        
        # Step 3: Generate report
        self.generate_report()
        
        print("\n✓ Pipeline completed successfully!")
        print(f"✓ Output file: {self.config['output_file']}")
        print("✓ Ready for database loading")
        
        return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    try:
        extractor = BatchOGDExtractor(CONFIG)
        success = extractor.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        sys.exit(1)
