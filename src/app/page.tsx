import Layout from '@/components/Layout'
import Link from 'next/link'

export default function Home() {
  return (
    <Layout>
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Unlock Your Career Potential
        </h1>
        <p className="text-xl text-gray-600 mb-12 max-w-4xl mx-auto">
          Get personalized career guidance and discover if you&apos;re ready for entrepreneurship. 
          Our AI-powered platform analyzes your skills and experience to provide actionable insights.
        </p>
        
        {/* Action Cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-6xl mx-auto mb-16">
          <Link href="/entrepreneur-assessment" className="group">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-primary-200 h-full">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors">
                Entrepreneur Readiness
              </h3>
              <p className="text-gray-600 mb-6">
                Take our 5-question assessment to discover your entrepreneurial potential and get personalized recommendations.
              </p>
              <div className="bg-primary-600 group-hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                Get Your Score →
              </div>
            </div>
          </Link>

          <Link href="/skills-assessment" className="group">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-secondary-200 h-full">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-secondary-600 transition-colors">
                Skills Assessment
              </h3>
              <p className="text-gray-600 mb-6">
                Discover the top 3 skills that will accelerate your career advancement in your specific role and industry.
              </p>
              <div className="bg-secondary-600 group-hover:bg-secondary-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                Find My Skills →
              </div>
            </div>
          </Link>

          <Link href="/resume-upload" className="group">
            <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-green-200 h-full">
              <div className="text-4xl mb-4">📄</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-green-600 transition-colors">
                Resume Analysis
              </h3>
              <p className="text-gray-600 mb-6">
                Upload your resume for AI-powered analysis. Get insights into your skills, experience, and career potential.
              </p>
              <div className="bg-green-600 group-hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                Analyze Resume →
              </div>
            </div>
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Why Choose Resume Reader?
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Our platform combines AI technology with personalized consulting to help you make informed career decisions.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="bg-blue-100 text-blue-600 p-4 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Instant Results</h3>
            <p className="text-gray-600 text-sm">Get immediate insights with our free assessment tools</p>
          </div>

          <div className="text-center">
            <div className="bg-green-100 text-green-600 p-4 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Personalized</h3>
            <p className="text-gray-600 text-sm">Tailored recommendations based on your unique profile</p>
          </div>

          <div className="text-center">
            <div className="bg-purple-100 text-purple-600 p-4 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Expert Guidance</h3>
            <p className="text-gray-600 text-sm">Professional consultation for detailed career planning</p>
          </div>

          <div className="text-center">
            <div className="bg-orange-100 text-orange-600 p-4 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Data-Driven</h3>
            <p className="text-gray-600 text-sm">AI-powered analysis based on industry trends and data</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl shadow-xl p-8 md:p-12 text-center text-white">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Ready to Accelerate Your Career?
        </h2>
        <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
          Start with our free assessments and discover actionable insights for your career growth.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/entrepreneur-assessment"
            className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
          >
            Start Free Assessment
          </Link>
          <Link
            href="/resume-upload"
            className="border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
          >
            Upload Resume
          </Link>
        </div>
      </div>
    </Layout>
  )
}