#!/usr/bin/env python3
# ============================================================================
# OGD State-Specific Data Extractor
# Fetches pincode data for specific Indian states from OGD
# ============================================================================

import pandas as pd
import requests
import os
from datetime import datetime
from collections import defaultdict
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

TARGET_STATES = ['JAMMU AND KASHMIR', 'HIMACHAL PRADESH', 'UTTARAKHAND']
OGD_CSV_URL = "https://www.data.gov.in/files/ogdpv2dms/s3fs-public/dataurl03122020/pincode.csv"

CONFIG = {
    'output_file': 'ogd_filtered_pincodes.csv',
    'report_file': 'ogd_fetch_report.txt',
}

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
        if state_name not in self.state_ids:
            self.state_counter += 1
            self.state_ids[state_name] = str(self.state_counter).zfill(4)
        return self.state_ids[state_name]

    def get_or_create_district_id(self, state_id: str, district_name: str) -> str:
        if district_name not in self.district_ids[state_id]:
            self.district_counters[state_id] += 1
            self.district_ids[state_id][district_name] = str(self.district_counters[state_id]).zfill(4)
        return self.district_ids[state_id][district_name]

    def get_or_create_city_id(self, district_id: str, city_name: str) -> str:
        if city_name not in self.city_ids[district_id]:
            self.city_counters[district_id] += 1
            self.city_ids[district_id][city_name] = str(self.city_counters[district_id]).zfill(4)
        return self.city_ids[district_id][city_name]

# ============================================================================
# OGD STATE DATA EXTRACTOR
# ============================================================================

class OGDStateExtractor:
    """Fetches and transforms OGD data for specific states."""

    def __init__(self, target_states, config):
        self.target_states = [s.upper() for s in target_states]
        self.config = config
        self.id_assigner = HierarchicalIDAssigner()
        self.records = []
        self.stats = {
            'downloaded_records': 0,
            'filtered_records': 0,
            'transformed_records': 0,
            'errors': 0,
        }
        self.start_time = datetime.now()

    def download_ogd_csv(self):
        """Download OGD CSV file."""
        print("\n" + "="*80)
        print("DOWNLOADING OGD DATA")
        print("="*80)
        
        try:
            print(f"Downloading from: {OGD_CSV_URL}")
            print("This may take 2-3 minutes...")
            
            response = requests.get(OGD_CSV_URL, timeout=600)
            response.raise_for_status()
            
            # Save to file
            csv_file = 'pin_code_data_full.csv'
            with open(csv_file, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(csv_file)
            print(f"✓ Downloaded successfully ({file_size/1024/1024:.2f} MB)")
            print(f"✓ Saved to: {csv_file}")
            
            return csv_file
            
        except Exception as e:
            print(f"✗ Download failed: {str(e)}")
            return None

    def process_data(self, csv_file):
        """Process OGD CSV and filter for target states."""
        print("\n" + "="*80)
        print("PROCESSING OGD DATA")
        print("="*80)
        
        try:
            print(f"Reading: {csv_file}")
            print(f"Filtering for states: {', '.join(self.target_states)}")
            
            # Read CSV in chunks to handle large file
            chunk_size = 10000
            processed = 0
            
            for chunk_df in pd.read_csv(csv_file, chunksize=chunk_size, 
                                        encoding='utf-8', low_memory=False):
                
                # Filter for target states
                filtered = chunk_df[
                    chunk_df['StateName'].str.upper().isin(self.target_states)
                ]
                
                self.stats['downloaded_records'] += len(chunk_df)
                self.stats['filtered_records'] += len(filtered)
                processed += len(chunk_df)
                
                # Transform filtered records
                for _, row in filtered.iterrows():
                    try:
                        pincode = str(row.get('Pincode', '')).strip()
                        
                        # Validate pincode
                        if not pincode or not pincode.isdigit() or len(pincode) < 5:
                            continue
                        
                        # Extract data
                        state_name = str(row.get('StateName', '')).strip()
                        district_name = str(row.get('DistrictName', '')).strip()
                        city_name = str(row.get('DivisionName', '')).strip() or \
                                   str(row.get('OfficeName', '')).strip()
                        
                        if not all([state_name, district_name, city_name]):
                            continue
                        
                        # Assign hierarchical IDs
                        state_id = self.id_assigner.get_or_create_state_id(state_name)
                        district_id = self.id_assigner.get_or_create_district_id(
                            state_id, district_name)
                        city_id = self.id_assigner.get_or_create_city_id(
                            district_id, city_name)
                        
                        # Create record
                        record = {
                            'pinCode': pincode,
                            'stateId': state_id,
                            'stateName': state_name,
                            'districtId': int(district_id),
                            'districtName': district_name,
                            'cityId': city_id,
                            'cityName': city_name,
                            'countryName': 'India',
                            'status': 'Active',
                            'createdDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'updatedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.records.append(record)
                        self.stats['transformed_records'] += 1
                        
                    except Exception as e:
                        self.stats['errors'] += 1
                        continue
                
                if processed % 50000 == 0:
                    print(f"  Processed {processed:,} records, found {self.stats['transformed_records']} for target states...")
            
            print(f"✓ Processing complete")
            print(f"  - Total records read: {self.stats['downloaded_records']:,}")
            print(f"  - Records for target states: {self.stats['filtered_records']:,}")
            print(f"  - Records transformed: {self.stats['transformed_records']}")
            
            return len(self.records) > 0
            
        except Exception as e:
            print(f"✗ Processing error: {str(e)}")
            return False

    def save_data(self):
        """Save transformed data to CSV."""
        print("\n" + "="*80)
        print("SAVING TRANSFORMED DATA")
        print("="*80)
        
        if not self.records:
            print("✗ No records to save")
            return False
        
        try:
            df = pd.DataFrame(self.records)
            
            # Ensure correct column order
            column_order = [
                'pinCode', 'stateId', 'stateName', 'districtId', 'districtName',
                'cityId', 'cityName', 'countryName', 'status', 'createdDate', 'updatedDate'
            ]
            df = df[column_order]
            
            # Save to CSV
            df.to_csv(self.config['output_file'], index=False)
            
            file_size = os.path.getsize(self.config['output_file'])
            print(f"✓ Saved to: {self.config['output_file']}")
            print(f"✓ File size: {file_size:,} bytes")
            print(f"✓ Total records: {len(df)}")
            
            return True
            
        except Exception as e:
            print(f"✗ Save error: {str(e)}")
            return False

    def generate_report(self):
        """Generate extraction report."""
        print("\n" + "="*80)
        print("GENERATING REPORT")
        print("="*80)
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Calculate stats by state
        state_stats = {}
        for record in self.records:
            state = record['stateName']
            if state not in state_stats:
                state_stats[state] = {'count': 0, 'districts': set(), 'cities': set()}
            state_stats[state]['count'] += 1
            state_stats[state]['districts'].add(record['districtId'])
            state_stats[state]['cities'].add(record['cityId'])
        
        report = f"""
================================================================================
OGD STATE-SPECIFIC DATA EXTRACTION REPORT
================================================================================

EXECUTION SUMMARY
{'─'*80}
Start Time:              {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time:                {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration:                {duration:.2f} seconds ({duration/60:.2f} minutes)

TARGET STATES: {', '.join(self.target_states)}

DATA STATISTICS
{'─'*80}
Total Downloaded:        {self.stats['downloaded_records']:,}
Filtered for States:     {self.stats['filtered_records']:,}
Successfully Transformed: {self.stats['transformed_records']:,}
Errors:                  {self.stats['errors']}

STATE-WISE BREAKDOWN
{'─'*80}
"""
        for state, stats in sorted(state_stats.items()):
            report += f"{state:30} | {stats['count']:6} records | {len(stats['districts']):3} districts | {len(stats['cities']):4} cities\n"
        
        report += f"""
{'─'*80}
TOTAL:                   {self.stats['transformed_records']:6} records

OUTPUT FILES
{'─'*80}
Transformed Data:  {self.config['output_file']}
Report:            {self.config['report_file']}

STATUS: ✓ EXTRACTION COMPLETED SUCCESSFULLY
================================================================================
"""
        
        with open(self.config['report_file'], 'w') as f:
            f.write(report)
        
        print(report)
        return True

    def run(self):
        """Run complete extraction pipeline."""
        print("\n" + "="*80)
        print("OGD STATE-SPECIFIC DATA EXTRACTION")
        print("Jammu & Kashmir | Himachal Pradesh | Uttarakhand")
        print("="*80)
        
        # Check for existing CSV
        csv_file = 'pin_code_data_full.csv'
        if not os.path.exists(csv_file):
            csv_file = self.download_ogd_csv()
            if not csv_file or not os.path.exists(csv_file):
                print("\n✗ Could not obtain OGD data")
                return False
        else:
            print(f"✓ Using existing file: {csv_file}")
        
        # Process data
        if not self.process_data(csv_file):
            print("\n✗ Processing failed")
            return False
        
        # Save data
        if not self.save_data():
            print("\n✗ Save failed")
            return False
        
        # Generate report
        self.generate_report()
        
        print("\n✓ Extraction pipeline completed successfully!")
        print(f"✓ Ready to load into PostgreSQL: {self.config['output_file']}")
        
        return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    try:
        extractor = OGDStateExtractor(TARGET_STATES, CONFIG)
        success = extractor.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        sys.exit(1)
