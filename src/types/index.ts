// Core data types for the Resume Reader platform

export interface FreemiumUser {
  id: string
  email: string
  createdAt: Date
  updatedAt: Date
  hasUsedEntrepreneurAssessment: boolean
  hasUsedSkillsAssessment: boolean
  currentRole?: string
  industry?: string
  yearsExperience?: number
  educationLevel?: string
  entrepreneurialInterest?: boolean
}

export interface FreemiumProfile {
  userId: string
  currentRole?: string
  industry?: string
  yearsExperience?: number
  educationLevel?: string
  entrepreneurialInterest?: boolean
}

export interface ClientProfile {
  id?: string
  userId: string
  fullName: string
  email: string
  phone?: string
  resumeText?: string
  resumeFileUrl?: string
  skills: Skill[]
  careerEvents: CareerEvent[]
  education: Education[]
  personalityAssessment?: PersonalityAssessment
  createdAt: Date
  updatedAt: Date
}

export interface Skill {
  id: string
  name: string
  category: string
  experienceLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  yearsExperience: number
  lastUsed: Date
  proficiency: number // 0-100
}

export interface CareerEvent {
  id: string
  type: 'job' | 'promotion' | 'education' | 'certification' | 'project'
  title: string
  company?: string
  startDate: Date
  endDate?: Date
  description?: string
  skills: string[]
  salaryRange?: {
    min: number
    max: number
  }
}

export interface Education {
  id: string
  degree: string
  institution: string
  field: string
  startDate: Date
  endDate?: Date
  gpa?: number
}

export interface PersonalityAssessment {
  id: string
  assessmentType: string
  results: Record<string, any>
  entrepreneurshipScore: number
  riskTolerance: number
  leadershipScore: number
  innovationScore: number
  completedAt: Date
}

export interface ClientSession {
  id: string
  clientId: string
  sessionDate: Date
  duration: number
  sessionType: 'consultation' | 'follow-up' | 'report-review'
  notes?: string
  actionItems: string[]
  nextSteps: string[]
}

export interface GeneratedReport {
  id: string
  clientId: string
  reportType: 'career-analysis' | 'skill-gap' | 'entrepreneurship-readiness'
  generatedAt: Date
  reportData: Record<string, any>
  pdfPath?: string
}

export interface EntrepreneurAssessment {
  email: string
  responses: Record<string, any>
  score: number
  recommendations: string[]
  completedAt: Date
}

export interface SkillsAssessment {
  email: string
  currentRole: string
  industry: string
  yearsExperience: number
  careerGoals?: string
  topSkills: {
    skill: string
    impact: string
    priority: number
  }[]
  completedAt: Date
}

export interface LeadInteraction {
  id: string
  userId: string
  interactionType: 'assessment_completed' | 'email_sent' | 'consultation_scheduled' | 'converted_to_client'
  interactionData?: any
  createdAt: Date
}

export interface DashboardStats {
  totalLeads: number
  totalClients: number
  entrepreneurAssessments: number
  skillsAssessments: number
  conversionRate: number
}