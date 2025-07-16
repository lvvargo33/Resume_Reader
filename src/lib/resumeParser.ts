import mammoth from 'mammoth'

export interface ParsedResume {
  text: string
  metadata: {
    fileName: string
    fileSize: number
    fileType: string
    parsedAt: Date
  }
  extractedData: {
    name?: string
    email?: string
    phone?: string
    skills: string[]
    experience: ExperienceItem[]
    education: EducationItem[]
    summary?: string
  }
}

export interface ExperienceItem {
  title: string
  company: string
  startDate?: string
  endDate?: string
  description: string
  skills: string[]
}

export interface EducationItem {
  degree: string
  institution: string
  startDate?: string
  endDate?: string
  field?: string
}

/**
 * Parse resume from buffer based on file type
 */
export async function parseResume(
  buffer: Buffer, 
  fileName: string, 
  mimeType: string
): Promise<ParsedResume> {
  let text = ''
  
  try {
    if (mimeType === 'application/pdf') {
      // For now, return a placeholder for PDF parsing
      // TODO: Implement server-safe PDF parsing
      text = 'PDF parsing is temporarily disabled. Please upload a Word document (.docx) for full parsing capabilities, or use this as a placeholder for PDF content extraction.'
    } else if (
      mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      mimeType === 'application/msword'
    ) {
      const docData = await mammoth.extractRawText({ buffer })
      text = docData.value
    } else {
      throw new Error(`Unsupported file type: ${mimeType}`)
    }

    const extractedData = extractResumeData(text)
    
    return {
      text,
      metadata: {
        fileName,
        fileSize: buffer.length,
        fileType: mimeType,
        parsedAt: new Date()
      },
      extractedData
    }
  } catch (error) {
    console.error('Error parsing resume:', error)
    throw new Error(`Failed to parse resume: ${error instanceof Error ? error.message : 'Unknown error'}`)
  }
}

/**
 * Extract structured data from resume text using pattern matching
 */
function extractResumeData(text: string) {
  const data: ParsedResume['extractedData'] = {
    skills: [],
    experience: [],
    education: []
  }

  // Extract email
  const emailMatch = text.match(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/)
  if (emailMatch) {
    data.email = emailMatch[0]
  }

  // Extract phone number
  const phoneMatch = text.match(/(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})/)
  if (phoneMatch) {
    data.phone = phoneMatch[0]
  }

  // Extract name (basic heuristic - first line that looks like a name)
  const lines = text.split('\n').map(line => line.trim()).filter(line => line.length > 0)
  for (const line of lines.slice(0, 5)) {
    if (isLikelyName(line)) {
      data.name = line
      break
    }
  }

  // Extract skills using common skill keywords
  data.skills = extractSkills(text)

  // Extract experience sections
  data.experience = extractExperience(text)

  // Extract education
  data.education = extractEducation(text)

  // Extract summary/objective
  data.summary = extractSummary(text)

  return data
}

/**
 * Check if a line is likely to be a person's name
 */
function isLikelyName(line: string): boolean {
  // Basic heuristics for name detection
  const words = line.split(/\s+/)
  
  // Should be 2-4 words
  if (words.length < 2 || words.length > 4) return false
  
  // Should not contain common resume keywords
  const excludeWords = ['resume', 'cv', 'curriculum', 'vitae', 'experience', 'education', 'skills', 'profile']
  if (excludeWords.some(word => line.toLowerCase().includes(word))) return false
  
  // Should not be all caps (likely a section header)
  if (line === line.toUpperCase()) return false
  
  // Should not contain numbers or special characters (except periods and apostrophes)
  if (/[0-9@#$%^&*()_+=<>?{}|\\~`]/.test(line)) return false
  
  // Each word should start with capital letter
  return words.every(word => /^[A-Z][a-z]*[.]?$/.test(word))
}

/**
 * Extract skills from resume text
 */
function extractSkills(text: string): string[] {
  const skillKeywords = [
    // Programming languages
    'JavaScript', 'TypeScript', 'Python', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
    'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS',
    
    // Frameworks and libraries
    'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Laravel', 'Spring',
    'Rails', 'Next.js', 'Nuxt.js', 'Svelte', 'jQuery', 'Bootstrap', 'Tailwind',
    
    // Databases
    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server',
    
    // Cloud and DevOps
    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitHub', 'GitLab',
    'CI/CD', 'Terraform', 'Ansible',
    
    // Tools and technologies
    'Linux', 'Windows', 'macOS', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
    'Machine Learning', 'AI', 'Data Science', 'Analytics', 'Tableau', 'Power BI',
    
    // Soft skills
    'Leadership', 'Communication', 'Project Management', 'Team Management', 'Problem Solving',
    'Critical Thinking', 'Analytical Skills', 'Creativity', 'Adaptability'
  ]

  const foundSkills: string[] = []
  const textLower = text.toLowerCase()

  skillKeywords.forEach(skill => {
    const skillLower = skill.toLowerCase()
    if (textLower.includes(skillLower)) {
      foundSkills.push(skill)
    }
  })

  return Array.from(new Set(foundSkills)) // Remove duplicates
}

/**
 * Extract work experience from resume text
 */
function extractExperience(text: string): ExperienceItem[] {
  const experience: ExperienceItem[] = []
  const sections = text.split(/(?=EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT)/i)
  
  if (sections.length > 1) {
    const experienceSection = sections[1]
    const jobEntries = experienceSection.split(/\n\s*\n/).filter(entry => entry.trim().length > 50)
    
    jobEntries.forEach(entry => {
      const lines = entry.split('\n').map(line => line.trim()).filter(line => line.length > 0)
      if (lines.length >= 2) {
        const item: ExperienceItem = {
          title: lines[0] || '',
          company: lines[1] || '',
          description: lines.slice(2).join(' '),
          skills: extractSkills(entry)
        }
        
        // Try to extract dates
        const dateMatch = entry.match(/(\d{4})\s*[-–—]\s*(\d{4}|present|current)/i)
        if (dateMatch) {
          item.startDate = dateMatch[1]
          item.endDate = dateMatch[2].toLowerCase() === 'present' || dateMatch[2].toLowerCase() === 'current' 
            ? 'Present' : dateMatch[2]
        }
        
        experience.push(item)
      }
    })
  }
  
  return experience
}

/**
 * Extract education from resume text
 */
function extractEducation(text: string): EducationItem[] {
  const education: EducationItem[] = []
  const sections = text.split(/(?=EDUCATION|ACADEMIC|QUALIFICATIONS)/i)
  
  if (sections.length > 1) {
    const educationSection = sections[1]
    const eduEntries = educationSection.split(/\n\s*\n/).filter(entry => entry.trim().length > 20)
    
    eduEntries.forEach(entry => {
      const lines = entry.split('\n').map(line => line.trim()).filter(line => line.length > 0)
      if (lines.length >= 2) {
        const item: EducationItem = {
          degree: lines[0] || '',
          institution: lines[1] || ''
        }
        
        // Try to extract field and dates
        const fieldMatch = entry.match(/\b(in|of)\s+([A-Za-z\s]+)\b/i)
        if (fieldMatch) {
          item.field = fieldMatch[2].trim()
        }
        
        const dateMatch = entry.match(/(\d{4})\s*[-–—]\s*(\d{4})/i)
        if (dateMatch) {
          item.startDate = dateMatch[1]
          item.endDate = dateMatch[2]
        }
        
        education.push(item)
      }
    })
  }
  
  return education
}

/**
 * Extract summary/objective from resume text
 */
function extractSummary(text: string): string | undefined {
  const summaryPatterns = [
    /(?:SUMMARY|OBJECTIVE|PROFILE|ABOUT)[\s\S]*?(?=\n[A-Z]{3,}|\n\n|\n\s*\n|$)/i
  ]
  
  for (const pattern of summaryPatterns) {
    const match = text.match(pattern)
    if (match) {
      const summary = match[0]
        .replace(/^(SUMMARY|OBJECTIVE|PROFILE|ABOUT)[:\s]*/i, '')
        .trim()
      
      if (summary.length > 50 && summary.length < 1000) {
        return summary
      }
    }
  }
  
  return undefined
}