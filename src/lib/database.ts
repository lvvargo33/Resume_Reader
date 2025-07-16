import { supabase } from './supabase'
import type { 
  FreemiumUser, 
  EntrepreneurAssessment, 
  SkillsAssessment,
  ClientProfile,
  Skill,
  CareerEvent,
  Education,
  PersonalityAssessment,
  ClientSession,
  GeneratedReport
} from '@/types'

// ==========================================
// FREEMIUM USER OPERATIONS
// ==========================================

export async function createFreemiumUser(email: string, profileData?: Partial<FreemiumUser>) {
  try {
    // First, create or get user
    const { data: user, error: userError } = await supabase
      .from('users')
      .upsert([
        { email, user_type: 'freemium' }
      ], { 
        onConflict: 'email',
        ignoreDuplicates: false 
      })
      .select()
      .single()

    if (userError) throw userError

    // Create freemium profile if it doesn't exist
    const { data: profile, error: profileError } = await supabase
      .from('freemium_profiles')
      .upsert([
        { 
          user_id: user.id,
          current_role: profileData?.currentRole,
          industry: profileData?.industry,
          years_experience: profileData?.yearsExperience,
          education_level: profileData?.educationLevel,
          entrepreneurial_interest: profileData?.entrepreneurialInterest
        }
      ], { 
        onConflict: 'user_id',
        ignoreDuplicates: false 
      })
      .select()
      .single()

    if (profileError) throw profileError

    return { user, profile }
  } catch (error) {
    console.error('Error creating freemium user:', error)
    throw error
  }
}

export async function getFreemiumUser(email: string) {
  try {
    const { data, error } = await supabase
      .from('users')
      .select(`
        *,
        freemium_profiles (*),
        entrepreneur_assessments (*),
        skills_assessments (*)
      `)
      .eq('email', email)
      .eq('user_type', 'freemium')
      .single()

    if (error) throw error
    return data
  } catch (error) {
    console.error('Error fetching freemium user:', error)
    throw error
  }
}

// ==========================================
// ENTREPRENEUR ASSESSMENT OPERATIONS
// ==========================================

export async function saveEntrepreneurAssessment(
  email: string,
  assessmentData: Omit<EntrepreneurAssessment, 'email'>
) {
  try {
    // Get or create user
    const { user } = await createFreemiumUser(email)
    
    // Save assessment
    const { data, error } = await supabase
      .from('entrepreneur_assessments')
      .insert([
        {
          user_id: user.id,
          responses: assessmentData.responses,
          score: assessmentData.score,
          recommendations: assessmentData.recommendations,
          completed_at: new Date().toISOString()
        }
      ])
      .select()
      .single()

    if (error) throw error

    // Update profile to mark assessment as completed
    await supabase
      .from('freemium_profiles')
      .update({ has_used_entrepreneur_assessment: true })
      .eq('user_id', user.id)

    // Log interaction
    await logLeadInteraction(user.id, 'assessment_completed', {
      assessment_type: 'entrepreneur',
      score: assessmentData.score
    })

    return data
  } catch (error) {
    console.error('Error saving entrepreneur assessment:', error)
    throw error
  }
}

// ==========================================
// SKILLS ASSESSMENT OPERATIONS
// ==========================================

export async function saveSkillsAssessment(
  email: string,
  assessmentData: Omit<SkillsAssessment, 'email'>
) {
  try {
    // Get or create user
    const { user } = await createFreemiumUser(email, {
      currentRole: assessmentData.currentRole,
      industry: assessmentData.industry,
      yearsExperience: assessmentData.yearsExperience
    })
    
    // Save assessment
    const { data, error } = await supabase
      .from('skills_assessments')
      .insert([
        {
          user_id: user.id,
          current_role: assessmentData.currentRole,
          industry: assessmentData.industry,
          years_experience: assessmentData.yearsExperience,
          career_goals: assessmentData.careerGoals || null,
          top_skills: assessmentData.topSkills,
          completed_at: new Date().toISOString()
        }
      ])
      .select()
      .single()

    if (error) throw error

    // Update profile to mark assessment as completed
    await supabase
      .from('freemium_profiles')
      .update({ has_used_skills_assessment: true })
      .eq('user_id', user.id)

    // Log interaction
    await logLeadInteraction(user.id, 'assessment_completed', {
      assessment_type: 'skills',
      role: assessmentData.currentRole,
      industry: assessmentData.industry
    })

    return data
  } catch (error) {
    console.error('Error saving skills assessment:', error)
    throw error
  }
}

// ==========================================
// CLIENT MANAGEMENT OPERATIONS
// ==========================================

export async function createClientProfile(email: string, profileData: Omit<ClientProfile, 'id' | 'userId' | 'email' | 'createdAt' | 'updatedAt'>) {
  try {
    // First, create or update user as client
    const { data: user, error: userError } = await supabase
      .from('users')
      .upsert([
        { email, user_type: 'client' }
      ], { 
        onConflict: 'email',
        ignoreDuplicates: false 
      })
      .select()
      .single()

    if (userError) throw userError

    // Create client profile
    const { data: profile, error: profileError } = await supabase
      .from('client_profiles')
      .insert([
        {
          user_id: user.id,
          full_name: profileData.fullName,
          phone: profileData.phone,
          resume_text: profileData.resumeText,
          resume_file_url: profileData.resumeFileUrl
        }
      ])
      .select()
      .single()

    if (profileError) throw profileError

    return { user, profile }
  } catch (error) {
    console.error('Error creating client profile:', error)
    throw error
  }
}

export async function getClientProfile(email: string) {
  try {
    const { data, error } = await supabase
      .from('users')
      .select(`
        *,
        client_profiles (*),
        skills (*),
        career_events (*),
        education (*),
        personality_assessments (*),
        client_sessions (*),
        generated_reports (*)
      `)
      .eq('email', email)
      .eq('user_type', 'client')
      .single()

    if (error) throw error
    return data
  } catch (error) {
    console.error('Error fetching client profile:', error)
    throw error
  }
}

export async function getAllClients() {
  try {
    const { data, error } = await supabase
      .from('users')
      .select(`
        *,
        client_profiles (*),
        client_sessions (*)
      `)
      .eq('user_type', 'client')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  } catch (error) {
    console.error('Error fetching all clients:', error)
    throw error
  }
}

// ==========================================
// LEAD MANAGEMENT OPERATIONS
// ==========================================

export async function getAllLeads() {
  try {
    const { data, error } = await supabase
      .from('users')
      .select(`
        *,
        freemium_profiles (*),
        entrepreneur_assessments (*),
        skills_assessments (*),
        lead_interactions (*)
      `)
      .eq('user_type', 'freemium')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  } catch (error) {
    console.error('Error fetching all leads:', error)
    throw error
  }
}

export async function logLeadInteraction(
  userId: string,
  interactionType: 'assessment_completed' | 'email_sent' | 'consultation_scheduled' | 'converted_to_client',
  interactionData?: any
) {
  try {
    const { data, error } = await supabase
      .from('lead_interactions')
      .insert([
        {
          user_id: userId,
          interaction_type: interactionType,
          interaction_data: interactionData
        }
      ])
      .select()
      .single()

    if (error) throw error
    return data
  } catch (error) {
    console.error('Error logging lead interaction:', error)
    throw error
  }
}

// ==========================================
// ANALYTICS AND REPORTING
// ==========================================

export async function getDashboardStats() {
  try {
    const [
      { count: totalLeads },
      { count: totalClients },
      { count: entrepreneurAssessments },
      { count: skillsAssessments }
    ] = await Promise.all([
      supabase.from('users').select('*', { count: 'exact', head: true }).eq('user_type', 'freemium'),
      supabase.from('users').select('*', { count: 'exact', head: true }).eq('user_type', 'client'),
      supabase.from('entrepreneur_assessments').select('*', { count: 'exact', head: true }),
      supabase.from('skills_assessments').select('*', { count: 'exact', head: true })
    ])

    const leadsCount = totalLeads || 0
    const clientsCount = totalClients || 0
    
    return {
      totalLeads: leadsCount,
      totalClients: clientsCount,
      entrepreneurAssessments: entrepreneurAssessments || 0,
      skillsAssessments: skillsAssessments || 0,
      conversionRate: leadsCount > 0 ? (clientsCount / leadsCount) * 100 : 0
    }
  } catch (error) {
    console.error('Error fetching dashboard stats:', error)
    throw error
  }
}