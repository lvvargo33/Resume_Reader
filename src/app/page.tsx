import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Unlock Your Career Potential
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Get personalized career guidance and discover if you&apos;re ready for entrepreneurship. 
            Our AI-powered platform analyzes your skills and experience to provide actionable insights.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link
              href="/entrepreneur-assessment"
              className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
            >
              Entrepreneur Readiness Score
            </Link>
            <Link
              href="/skills-assessment"
              className="bg-secondary-600 hover:bg-secondary-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
            >
              Top 3 Skills for Advancement
            </Link>
            <Link
              href="/resume-upload"
              className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors"
            >
              Upload & Analyze Resume
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Career Analysis
            </h3>
            <p className="text-gray-600">
              Deep dive into your career path and identify opportunities for growth and advancement.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Skill Mapping
            </h3>
            <p className="text-gray-600">
              Discover which skills are most valuable in your industry and how to acquire them.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Entrepreneurship Readiness
            </h3>
            <p className="text-gray-600">
              Assess your entrepreneurial potential and get guidance on building your own business.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}