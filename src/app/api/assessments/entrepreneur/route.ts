import { NextRequest, NextResponse } from 'next/server'
import { saveEntrepreneurAssessment } from '@/lib/database'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, responses, score, recommendations } = body

    // Validate required fields
    if (!email || !responses || score === undefined) {
      return NextResponse.json(
        { error: 'Missing required fields: email, responses, score' },
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

    // Validate score range
    if (score < 0 || score > 100) {
      return NextResponse.json(
        { error: 'Score must be between 0 and 100' },
        { status: 400 }
      )
    }

    // Save assessment to database
    const assessment = await saveEntrepreneurAssessment(email, {
      responses,
      score,
      recommendations: recommendations || [],
      completedAt: new Date()
    })

    return NextResponse.json({
      success: true,
      assessment: {
        id: assessment.id,
        score: assessment.score,
        recommendations: assessment.recommendations,
        completedAt: assessment.completed_at
      }
    })

  } catch (error) {
    console.error('Error saving entrepreneur assessment:', error)
    return NextResponse.json(
      { error: 'Failed to save assessment' },
      { status: 500 }
    )
  }
}