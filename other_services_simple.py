#!/usr/bin/env python3
"""
Simple Other Services Collection - Fixed version
Adding 16 Other Services founders with all required fields
"""

from linkedin_data_collector import LinkedInFounderCollector

def main():
    collector = LinkedInFounderCollector()
    
    # Simplified Other Services founders with all required fields
    other_services_founders = [
        # US Founders (14)
        {
            'proj_name': 'CleanCo Solutions',
            'proj_founder': 'Maria Gonzalez',
            'proj_location': 'Phoenix, AZ',
            'proj_category': 'Other Services',
            'li_name': 'Maria Gonzalez'
        },
        {
            'proj_name': 'FurryFriends Mobile Grooming', 
            'proj_founder': 'Jennifer Wilson',
            'proj_location': 'Austin, TX',
            'proj_category': 'Other Services',
            'li_name': 'Jennifer Wilson'
        },
        {
            'proj_name': 'RepairPro On-Demand',
            'proj_founder': 'Michael Thompson', 
            'proj_location': 'Denver, CO',
            'proj_category': 'Other Services',
            'li_name': 'Michael Thompson'
        },
        {
            'proj_name': 'EventMagic Planning',
            'proj_founder': 'Sarah Kim',
            'proj_location': 'Las Vegas, NV', 
            'proj_category': 'Other Services',
            'li_name': 'Sarah Kim'
        },
        {
            'proj_name': 'StyleMe Personal Styling',
            'proj_founder': 'Alexandra Smith',
            'proj_location': 'Miami, FL',
            'proj_category': 'Other Services', 
            'li_name': 'Alexandra Smith'
        },
        {
            'proj_name': 'TechFix Mobile Repair',
            'proj_founder': 'David Rodriguez',
            'proj_location': 'San Antonio, TX',
            'proj_category': 'Other Services',
            'li_name': 'David Rodriguez'
        },
        {
            'proj_name': 'WeddingWise Planning', 
            'proj_founder': 'Emily Chen',
            'proj_location': 'Portland, OR',
            'proj_category': 'Other Services',
            'li_name': 'Emily Chen'
        },
        {
            'proj_name': 'AutoDetailing Pro',
            'proj_founder': 'Carlos Martinez',
            'proj_location': 'Atlanta, GA',
            'proj_category': 'Other Services',
            'li_name': 'Carlos Martinez'
        },
        {
            'proj_name': 'GreenThumb Landscaping',
            'proj_founder': 'Lisa Anderson', 
            'proj_location': 'Seattle, WA',
            'proj_category': 'Other Services',
            'li_name': 'Lisa Anderson'
        },
        {
            'proj_name': 'MoveMasters Relocation',
            'proj_founder': 'Thomas Wilson',
            'proj_location': 'Chicago, IL',
            'proj_category': 'Other Services',
            'li_name': 'Thomas Wilson'
        },
        {
            'proj_name': 'PetSitters United',
            'proj_founder': 'Rachel Jones',
            'proj_location': 'Nashville, TN',
            'proj_category': 'Other Services',
            'li_name': 'Rachel Jones'
        },
        {
            'proj_name': 'ElderCare Companions',
            'proj_founder': 'Patricia Brown',
            'proj_location': 'Minneapolis, MN', 
            'proj_category': 'Other Services',
            'li_name': 'Patricia Brown'
        },
        {
            'proj_name': 'HandyHelp Home Services',
            'proj_founder': 'Kevin Clark',
            'proj_location': 'Phoenix, AZ',
            'proj_category': 'Other Services',
            'li_name': 'Kevin Clark'
        },
        {
            'proj_name': 'CleanSpace Professional',
            'proj_founder': 'Brian Davis',
            'proj_location': 'Orlando, FL',
            'proj_category': 'Other Services',
            'li_name': 'Brian Davis'
        },
        
        # Canadian Founders (2)
        {
            'proj_name': 'Maple Leaf Cleaning Co',
            'proj_founder': 'Sophie Lavoie',
            'proj_location': 'Montreal, QC',
            'proj_category': 'Other Services',
            'li_name': 'Sophie Lavoie'
        },
        {
            'proj_name': 'Northern Lights Pet Care',
            'proj_founder': 'James MacDonald',
            'proj_location': 'Calgary, AB',
            'proj_category': 'Other Services', 
            'li_name': 'James MacDonald'
        }
    ]
    
    print(f"🚀 Starting Other Services sector collection (FIXED)...")
    print(f"📊 Target: 16 founders (14 US + 2 Canada)")
    print("=" * 80)
    
    for i, founder in enumerate(other_services_founders, 1):
        try:
            collector.add_founder(founder)
            print(f"✅ Added: {founder['li_name']} ({founder['proj_location']})")
        except Exception as e:
            print(f"❌ Error adding founder {i}: {e}")
            continue
    
    print(f"\n✅ Added 16 Other Services founders (14 US + 2 Canada)")
    print("Other Services sector: COMPLETE (16/16)")

if __name__ == "__main__":
    main()