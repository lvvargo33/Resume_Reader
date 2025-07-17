import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({
  apiKey: process.env.CLAUDE_API_KEY,
})

export interface ClaudeExtractedData {
  personal_info: {
    name?: string
    email?: string
    phone?: string
    address?: string
    linkedin?: string
    website?: string
    work_authorization?: string
  }
  professional_summary?: string
  hard_skills: {
    programming_languages: string[]
    software_applications: string[]
    platforms_tools: string[]
    databases: string[]
    methodologies: string[]
  }
  soft_skills: string[]
  experience: Array<{
    job_title: string
    company: string
    location?: string
    start_date?: string
    end_date?: string
    key_responsibilities: string[]
    achievements: string[]
    technologies_used: string[]
  }>
  education: Array<{
    degree: string
    field_of_study?: string
    institution: string
    location?: string
    graduation_date?: string
    relevant_coursework: string[]
    honors: string[]
    publications: string[]
  }>
  certifications: Array<{
    name: string
    issuing_organization?: string
    date_obtained?: string
    expiration_date?: string
  }>
  projects: Array<{
    name: string
    description?: string
    technologies: string[]
    url?: string
  }>
  awards_achievements: Array<{
    name: string
    organization?: string
    date?: string
    description?: string
  }>
  languages: Array<{
    language: string
    proficiency?: string
  }>
  additional_info: {
    volunteer_experience: string[]
    professional_memberships: string[]
    interests: string[]
    other_notes: string[]
  }
}

export interface ClaudeParseResult {
  extractedData: ClaudeExtractedData
  metadata: {
    fileName: string
    fileSize: number
    fileType: string
    parsedAt: Date
    textLength: number
  }
}

/**
 * Strip user-provided contact information from resume text for privacy
 */
function stripContactInfo(text: string, userContact: { name?: string, email?: string, phone?: string }): string {
  let cleanedText = text

  // Strip user's name if provided
  if (userContact.name) {
    const nameRegex = new RegExp(userContact.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
    cleanedText = cleanedText.replace(nameRegex, '[NAME_REDACTED]')
  }

  // Strip user's email if provided
  if (userContact.email) {
    const emailRegex = new RegExp(userContact.email.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
    cleanedText = cleanedText.replace(emailRegex, '[EMAIL_REDACTED]')
  }

  // Strip user's phone if provided
  if (userContact.phone) {
    const phoneRegex = new RegExp(userContact.phone.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
    cleanedText = cleanedText.replace(phoneRegex, '[PHONE_REDACTED]')
  }

  return cleanedText
}

/**
 * Parse resume using Claude AI
 */
export async function parseResumeWithClaude(
  resumeText: string,
  fileName: string,
  fileSize: number,
  fileType: string,
  userContact: { name?: string, email?: string, phone?: string }
): Promise<ClaudeParseResult> {
  try {
    // Strip user contact info for privacy
    const cleanedText = stripContactInfo(resumeText, userContact)

    const prompt = `You are an expert resume parser. Extract ALL information from the provided resume into structured JSON format.
CRITICAL: Your response must be ONLY valid JSON. Do not include markdown formatting, backticks, or any text outside the JSON structure. Start directly with { and end with }.

Instructions:
- Extract information from ALL sections, including details embedded in descriptions
- Categorize skills as hard vs soft skills appropriately
- Include quantified achievements and specific technologies mentioned
- Capture all dates, locations, and company information
- Do not invent information not present in the resume

Required Output Format:
{
  "personal_info": {
    "name": "string",
    "email": "string", 
    "phone": "string",
    "address": "string",
    "linkedin": "string",
    "website": "string",
    "work_authorization": "string"
  },
  "professional_summary": "string",
  "hard_skills": {
    "programming_languages": ["array"],
    "software_applications": ["array"],
    "platforms_tools": ["array"],
    "databases": ["array"],
    "methodologies": ["array"]
  },
  "soft_skills": ["array"],
  "experience": [
    {
      "job_title": "string",
      "company": "string",
      "location": "string",
      "start_date": "string",
      "end_date": "string",
      "key_responsibilities": ["array"],
      "achievements": ["array"],
      "technologies_used": ["array"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "field_of_study": "string",
      "institution": "string",
      "location": "string",
      "graduation_date": "string",
      "relevant_coursework": ["array"],
      "honors": ["array"],
      "publications": ["array"]
    }
  ],
  "certifications": [
    {
      "name": "string",
      "issuing_organization": "string",
      "date_obtained": "string",
      "expiration_date": "string"
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": ["array"],
      "url": "string"
    }
  ],
  "awards_achievements": [
    {
      "name": "string",
      "organization": "string",
      "date": "string",
      "description": "string"
    }
  ],
  "languages": [
    {
      "language": "string",
      "proficiency": "string"
    }
  ],
  "additional_info": {
    "volunteer_experience": ["array"],
    "professional_memberships": ["array"],
    "interests": ["array"],
    "other_notes": ["array"]
  }
}

Resume text:
${cleanedText}`

    const message = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4000,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    })

    // Extract the text content from Claude's response
    const responseText = message.content[0].type === 'text' ? message.content[0].text : ''
    
    if (!responseText) {
      throw new Error('No response received from Claude')
    }

    // Parse the JSON response
    const extractedData = JSON.parse(responseText) as ClaudeExtractedData

    return {
      extractedData,
      metadata: {
        fileName,
        fileSize,
        fileType,
        parsedAt: new Date(),
        textLength: cleanedText.length
      }
    }

  } catch (error) {
    console.error('Claude parsing error:', error)
    throw new Error('Failed to parse resume with AI. Please try again later.')
  }
}