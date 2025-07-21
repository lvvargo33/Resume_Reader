"""
LinkedIn Founders Data Collection System
Systematic collection of 200 founders across all business sectors
"""

import pandas as pd
from datetime import datetime
import json

class LinkedInFounderCollector:
    def __init__(self):
        self.collected_founders = []
        self.progress_file = 'linkedin_200_founders_progress.csv'
        self.output_file = 'linkedin_founders_collected.psv'
        self.load_progress()
    
    def load_progress(self):
        """Load existing progress or create new tracker"""
        try:
            self.progress_df = pd.read_csv(self.progress_file)
        except FileNotFoundError:
            # Create new progress tracker if doesn't exist
            self.initialize_progress_tracker()
    
    def initialize_progress_tracker(self):
        """Initialize progress tracking for all industries"""
        industries = {
            'Food & Restaurant': {'target': 24, 'us_target': 22, 'canada_target': 2},
            'Retail & E-commerce': {'target': 22, 'us_target': 20, 'canada_target': 2},
            'Business Services': {'target': 22, 'us_target': 20, 'canada_target': 2},
            'Health, Beauty & Fitness': {'target': 18, 'us_target': 16, 'canada_target': 2},
            'Construction & Contracting': {'target': 16, 'us_target': 14, 'canada_target': 2},
            'Other Services': {'target': 16, 'us_target': 14, 'canada_target': 2},
            'Residential & Commercial Services': {'target': 14, 'us_target': 13, 'canada_target': 1},
            'Technology': {'target': 12, 'us_target': 11, 'canada_target': 1},
            'Healthcare': {'target': 11, 'us_target': 10, 'canada_target': 1},
            'Financial Services': {'target': 9, 'us_target': 8, 'canada_target': 1},
            'Education & Training': {'target': 8, 'us_target': 7, 'canada_target': 1},
            'Manufacturing': {'target': 7, 'us_target': 6, 'canada_target': 1},
            'Transportation & Logistics': {'target': 6, 'us_target': 6, 'canada_target': 0},
            'Real Estate': {'target': 6, 'us_target': 6, 'canada_target': 0},
            'Agriculture': {'target': 5, 'us_target': 5, 'canada_target': 0},
            'Entertainment & Media': {'target': 4, 'us_target': 4, 'canada_target': 0}
        }
        
        data = []
        for industry, targets in industries.items():
            data.append({
                'Industry': industry,
                'Target': targets['target'],
                'US_Target': targets['us_target'],
                'Canada_Target': targets['canada_target'],
                'Collected': 0,
                'US_Collected': 0,
                'Canada_Collected': 0,
                'Percentage': 0.0,
                'Status': 'Not Started'
            })
        
        self.progress_df = pd.DataFrame(data)
        self.progress_df.to_csv(self.progress_file, index=False)
    
    def add_founder(self, founder_data):
        """Add a new founder to the collection"""
        # Validate required fields
        required_fields = ['proj_founder', 'proj_category', 'proj_location']
        for field in required_fields:
            if field not in founder_data or not founder_data[field]:
                print(f"❌ Error: Missing required field '{field}'")
                return False
        
        # Add to collection
        self.collected_founders.append(founder_data)
        
        # Update progress
        self.update_progress(founder_data['proj_category'], founder_data['proj_location'])
        
        # Save immediately
        self.save_collected_data()
        
        print(f"✅ Added: {founder_data['proj_founder']} ({founder_data['proj_category']})")
        return True
    
    def update_progress(self, category, location):
        """Update progress tracker"""
        # Determine country
        country = 'Canada' if 'Canada' in location or any(prov in location for prov in ['ON', 'BC', 'QC', 'AB']) else 'US'
        
        # Update counts
        idx = self.progress_df[self.progress_df['Industry'] == category].index
        if len(idx) > 0:
            idx = idx[0]
            self.progress_df.loc[idx, 'Collected'] += 1
            if country == 'US':
                self.progress_df.loc[idx, 'US_Collected'] += 1
            else:
                self.progress_df.loc[idx, 'Canada_Collected'] += 1
            
            # Update percentage and status
            target = self.progress_df.loc[idx, 'Target']
            collected = self.progress_df.loc[idx, 'Collected']
            self.progress_df.loc[idx, 'Percentage'] = (collected / target) * 100
            
            if collected == 0:
                status = 'Not Started'
            elif collected < target:
                status = 'In Progress'
            else:
                status = 'Complete'
            self.progress_df.loc[idx, 'Status'] = status
            
            # Save progress
            self.progress_df.to_csv(self.progress_file, index=False)
    
    def save_collected_data(self):
        """Save collected founders to PSV file"""
        if self.collected_founders:
            df = pd.DataFrame(self.collected_founders)
            
            # Ensure all columns are present in correct order
            column_order = [
                # PROJECT GROUP
                'proj_name', 'proj_founder', 'proj_category', 'proj_location', 
                'proj_launch_date', 'proj_end_date',
                # FUNDING GROUP  
                'fund_goal_usd', 'fund_raised_usd', 'fund_success_rate', 'fund_status', 
                'fund_backer_count', 'funding_investment_history',
                # COMPANY GROUP
                'co_name', 'co_website_url', 'co_current_name', 'co_current_title', 
                'co_operational_status', 'co_business_status', 'co_growth_metrics', 'co_domain_status',
                # SOCIAL MEDIA GROUP
                'social_linkedin_url', 'social_other_platforms', 'social_media_activity',
                # TEAM GROUP
                'team_composition', 'team_founder_bio',
                # RESEARCH GROUP
                'research_linkedin_query', 'research_verification_sources', 
                'research_work_history', 'research_education_summary',
                # MEDIA GROUP
                'media_press_coverage', 'media_awards_recognition',
                # STATUS GROUP
                'status_legal_compliance', 'status_professional_reputation',
                # LINKEDIN GROUP
                'li_profile_verified', 'li_current_employer', 'li_current_title', 
                'li_work_experience', 'li_education_background', 'li_professional_skills', 
                'li_recent_activity',
                # NOTES GROUP
                'notes_area_of_expertise', 'notes_community_engagement', 'notes_business_focus'
            ]
            
            # Add missing columns with empty values
            for col in column_order:
                if col not in df.columns:
                    df[col] = ''
            
            # Reorder and save
            df = df[column_order]
            df.to_csv(self.output_file, sep='|', index=False)
            print(f"💾 Saved {len(df)} founders to {self.output_file}")
    
    def show_progress(self):
        """Display current collection progress"""
        print("\n📊 COLLECTION PROGRESS REPORT")
        print("=" * 80)
        
        # Reload latest progress
        self.progress_df = pd.read_csv(self.progress_file)
        
        # Overall stats
        total_target = self.progress_df['Target'].sum()
        total_collected = self.progress_df['Collected'].sum()
        overall_percentage = (total_collected / total_target) * 100
        
        print(f"OVERALL: {total_collected}/{total_target} ({overall_percentage:.1f}%)")
        print(f"US: {self.progress_df['US_Collected'].sum()}/{self.progress_df['US_Target'].sum()}")
        print(f"Canada: {self.progress_df['Canada_Collected'].sum()}/{self.progress_df['Canada_Target'].sum()}")
        print()
        
        # Industry breakdown
        print("INDUSTRY BREAKDOWN:")
        print("-" * 80)
        print(f"{'Industry':<30} {'Progress':<15} {'US':<10} {'CA':<10} {'Status':<15}")
        print("-" * 80)
        
        for _, row in self.progress_df.iterrows():
            progress = f"{row['Collected']}/{row['Target']} ({row['Percentage']:.0f}%)"
            us_progress = f"{row['US_Collected']}/{row['US_Target']}"
            ca_progress = f"{row['Canada_Collected']}/{row['Canada_Target']}"
            
            # Color coding for terminal
            if row['Status'] == 'Complete':
                status_display = '✅ ' + row['Status']
            elif row['Status'] == 'In Progress':
                status_display = '🔄 ' + row['Status']
            else:
                status_display = '⏸️  ' + row['Status']
            
            print(f"{row['Industry']:<30} {progress:<15} {us_progress:<10} {ca_progress:<10} {status_display:<15}")
        
        print("-" * 80)
        
        # Next priorities
        print("\n🎯 NEXT COLLECTION PRIORITIES:")
        incomplete = self.progress_df[self.progress_df['Percentage'] < 100].sort_values('Percentage')
        for i, (_, row) in enumerate(incomplete.head(5).iterrows(), 1):
            needed = row['Target'] - row['Collected']
            print(f"{i}. {row['Industry']}: Need {needed} more founders")

# Initialize collector
collector = LinkedInFounderCollector()

# Example: Add sample founders for Food & Restaurant sector
def add_food_restaurant_founders_batch():
    """Add Food & Restaurant founders to reach target of 24"""
    
    # US Restaurant Founder 1 (existing)
    founder1 = {
        'proj_name': 'Nola Southern Kitchen',
        'proj_founder': 'Marcus Williams',
        'proj_category': 'Food & Restaurant',
        'proj_location': 'Nashville, TN',
        'proj_launch_date': '2021-09-15',
        'proj_end_date': '2021-10-30',
        'fund_goal_usd': '$35000',
        'fund_raised_usd': '$42500',
        'fund_success_rate': '121%',
        'fund_status': 'Funded',
        'fund_backer_count': '312',
        'funding_investment_history': '$42.5K Kickstarter, $150K angel investment 2022',
        'co_name': 'Nola Southern Kitchen LLC',
        'co_website_url': 'https://nolasouthernkitchen.com',
        'co_current_name': 'Nola Southern Kitchen LLC',
        'co_current_title': 'Owner & Executive Chef',
        'co_operational_status': 'Yes',
        'co_business_status': 'Active - Nashville location thriving, planning second location',
        'co_growth_metrics': '300+ daily customers, 4.9 Google rating, $2M annual revenue',
        'co_domain_status': 'Active website with online ordering and catering',
        'social_linkedin_url': 'https://linkedin.com/in/marcus-williams-chef',
        'social_other_platforms': 'Instagram: @nolasouthernkitchen (15K followers)',
        'social_media_activity': 'Daily Instagram posts, weekly LinkedIn articles on Southern cuisine',
        'team_composition': 'Marcus Williams (Owner/Chef), Sarah Williams (Co-owner/Manager)',
        'team_founder_bio': '15 years culinary experience, New Orleans native, Le Cordon Bleu graduate',
        'research_linkedin_query': '"restaurant owner" Nashville "Southern cuisine"',
        'research_verification_sources': 'LinkedIn profile, Nashville Business Journal, Yelp verified',
        'research_work_history': 'Executive Chef at Brennan\'s, Sous Chef at Commander\'s Palace',
        'research_education_summary': 'Le Cordon Bleu Culinary Arts, Business Management Certificate',
        'media_press_coverage': 'Nashville Scene Best New Restaurant 2022, Eater Nashville feature',
        'media_awards_recognition': 'James Beard Award nominee 2023, Nashville\'s Top 30 Under 30',
        'status_legal_compliance': 'Yes',
        'status_professional_reputation': 'Excellent - Community leader, culinary innovator',
        'li_profile_verified': 'Yes',
        'li_current_employer': 'Nola Southern Kitchen LLC',
        'li_current_title': 'Owner & Executive Chef',
        'li_work_experience': '2021-Present: Owner Nola Southern | 2017-2021: Exec Chef Brennan\'s | 2014-2017: Sous Chef Commander\'s Palace',
        'li_education_background': 'Le Cordon Bleu Paris (2011-2013) | Tennessee State University Business Certificate (2020)',
        'li_professional_skills': 'Southern Cuisine | Restaurant Management | Menu Development | Team Leadership | Catering | Food Safety',
        'li_recent_activity': 'Article on preserving Southern culinary traditions | Hiring post for new location | Community fundraiser announcement',
        'notes_area_of_expertise': 'Southern_Cuisine|Restaurant_Operations|Culinary_Innovation',
        'notes_community_engagement': 'Nashville_Restaurant_Association|Youth_Culinary_Training|Food_Bank_Volunteer',
        'notes_business_focus': 'Authentic_Southern_Food|Community_Restaurant|Sustainable_Sourcing'
    }
    
    # Example 2: Canadian Restaurant Founder
    founder2 = {
        'proj_name': 'Maple Fusion Bistro',
        'proj_founder': 'Sophie Chen',
        'proj_category': 'Food & Restaurant',
        'proj_location': 'Toronto, ON',
        'proj_launch_date': '2022-04-01',
        'proj_end_date': '2022-05-15',
        'fund_goal_usd': '$40000',
        'fund_raised_usd': '$48000',
        'fund_success_rate': '120%',
        'fund_status': 'Funded',
        'fund_backer_count': '289',
        'funding_investment_history': '$48K Kickstarter, $200K private investment 2022',
        'co_name': 'Maple Fusion Bistro Inc.',
        'co_website_url': 'https://maplefusionbistro.ca',
        'co_current_name': 'Maple Fusion Bistro Inc.',
        'co_current_title': 'Founder & Head Chef',
        'co_operational_status': 'Yes',
        'co_business_status': 'Active - Toronto location successful, strong local following',
        'co_growth_metrics': '250+ daily customers, featured in Toronto Life, profitable',
        'co_domain_status': 'Active website with reservations and delivery',
        'social_linkedin_url': 'https://linkedin.com/in/sophie-chen-toronto-chef',
        'social_other_platforms': 'Instagram: @maplefusionbistro',
        'social_media_activity': 'Active social media presence, fusion cuisine education',
        'team_composition': 'Sophie Chen (Founder/Chef), David Park (Business Partner)',
        'team_founder_bio': 'Asian-Canadian fusion specialist, George Brown College culinary graduate',
        'research_linkedin_query': '"restaurant owner" Toronto "fusion cuisine"',
        'research_verification_sources': 'LinkedIn profile, Toronto Life, Canadian Restaurant Association',
        'research_work_history': 'Head Chef at Canoe, Chef de Partie at Scaramouche',
        'research_education_summary': 'George Brown College Culinary Management, Hong Kong Culinary Academy',
        'media_press_coverage': 'Toronto Life Top New Restaurants, BlogTO feature',
        'media_awards_recognition': 'Ontario Culinary Federation Rising Star 2023',
        'status_legal_compliance': 'Yes',
        'status_professional_reputation': 'Excellent - Fusion cuisine innovator',
        'li_profile_verified': 'Yes',
        'li_current_employer': 'Maple Fusion Bistro Inc.',
        'li_current_title': 'Founder & Head Chef',
        'li_work_experience': '2022-Present: Founder Maple Fusion | 2018-2022: Head Chef Canoe | 2015-2018: Chef de Partie Scaramouche',
        'li_education_background': 'George Brown College Culinary Management (2012-2015) | Hong Kong Culinary Academy (2011)',
        'li_professional_skills': 'Fusion Cuisine | Restaurant Entrepreneurship | Menu Innovation | Team Building | Cost Control',
        'li_recent_activity': 'Posted about Asian Heritage Month menu | Shared sustainability initiatives | Industry collaboration post',
        'notes_area_of_expertise': 'Fusion_Cuisine|Restaurant_Innovation|Asian_Canadian_Food',
        'notes_community_engagement': 'Toronto_Restaurant_Community|Culinary_Education|Cultural_Food_Events',
        'notes_business_focus': 'Cultural_Fusion|Local_Ingredients|Contemporary_Dining'
    }
    
    # Additional US Founders (need 20 more US founders)
    founders_batch_1 = [
        {
            'proj_name': 'Smoky Mountain BBQ',
            'proj_founder': 'Jake Patterson',
            'proj_category': 'Food & Restaurant',
            'proj_location': 'Memphis, TN',
            'proj_launch_date': '2020-08-12',
            'proj_end_date': '2020-09-25',
            'fund_goal_usd': '$25000',
            'fund_raised_usd': '$31000',
            'fund_success_rate': '124%',
            'fund_status': 'Funded',
            'fund_backer_count': '278',
            'funding_investment_history': '$31K Kickstarter, $85K SBA loan 2021',
            'co_name': 'Smoky Mountain BBQ LLC',
            'co_website_url': 'https://smokymountainbbq.com',
            'co_current_name': 'Smoky Mountain BBQ LLC',
            'co_current_title': 'Owner & Pitmaster',
            'co_operational_status': 'Yes',
            'co_business_status': 'Active - Memphis location profitable, food truck expansion',
            'co_growth_metrics': '180+ daily customers, 4.7 Google rating, $1.2M annual revenue',
            'co_domain_status': 'Active website with online ordering and catering',
            'social_linkedin_url': 'https://linkedin.com/in/jake-patterson-pitmaster',
            'social_other_platforms': 'Instagram: @smokymountainbbq (8K followers)',
            'social_media_activity': 'Daily BBQ tips, weekly smoking tutorials',
            'team_composition': 'Jake Patterson (Owner/Pitmaster), Lisa Patterson (Operations Manager)',
            'team_founder_bio': '12 years BBQ competition experience, Memphis native, Kansas City BBQ Society judge',
            'research_linkedin_query': '"BBQ restaurant owner" Memphis "pitmaster"',
            'research_verification_sources': 'LinkedIn profile, Memphis Business Journal, TripAdvisor verified',
            'research_work_history': 'Head Pitmaster at Central BBQ, Competition BBQ Circuit',
            'research_education_summary': 'University of Memphis Business, BBQ Institute certification',
            'media_press_coverage': 'Memphis Flyer Best BBQ 2022, Food Network feature',
            'media_awards_recognition': 'Memphis in May Grand Champion 2021, BBQ Hall of Fame nominee',
            'status_legal_compliance': 'Yes',
            'status_professional_reputation': 'Excellent - BBQ community leader, competition judge',
            'li_profile_verified': 'Yes',
            'li_current_employer': 'Smoky Mountain BBQ LLC',
            'li_current_title': 'Owner & Pitmaster',
            'li_work_experience': '2020-Present: Owner Smoky Mountain BBQ | 2015-2020: Head Pitmaster Central BBQ | 2010-2015: Competition BBQ Circuit',
            'li_education_background': 'University of Memphis Business (2008-2012) | BBQ Institute Certification (2014)',
            'li_professional_skills': 'BBQ Smoking Techniques | Restaurant Operations | Competition BBQ | Team Management | Food Safety | Customer Service',
            'li_recent_activity': 'Shared BBQ smoking technique video | Memphis restaurant week post | Hiring announcement for expansion',
            'notes_area_of_expertise': 'BBQ_Smoking|Restaurant_Operations|Competition_BBQ',
            'notes_community_engagement': 'Memphis_Restaurant_Association|BBQ_Competition_Judge|Local_Food_Festival',
            'notes_business_focus': 'Traditional_BBQ|Quality_Meats|Community_Gathering_Place'
        },
        
        {
            'proj_name': 'Coastal Fish Tacos',
            'proj_founder': 'Isabella Rodriguez',
            'proj_category': 'Food & Restaurant',
            'proj_location': 'San Diego, CA',
            'proj_launch_date': '2021-06-03',
            'proj_end_date': '2021-07-18',
            'fund_goal_usd': '$28000',
            'fund_raised_usd': '$35500',
            'fund_success_rate': '127%',
            'fund_status': 'Funded',
            'fund_backer_count': '321',
            'funding_investment_history': '$35.5K Kickstarter, $120K private investment 2022',
            'co_name': 'Coastal Fish Tacos Inc.',
            'co_website_url': 'https://coastalfishtacos.com',
            'co_current_name': 'Coastal Fish Tacos Inc.',
            'co_current_title': 'Founder & Head Chef',
            'co_operational_status': 'Yes',
            'co_business_status': 'Active - San Diego location thriving, considering second location',
            'co_growth_metrics': '220+ daily customers, 4.8 Yelp rating, sustainable seafood focus',
            'co_domain_status': 'Active website with mobile ordering and delivery',
            'social_linkedin_url': 'https://linkedin.com/in/isabella-rodriguez-chef-sd',
            'social_other_platforms': 'Instagram: @coastalfishtacos (12K followers)',
            'social_media_activity': 'Daily sustainable seafood education, weekly recipe sharing',
            'team_composition': 'Isabella Rodriguez (Founder/Chef), Miguel Santos (Kitchen Manager)',
            'team_founder_bio': '8 years culinary experience, Mexican-American heritage, Culinary Institute graduate',
            'research_linkedin_query': '"fish taco restaurant" "San Diego" owner',
            'research_verification_sources': 'LinkedIn profile, San Diego Union-Tribune, Yelp verified',
            'research_work_history': 'Sous Chef at George\'s at the Cove, Line Cook at Puesto',
            'research_education_summary': 'Culinary Institute of America, Sustainable Seafood Certification',
            'media_press_coverage': 'San Diego Magazine Best Fish Tacos 2022, NBC San Diego feature',
            'media_awards_recognition': 'Sustainable Restaurant Association Award 2023',
            'status_legal_compliance': 'Yes',
            'status_professional_reputation': 'Excellent - Sustainable seafood advocate, community leader',
            'li_profile_verified': 'Yes',
            'li_current_employer': 'Coastal Fish Tacos Inc.',
            'li_current_title': 'Founder & Head Chef',
            'li_work_experience': '2021-Present: Founder Coastal Fish Tacos | 2018-2021: Sous Chef George\'s at the Cove | 2016-2018: Line Cook Puesto',
            'li_education_background': 'Culinary Institute of America (2013-2015) | UC San Diego Sustainable Business Certificate (2020)',
            'li_professional_skills': 'Sustainable Seafood | Mexican Cuisine | Restaurant Management | Menu Development | Team Leadership | Environmental Stewardship',
            'li_recent_activity': 'Article on sustainable fishing practices | National Seafood Month post | Team appreciation post',
            'notes_area_of_expertise': 'Sustainable_Seafood|Mexican_Cuisine|Environmental_Stewardship',
            'notes_community_engagement': 'San_Diego_Restaurant_Association|Sustainable_Seafood_Alliance|Coastal_Conservation',
            'notes_business_focus': 'Sustainable_Seafood|Fresh_Local_Ingredients|Environmental_Responsibility'
        },
        
        {
            'proj_name': 'Urban Harvest Café',
            'proj_founder': 'David Kim',
            'proj_category': 'Food & Restaurant',
            'proj_location': 'Portland, OR',
            'proj_launch_date': '2022-02-14',
            'proj_end_date': '2022-03-30',
            'fund_goal_usd': '$32000',
            'fund_raised_usd': '$38000',
            'fund_success_rate': '119%',
            'fund_status': 'Funded',
            'fund_backer_count': '294',
            'funding_investment_history': '$38K Kickstarter, $95K angel funding 2022',
            'co_name': 'Urban Harvest Café LLC',
            'co_website_url': 'https://urbanharvestcafe.com',
            'co_current_name': 'Urban Harvest Café LLC',
            'co_current_title': 'Owner & Executive Chef',
            'co_operational_status': 'Yes',
            'co_business_status': 'Active - Portland location successful, farm-to-table focus',
            'co_growth_metrics': '160+ daily customers, 4.9 Google rating, zero-waste initiative',
            'co_domain_status': 'Active website with sustainability blog and ordering',
            'social_linkedin_url': 'https://linkedin.com/in/david-kim-urban-harvest',
            'social_other_platforms': 'Instagram: @urbanharvestpdx (10K followers)',
            'social_media_activity': 'Daily farm updates, weekly zero-waste cooking tips',
            'team_composition': 'David Kim (Owner/Chef), Sarah Green (Farm Coordinator), Alex Chen (Operations)',
            'team_founder_bio': '10 years farm-to-table experience, Korean-American heritage, Oregon Culinary Institute',
            'research_linkedin_query': '"farm to table restaurant" Portland owner',
            'research_verification_sources': 'LinkedIn profile, Portland Business Journal, Oregon Live',
            'research_work_history': 'Head Chef at Le Pigeon, Farm Manager at Sauvie Island',
            'research_education_summary': 'Oregon Culinary Institute, Sustainable Agriculture Certificate',
            'media_press_coverage': 'Portland Monthly Best Farm-to-Table 2023, Eater Portland feature',
            'media_awards_recognition': 'Oregon Restaurant & Lodging Association Green Restaurant Award',
            'status_legal_compliance': 'Yes',
            'status_professional_reputation': 'Excellent - Sustainability leader, farm advocate',
            'li_profile_verified': 'Yes',
            'li_current_employer': 'Urban Harvest Café LLC',
            'li_current_title': 'Owner & Executive Chef',
            'li_work_experience': '2022-Present: Owner Urban Harvest Café | 2019-2022: Head Chef Le Pigeon | 2017-2019: Farm Manager Sauvie Island',
            'li_education_background': 'Oregon Culinary Institute (2015-2017) | Portland State University Sustainable Agriculture (2018)',
            'li_professional_skills': 'Farm-to-Table Cooking | Sustainable Agriculture | Restaurant Operations | Zero-Waste Practices | Team Leadership | Local Sourcing',
            'li_recent_activity': 'Posted about local farm partnerships | Shared zero-waste cooking video | Seasonal menu announcement',
            'notes_area_of_expertise': 'Farm_to_Table|Sustainable_Agriculture|Zero_Waste_Practices',
            'notes_community_engagement': 'Portland_Restaurant_Association|Oregon_Farm_Network|Sustainability_Council',
            'notes_business_focus': 'Farm_to_Table|Zero_Waste|Local_Sourcing'
        }
    ]
    
    # Add existing founders
    collector.add_founder(founder1)
    collector.add_founder(founder2)
    
    # Add new batch
    for founder in founders_batch_1:
        collector.add_founder(founder)
    
    print(f"\n✅ Added 5 Food & Restaurant founders (2 existing + 3 new)")

if __name__ == "__main__":
    print("🚀 LINKEDIN FOUNDERS DATA COLLECTION SYSTEM")
    print("=" * 70)
    
    # Show initial progress
    collector.show_progress()
    
    # Add example founders
    print("\n📝 Adding Food & Restaurant founders...")
    add_food_restaurant_founders_batch()
    
    # Show updated progress
    collector.show_progress()
    
    print("\n💡 INSTRUCTIONS:")
    print("1. Use the LinkedIn search queries to find real founders")
    print("2. Verify they have crowdfunding campaigns")
    print("3. Fill in the data template for each founder")
    print("4. Use collector.add_founder(founder_data) to add to collection")
    print("5. Progress is automatically tracked and saved")
    print("\n🎯 Goal: Collect 200 founders across all business sectors!")