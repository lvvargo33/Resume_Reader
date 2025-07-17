import { NextRequest, NextResponse } from 'next/server'
import { parseResume } from '@/lib/resumeParser'
import { parseResumeWithClaude } from '@/lib/claudeResumeParser'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    const email = formData.get('email') as string
    const name = formData.get('name') as string
    const phone = formData.get('phone') as string

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      )
    }

    if (!email || !name) {
      return NextResponse.json(
        { error: 'Name and email are required' },
        { status: 400 }
      )
    }

    // Validate file type
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword'
    ]

    if (!allowedTypes.includes(file.type)) {
      return NextResponse.json(
        { error: 'Invalid file type. Please upload a PDF or Word document.' },
        { status: 400 }
      )
    }

    // Validate file size (5MB limit)
    const maxSize = 5 * 1024 * 1024 // 5MB
    if (file.size > maxSize) {
      return NextResponse.json(
        { error: 'File too large. Maximum size is 5MB.' },
        { status: 400 }
      )
    }

    // Convert file to buffer
    const arrayBuffer = await file.arrayBuffer()
    const buffer = Buffer.from(arrayBuffer)

    // Extract text from the resume first
    const parsedResume = await parseResume(buffer, file.name, file.type)
    
    // Use Claude to intelligently extract structured data
    const claudeResult = await parseResumeWithClaude(
      parsedResume.text,
      file.name,
      buffer.length,
      file.type,
      { name, email, phone }
    )

    // TODO: Save parsed resume to database
    // This would involve creating a client profile and storing the resume data
    
    return NextResponse.json({
      success: true,
      data: {
        fileName: claudeResult.metadata.fileName,
        fileSize: claudeResult.metadata.fileSize,
        parsedAt: claudeResult.metadata.parsedAt,
        extractedData: {
          ...claudeResult.extractedData,
          // Override with user-provided contact info for display
          personal_info: {
            ...claudeResult.extractedData.personal_info,
            name: name,
            email: email,
            phone: phone || undefined
          }
        },
        textLength: claudeResult.metadata.textLength
      }
    })

  } catch (error) {
    console.error('Error parsing resume:', error)
    
    // Check if it's a Claude API error
    if (error instanceof Error && error.message.includes('Failed to parse resume with AI')) {
      return NextResponse.json(
        { 
          success: false,
          error: 'Sorry, please try again later'
        },
        { status: 500 }
      )
    }
    
    return NextResponse.json(
      { 
        success: false,
        error: error instanceof Error ? error.message : 'Failed to parse resume' 
      },
      { status: 500 }
    )
  }
}

// Add OPTIONS handler for CORS if needed
export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  })
}