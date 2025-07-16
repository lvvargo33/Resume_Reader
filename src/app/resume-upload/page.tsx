'use client'

import { useState } from 'react'
import Layout from '@/components/Layout'

interface ParsedData {
  fileName: string
  fileSize: number
  parsedAt: string
  textLength: number
  extractedData: {
    name?: string
    email?: string
    phone?: string
    skills: string[]
    experience: any[]
    education: any[]
    summary?: string
  }
}

export default function ResumeUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [parsedData, setParsedData] = useState<ParsedData | null>(null)
  const [error, setError] = useState('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError('')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!file || !email) {
      setError('Please provide both a file and email address')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('email', email)

      const response = await fetch('/api/resume/parse', {
        method: 'POST',
        body: formData
      })

      const result = await response.json()

      if (result.success) {
        setParsedData(result.data)
      } else {
        setError(result.error || 'Failed to parse resume')
      }
    } catch (err) {
      setError('Network error. Please try again.')
      console.error('Upload error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const resetForm = () => {
    setFile(null)
    setEmail('')
    setParsedData(null)
    setError('')
  }

  if (parsedData) {
    return (
      <Layout 
        title="Resume Analysis Complete!" 
        description="Here's what we extracted from your resume"
        showBackButton={true}
        backHref="/resume-upload"
      >
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8">

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              {/* File Info */}
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">File Information</h3>
                <div className="space-y-2 text-sm">
                  <p><span className="font-medium">File:</span> {parsedData.fileName}</p>
                  <p><span className="font-medium">Size:</span> {(parsedData.fileSize / 1024).toFixed(1)} KB</p>
                  <p><span className="font-medium">Text Length:</span> {parsedData.textLength} characters</p>
                </div>
              </div>

              {/* Contact Info */}
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
                <div className="space-y-2 text-sm">
                  <p><span className="font-medium">Name:</span> {parsedData.extractedData.name || 'Not found'}</p>
                  <p><span className="font-medium">Email:</span> {parsedData.extractedData.email || 'Not found'}</p>
                  <p><span className="font-medium">Phone:</span> {parsedData.extractedData.phone || 'Not found'}</p>
                </div>
              </div>
            </div>

            {/* Skills */}
            {parsedData.extractedData.skills.length > 0 && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Detected Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {parsedData.extractedData.skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Experience */}
            {parsedData.extractedData.experience.length > 0 && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Work Experience</h3>
                <div className="space-y-4">
                  {parsedData.extractedData.experience.map((exp, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900">{exp.title}</h4>
                      <p className="text-gray-600">{exp.company}</p>
                      {(exp.startDate || exp.endDate) && (
                        <p className="text-sm text-gray-500">
                          {exp.startDate} - {exp.endDate || 'Present'}
                        </p>
                      )}
                      {exp.description && (
                        <p className="text-sm text-gray-700 mt-2">{exp.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Education */}
            {parsedData.extractedData.education.length > 0 && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Education</h3>
                <div className="space-y-4">
                  {parsedData.extractedData.education.map((edu, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900">{edu.degree}</h4>
                      <p className="text-gray-600">{edu.institution}</p>
                      {edu.field && (
                        <p className="text-sm text-gray-500">{edu.field}</p>
                      )}
                      {(edu.startDate || edu.endDate) && (
                        <p className="text-sm text-gray-500">
                          {edu.startDate} - {edu.endDate || 'Present'}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Summary */}
            {parsedData.extractedData.summary && (
              <div className="mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Summary</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700">{parsedData.extractedData.summary}</p>
                </div>
              </div>
            )}

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">
                📋 Want a Professional Analysis?
              </h3>
              <p className="text-blue-700 mb-4">
                This basic parsing shows what we can extract. For a comprehensive career analysis including:
              </p>
              <ul className="list-disc list-inside text-blue-700 mb-4">
                <li>Detailed skill gap analysis and recommendations</li>
                <li>Career path optimization based on your experience</li>
                <li>Salary benchmarking and negotiation strategies</li>
                <li>Industry-specific insights and opportunities</li>
                <li>Personalized action plan for career advancement</li>
              </ul>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold">
                Schedule a Professional Consultation
              </button>
            </div>

            <div className="flex justify-center space-x-4">
              <button
                onClick={resetForm}
                className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              >
                Upload Another Resume
              </button>
            </div>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout 
      title="Resume Analysis Tool" 
      description="Upload your resume and get instant insights into what employers see"
    >
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8">

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
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

            <div>
              <label htmlFor="resume" className="block text-sm font-medium text-gray-700 mb-2">
                Resume File (Word documents work best)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <svg
                    className="mx-auto h-12 w-12 text-gray-400"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 48 48"
                  >
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      strokeWidth={2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <div className="flex text-sm text-gray-600">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                    >
                      <span>Upload a file</span>
                      <input
                        id="file-upload"
                        name="file-upload"
                        type="file"
                        className="sr-only"
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileChange}
                        required
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">DOC, DOCX, PDF up to 5MB (Word docs work best)</p>
                  {file && (
                    <p className="text-sm text-green-600 mt-2">
                      Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
                    </p>
                  )}
                </div>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || !file || !email}
              className="w-full bg-primary-600 text-white py-3 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Parsing Resume...' : 'Analyze Resume'}
            </button>
          </form>

        </div>
      </div>
    </Layout>
  )
}