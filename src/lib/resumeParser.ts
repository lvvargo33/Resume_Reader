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
      // Parse PDF using pdfreader library
      try {
        const { PdfReader } = await import('pdfreader')
        
        return new Promise<ParsedResume>((resolve, reject) => {
          const textItems: { text: string, y: number, x: number }[] = []
          
          new PdfReader().parseBuffer(buffer, (err: any, item: any) => {
            if (err) {
              reject(new Error('PDF parsing failed: ' + err.message))
              return
            }
            
            if (!item) {
              // End of document - sort by position and join with proper spacing
              textItems.sort((a, b) => {
                // Sort by y position (top to bottom), then x position (left to right)
                if (Math.abs(a.y - b.y) < 0.1) {
                  return a.x - b.x
                }
                return b.y - a.y
              })
              
              let extractedText = ''
              let lastY = -1
              
              for (const item of textItems) {
                if (lastY !== -1 && Math.abs(item.y - lastY) > 0.1) {
                  // New line
                  extractedText += '\n'
                } else if (extractedText && !extractedText.endsWith(' ')) {
                  // Same line, add space
                  extractedText += ' '
                }
                extractedText += item.text
                lastY = item.y
              }
              
              const extractedData = extractResumeData(extractedText.trim())
              
              resolve({
                text: extractedText.trim(),
                metadata: {
                  fileName,
                  fileSize: buffer.length,
                  fileType: mimeType,
                  parsedAt: new Date()
                },
                extractedData
              })
              return
            }
            
            if (item.text) {
              // Store text with position information
              textItems.push({
                text: item.text,
                y: item.y || 0,
                x: item.x || 0
              })
            }
          })
        })
      } catch (pdfError) {
        console.error('PDF parsing failed:', pdfError)
        throw new Error('PDF parsing failed. Please try uploading a Word document instead.')
      }
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

  // Focus on extracting skills and experience - contact info will come from user input
  data.skills = extractSkills(text)
  data.experience = extractExperience(text)
  data.education = extractEducation(text)
  data.summary = extractSummary(text)

  return data
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
    // Use word boundaries to avoid partial matches
    const regex = new RegExp(`\\b${skillLower.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i')
    if (regex.test(text)) {
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