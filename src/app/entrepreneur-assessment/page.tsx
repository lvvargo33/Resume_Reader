'use client'

import { useState } from 'react'
import Link from 'next/link'

const questions = [
  {
    id: 'risk-tolerance',
    question: 'How comfortable are you with taking calculated risks?',
    options: [
      { value: 1, label: 'Very uncomfortable - I prefer certainty' },
      { value: 2, label: 'Somewhat uncomfortable - I avoid most risks' },
      { value: 3, label: 'Neutral - I take risks when necessary' },
      { value: 4, label: 'Comfortable - I enjoy calculated risks' },
      { value: 5, label: 'Very comfortable - I thrive on uncertainty' }
    ]
  },
  {
    id: 'leadership',
    question: 'How often do you take leadership roles in projects or teams?',
    options: [
      { value: 1, label: 'Never - I prefer to follow' },
      { value: 2, label: 'Rarely - Only when asked' },
      { value: 3, label: 'Sometimes - When the situation calls for it' },
      { value: 4, label: 'Often - I naturally step up' },
      { value: 5, label: 'Always - I&apos;m always the leader' }
    ]
  },
  {
    id: 'innovation',
    question: 'How do you approach problem-solving?',
    options: [
      { value: 1, label: 'Use proven methods' },
      { value: 2, label: 'Slight modifications to existing solutions' },
      { value: 3, label: 'Mix of old and new approaches' },
      { value: 4, label: 'Creative and original solutions' },
      { value: 5, label: 'Revolutionary new approaches' }
    ]
  },
  {
    id: 'persistence',
    question: 'When facing setbacks, how do you typically respond?',
    options: [
      { value: 1, label: 'Give up quickly' },
      { value: 2, label: 'Try a few times then move on' },
      { value: 3, label: 'Keep trying with some breaks' },
      { value: 4, label: 'Persist until resolved' },
      { value: 5, label: 'Never give up, always find a way' }
    ]
  },
  {
    id: 'networking',
    question: 'How comfortable are you with networking and building relationships?',
    options: [
      { value: 1, label: 'Very uncomfortable - I avoid networking' },
      { value: 2, label: 'Uncomfortable - I network only when required' },
      { value: 3, label: 'Neutral - I network occasionally' },
      { value: 4, label: 'Comfortable - I enjoy meeting new people' },
      { value: 5, label: 'Very comfortable - I actively build networks' }
    ]
  }
]

export default function EntrepreneurAssessment() {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [responses, setResponses] = useState<Record<string, number>>({})
  const [email, setEmail] = useState('')
  const [showResults, setShowResults] = useState(false)
  const [score, setScore] = useState(0)

  const handleResponse = (questionId: string, value: number) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: value
    }))
  }

  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1)
    } else {
      calculateScore()
    }
  }

  const calculateScore = async () => {
    const totalScore = Object.values(responses).reduce((sum, score) => sum + score, 0)
    const maxScore = questions.length * 5
    const percentage = Math.round((totalScore / maxScore) * 100)
    setScore(percentage)
    
    // Save assessment to database
    try {
      const response = await fetch('/api/assessments/entrepreneur', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          responses,
          score: percentage,
          recommendations: generateRecommendations(percentage)
        })
      })
      
      if (!response.ok) {
        console.error('Failed to save assessment')
      }
    } catch (error) {
      console.error('Error saving assessment:', error)
    }
    
    setShowResults(true)
  }
  
  const generateRecommendations = (score: number): string[] => {
    const recommendations: string[] = []
    
    if (score >= 80) {
      recommendations.push('Consider starting your business venture soon')
      recommendations.push('Focus on market research and business plan development')
      recommendations.push('Network with other entrepreneurs and potential investors')
    } else if (score >= 60) {
      recommendations.push('Work on developing stronger leadership skills')
      recommendations.push('Build a larger professional network')
      recommendations.push('Consider taking entrepreneurship courses or workshops')
    } else {
      recommendations.push('Focus on building core business skills')
      recommendations.push('Gain more experience in your current field')
      recommendations.push('Consider starting with a side project to test ideas')
    }
    
    return recommendations
  }

  const getScoreMessage = (score: number) => {
    if (score >= 80) return {
      level: 'High Entrepreneurial Readiness',
      message: 'You show strong entrepreneurial traits! Consider taking the next step.',
      color: 'text-green-600'
    }
    if (score >= 60) return {
      level: 'Moderate Entrepreneurial Readiness',
      message: 'You have good entrepreneurial potential with some areas to develop.',
      color: 'text-yellow-600'
    }
    return {
      level: 'Developing Entrepreneurial Readiness',
      message: 'Focus on building key entrepreneurial skills before starting a business.',
      color: 'text-red-600'
    }
  }

  if (showResults) {
    const scoreInfo = getScoreMessage(score)
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-16">
        <div className="container mx-auto px-4 max-w-2xl">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Your Entrepreneurship Readiness Score
              </h1>
              <div className="text-6xl font-bold text-primary-600 mb-2">
                {score}%
              </div>
              <p className={`text-xl font-semibold ${scoreInfo.color}`}>
                {scoreInfo.level}
              </p>
            </div>
            
            <div className="mb-8">
              <p className="text-gray-600 text-lg text-center">
                {scoreInfo.message}
              </p>
            </div>

            <div className="bg-gray-50 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Want a detailed analysis?
              </h3>
              <p className="text-gray-600 mb-4">
                This free assessment gives you a basic overview. For a comprehensive analysis including:
              </p>
              <ul className="list-disc list-inside text-gray-600 mb-4">
                <li>Detailed entrepreneurial strengths and weaknesses</li>
                <li>Personalized action plan for business readiness</li>
                <li>Industry-specific insights and recommendations</li>
                <li>One-on-one consultation with a career expert</li>
              </ul>
              <button className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-semibold">
                Schedule a Consultation
              </button>
            </div>

            <div className="text-center">
              <Link
                href="/"
                className="text-primary-600 hover:text-primary-700 font-semibold"
              >
                ← Back to Home
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-16">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-bold text-gray-900">
                Entrepreneurship Readiness Assessment
              </h1>
              <span className="text-sm text-gray-500">
                {currentQuestion + 1} of {questions.length}
              </span>
            </div>
            
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
              />
            </div>
          </div>

          {currentQuestion === 0 && Object.keys(responses).length === 0 && (
            <div className="mb-8">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address (to receive your results)
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="your@email.com"
                required
              />
            </div>
          )}

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              {questions[currentQuestion].question}
            </h2>
            
            <div className="space-y-3">
              {questions[currentQuestion].options.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleResponse(questions[currentQuestion].id, option.value)}
                  className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
                    responses[questions[currentQuestion].id] === option.value
                      ? 'border-primary-600 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-between">
            <button
              onClick={() => setCurrentQuestion(prev => prev - 1)}
              disabled={currentQuestion === 0}
              className="px-6 py-2 text-gray-600 hover:text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <button
              onClick={nextQuestion}
              disabled={!responses[questions[currentQuestion].id] || (currentQuestion === 0 && !email)}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {currentQuestion === questions.length - 1 ? 'Get Results' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}