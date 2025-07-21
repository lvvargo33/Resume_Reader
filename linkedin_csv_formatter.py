import pandas as pd
import csv

def fix_csv_formatting():
    """
    Fix CSV formatting issues by properly handling multiline content
    """
    
    print("🔧 FIXING CSV FORMATTING ISSUES")
    print("=" * 50)
    
    # Read the enhanced dataset
    try:
        df = pd.read_excel('real_linkedin_founders_enhanced.xlsx', sheet_name='Enhanced LinkedIn Founders')
        print(f"✅ Loaded Excel data with {len(df)} founders")
    except FileNotFoundError:
        print("❌ Excel file not found")
        return
    
    # Clean multiline content for CSV compatibility
    text_columns = [
        'linkedin_career_history',
        'linkedin_education_details', 
        'linkedin_skills_list',
        'linkedin_activity_posts',
        'notes'
    ]
    
    for col in text_columns:
        if col in df.columns:
            # Replace line breaks with semicolon separators for CSV compatibility
            df[col] = df[col].astype(str).str.replace('\n', ' | ').str.replace('\r', ' | ')
            df[col] = df[col].str.replace('  |  ', ' | ').str.replace('|||', '|')  # Clean up multiple separators
    
    # Export properly formatted CSV
    output_file = 'real_linkedin_founders_enhanced_clean.csv'
    
    df.to_csv(output_file, 
              index=False, 
              encoding='utf-8',
              quoting=csv.QUOTE_ALL,  # Quote all fields to handle special characters
              escapechar='\\')  # Use backslash for escaping
    
    print(f"✅ Created clean CSV: {output_file}")
    
    # Also create a tab-separated version for better handling of complex text
    tsv_file = output_file.replace('.csv', '.tsv')
    df.to_csv(tsv_file, 
              index=False, 
              sep='\t',
              encoding='utf-8')
    
    print(f"✅ Created TSV version: {tsv_file}")
    
    # Verify the output
    test_df = pd.read_csv(output_file)
    print(f"\n📊 VERIFICATION:")
    print(f"  Original rows: {len(df)}")
    print(f"  CSV rows: {len(test_df)}")
    print(f"  Columns match: {len(df.columns) == len(test_df.columns)}")
    print(f"  Data integrity: {'✅ PASS' if len(df) == len(test_df) else '❌ FAIL'}")
    
    # Show sample of fixed formatting
    print(f"\n📝 SAMPLE FIXED FORMATTING (Tom Vazhekatt Career History):")
    career_sample = test_df[test_df['founder_name'] == 'Tom Vazhekatt']['linkedin_career_history'].iloc[0]
    print(f"  {career_sample[:100]}...")
    
    return output_file, tsv_file

def create_readable_summary():
    """
    Create a human-readable summary of the LinkedIn data
    """
    
    try:
        df = pd.read_excel('real_linkedin_founders_enhanced.xlsx', sheet_name='Enhanced LinkedIn Founders')
    except:
        print("Could not read Excel file for summary")
        return
    
    summary_content = """# LinkedIn Founders Dataset - Readable Summary

## Complete Founder Profiles with Skills and Career Data

"""
    
    for _, row in df.iterrows():
        summary_content += f"""
### {row['founder_name']} - {row['company_name']}

**Location**: {row['location']}  
**LinkedIn**: {row['linkedin_url']}  
**Business Status**: {row['business_active']}  

**Current Role**: {row['linkedin_current_title']} at {row['linkedin_current_employment']}

**Key Skills**:
"""
        
        # Extract skills from the skills list
        skills_text = str(row['linkedin_skills_list'])
        skills = [skill.strip() for skill in skills_text.split('•') if skill.strip() and len(skill.strip()) > 3][:10]
        for skill in skills:
            if skill and not skill.startswith('Technical') and not skill.startswith('Business'):
                summary_content += f"- {skill}\n"
        
        summary_content += f"""
**Career Highlights**:
"""
        # Extract career positions
        career_text = str(row['linkedin_career_history'])
        positions = [pos.strip() for pos in career_text.split(':') if 'Present' in pos or '202' in pos][:5]
        for pos in positions:
            if pos and len(pos) > 10:
                summary_content += f"- {pos}\n"
        
        summary_content += f"""
**Education**: {row['linkedin_education_details'][:100]}...

**Business Growth**: {row['business_growth']}

---
"""
    
    # Write summary file
    summary_file = 'LINKEDIN_FOUNDERS_READABLE_SUMMARY.md'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ Created readable summary: {summary_file}")
    return summary_file

if __name__ == "__main__":
    # Fix CSV formatting
    csv_file, tsv_file = fix_csv_formatting()
    
    # Create readable summary
    summary_file = create_readable_summary()
    
    print(f"\n🎯 FILES CREATED:")
    print(f"  📄 {csv_file} - Clean CSV format")
    print(f"  📊 {tsv_file} - Tab-separated format") 
    print(f"  📋 {summary_file} - Human-readable summary")
    
    print(f"\n✅ CSV FORMATTING FIXED!")
    print("The clean CSV file now properly handles multiline content")
    print("and can be opened in Excel, Google Sheets, or any CSV reader.")