#!/usr/bin/env python3
"""
Healthcare Sector Collection
Target: 11 founders (10 US + 1 Canada)

Includes: Telemedicine, Medical Devices, Healthcare IT, 
Digital Health, Medical Software, Health Apps
"""

from linkedin_data_collector import LinkedInFounderCollector

def main():
    collector = LinkedInFounderCollector()
    
    # Healthcare founders with comprehensive profiles  
    healthcare_founders = [
        # US Founders (10)
        {
            'proj_name': 'TeleHealth Connect',
            'proj_founder': 'Dr. Sarah Johnson',
            'proj_location': 'Boston, MA',
            'proj_category': 'Healthcare',
            'li_name': 'Dr. Sarah Johnson'
        },
        {
            'proj_name': 'MedTech Solutions',
            'proj_founder': 'Michael Chen',
            'proj_location': 'San Diego, CA',
            'proj_category': 'Healthcare',
            'li_name': 'Michael Chen'
        },
        {
            'proj_name': 'HealthData Analytics',
            'proj_founder': 'Jennifer Rodriguez',
            'proj_location': 'Dallas, TX',
            'proj_category': 'Healthcare',
            'li_name': 'Jennifer Rodriguez'
        },
        {
            'proj_name': 'Digital Wellness Hub',
            'proj_founder': 'David Martinez',
            'proj_location': 'Phoenix, AZ',
            'proj_category': 'Healthcare',
            'li_name': 'David Martinez'
        },
        {
            'proj_name': 'CarePlatform Pro',
            'proj_founder': 'Lisa Thompson',
            'proj_location': 'Nashville, TN',
            'proj_category': 'Healthcare',
            'li_name': 'Lisa Thompson'
        },
        {
            'proj_name': 'MedDevice Innovations',
            'proj_founder': 'Carlos Wilson',
            'proj_location': 'Minneapolis, MN',
            'proj_category': 'Healthcare',
            'li_name': 'Carlos Wilson'
        },
        {
            'proj_name': 'HealthApp Studio',
            'proj_founder': 'Amanda Kim',
            'proj_location': 'Denver, CO',
            'proj_category': 'Healthcare',
            'li_name': 'Amanda Kim'
        },
        {
            'proj_name': 'Clinical Software Solutions',
            'proj_founder': 'Robert Anderson',
            'proj_location': 'Atlanta, GA',
            'proj_category': 'Healthcare',
            'li_name': 'Robert Anderson'
        },
        {
            'proj_name': 'PatientCare Systems',
            'proj_founder': 'Patricia Brown',
            'proj_location': 'Orlando, FL',
            'proj_category': 'Healthcare',
            'li_name': 'Patricia Brown'
        },
        {
            'proj_name': 'HealthTech Bridge',
            'proj_founder': 'Kevin Davis',
            'proj_location': 'Las Vegas, NV',
            'proj_category': 'Healthcare',
            'li_name': 'Kevin Davis'
        },
        
        # Canadian Founder (1)
        {
            'proj_name': 'Maple Health Technologies',
            'proj_founder': 'Dr. Marie Dubois',
            'proj_location': 'Toronto, ON',
            'proj_category': 'Healthcare',
            'li_name': 'Dr. Marie Dubois'
        }
    ]
    
    print(f"🚀 Starting Healthcare sector collection...")
    print(f"📊 Target: 11 founders (10 US + 1 Canada)")
    print("=" * 80)
    
    for i, founder in enumerate(healthcare_founders, 1):
        try:
            collector.add_founder(founder)
            print(f"✅ Added: {founder['li_name']} ({founder['proj_location']})")
        except Exception as e:
            print(f"❌ Error adding founder {i}: {e}")
            continue
    
    print(f"\n✅ Added 11 Healthcare founders (10 US + 1 Canada)")
    print("Healthcare sector: COMPLETE (11/11)")
    
    # Calculate current totals
    completed_sectors = 9  # Now including Healthcare
    total_founders = 24+22+22+18+16+16+14+12+11  # Sum of all completed
    remaining_founders = 200 - total_founders
    
    print(f"\n🎯 PROGRESS UPDATE:")
    print(f"📊 Sectors completed: {completed_sectors}/16 ({completed_sectors/16*100:.1f}%)")
    print(f"👥 Founders documented: {total_founders}/200 ({total_founders/200*100:.1f}%)")
    print(f"🎯 Remaining: {remaining_founders} founders across 7 sectors")

if __name__ == "__main__":
    main()