'use client'

import { useState } from 'react'
import Link from 'next/link'

const skillRecommendations = {
  'software-engineer': {
    'junior': [
      { skill: 'System Design', impact: 'Essential for senior roles and salary jumps', priority: 1 },
      { skill: 'Cloud Architecture (AWS/Azure)', impact: 'High demand, 25-40% salary increase', priority: 2 },
      { skill: 'Leadership & Mentoring', impact: 'Required for team lead positions', priority: 3 }
    ],
    'mid': [
      { skill: 'Technical Leadership', impact: 'Path to senior/principal roles', priority: 1 },
      { skill: 'Product Strategy', impact: 'Bridge to product management roles', priority: 2 },
      { skill: 'Machine Learning/AI', impact: 'Emerging field with premium salaries', priority: 3 }
    ],
    'senior': [
      { skill: 'Executive Communication', impact: 'Essential for C-level progression', priority: 1 },
      { skill: 'Business Strategy', impact: 'Transition to VP/Director roles', priority: 2 },
      { skill: 'Team Scaling', impact: 'Required for engineering management', priority: 3 }
    ]
  },
  'marketing': {
    'junior': [
      { skill: 'Data Analytics', impact: 'Measure and prove marketing ROI', priority: 1 },
      { skill: 'Marketing Automation', impact: 'Efficiency gains and scalability', priority: 2 },
      { skill: 'Content Strategy', impact: 'Foundation for all marketing efforts', priority: 3 }
    ],
    'mid': [
      { skill: 'Growth Hacking', impact: 'High-impact strategies for rapid growth', priority: 1 },
      { skill: 'Customer Psychology', impact: 'Better targeting and conversion', priority: 2 },
      { skill: 'Performance Marketing', impact: 'Measurable results and ROI', priority: 3 }
    ],
    'senior': [
      { skill: 'Strategic Planning', impact: 'Long-term vision and execution', priority: 1 },
      { skill: 'Cross-functional Leadership', impact: 'Collaborate across departments', priority: 2 },
      { skill: 'Market Research', impact: 'Data-driven decision making', priority: 3 }
    ]
  },
  'sales': {
    'junior': [
      { skill: 'CRM Management', impact: 'Systematic approach to sales process', priority: 1 },
      { skill: 'Consultative Selling', impact: 'Higher close rates and deal sizes', priority: 2 },
      { skill: 'Social Selling', impact: 'Modern prospecting and relationship building', priority: 3 }
    ],
    'mid': [
      { skill: 'Sales Analytics', impact: 'Data-driven sales optimization', priority: 1 },
      { skill: 'Account Management', impact: 'Recurring revenue and upselling', priority: 2 },
      { skill: 'Team Leadership', impact: 'Path to sales management roles', priority: 3 }
    ],
    'senior': [
      { skill: 'Strategic Account Planning', impact: 'Enterprise sales and large deals', priority: 1 },
      { skill: 'Sales Operations', impact: 'Scalable sales systems and processes', priority: 2 },
      { skill: 'Revenue Operations', impact: 'Holistic approach to revenue growth', priority: 3 }
    ]
  },
  'other': [
    { skill: 'Digital Literacy', impact: 'Essential for modern workplace', priority: 1 },
    { skill: 'Communication Skills', impact: 'Universal skill for career advancement', priority: 2 },
    { skill: 'Problem Solving', impact: 'Critical thinking for complex challenges', priority: 3 }
  ]
}

export default function SkillsAssessment() {
  const [formData, setFormData] = useState({
    email: '',
    currentRole: '',
    industry: '',
    yearsExperience: '',
    careerGoals: ''
  })
  const [showResults, setShowResults] = useState(false)
  const [recommendations, setRecommendations] = useState<any[]>([])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Simple logic to determine skill recommendations
    const role = formData.currentRole.toLowerCase()
    const years = parseInt(formData.yearsExperience)
    
    let experienceLevel = 'junior'
    if (years >= 7) experienceLevel = 'senior'
    else if (years >= 3) experienceLevel = 'mid'
    
    let roleCategory = 'other'
    if (role.includes('engineer') || role.includes('developer') || role.includes('software')) {
      roleCategory = 'software-engineer'
    } else if (role.includes('marketing')) {
      roleCategory = 'marketing'
    } else if (role.includes('sales')) {
      roleCategory = 'sales'
    }
    
    const skillRecs = roleCategory === 'other' 
      ? skillRecommendations.other 
      : (skillRecommendations as any)[roleCategory][experienceLevel]
    
    // Save assessment to database
    try {
      const response = await fetch('/api/assessments/skills', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          currentRole: formData.currentRole,
          industry: formData.industry,
          yearsExperience: formData.yearsExperience,
          careerGoals: formData.careerGoals,
          topSkills: skillRecs
        })
      })
      
      if (!response.ok) {
        console.error('Failed to save skills assessment')
      }
    } catch (error) {
      console.error('Error saving skills assessment:', error)
    }
    
    setRecommendations(skillRecs)
    setShowResults(true)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  if (showResults) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-16">
        <div className="container mx-auto px-4 max-w-2xl">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Your Top 3 Skills for Career Advancement
              </h1>
              <p className="text-gray-600">
                Based on your current role and experience level
              </p>
            </div>
            
            <div className="space-y-6 mb-8">
              {recommendations.map((rec, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-6">
                  <div className="flex items-center mb-3">
                    <div className="bg-primary-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-3">
                      {rec.priority}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900">
                      {rec.skill}
                    </h3>
                  </div>
                  <p className="text-gray-600">
                    {rec.impact}
                  </p>
                </div>
              ))}
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-semibold text-yellow-800 mb-2">
                📊 Want to know the salary impact?
              </h3>
              <p className="text-yellow-700 mb-4">
                This free assessment shows you what skills to focus on, but doesn&apos;t include salary data. 
                For detailed salary insights, market trends, and a personalized learning roadmap:
              </p>
              <button className="bg-yellow-600 hover:bg-yellow-700 text-white px-6 py-3 rounded-lg font-semibold">
                Get Full Career Analysis
              </button>
            </div>

            <div className="text-center">
              <Link
                href="/"
                className="text-primary-600 hover:text-primary-700 font-semibold"
              >
                ← Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-16">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Skills Assessment for Career Advancement
            </h1>
            <p className="text-gray-600">
              Tell us about your current situation and we&apos;ll identify the top 3 skills 
              that will have the biggest impact on your career growth.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="your@email.com"
                required
              />
            </div>

            <div>
              <label htmlFor="currentRole" className="block text-sm font-medium text-gray-700 mb-2">
                Current Role *
              </label>
              <input
                type="text"
                id="currentRole"
                name="currentRole"
                value={formData.currentRole}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., Software Engineer, Marketing Manager"
                required
              />
            </div>

            <div>
              <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
                Industry *
              </label>
              <select
                id="industry"
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              >
                <option value="">Select your industry</option>
                <option value="technology">Technology</option>
                <option value="finance">Finance</option>
                <option value="healthcare">Healthcare</option>
                <option value="marketing">Marketing</option>
                <option value="sales">Sales</option>
                <option value="consulting">Consulting</option>
                <option value="education">Education</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label htmlFor="yearsExperience" className="block text-sm font-medium text-gray-700 mb-2">
                Years of Experience *
              </label>
              <select
                id="yearsExperience"
                name="yearsExperience"
                value={formData.yearsExperience}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              >
                <option value="">Select experience level</option>
                <option value="0-1">0-1 years</option>
                <option value="2-3">2-3 years</option>
                <option value="4-6">4-6 years</option>
                <option value="7-10">7-10 years</option>
                <option value="10+">10+ years</option>
              </select>
            </div>

            <div>
              <label htmlFor="careerGoals" className="block text-sm font-medium text-gray-700 mb-2">
                Career Goals (Optional)
              </label>
              <input
                type="text"
                id="careerGoals"
                name="careerGoals"
                value={formData.careerGoals}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="e.g., Become a team lead, transition to management"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-primary-600 hover:bg-primary-700 text-white py-3 px-6 rounded-lg font-semibold transition-colors"
            >
              Get My Top 3 Skills
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}