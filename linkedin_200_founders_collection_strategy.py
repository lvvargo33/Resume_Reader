"""
LinkedIn 200 Founders Data Collection Strategy
Target: Representative sample across all business sectors
"""

import pandas as pd
from datetime import datetime

def create_200_founder_collection_plan():
    """
    Create comprehensive plan for collecting 200 founders proportionally across industries
    """
    
    print("📊 LINKEDIN 200 FOUNDERS COLLECTION STRATEGY")
    print("=" * 70)
    print("Target: 200 founders representing all business sectors")
    print("Geographic Split: 180 US (90%) | 20 Canada (10%)")
    print()
    
    # Industry distribution for 200 founders (based on our research)
    industry_targets = {
        'Food & Restaurant': {
            'percentage': 12.0,
            'target_count': 24,
            'us_count': 22,
            'canada_count': 2,
            'search_terms': [
                '"restaurant owner" OR "restaurant founder" Kickstarter OR Indiegogo',
                '"food truck owner" "launched" OR "started"',
                '"chef entrepreneur" "opened restaurant"',
                '"catering business" founder OR owner'
            ],
            'profile_keywords': ['Restaurant', 'Chef', 'Food', 'Catering', 'Culinary']
        },
        
        'Retail & E-commerce': {
            'percentage': 11.0,
            'target_count': 22,
            'us_count': 20,
            'canada_count': 2,
            'search_terms': [
                '"e-commerce founder" "online store" Shopify OR Amazon',
                '"retail store owner" "opened" OR "launched"',
                '"boutique owner" fashion OR clothing',
                '"Amazon FBA" entrepreneur OR seller'
            ],
            'profile_keywords': ['Retail', 'E-commerce', 'Store Owner', 'Online Business']
        },
        
        'Business Services': {
            'percentage': 11.0,
            'target_count': 22,
            'us_count': 20,
            'canada_count': 2,
            'search_terms': [
                '"marketing agency founder" OR "marketing agency owner"',
                '"consulting firm" founder OR principal',
                '"B2B services" entrepreneur OR founder',
                '"business consultant" "started own" OR "launched"'
            ],
            'profile_keywords': ['Consultant', 'Agency', 'B2B', 'Business Services']
        },
        
        'Health, Beauty & Fitness': {
            'percentage': 9.0,
            'target_count': 18,
            'us_count': 16,
            'canada_count': 2,
            'search_terms': [
                '"gym owner" OR "fitness studio founder"',
                '"salon owner" OR "spa owner" entrepreneur',
                '"personal trainer" "own business" OR "founded"',
                '"wellness" founder OR entrepreneur'
            ],
            'profile_keywords': ['Fitness', 'Beauty', 'Wellness', 'Health', 'Salon']
        },
        
        'Construction & Contracting': {
            'percentage': 8.0,
            'target_count': 16,
            'us_count': 14,
            'canada_count': 2,
            'search_terms': [
                '"general contractor" "own business" OR founder',
                '"construction company" owner OR founder',
                '"plumbing business" OR "electrical contractor" owner',
                '"home renovation" entrepreneur OR founder'
            ],
            'profile_keywords': ['Contractor', 'Construction', 'Builder', 'Trades']
        },
        
        'Other Services': {
            'percentage': 8.0,
            'target_count': 16,
            'us_count': 14,
            'canada_count': 2,
            'search_terms': [
                '"pet services" owner OR founder',
                '"automotive repair" "own shop" OR business',
                '"cleaning service" founder OR owner',
                '"personal services" entrepreneur'
            ],
            'profile_keywords': ['Services', 'Pet Care', 'Automotive', 'Personal Services']
        },
        
        'Residential & Commercial Services': {
            'percentage': 7.0,
            'target_count': 14,
            'us_count': 13,
            'canada_count': 1,
            'search_terms': [
                '"landscaping business" owner OR founder',
                '"property management" entrepreneur OR founder',
                '"commercial cleaning" business owner',
                '"maintenance services" founder'
            ],
            'profile_keywords': ['Property Management', 'Landscaping', 'Maintenance']
        },
        
        'Technology': {
            'percentage': 6.0,
            'target_count': 12,
            'us_count': 11,
            'canada_count': 1,
            'search_terms': [
                '"software startup" founder OR co-founder',
                '"SaaS founder" OR "app developer" entrepreneur',
                '"tech startup" Kickstarter OR "seed funding"',
                '"AI startup" OR "ML company" founder'
            ],
            'profile_keywords': ['Software', 'Technology', 'Startup', 'App', 'SaaS']
        },
        
        'Healthcare': {
            'percentage': 5.5,
            'target_count': 11,
            'us_count': 10,
            'canada_count': 1,
            'search_terms': [
                '"medical practice" owner OR founder physician',
                '"healthcare startup" founder OR entrepreneur',
                '"telehealth" OR "telemedicine" founder',
                '"medical device" entrepreneur OR inventor'
            ],
            'profile_keywords': ['Healthcare', 'Medical', 'Doctor', 'Physician', 'Health Tech']
        },
        
        'Financial Services': {
            'percentage': 4.5,
            'target_count': 9,
            'us_count': 8,
            'canada_count': 1,
            'search_terms': [
                '"financial advisor" "own practice" OR firm',
                '"insurance agency" owner OR founder',
                '"fintech startup" founder OR entrepreneur',
                '"investment firm" founder OR principal'
            ],
            'profile_keywords': ['Financial', 'Insurance', 'Investment', 'Fintech']
        },
        
        'Education & Training': {
            'percentage': 4.0,
            'target_count': 8,
            'us_count': 7,
            'canada_count': 1,
            'search_terms': [
                '"online course" creator OR founder',
                '"tutoring business" owner OR founder',
                '"education startup" entrepreneur',
                '"training company" founder OR owner'
            ],
            'profile_keywords': ['Education', 'Training', 'Course Creator', 'Tutor']
        },
        
        'Manufacturing': {
            'percentage': 3.5,
            'target_count': 7,
            'us_count': 6,
            'canada_count': 1,
            'search_terms': [
                '"manufacturing business" owner OR founder',
                '"product manufacturer" entrepreneur',
                '"custom manufacturing" OR "3D printing" business',
                '"craft production" business owner'
            ],
            'profile_keywords': ['Manufacturing', 'Production', 'Factory', 'Maker']
        },
        
        'Transportation & Logistics': {
            'percentage': 3.0,
            'target_count': 6,
            'us_count': 6,
            'canada_count': 0,
            'search_terms': [
                '"trucking company" owner OR founder',
                '"delivery service" entrepreneur OR founder',
                '"logistics company" founder OR owner',
                '"freight broker" business owner'
            ],
            'profile_keywords': ['Transportation', 'Logistics', 'Trucking', 'Delivery']
        },
        
        'Real Estate': {
            'percentage': 3.0,
            'target_count': 6,
            'us_count': 6,
            'canada_count': 0,
            'search_terms': [
                '"real estate agency" owner OR broker',
                '"property developer" OR "real estate investor"',
                '"property flipping" business OR entrepreneur',
                '"real estate" "own brokerage" OR firm'
            ],
            'profile_keywords': ['Real Estate', 'Broker', 'Property', 'Realtor']
        },
        
        'Agriculture': {
            'percentage': 2.5,
            'target_count': 5,
            'us_count': 5,
            'canada_count': 0,
            'search_terms': [
                '"farm owner" OR "farmer" entrepreneur',
                '"organic farm" founder OR owner',
                '"agricultural" business OR startup founder',
                '"urban farming" OR "vertical farm" entrepreneur'
            ],
            'profile_keywords': ['Agriculture', 'Farming', 'Farm', 'Agricultural']
        },
        
        'Entertainment & Media': {
            'percentage': 2.0,
            'target_count': 4,
            'us_count': 4,
            'canada_count': 0,
            'search_terms': [
                '"production company" founder OR owner',
                '"content creator" "own business" OR agency',
                '"event planning" business owner OR founder',
                '"entertainment" entrepreneur OR founder'
            ],
            'profile_keywords': ['Entertainment', 'Media', 'Production', 'Events']
        }
    }
    
    return industry_targets

def generate_linkedin_search_queries():
    """
    Generate specific LinkedIn search queries for each industry
    """
    
    industry_targets = create_200_founder_collection_plan()
    
    print("\n🔍 LINKEDIN SEARCH QUERIES BY INDUSTRY")
    print("=" * 70)
    
    all_queries = []
    
    for industry, data in industry_targets.items():
        print(f"\n📌 {industry} (Target: {data['target_count']} founders)")
        print(f"   US: {data['us_count']} | Canada: {data['canada_count']}")
        print("\n   Search Queries:")
        
        for i, query in enumerate(data['search_terms'], 1):
            # US version
            us_query = f'site:linkedin.com/in/ {query} location:"United States"'
            print(f"   {i}. US: {us_query}")
            
            # Canada version if needed
            if data['canada_count'] > 0:
                ca_query = f'site:linkedin.com/in/ {query} location:"Canada"'
                print(f"      CA: {ca_query}")
            
            all_queries.append({
                'industry': industry,
                'query': query,
                'us_query': us_query,
                'canada_query': ca_query if data['canada_count'] > 0 else None
            })
    
    return all_queries

def create_data_collection_template():
    """
    Create template matching the PSV file structure for data collection
    """
    
    print("\n📋 DATA COLLECTION TEMPLATE")
    print("=" * 70)
    print("Template for collecting founder data in PSV format")
    print()
    
    # Template structure matching linkedin_founders_reformatted.psv
    template = {
        # PROJECT GROUP (proj_*)
        'proj_name': '',  # e.g., "Joe's Pizza Restaurant"
        'proj_founder': '',  # e.g., "Joe Smith"
        'proj_category': '',  # Industry category
        'proj_location': '',  # City, State/Province
        'proj_launch_date': '',  # YYYY-MM-DD format
        'proj_end_date': '',  # YYYY-MM-DD or 'TBD'
        
        # FUNDING GROUP (fund_*)
        'fund_goal_usd': '',  # e.g., "$50000"
        'fund_raised_usd': '',  # e.g., "$75000" or 'TBD'
        'fund_success_rate': '',  # e.g., "150%" or 'TBD'
        'fund_status': '',  # 'Funded' or 'Not Funded'
        'fund_backer_count': '',  # Number or 'TBD'
        'funding_investment_history': '',  # Full funding history
        
        # COMPANY GROUP (co_*)
        'co_name': '',  # Company name
        'co_website_url': '',  # Company website
        'co_current_name': '',  # Current company name
        'co_current_title': '',  # Current job title
        'co_operational_status': '',  # 'Yes' or 'No'
        'co_business_status': '',  # Business status description
        'co_growth_metrics': '',  # Growth metrics
        'co_domain_status': '',  # Domain/website status
        
        # SOCIAL MEDIA GROUP (social_*)
        'social_linkedin_url': '',  # LinkedIn profile URL
        'social_other_platforms': '',  # Other social media
        'social_media_activity': '',  # Social media activity level
        
        # TEAM GROUP (team_*)
        'team_composition': '',  # Team members
        'team_founder_bio': '',  # Founder background
        
        # RESEARCH GROUP (research_*)
        'research_linkedin_query': '',  # Search query used
        'research_verification_sources': '',  # Verification sources
        'research_work_history': '',  # Previous work experience
        'research_education_summary': '',  # Education summary
        
        # MEDIA GROUP (media_*)
        'media_press_coverage': '',  # Press mentions
        'media_awards_recognition': '',  # Awards/recognition
        
        # STATUS GROUP (status_*)
        'status_legal_compliance': '',  # 'Yes' or 'No'
        'status_professional_reputation': '',  # Reputation status
        
        # LINKEDIN GROUP (li_*)
        'li_profile_verified': '',  # 'Yes' or 'No'
        'li_current_employer': '',  # From LinkedIn
        'li_current_title': '',  # From LinkedIn
        'li_work_experience': '',  # Career history
        'li_education_background': '',  # Education details
        'li_professional_skills': '',  # Skills list
        'li_recent_activity': '',  # Recent posts/activity
        
        # NOTES GROUP (notes_*)
        'notes_area_of_expertise': '',  # Pipe-separated expertise
        'notes_community_engagement': '',  # Pipe-separated engagement
        'notes_business_focus': ''  # Pipe-separated focus areas
    }
    
    return template

def generate_collection_progress_tracker():
    """
    Create a progress tracking system for the 200 founders collection
    """
    
    industry_targets = create_200_founder_collection_plan()
    
    print("\n📊 COLLECTION PROGRESS TRACKER")
    print("=" * 70)
    
    # Create progress tracking dataframe
    progress_data = []
    
    for industry, data in industry_targets.items():
        progress_data.append({
            'Industry': industry,
            'Target': data['target_count'],
            'US_Target': data['us_count'],
            'Canada_Target': data['canada_count'],
            'Collected': 0,
            'US_Collected': 0,
            'Canada_Collected': 0,
            'Percentage': 0.0,
            'Status': 'Not Started'
        })
    
    progress_df = pd.DataFrame(progress_data)
    
    # Calculate totals
    total_target = progress_df['Target'].sum()
    total_us_target = progress_df['US_Target'].sum()
    total_canada_target = progress_df['Canada_Target'].sum()
    
    print(f"TOTAL FOUNDERS TARGET: {total_target}")
    print(f"  • US: {total_us_target} ({total_us_target/total_target*100:.1f}%)")
    print(f"  • Canada: {total_canada_target} ({total_canada_target/total_target*100:.1f}%)")
    print()
    
    # Display initial progress table
    print("INITIAL PROGRESS BY INDUSTRY:")
    print("-" * 80)
    print(f"{'Industry':<30} {'Target':<8} {'US':<6} {'CA':<6} {'Status':<15}")
    print("-" * 80)
    
    for _, row in progress_df.iterrows():
        print(f"{row['Industry']:<30} {row['Target']:<8} {row['US_Target']:<6} {row['Canada_Target']:<6} {row['Status']:<15}")
    
    # Save progress tracker
    progress_df.to_csv('linkedin_200_founders_progress.csv', index=False)
    
    return progress_df

def create_example_entries():
    """
    Create example entries to demonstrate the data format
    """
    
    print("\n📝 EXAMPLE DATA ENTRIES")
    print("=" * 70)
    
    # Example for Food & Restaurant
    food_example = {
        'proj_name': 'Mama Rosa Italian Kitchen',
        'proj_founder': 'Maria Rossi',
        'proj_category': 'Food & Restaurant',
        'proj_location': 'Brooklyn, NY',
        'proj_launch_date': '2022-03-15',
        'proj_end_date': '2022-04-30',
        'fund_goal_usd': '$45000',
        'fund_raised_usd': '$52000',
        'fund_success_rate': '116%',
        'fund_status': 'Funded',
        'fund_backer_count': '285',
        'funding_investment_history': '$52K Kickstarter, $100K private investment 2023',
        'co_name': 'Mama Rosa LLC',
        'co_website_url': 'https://mamarosa-brooklyn.com',
        'co_current_name': 'Mama Rosa LLC',
        'co_current_title': 'Owner & Head Chef',
        'co_operational_status': 'Yes',
        'co_business_status': 'Active - Brooklyn location thriving',
        'co_growth_metrics': '200+ daily customers, 4.8 Yelp rating',
        'co_domain_status': 'Active website with online ordering',
        'social_linkedin_url': 'https://linkedin.com/in/maria-rossi-chef',
        'social_other_platforms': 'Instagram: @mamarosabrooklyn',
        'social_media_activity': 'Daily Instagram posts, weekly LinkedIn updates',
        'team_composition': 'Maria Rossi (Owner/Chef), Tony Rossi (Co-owner)',
        'team_founder_bio': '20 years culinary experience, Italian heritage, CIA graduate',
        'research_linkedin_query': '"restaurant owner" Brooklyn "Italian restaurant"',
        'research_verification_sources': 'LinkedIn profile, Yelp listing, NYC business registry',
        'research_work_history': 'Head Chef at Rao\'s, Sous Chef at Carbone',
        'research_education_summary': 'Culinary Institute of America, Italian cooking certifications',
        'media_press_coverage': 'Brooklyn Paper feature, Eater NY mention',
        'media_awards_recognition': 'Best New Restaurant Brooklyn 2023',
        'status_legal_compliance': 'Yes',
        'status_professional_reputation': 'Excellent - community favorite',
        'li_profile_verified': 'Yes',
        'li_current_employer': 'Mama Rosa LLC',
        'li_current_title': 'Owner & Head Chef',
        'li_work_experience': '2022-Present: Owner Mama Rosa | 2018-2022: Head Chef Rao\'s | 2015-2018: Sous Chef Carbone',
        'li_education_background': 'Culinary Institute of America (2010-2012) | Italian Culinary Institute (2013)',
        'li_professional_skills': 'Italian Cuisine | Restaurant Management | Menu Development | Team Leadership | Food Safety',
        'li_recent_activity': 'Posted about new seasonal menu | Shared community event | Restaurant industry insights',
        'notes_area_of_expertise': 'Italian_Cuisine|Restaurant_Operations|Culinary_Arts',
        'notes_community_engagement': 'Local_Business_Association|Brooklyn_Restaurant_Week|Community_Events',
        'notes_business_focus': 'Authentic_Italian_Food|Local_Sourcing|Community_Restaurant'
    }
    
    print("Example 1: Food & Restaurant Founder")
    print("-" * 50)
    for key, value in list(food_example.items())[:10]:  # Show first 10 fields
        print(f"{key}: {value}")
    print("... (33 more fields)")
    
    return food_example

if __name__ == "__main__":
    # Execute collection strategy
    print("🚀 INITIATING 200 FOUNDERS COLLECTION STRATEGY")
    print("=" * 70)
    
    # 1. Create collection plan
    industry_targets = create_200_founder_collection_plan()
    
    # 2. Generate search queries
    queries = generate_linkedin_search_queries()
    
    # 3. Create data template
    template = create_data_collection_template()
    
    # 4. Set up progress tracker
    progress_tracker = generate_collection_progress_tracker()
    
    # 5. Create example entries
    example = create_example_entries()
    
    print("\n✅ COLLECTION STRATEGY COMPLETE!")
    print("\n📌 NEXT STEPS:")
    print("1. Use the LinkedIn search queries to find founders")
    print("2. Fill in the data template for each founder")
    print("3. Update progress tracker as you collect data")
    print("4. Aim for proportional representation across industries")
    print("5. Maintain 90% US / 10% Canada geographic split")
    
    print("\n🎯 TARGET: 200 founders representing all business sectors")
    print("   Not just tech - the full entrepreneurial landscape!")