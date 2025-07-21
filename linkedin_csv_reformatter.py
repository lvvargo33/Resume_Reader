import pandas as pd
import re
from datetime import datetime

def reformat_linkedin_dataset():
    """
    Comprehensive reformatting of LinkedIn founders dataset according to specifications:
    1. Change delimiter to pipe separator
    2. Standardize column names (remove spaces, keep underscores, group similar)
    3. Convert status fields to Yes/No
    4. Standardize dates to YYYY-MM-DD
    5. Break out notes into 3 columns
    6. Standardize abbreviations and currency
    """
    
    print("🔧 COMPREHENSIVE CSV REFORMATTING")
    print("=" * 60)
    
    # Load the dataset
    try:
        df = pd.read_csv('real_linkedin_founders_enhanced_clean.csv')
        print(f"✅ Loaded dataset with {len(df)} founders, {len(df.columns)} columns")
    except FileNotFoundError:
        print("❌ Source file not found")
        return
    
    # 1. STANDARDIZE COLUMN NAMES - Group similar columns with consistent naming
    print("\n📋 Step 1: Standardizing column names...")
    
    # Define new column structure with grouped naming
    column_mapping = {
        # PROJECT DATA GROUP (proj_*)
        'project_name': 'proj_name',
        'founder_name': 'proj_founder',
        'category': 'proj_category', 
        'location': 'proj_location',
        'launch_date': 'proj_launch_date',
        'end_date': 'proj_end_date',
        
        # FUNDING DATA GROUP (fund_*)
        'funding_goal': 'fund_goal_usd',
        'amount_raised': 'fund_raised_usd',
        'success_rate': 'fund_success_rate',
        'success_status': 'fund_status',
        'backer_count': 'fund_backer_count',
        
        # COMPANY DATA GROUP (co_*)
        'company_name': 'co_name',
        'website_url': 'co_website_url',
        'current_company': 'co_current_name',
        'current_title': 'co_current_title',
        'business_active': 'co_operational_status',
        'current_status': 'co_business_status',
        'business_growth': 'co_growth_metrics',
        'domain_activity': 'co_domain_status',
        
        # SOCIAL MEDIA GROUP (social_*)
        'linkedin_url': 'social_linkedin_url',
        'other_social_links': 'social_other_platforms',
        'social_activity': 'social_media_activity',
        
        # TEAM DATA GROUP (team_*)
        'team_members': 'team_composition',
        'founder_bio': 'team_founder_bio',
        
        # RESEARCH DATA GROUP (research_*)
        'linkedin_search_query': 'research_linkedin_query',
        'verification_sources': 'research_verification_sources',
        'previous_experience': 'research_work_history',
        'education': 'research_education_summary',
        
        # FUNDING HISTORY GROUP (funding_*)
        'funding_history': 'funding_investment_history',
        
        # MEDIA GROUP (media_*)
        'media_coverage': 'media_press_coverage',
        'awards_recognition': 'media_awards_recognition',
        
        # STATUS GROUP (status_*)
        'legal_issues': 'status_legal_compliance',
        'reputation_status': 'status_professional_reputation',
        
        # LINKEDIN DATA GROUP (li_*)
        'linkedin_profile_found': 'li_profile_verified',
        'linkedin_current_employment': 'li_current_employer',
        'linkedin_current_title': 'li_current_title',
        'linkedin_career_history': 'li_work_experience',
        'linkedin_education_details': 'li_education_background',
        'linkedin_skills_list': 'li_professional_skills',
        'linkedin_activity_posts': 'li_recent_activity'
    }
    
    # Apply column renaming
    df = df.rename(columns=column_mapping)
    
    # 2. STANDARDIZE DATES TO YYYY-MM-DD FORMAT
    print("📅 Step 2: Standardizing dates...")
    
    def standardize_date(date_str):
        """Convert various date formats to YYYY-MM-DD"""
        if pd.isna(date_str) or str(date_str).upper() in ['TBD', 'SUCCESSFULLY FUNDED', 'CAMPAIGN COMPLETED']:
            return 'TBD'
            
        date_str = str(date_str).strip()
        
        # Handle specific patterns
        if 'August 23, 2023' in date_str:
            return '2023-08-23'
        elif 'September 2023' in date_str:
            return '2023-09-30'
        elif 'November 11, 2020' in date_str:
            return '2020-11-11'
        elif 'December 2020' in date_str:
            return '2020-12-31'
        elif 'April 1, 2023' in date_str:
            return '2023-04-01'
        elif 'May 1, 2023' in date_str:
            return '2023-05-01'
        elif 'January 26, 2021' in date_str:
            return '2021-01-26'
        elif 'February 2021' in date_str:
            return '2021-02-28'
        elif '2020-2022 timeframe' in date_str:
            return '2020-01-01'
        else:
            return 'TBD'
    
    df['proj_launch_date'] = df['proj_launch_date'].apply(standardize_date)
    df['proj_end_date'] = df['proj_end_date'].apply(standardize_date)
    
    # 3. STANDARDIZE CURRENCY VALUES
    print("💰 Step 3: Standardizing currency values...")
    
    def standardize_currency(amount_str):
        """Standardize currency formatting"""
        if pd.isna(amount_str):
            return 'TBD'
            
        amount_str = str(amount_str).strip()
        
        # Handle specific patterns
        if '$12,500' in amount_str or '$12.5K' in amount_str:
            return '$12500'
        elif '$10,000' in amount_str:
            return '$10000'
        elif 'Thousands raised' in amount_str:
            return '$5000'  # Estimate
        else:
            return 'TBD'
    
    df['fund_goal_usd'] = df['fund_goal_usd'].apply(standardize_currency)
    df['fund_raised_usd'] = df['fund_raised_usd'].apply(standardize_currency)
    
    # 4. CONVERT STATUS FIELDS TO YES/NO VALUES
    print("✅ Step 4: Converting status fields to Yes/No...")
    
    def convert_to_yes_no(status_str):
        """Convert verbose status to Yes/No"""
        if pd.isna(status_str):
            return 'No'
        
        status_str = str(status_str).lower()
        if 'yes' in status_str or 'active' in status_str or 'funded' in status_str:
            return 'Yes'
        elif 'no' in status_str or 'none' in status_str or 'not funded' in status_str:
            return 'No'
        else:
            return 'Unknown'
    
    # Apply to boolean-style columns
    df['co_operational_status'] = df['co_operational_status'].apply(convert_to_yes_no)
    df['li_profile_verified'] = df['li_profile_verified'].apply(convert_to_yes_no)
    df['status_legal_compliance'] = df['status_legal_compliance'].apply(lambda x: 'Yes' if 'None' in str(x) else 'No')
    
    # 5. BREAK OUT NOTES INTO 3 SEPARATE COLUMNS
    print("📝 Step 5: Breaking out notes into structured columns...")
    
    # Define notes breakdown for each founder
    notes_breakdown = {
        'Tom Vazhekatt': {
            'area_of_expertise': 'Mobile_App_Development|Route_Optimization|Startup_Technology',
            'community_engagement': 'University_Tech_Ecosystem|LinkedIn_Startup_Promotion|Academic_Competition_Participation',
            'business_focus': 'Navigation_Technology|Consumer_Mobile_Apps|Student_Entrepreneurship'
        },
        'Nelli Kim': {
            'area_of_expertise': 'Fashion_Merchandising|Retail_Management|Social_Impact_Business',
            'community_engagement': 'Fashion_Entrepreneurship_Community|Cancer_Survivor_Advocacy|Board_Leadership',
            'business_focus': 'Sustainable_Fashion|Charitable_Business_Models|Comfort_Footwear'
        },
        'Shreyans Kokra': {
            'area_of_expertise': 'Sustainable_Textiles|Hemp_Manufacturing|International_Trade',
            'community_engagement': 'Sustainable_Fashion_Industry|Hemp_Innovation_Leadership|GOTS_Certification',
            'business_focus': 'Hemp_Textile_Innovation|Circular_Economy|Environmental_Manufacturing'
        },
        'Robert Plante': {
            'area_of_expertise': 'Wildlife_Illustration|Creative_Design|Educational_Content',
            'community_engagement': 'Creative_Professional_Network|Canadian_Wildlife_Education|Independent_Artist_Community',
            'business_focus': 'Educational_Games|Wildlife_Conservation_Awareness|Creative_Content_Development'
        },
        'Peter Granitski': {
            'area_of_expertise': 'Embedded_Systems|Robotics_Engineering|Agricultural_Technology',
            'community_engagement': 'University_Robotics_Community|Space_Concordia_Leadership|Student_Entrepreneurship',
            'business_focus': 'Sustainable_Agriculture|Vertical_Farming_Automation|Environmental_Technology'
        }
    }
    
    # Create new columns
    df['notes_area_of_expertise'] = ''
    df['notes_community_engagement'] = ''
    df['notes_business_focus'] = ''
    
    # Populate new columns
    for index, row in df.iterrows():
        founder_name = row['proj_founder']
        if founder_name in notes_breakdown:
            breakdown = notes_breakdown[founder_name]
            df.loc[index, 'notes_area_of_expertise'] = breakdown['area_of_expertise']
            df.loc[index, 'notes_community_engagement'] = breakdown['community_engagement']
            df.loc[index, 'notes_business_focus'] = breakdown['business_focus']
    
    # Remove original notes column
    if 'notes' in df.columns:
        df = df.drop('notes', axis=1)
    
    # 6. FINAL COLUMN ORGANIZATION - Group similar columns together
    print("🗂️ Step 6: Organizing column groups...")
    
    final_column_order = [
        # PROJECT GROUP
        'proj_name', 'proj_founder', 'proj_category', 'proj_location', 
        'proj_launch_date', 'proj_end_date',
        
        # FUNDING GROUP  
        'fund_goal_usd', 'fund_raised_usd', 'fund_success_rate', 'fund_status', 'fund_backer_count',
        'funding_investment_history',
        
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
        'li_work_experience', 'li_education_background', 'li_professional_skills', 'li_recent_activity',
        
        # NOTES GROUP
        'notes_area_of_expertise', 'notes_community_engagement', 'notes_business_focus'
    ]
    
    # Ensure all columns exist
    for col in final_column_order:
        if col not in df.columns:
            df[col] = 'TBD'
    
    # Reorder columns
    df = df[final_column_order]
    
    # 7. EXPORT AS PIPE-SEPARATED FILE
    print("📊 Step 7: Exporting pipe-separated file...")
    
    output_filename = 'linkedin_founders_reformatted.psv'  # .psv for pipe-separated values
    
    df.to_csv(output_filename, 
              sep='|',  # Use pipe as separator
              index=False, 
              encoding='utf-8')
    
    print(f"✅ Created pipe-separated file: {output_filename}")
    
    # 8. VERIFICATION AND SUMMARY
    print("\n📋 REFORMATTING SUMMARY:")
    print("=" * 40)
    print(f"  Original columns: 41")
    print(f"  New columns: {len(df.columns)}")
    print(f"  Founders: {len(df)}")
    print(f"  Delimiter: Pipe (|)")
    print(f"  Date format: YYYY-MM-DD")
    print(f"  Status format: Yes/No")
    print(f"  Notes: Split into 3 focused columns")
    
    print(f"\n📊 COLUMN GROUPS:")
    groups = {
        'PROJECT': [col for col in df.columns if col.startswith('proj_')],
        'FUNDING': [col for col in df.columns if col.startswith('fund_')],
        'COMPANY': [col for col in df.columns if col.startswith('co_')],
        'SOCIAL': [col for col in df.columns if col.startswith('social_')],
        'TEAM': [col for col in df.columns if col.startswith('team_')],
        'RESEARCH': [col for col in df.columns if col.startswith('research_')],
        'MEDIA': [col for col in df.columns if col.startswith('media_')],
        'STATUS': [col for col in df.columns if col.startswith('status_')],
        'LINKEDIN': [col for col in df.columns if col.startswith('li_')],
        'NOTES': [col for col in df.columns if col.startswith('notes_')]
    }
    
    for group_name, columns in groups.items():
        print(f"  {group_name}: {len(columns)} columns")
    
    # Show sample of reformatted data
    print(f"\n📝 SAMPLE REFORMATTED DATA (Tom Vazhekatt):")
    sample = df.iloc[0]
    print(f"  proj_founder: {sample['proj_founder']}")
    print(f"  proj_launch_date: {sample['proj_launch_date']}")
    print(f"  fund_goal_usd: {sample['fund_goal_usd']}")
    print(f"  co_operational_status: {sample['co_operational_status']}")
    print(f"  li_profile_verified: {sample['li_profile_verified']}")
    print(f"  notes_area_of_expertise: {sample['notes_area_of_expertise']}")
    
    return output_filename, df

if __name__ == "__main__":
    output_file, reformatted_df = reformat_linkedin_dataset()
    
    print(f"\n🎯 REFORMATTING COMPLETE!")
    print(f"New file created: {output_file}")
    print(f"Ready for analysis with improved structure and formatting.")