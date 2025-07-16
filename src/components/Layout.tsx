'use client'

import Navigation from './Navigation'

interface LayoutProps {
  children: React.ReactNode
  title?: string
  description?: string
  showBackButton?: boolean
  backHref?: string
}

export default function Layout({ 
  children, 
  title, 
  description, 
  showBackButton = false, 
  backHref = '/' 
}: LayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        {(title || showBackButton) && (
          <div className="mb-8">
            {showBackButton && (
              <a
                href={backHref}
                className="inline-flex items-center text-primary-600 hover:text-primary-700 font-semibold mb-4 transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Back
              </a>
            )}
            {title && (
              <div className="text-center">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                  {title}
                </h1>
                {description && (
                  <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                    {description}
                  </p>
                )}
              </div>
            )}
          </div>
        )}
        
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-16">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="bg-primary-600 text-white p-2 rounded-lg">
                  <span className="text-lg font-bold">RR</span>
                </div>
                <div>
                  <h3 className="text-lg font-bold">Resume Reader</h3>
                  <p className="text-sm text-gray-400">Career Guidance Platform</p>
                </div>
              </div>
              <p className="text-gray-400 text-sm">
                Unlock your career potential with personalized guidance and AI-powered insights.
              </p>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold mb-4">Free Tools</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="/entrepreneur-assessment" className="text-gray-400 hover:text-white transition-colors">Entrepreneur Readiness Score</a></li>
                <li><a href="/skills-assessment" className="text-gray-400 hover:text-white transition-colors">Skills Assessment</a></li>
                <li><a href="/resume-upload" className="text-gray-400 hover:text-white transition-colors">Resume Analysis</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold mb-4">Professional Services</h4>
              <ul className="space-y-2 text-sm">
                <li><span className="text-gray-400">Career Consultation</span></li>
                <li><span className="text-gray-400">Resume Optimization</span></li>
                <li><span className="text-gray-400">Interview Preparation</span></li>
                <li><span className="text-gray-400">Salary Negotiation</span></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center">
            <p className="text-gray-400 text-sm">
              © 2025 Resume Reader. All rights reserved. Built with 💻 for career success.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}