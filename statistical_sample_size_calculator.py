import math

def calculate_sample_size():
    """
    Calculate the required sample size for a representative study of entrepreneurs
    in the United States and Canada with 95% confidence level
    """
    
    print("📊 STATISTICAL SAMPLE SIZE CALCULATION")
    print("=" * 70)
    print("For representative entrepreneur study: United States & Canada")
    print()
    
    # POPULATION DATA (2024 estimates)
    print("🌎 POPULATION ESTIMATES:")
    print("-" * 50)
    
    # US Entrepreneurs
    us_small_businesses = 33_200_000  # 33.2 million small businesses (SBA 2024)
    us_entrepreneurs_percent = 0.15  # ~15% of adults are entrepreneurs
    us_adult_population = 258_000_000  # US adults (18+)
    us_entrepreneurs_estimate = us_adult_population * us_entrepreneurs_percent
    
    print(f"United States:")
    print(f"  • Small businesses: {us_small_businesses:,}")
    print(f"  • Adult population: {us_adult_population:,}")
    print(f"  • Entrepreneur estimate (15%): {us_entrepreneurs_estimate:,.0f}")
    
    # Canada Entrepreneurs
    canada_small_businesses = 1_230_000  # 1.23 million small businesses
    canada_entrepreneurs_percent = 0.14  # ~14% of adults are entrepreneurs
    canada_adult_population = 31_000_000  # Canada adults (18+)
    canada_entrepreneurs_estimate = canada_adult_population * canada_entrepreneurs_percent
    
    print(f"\nCanada:")
    print(f"  • Small businesses: {canada_small_businesses:,}")
    print(f"  • Adult population: {canada_adult_population:,}")
    print(f"  • Entrepreneur estimate (14%): {canada_entrepreneurs_estimate:,.0f}")
    
    # TOTAL POPULATION
    total_entrepreneurs = us_entrepreneurs_estimate + canada_entrepreneurs_estimate
    print(f"\n📈 TOTAL ENTREPRENEUR POPULATION (US + Canada):")
    print(f"  • Estimated total: {total_entrepreneurs:,.0f}")
    
    # SAMPLE SIZE CALCULATION
    print("\n🧮 SAMPLE SIZE CALCULATION:")
    print("-" * 50)
    
    # Standard sample size formula for finite population
    # n = N * Z² * p * (1-p) / (E² * (N-1) + Z² * p * (1-p))
    
    # Parameters
    confidence_level = 0.95
    z_score = 1.96  # For 95% confidence level
    margin_of_error_options = [0.01, 0.02, 0.03, 0.04, 0.05]  # 1%, 2%, 3%, 4%, 5%
    proportion = 0.5  # Maximum variability (most conservative estimate)
    
    print(f"Parameters:")
    print(f"  • Confidence Level: {confidence_level*100}%")
    print(f"  • Z-Score: {z_score}")
    print(f"  • Proportion: {proportion} (maximum variability)")
    print(f"  • Population: {total_entrepreneurs:,.0f}")
    
    print("\n📊 REQUIRED SAMPLE SIZES BY MARGIN OF ERROR:")
    print("-" * 60)
    print(f"{'Margin of Error':<20} {'Sample Size':<15} {'% of Population':<15}")
    print("-" * 60)
    
    sample_sizes = {}
    
    for margin_error in margin_of_error_options:
        # Finite population sample size formula
        numerator = total_entrepreneurs * (z_score**2) * proportion * (1 - proportion)
        denominator = (margin_error**2) * (total_entrepreneurs - 1) + (z_score**2) * proportion * (1 - proportion)
        sample_size = math.ceil(numerator / denominator)
        
        percentage_of_pop = (sample_size / total_entrepreneurs) * 100
        
        sample_sizes[margin_error] = sample_size
        
        print(f"±{margin_error*100:>3.0f}%                 {sample_size:>10,}      {percentage_of_pop:>10.4f}%")
    
    # PRACTICAL RECOMMENDATIONS
    print("\n💡 PRACTICAL RECOMMENDATIONS:")
    print("=" * 70)
    
    # Standard recommendation (3% margin of error)
    recommended_margin = 0.03
    recommended_sample = sample_sizes[recommended_margin]
    
    print(f"\n🎯 STANDARD RESEARCH RECOMMENDATION:")
    print(f"  • Margin of Error: ±{recommended_margin*100}%")
    print(f"  • Required Sample: {recommended_sample:,} entrepreneurs")
    print(f"  • This provides 95% confidence that results are within ±3% of true population values")
    
    # By country breakdown
    us_proportion = us_entrepreneurs_estimate / total_entrepreneurs
    canada_proportion = canada_entrepreneurs_estimate / total_entrepreneurs
    
    us_sample = math.ceil(recommended_sample * us_proportion)
    canada_sample = math.ceil(recommended_sample * canada_proportion)
    
    print(f"\n🌍 GEOGRAPHIC DISTRIBUTION:")
    print(f"  • US entrepreneurs: {us_sample:,} ({us_proportion*100:.1f}%)")
    print(f"  • Canadian entrepreneurs: {canada_sample:,} ({canada_proportion*100:.1f}%)")
    
    # By industry sector (using our previous distribution)
    print(f"\n🏢 INDUSTRY SECTOR BREAKDOWN (for {recommended_sample:,} sample):")
    print("-" * 50)
    
    sectors = [
        ("Food & Restaurant", 0.12),
        ("Retail & E-commerce", 0.11),
        ("Business Services", 0.11),
        ("Health, Beauty & Fitness", 0.09),
        ("Construction & Contracting", 0.08),
        ("Other Services", 0.08),
        ("Residential & Commercial Services", 0.07),
        ("Technology", 0.06),
        ("Healthcare", 0.055),
        ("Financial Services", 0.045),
        ("Education & Training", 0.04),
        ("Manufacturing", 0.035),
        ("Transportation & Logistics", 0.03),
        ("Real Estate", 0.03),
        ("Agriculture", 0.025),
        ("Entertainment & Media", 0.02)
    ]
    
    print(f"{'Sector':<35} {'Count':<10}")
    print("-" * 50)
    
    total_by_sector = 0
    for sector, percentage in sectors:
        count = math.ceil(recommended_sample * percentage)
        total_by_sector += count
        print(f"{sector:<35} {count:<10,}")
    
    # ALTERNATIVE OPTIONS
    print("\n📈 ALTERNATIVE SAMPLE SIZE OPTIONS:")
    print("-" * 70)
    
    print("\n1️⃣ BUDGET-CONSCIOUS OPTION:")
    budget_sample = sample_sizes[0.05]  # 5% margin of error
    print(f"   • Sample Size: {budget_sample:,} entrepreneurs")
    print(f"   • Margin of Error: ±5%")
    print(f"   • Good for exploratory research or pilot studies")
    
    print("\n2️⃣ HIGH-PRECISION OPTION:")
    precision_sample = sample_sizes[0.01]  # 1% margin of error
    print(f"   • Sample Size: {precision_sample:,} entrepreneurs")
    print(f"   • Margin of Error: ±1%")
    print(f"   • For publication-quality research or policy decisions")
    
    print("\n3️⃣ MINIMUM VIABLE SAMPLE:")
    print(f"   • Sample Size: 385 entrepreneurs")
    print(f"   • Based on infinite population formula")
    print(f"   • Suitable for very large populations where N > 20,000")
    
    # PRACTICAL CONSIDERATIONS
    print("\n⚠️  PRACTICAL CONSIDERATIONS:")
    print("-" * 50)
    print("1. Response Rate: Plan for 20-30% response rate")
    print(f"   • Need to contact ~{recommended_sample * 4:,} entrepreneurs for {recommended_sample:,} responses")
    print("2. Data Quality: LinkedIn-verified profiles ensure higher quality")
    print("3. Stratification: Ensure proportional representation by:")
    print("   • Geographic region")
    print("   • Industry sector")
    print("   • Business size/age")
    print("   • Success/failure status")
    print("4. Time & Cost: Larger samples = more time and resources")
    
    return sample_sizes, recommended_sample

if __name__ == "__main__":
    sample_sizes, recommended = calculate_sample_size()
    
    print("\n" + "="*70)
    print("🎯 FINAL RECOMMENDATION:")
    print(f"   For a representative study of US & Canadian entrepreneurs")
    print(f"   with 95% confidence level and ±3% margin of error:")
    print(f"   \n   ✅ COLLECT DATA FROM {recommended:,} ENTREPRENEURS")
    print("="*70)