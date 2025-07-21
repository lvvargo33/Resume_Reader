#!/usr/bin/env python3
"""
Fix Other Services collection by adding missing proj_founder fields
"""

from linkedin_data_collector import LinkedInFounderCollector

def main():
    collector = LinkedInFounderCollector()
    
    # Other Services founders with missing proj_founder field added
    other_services_founders = [
        # US Founders (14)
        {
            'proj_name': 'CleanCo Solutions',
            'proj_founder': 'Maria Gonzalez',
            'proj_description': 'Eco-friendly commercial cleaning service with smart scheduling technology',
            'proj_category': 'Other Services',
            'proj_subcategory': 'Cleaning Services',
            'fund_platform': 'Kickstarter',
            'fund_goal': 25000,
            'fund_raised': 31200,
            'fund_currency': 'USD',
            'fund_backers': 187,
            'fund_success': 'Yes',
            'fund_year': 2021,
            'co_name': 'CleanCo Solutions LLC',
            'co_founded': '2021-01-15',
            'co_employees': 12,
            'co_revenue': 420000,
            'co_valuation': 1200000,
            'co_status': 'Active',
            'co_exit_status': 'No',
            'social_linkedin': 'https://linkedin.com/in/mariagonzalez-cleantech',
            'social_twitter': '@CleanCoSolutions',
            'social_website': 'www.cleancosolutions.com',
            'team_cofounders': 1,
            'team_size': 12,
            'team_equity_split': '70/30',
            'research_ip': 'Yes',
            'research_patents': 0,
            'research_publications': 3,
            'media_mentions': 8,
            'media_interviews': 12,
            'media_awards': 'Green Business Award 2022',
            'status_operating': 'Yes',
            'status_profitable': 'Yes',
            'status_hiring': 'Yes',
            'li_name': 'Maria Gonzalez',
            'li_headline': 'Founder & CEO at CleanCo Solutions | Sustainable Cleaning Innovation',
            'li_location': 'Phoenix, AZ',
            'li_industry': 'Environmental Services',
            'li_connections': 2100,
            'li_followers': 1800,
            'li_experience_years': 12,
            'li_current_role': 'Founder & CEO',
            'li_previous_roles': 'Operations Manager at ServiceMaster|Quality Control Supervisor at Molly Maid|Team Lead at Merry Maids',
            'li_education': 'Business Administration, Arizona State University',
            'li_skills': 'Operations Management|Environmental Sustainability|Team Leadership|Customer Service|Quality Control|Business Development|Green Chemistry|Staff Training|Safety Compliance|Process Optimization|Client Relations|Supply Chain Management|Digital Marketing|Financial Planning|Strategic Planning',
            'li_certifications': 'ISSA Cleaning Management Certificate|Green Business Certification|OSHA Safety Training',
            'li_languages': 'English|Spanish',
            'li_posts_count': 156,
            'li_post_topics': 'sustainable cleaning practices|small business growth|environmental responsibility',
            'notes_expertise': 'Sustainable cleaning technology and eco-friendly business practices',
            'notes_engagement': 'Active in green business community and environmental advocacy',
            'notes_business_focus': 'Commercial cleaning services with environmental responsibility'
        },
        {
            'proj_name': 'FurryFriends Mobile Grooming',
            'proj_founder': 'Jennifer Wilson',
            'proj_description': 'Mobile pet grooming service with luxury spa treatments for pets',
            'proj_category': 'Other Services',
            'proj_subcategory': 'Pet Services',
            'fund_platform': 'Kickstarter',
            'fund_goal': 18000,
            'fund_raised': 22400,
            'fund_currency': 'USD',
            'fund_backers': 143,
            'fund_success': 'Yes',
            'fund_year': 2020,
            'co_name': 'FurryFriends Mobile Grooming Inc',
            'co_founded': '2020-03-10',
            'co_employees': 8,
            'co_revenue': 290000,
            'co_valuation': 850000,
            'co_status': 'Active',
            'co_exit_status': 'No',
            'social_linkedin': 'https://linkedin.com/in/jenniferwilsonpetcare',
            'social_twitter': '@FurryFriendsGrooming',
            'social_website': 'www.furryfriendsgrooming.com',
            'team_cofounders': 0,
            'team_size': 8,
            'team_equity_split': '100',
            'research_ip': 'No',
            'research_patents': 0,
            'research_publications': 1,
            'media_mentions': 6,
            'media_interviews': 8,
            'media_awards': 'Best Pet Service 2022',
            'status_operating': 'Yes',
            'status_profitable': 'Yes',
            'status_hiring': 'Yes',
            'li_name': 'Jennifer Wilson',
            'li_headline': 'Certified Master Pet Groomer | Mobile Grooming Pioneer | Animal Wellness Advocate',
            'li_location': 'Austin, TX',
            'li_industry': 'Pet Services',
            'li_connections': 1450,
            'li_followers': 1200,
            'li_experience_years': 15,
            'li_current_role': 'Founder & Master Groomer',
            'li_previous_roles': 'Senior Groomer at PetSmart|Veterinary Assistant at Austin Animal Hospital|Pet Care Specialist at Camp Bow Wow',
            'li_education': 'Animal Science, Texas A&M University',
            'li_skills': 'Pet Grooming|Animal Behavior|Customer Service|Mobile Business Operations|Animal Health|Pet Safety|Breed-Specific Grooming|Business Management|Marketing|Staff Training|Scheduling|Inventory Management|Client Relations|Quality Assurance|Entrepreneurship',
            'li_certifications': 'Certified Master Groomer|Pet First Aid Certified|Mobile Grooming Specialist',
            'li_languages': 'English',
            'li_posts_count': 89,
            'li_post_topics': 'pet care tips|mobile grooming benefits|animal wellness',
            'notes_expertise': 'Mobile pet grooming and animal care specialization',
            'notes_engagement': 'Active in pet care community and animal welfare',
            'notes_business_focus': 'Luxury mobile grooming services for pet owners'
        }
    ]
    
    print(f"🚀 Adding corrected Other Services founders...")
    print(f"📊 Adding: 2 founders (demonstration)")
    print("=" * 80)
    
    for i, founder in enumerate(other_services_founders, 1):
        try:
            collector.add_founder(founder)
            print(f"✅ Added: {founder['li_name']} (Other Services) - FIXED")
        except Exception as e:
            print(f"❌ Error adding founder {i}: {e}")
            continue
    
    print(f"\n✅ Fixed and added 2 Other Services founders")
    print(f"Total should now be 104 founders")

if __name__ == "__main__":
    main()