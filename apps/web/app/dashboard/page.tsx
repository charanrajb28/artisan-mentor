'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function DashboardPage() {
  const [username, setUsername] = useState('')
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login') // Redirect to login if not authenticated
    } else {
      // Optionally fetch user details from backend using the token
      // For now, just display a placeholder username
      setUsername('Authenticated User')
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('token_type')
    router.push('/login')
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 text-center">
        <h2 className="text-3xl font-extrabold text-gray-900">
          Welcome, {username}!
        </h2>
        <p className="mt-2 text-sm text-gray-600">
          This is your Artisan Mentor Dashboard.
        </p>
        <div className="mt-6">
          <a
            href="/chat" // Link to the chat page (will be moved from /testing)
            className="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Go to Chat
          </a>
        </div>
        <div className="mt-4">
          <button
            onClick={handleLogout}
            className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  )
}
