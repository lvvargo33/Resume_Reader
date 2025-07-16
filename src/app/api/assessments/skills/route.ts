import { NextRequest, NextResponse } from 'next/server'
import { saveSkillsAssessment } from '@/lib/database'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { 
      email, 
      currentRole, 
      industry, 
      yearsExperience, 
      careerGoals, 
      topSkills 
    } = body

    // Validate required fields
    if (!email || !currentRole || !industry || !yearsExperience || !topSkills) {
      return NextResponse.json(
        { error: 'Missing required fields: email, currentRole, industry, yearsExperience, topSkills' },
        { status: 400 }
      )
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Invalid email format' },
        { status: 400 }
      )
    }

    // Validate years experience
    const experience = parseInt(yearsExperience)
    if (isNaN(experience) || experience < 0) {
      return NextResponse.json(
        { error: 'Years experience must be a valid number' },
        { status: 400 }
      )
    }

    // Validate top skills structure
    if (!Array.isArray(topSkills) || topSkills.length === 0) {
      return NextResponse.json(
        { error: 'Top skills must be a non-empty array' },
        { status: 400 }
      )
    }

    // Save assessment to database
    const assessment = await saveSkillsAssessment(email, {
      currentRole,
      industry,
      yearsExperience: experience,
      careerGoals,
      topSkills,
      completedAt: new Date()
    })

    return NextResponse.json({
      success: true,
      assessment: {
        id: assessment.id,
        currentRole: assessment.current_role,
        industry: assessment.industry,
        yearsExperience: assessment.years_experience,
        topSkills: assessment.top_skills,
        completedAt: assessment.completed_at
      }
    })

  } catch (error) {
    console.error('Error saving skills assessment:', error)
    return NextResponse.json(
      { error: 'Failed to save assessment' },
      { status: 500 }
    )
  }
}