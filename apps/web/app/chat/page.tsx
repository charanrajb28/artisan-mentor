'use client'

import { useState, useEffect } from 'react'
import { Send, User, Bot, PlusCircle, MessageSquare, Mic, MicOff } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { useRouter } from 'next/navigation'

interface ChatMessage {
  sender: string
  text: string
  time: string
  timestamp?: string
}

interface ChatSession {
  id: number
  title: string
  owner_id: number
  created_at: string
  messages: ChatMessage[]
}

// Declare SpeechRecognition globally
declare global {
  interface Window {
    SpeechRecognition: any
    webkitSpeechRecognition: any
  }
}

export default function MentorChat() {
  const [mentorPrompt, setMentorPrompt] = useState('')
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  const [mentorLoading, setMentorLoading] = useState(false)
  const [mentorError, setMentorError] = useState<string | null>(null)
  const [chatSessionId, setChatSessionId] = useState<number | null>(null)
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([])
  const [isListening, setIsListening] = useState(false)
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null)

  const router = useRouter()

  // Initialize SpeechRecognition in the browser only
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition
      if (SpeechRecognition) {
        const recog = new SpeechRecognition()
        recog.continuous = false
        recog.interimResults = false
        recog.lang = 'en-US'

        recog.onresult = (event: SpeechRecognitionEvent) => {
          const transcript = event.results[0][0].transcript
          setMentorPrompt(transcript)
          setIsListening(false)
        }

        recog.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error)
          setIsListening(false)
          setMentorError('Voice input error. Please try again.')
        }

        recog.onend = () => setIsListening(false)
        setRecognition(recog)
      }
    }
  }, [])

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
      return
    }

    const fetchChatSessions = async () => {
      try {
        const res = await fetch('http://localhost:8000/chat/chats', {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (!res.ok) throw new Error('Failed to fetch chat sessions')
        const data: ChatSession[] = await res.json()
        setChatSessions(data)
        if (data.length > 0) {
          setChatSessionId(data[0].id)
          setChatHistory(
            data[0].messages.map((msg) => ({
              sender: msg.sender,
              text: msg.text,
              time: msg.timestamp
                ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            }))
          )
        } else {
          setChatHistory([
            {
              sender: 'mentor',
              text: "👋 Welcome! I'm your Artisan Mentor. Ask me about design, creativity, or growth.",
              time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            },
          ])
        }
      } catch (error: any) {
        setMentorError(error.message || 'Failed to load chat sessions')
        router.push('/login')
      }
    }

    fetchChatSessions()
  }, [router])

  const toggleListening = () => {
    if (!recognition) {
      setMentorError('Speech recognition not supported in your browser.')
      return
    }
    if (isListening) {
      recognition.stop()
      setIsListening(false)
    } else {
      setMentorError(null)
      recognition.start()
      setIsListening(true)
    }
  }

  const createNewChatSession = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return router.push('/login')

    try {
      const res = await fetch('http://localhost:8000/chat/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title: `New Chat ${chatSessions.length + 1}` }),
      })
      if (!res.ok) throw new Error('Failed to create new chat session')
      const newSession: ChatSession = await res.json()
      setChatSessions((prev) => [...prev, newSession])
      setChatSessionId(newSession.id)
      setChatHistory([
        {
          sender: 'mentor',
          text: "👋 Welcome! I'm your Artisan Mentor. Ask me about design, creativity, or growth.",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ])
    } catch (error: any) {
      setMentorError(error.message || 'Failed to create new chat session')
    }
  }

  const loadChatSession = async (sessionId: number) => {
    const token = localStorage.getItem('access_token')
    if (!token) return router.push('/login')

    try {
      const res = await fetch(`http://localhost:8000/chat/chats/${sessionId}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!res.ok) throw new Error('Failed to load chat session')
      const session: ChatSession = await res.json()
      setChatSessionId(session.id)
      setChatHistory(
        session.messages.map((msg) => ({
          sender: msg.sender,
          text: msg.text,
          time: msg.timestamp
            ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }))
      )
    } catch (error: any) {
      setMentorError(error.message || 'Failed to load chat session')
    }
  }

  const saveChatMessage = async (sessionId: number, message: ChatMessage) => {
    const token = localStorage.getItem('access_token')
    if (!token) return router.push('/login')
    try {
      await fetch(`http://localhost:8000/chat/chats/${sessionId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ sender: message.sender, text: message.text }),
      })
    } catch (error: any) {
      console.error('Error saving message:', error)
    }
  }

  const getMentorAdvisory = async () => {
    if (!mentorPrompt.trim() || !chatSessionId) return
    setMentorLoading(true)
    setMentorError(null)

    const userMessage: ChatMessage = {
      sender: 'user',
      text: mentorPrompt,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }

    setChatHistory((prev) => [...prev, userMessage])
    await saveChatMessage(chatSessionId, userMessage)

    try {
      const token = localStorage.getItem('access_token')
      if (!token) throw new Error('Authentication token not found. Please log in.')

      const res = await fetch(`http://127.0.0.1:8000/mentor/advise`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ prompt: mentorPrompt, chat_id: chatSessionId }),
      })
      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || errorData.message || 'Failed to get mentor advisory')
      }

      const data = await res.json()
      const mentorMessage: ChatMessage = {
        sender: 'mentor',
        text: data.response,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      }

      setChatHistory((prev) => [...prev, mentorMessage])
      await saveChatMessage(chatSessionId, mentorMessage)
      setMentorPrompt('')
    } catch (error: any) {
      setMentorError(error.message || 'An unknown error occurred')
      if (
        error.message.includes('Authentication token not found') ||
        error.message.includes('Could not validate credentials')
      ) {
        router.push('/login')
      }
    } finally {
      setMentorLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-blue-300 flex p-4">
      {/* Sidebar */}
      <div className="w-64 bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col mr-4">
        <div className="bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Chats</h2>
          <button onClick={createNewChatSession} className="p-1 rounded-full hover:bg-white hover:bg-opacity-20 transition">
            <PlusCircle className="h-6 w-6" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-2">
          {chatSessions.map((session) => (
            <button
              key={session.id}
              onClick={() => loadChatSession(session.id)}
              className={`w-full text-left p-2 rounded-lg flex items-center gap-2 ${
                chatSessionId === session.id ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'
              }`}
            >
              <MessageSquare className="h-5 w-5" />
              <span className="text-sm font-medium truncate">{session.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Chat */}
      <div className="flex-1 w-full max-w-2xl bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col">
        <div className="bg-gradient-to-r from-blue-700 to-blue-900 text-white p-4 flex items-center gap-3">
          <Bot className="h-7 w-7" />
          <div>
            <h1 className="text-lg font-semibold">Artisan Mentor</h1>
            <p className="text-sm opacity-80">Your personal creative guide</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {chatHistory.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-sm px-4 py-2 rounded-2xl shadow-md relative ${
                  msg.sender === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-white border text-gray-800 rounded-bl-none'
                }`}
              >
                {msg.sender === 'mentor' && <Bot className="absolute -top-3 -left-3 h-6 w-6 text-blue-700 bg-white rounded-full shadow-md" />}
                {msg.sender === 'user' && <User className="absolute -top-3 -right-3 h-6 w-6 text-blue-600 bg-white rounded-full shadow-md" />}
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{msg.text}</ReactMarkdown>
                </div>
                <span className="block text-xs opacity-70 mt-1 text-right">{msg.time}</span>
              </div>
            </div>
          ))}
          {mentorLoading && <div className="text-gray-500 text-sm animate-pulse">Mentor is thinking...</div>}
          {mentorError && <div className="text-red-500 text-sm">Error: {mentorError}</div>}
        </div>

        <div className="border-t bg-white flex items-center p-3">
          <input
            type="text"
            value={mentorPrompt}
            onChange={(e) => setMentorPrompt(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && getMentorAdvisory()}
            placeholder="Ask your mentor..."
            className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            disabled={mentorLoading || chatSessionId === null}
          />
          <button
            onClick={toggleListening}
            disabled={mentorLoading || chatSessionId === null || !recognition}
            className={`ml-2 p-2 rounded-full shadow-lg transition ${isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'} text-white`}
          >
            {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
          </button>
          <button
            onClick={getMentorAdvisory}
            disabled={mentorLoading || chatSessionId === null}
            className="ml-2 bg-blue-700 hover:bg-blue-800 text-white p-2 rounded-full shadow-lg transition"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>

        <div className="bg-gray-100 text-xs text-gray-600 p-2 text-center">
          💡 Try asking: "How can I grow as a creative?" or "Give me a minimal design idea."
        </div>
      </div>
    </div>
  )
}
