'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Task {
  id: number
  title: string
  description?: string
  start_time: string
  duration_minutes: number
  category: string
  priority: string
  is_completed: boolean
  completed_at?: string
}

interface Streak {
  id: number
  streak_type: string
  current_streak: number
  longest_streak: number
  last_completed_date: string
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [streaks, setStreaks] = useState<Streak[]>([])
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      window.location.href = '/auth/login'
      return
    }

    fetchDashboardData(token)
    
    // Refresh data every 30 seconds to keep it updated
    const interval = setInterval(() => {
      fetchDashboardData(token)
    }, 30000)

    return () => clearInterval(interval)
  }, [])

  const fetchDashboardData = async (token: string) => {
    try {
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }

              const [tasksResponse, streaksResponse] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/tasks`, { headers }),
          fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/streaks`, { headers })
        ])

      if (tasksResponse.ok) {
        const tasksData = await tasksResponse.json()
        setTasks(tasksData.tasks || [])
      }

      if (streaksResponse.ok) {
        const streaksData = await streaksResponse.json()
        setStreaks(streaksData.streaks || [])
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.href = '/'
  }

  const handleCompleteTask = async (taskId: number, isCompleted: boolean) => {
    const token = localStorage.getItem('token')
    if (!token) return

    try {
      const endpoint = isCompleted ? 'uncomplete' : 'complete'
              const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/tasks/${taskId}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        // Refresh the dashboard data
        fetchDashboardData(token)
      } else {
        alert('Failed to update task status')
      }
    } catch (error) {
      console.error('Error updating task:', error)
      alert('Failed to update task status')
    }
  }

    const handleDeleteTask = async (taskId: number) => {
    const token = localStorage.getItem('token')
    if (!token) return

    // Confirm deletion
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        // Refresh the dashboard data
        fetchDashboardData(token)
      } else {
        alert('Failed to delete task')
      }
    } catch (error) {
      console.error('Error deleting task:', error)
      alert('Failed to delete task')
    }
  }

  const formatTimeDisplay = (time: string) => {
    if (!time || time === 'NaN:undefined' || time === 'Invalid time') return 'Invalid time'
    try {
      const [hours, minutes] = time.split(':')
      const hour = parseInt(hours)
      if (isNaN(hour) || isNaN(parseInt(minutes))) return 'Invalid time'
      const ampm = hour >= 12 ? 'PM' : 'AM'
      const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour
      return `${displayHour}:${minutes} ${ampm}`
    } catch (error) {
      return 'Invalid time'
    }
  }

  const calculateEndTime = (startTime: string, durationMinutes: number) => {
    if (!startTime || !durationMinutes) return 'Invalid time'
    
    try {
      // Handle time format like "09:00", "9:00", or "09:00:00"
      let formattedStartTime = startTime
      
      // If it's already in HH:MM:SS format, use it as is
      if (startTime.includes(':')) {
        const parts = startTime.split(':')
        if (parts.length === 3) {
          // Already has seconds, use as is
          formattedStartTime = startTime
        } else if (parts.length === 2) {
          // Has hours and minutes, add seconds
          formattedStartTime = `${startTime}:00`
        }
      } else {
        // Handle edge cases
        formattedStartTime = `${startTime}:00`
      }
      
      const start = new Date(`2000-01-01T${formattedStartTime}`)
      
      if (isNaN(start.getTime())) return 'Invalid time'
      
      const end = new Date(start.getTime() + durationMinutes * 60000)
      const endTimeString = end.toTimeString().slice(0, 5)
      
      // Validate the calculated end time
      if (endTimeString === 'Invalid Date' || endTimeString.includes('NaN')) {
        return 'Invalid time'
      }
      
      return endTimeString
    } catch (error) {
      return 'Invalid time'
    }
  }

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    if (hours > 0) {
      return `${hours}h ${mins}m`
    }
    return `${mins}m`
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center py-3 sm:py-6 space-y-3 sm:space-y-0">
            <h1 className="text-xl sm:text-3xl font-bold text-gray-900">Dashboard</h1>
            <div className="flex flex-wrap items-center gap-2 sm:gap-4 w-full sm:w-auto">
              <button
                onClick={() => {
                  const token = localStorage.getItem('token')
                  if (token) fetchDashboardData(token)
                }}
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded border hover:bg-gray-50 text-sm sm:text-base"
              >
                Refresh
              </button>
              <Link 
                href="/tasks/new"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm sm:text-base"
              >
                Add Task
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-600 hover:text-gray-900 text-sm sm:text-base"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-3 sm:gap-8">
          {/* Today's Tasks */}
          <div className="lg:col-span-2">
                          <div className="bg-white rounded-lg shadow p-4 sm:p-6">
                <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Today's Tasks</h2>
              {tasks.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500 mb-4">No tasks scheduled for today</p>
                  <Link 
                    href="/tasks/new"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md text-sm sm:text-base font-medium"
                  >
                    Create Your First Task
                  </Link>
                </div>
              ) : (
                <div className="space-y-2 sm:space-y-3">
                  {tasks.map((task) => (
                    <div key={task.id} className={`border rounded-lg p-3 sm:p-4 ${task.is_completed ? 'bg-green-50 border-green-200' : ''}`}>
                      <div className="flex flex-col sm:flex-row justify-between items-start space-y-2 sm:space-y-0">
                        <div className="flex-1 w-full">
                          <div className="flex flex-col sm:flex-row sm:items-center space-y-1 sm:space-y-0 sm:space-x-2">
                            <h3 className={`font-medium text-sm sm:text-base ${task.is_completed ? 'line-through text-gray-500' : ''}`}>
                              {task.title}
                            </h3>
                            {task.is_completed && (
                              <span className="text-green-600 text-xs sm:text-sm">✓ Completed</span>
                            )}
                          </div>
                          {task.description && (
                            <p className={`text-xs sm:text-sm mt-1 ${task.is_completed ? 'text-gray-400' : 'text-gray-600'}`}>
                              {task.description}
                            </p>
                          )}
                          <div className="flex flex-wrap items-center gap-2 mt-2 text-sm text-gray-500">
                            <span>{formatTimeDisplay(task.start_time)}</span>
                            <span className="hidden sm:inline">→</span>
                            <span className="sm:hidden">-</span>
                            <span>{formatTimeDisplay(calculateEndTime(task.start_time, task.duration_minutes))}</span>
                            <span className="text-xs">({formatDuration(task.duration_minutes)})</span>
                            <span className="capitalize text-xs">{task.category}</span>
                          </div>
                        </div>
                        <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-2 w-full sm:w-auto">
                          <span className={`px-2 py-1 rounded text-xs font-medium self-start ${
                            task.priority === 'high' ? 'bg-red-100 text-red-800' :
                            task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {task.priority}
                          </span>
                          <div className="flex flex-wrap gap-2 w-full sm:w-auto">
                            <Link
                              href={`/tasks/edit/${task.id}`}
                              className="flex-1 sm:flex-none px-3 py-2 rounded text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors text-center"
                            >
                              Edit
                            </Link>
                            <button
                              onClick={() => handleCompleteTask(task.id, task.is_completed)}
                              className={`flex-1 sm:flex-none px-3 py-2 rounded text-sm font-medium transition-colors text-center ${
                                task.is_completed
                                  ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                  : 'bg-green-600 text-white hover:bg-green-700'
                              }`}
                            >
                              {task.is_completed ? 'Undo' : 'Complete'}
                            </button>
                            <button
                              onClick={() => handleDeleteTask(task.id)}
                              className="flex-1 sm:flex-none px-3 py-2 rounded text-sm font-medium bg-red-600 text-white hover:bg-red-700 transition-colors text-center"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Streaks */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-4 sm:p-6">
              <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Your Streaks</h2>
              {streaks.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500">No streaks yet</p>
                  <p className="text-sm text-gray-400 mt-1">Complete tasks to build streaks!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {streaks.map((streak) => (
                    <div key={streak.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="font-medium capitalize">{streak.streak_type} Streak</h3>
                          <p className="text-2xl font-bold text-blue-600">{streak.current_streak}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-500">Longest</p>
                          <p className="font-medium">{streak.longest_streak}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 