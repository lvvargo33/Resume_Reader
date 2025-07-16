-- Resume Reader Database Schema
-- This script creates the initial database schema for the consultant agency model

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================
-- USERS TABLE
-- ==========================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    user_type VARCHAR(20) NOT NULL DEFAULT 'freemium' CHECK (user_type IN ('freemium', 'client')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- FREEMIUM PROFILES TABLE
-- ==========================================
CREATE TABLE freemium_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    current_role VARCHAR(255),
    industry VARCHAR(255),
    years_experience INTEGER,
    education_level VARCHAR(100),
    entrepreneurial_interest BOOLEAN DEFAULT FALSE,
    has_used_entrepreneur_assessment BOOLEAN DEFAULT FALSE,
    has_used_skills_assessment BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- ENTREPRENEUR ASSESSMENTS TABLE
-- ==========================================
CREATE TABLE entrepreneur_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    responses JSONB NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
    recommendations TEXT[],
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- SKILLS ASSESSMENTS TABLE
-- ==========================================
CREATE TABLE skills_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    current_role VARCHAR(255) NOT NULL,
    industry VARCHAR(255) NOT NULL,
    years_experience INTEGER NOT NULL,
    career_goals TEXT,
    top_skills JSONB NOT NULL, -- Array of {skill, impact, priority}
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- CLIENT PROFILES TABLE (for paid clients)
-- ==========================================
CREATE TABLE client_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    resume_text TEXT,
    resume_file_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- SKILLS TABLE
-- ==========================================
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_profile_id UUID NOT NULL REFERENCES client_profiles(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    experience_level VARCHAR(20) NOT NULL CHECK (experience_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
    years_experience INTEGER NOT NULL DEFAULT 0,
    last_used DATE,
    proficiency INTEGER NOT NULL DEFAULT 0 CHECK (proficiency >= 0 AND proficiency <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- CAREER EVENTS TABLE
-- ==========================================
CREATE TABLE career_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_profile_id UUID NOT NULL REFERENCES client_profiles(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('job', 'promotion', 'education', 'certification', 'project')),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    skills_used TEXT[],
    salary_min INTEGER,
    salary_max INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- EDUCATION TABLE
-- ==========================================
CREATE TABLE education (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_profile_id UUID NOT NULL REFERENCES client_profiles(id) ON DELETE CASCADE,
    degree VARCHAR(255) NOT NULL,
    institution VARCHAR(255) NOT NULL,
    field VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    gpa DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- PERSONALITY ASSESSMENTS TABLE
-- ==========================================
CREATE TABLE personality_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_profile_id UUID NOT NULL REFERENCES client_profiles(id) ON DELETE CASCADE,
    assessment_type VARCHAR(100) NOT NULL,
    results JSONB NOT NULL,
    entrepreneurship_score INTEGER CHECK (entrepreneurship_score >= 0 AND entrepreneurship_score <= 100),
    risk_tolerance INTEGER CHECK (risk_tolerance >= 0 AND risk_tolerance <= 100),
    leadership_score INTEGER CHECK (leadership_score >= 0 AND leadership_score <= 100),
    innovation_score INTEGER CHECK (innovation_score >= 0 AND innovation_score <= 100),
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- CLIENT SESSIONS TABLE
-- ==========================================
CREATE TABLE client_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_profile_id UUID NOT NULL REFERENCES client_profiles(id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 60,
    session_type VARCHAR(50) NOT NULL CHECK (session_type IN ('consultation', 'follow-up', 'report-review')),
    notes TEXT,
    action_items TEXT[],
    next_steps TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- GENERATED REPORTS TABLE
-- ==========================================
CREATE TABLE generated_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_profile_id UUID NOT NULL REFERENCES client_profiles(id) ON DELETE CASCADE,
    report_type VARCHAR(50) NOT NULL CHECK (report_type IN ('career-analysis', 'skill-gap', 'entrepreneurship-readiness')),
    report_data JSONB NOT NULL,
    pdf_url VARCHAR(500),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- LEAD INTERACTIONS TABLE
-- ==========================================
CREATE TABLE lead_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL CHECK (interaction_type IN ('assessment_completed', 'email_sent', 'consultation_scheduled', 'converted_to_client')),
    interaction_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================
-- INDEXES FOR PERFORMANCE
-- ==========================================
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_user_type ON users(user_type);
CREATE INDEX idx_freemium_profiles_user_id ON freemium_profiles(user_id);
CREATE INDEX idx_entrepreneur_assessments_user_id ON entrepreneur_assessments(user_id);
CREATE INDEX idx_skills_assessments_user_id ON skills_assessments(user_id);
CREATE INDEX idx_client_profiles_user_id ON client_profiles(user_id);
CREATE INDEX idx_skills_client_profile_id ON skills(client_profile_id);
CREATE INDEX idx_career_events_client_profile_id ON career_events(client_profile_id);
CREATE INDEX idx_education_client_profile_id ON education(client_profile_id);
CREATE INDEX idx_personality_assessments_client_profile_id ON personality_assessments(client_profile_id);
CREATE INDEX idx_client_sessions_client_profile_id ON client_sessions(client_profile_id);
CREATE INDEX idx_generated_reports_client_profile_id ON generated_reports(client_profile_id);
CREATE INDEX idx_lead_interactions_user_id ON lead_interactions(user_id);

-- ==========================================
-- UPDATED_AT TRIGGER FUNCTION
-- ==========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_freemium_profiles_updated_at BEFORE UPDATE ON freemium_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_client_profiles_updated_at BEFORE UPDATE ON client_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==========================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==========================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE freemium_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE entrepreneur_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE skills_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE education ENABLE ROW LEVEL SECURITY;
ALTER TABLE personality_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE generated_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_interactions ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (can be expanded based on security needs)
CREATE POLICY "Users can view their own data" ON users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own data" ON users FOR UPDATE USING (auth.uid() = id);

-- Note: More specific RLS policies should be added based on your security requirements
-- For now, you'll likely need to use the service role key for admin operations