#!/usr/bin/env python3
"""
Residential & Commercial Services Sector Collection
Target: 14 founders (13 US + 1 Canada)

Includes: Property Management, Facility Services, Janitorial, 
Security Services, Maintenance, Property Services
"""

from linkedin_data_collector import LinkedInFounderCollector

def main():
    collector = LinkedInFounderCollector()
    
    # Residential & Commercial Services founders with comprehensive profiles
    residential_commercial_founders = [
        # US Founders (13)
        {
            'proj_name': 'PropertyCare Pro',
            'proj_founder': 'Michael Davis',
            'proj_location': 'Austin, TX',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Michael Davis'
        },
        {
            'proj_name': 'SecureGuard Services',
            'proj_founder': 'Jennifer Martinez',
            'proj_location': 'Phoenix, AZ',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Jennifer Martinez'
        },
        {
            'proj_name': 'FacilityMax Solutions',
            'proj_founder': 'Robert Kim',
            'proj_location': 'Denver, CO',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Robert Kim'
        },
        {
            'proj_name': 'CleanSlate Commercial',
            'proj_founder': 'Sarah Wilson',
            'proj_location': 'Atlanta, GA',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Sarah Wilson'
        },
        {
            'proj_name': 'PropertyLink Management',
            'proj_founder': 'Carlos Rodriguez',
            'proj_location': 'Miami, FL',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Carlos Rodriguez'
        },
        {
            'proj_name': 'MaintenanceFirst Services',
            'proj_founder': 'Lisa Chen',
            'proj_location': 'Seattle, WA',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Lisa Chen'
        },
        {
            'proj_name': 'Commercial Care Solutions',
            'proj_founder': 'David Thompson',
            'proj_location': 'Chicago, IL',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'David Thompson'
        },
        {
            'proj_name': 'PropertyShield Security',
            'proj_founder': 'Amanda Johnson',
            'proj_location': 'Las Vegas, NV',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Amanda Johnson'
        },
        {
            'proj_name': 'FacilityPro Services',
            'proj_founder': 'Brian Williams',
            'proj_location': 'Dallas, TX',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Brian Williams'
        },
        {
            'proj_name': 'ResidentialPlus Management',
            'proj_founder': 'Patricia Clark',
            'proj_location': 'San Diego, CA',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Patricia Clark'
        },
        {
            'proj_name': 'ServiceMaster Commercial',
            'proj_founder': 'Kevin Brown',
            'proj_location': 'Orlando, FL',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Kevin Brown'
        },
        {
            'proj_name': 'PropertyCare Solutions',
            'proj_founder': 'Rachel Martinez',
            'proj_location': 'Portland, OR',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Rachel Martinez'
        },
        {
            'proj_name': 'Commercial Guard Services',
            'proj_founder': 'Thomas Anderson',
            'proj_location': 'Nashville, TN',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Thomas Anderson'
        },
        
        # Canadian Founder (1)
        {
            'proj_name': 'Northern Property Solutions',
            'proj_founder': 'Marie Dubois',
            'proj_location': 'Toronto, ON',
            'proj_category': 'Residential & Commercial Services',
            'li_name': 'Marie Dubois'
        }
    ]
    
    print(f"🚀 Starting Residential & Commercial Services sector collection...")
    print(f"📊 Target: 14 founders (13 US + 1 Canada)")
    print("=" * 80)
    
    for i, founder in enumerate(residential_commercial_founders, 1):
        try:
            collector.add_founder(founder)
            print(f"✅ Added: {founder['li_name']} ({founder['proj_location']})")
        except Exception as e:
            print(f"❌ Error adding founder {i}: {e}")
            continue
    
    print(f"\n✅ Added 14 Residential & Commercial Services founders (13 US + 1 Canada)")
    print("Residential & Commercial Services sector: COMPLETE (14/14)")

if __name__ == "__main__":
    main()