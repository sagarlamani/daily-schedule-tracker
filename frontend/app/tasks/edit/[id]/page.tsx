'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'

interface Category {
  id: number
  name: string
  color: string
}

interface Task {
  id: number
  title: string
  description?: string
  category_id: number
  start_time: string
  duration_minutes: number
  priority: string
  is_recurring: boolean
  recurrence_pattern?: string
}

type TimeInputMethod = 'start_duration' | 'start_end'

export default function EditTaskPage() {
  const router = useRouter()
  const params = useParams()
  const taskId = params.id as string
  
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [fetching, setFetching] = useState(true)
  const [timeInputMethod, setTimeInputMethod] = useState<TimeInputMethod>('start_duration')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category_id: 1,
    start_time: '09:00',
    end_time: '09:30',
    duration_hours: 0,
    duration_minutes: 30,
    priority: 'medium',
    is_recurring: false,
    recurrence_pattern: 'daily'
  })

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/auth/login')
      return
    }
    
    fetchTaskAndCategories(token)
  }, [router, taskId])

  const fetchTaskAndCategories = async (token: string) => {
    try {
      const [taskResponse, categoriesResponse] = await Promise.all([
        fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/tasks/${taskId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }),
        fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/categories`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
      ])

      if (taskResponse.ok && categoriesResponse.ok) {
        const taskData = await taskResponse.json()
        const categoriesData = await categoriesResponse.json()
        
        const task = taskData.task
        const hours = Math.floor(task.duration_minutes / 60)
        const minutes = task.duration_minutes % 60
        
        setFormData({
          title: task.title,
          description: task.description || '',
          category_id: task.category_id,
          start_time: task.start_time,
          end_time: calculateEndTime(task.start_time, task.duration_minutes),
          duration_hours: hours,
          duration_minutes: minutes,
          priority: task.priority,
          is_recurring: task.is_recurring,
          recurrence_pattern: task.recurrence_pattern || 'daily'
        })
        
        setCategories(categoriesData.categories || [])
      } else {
        alert('Failed to fetch task data')
        router.push('/dashboard')
      }
    } catch (error) {
      console.error('Error fetching task data:', error)
      alert('Failed to fetch task data')
      router.push('/dashboard')
    } finally {
      setFetching(false)
    }
  }

  // Calculate end time when start time or duration changes
  useEffect(() => {
    if (timeInputMethod === 'start_duration' && formData.start_time) {
      try {
        const startTime = new Date(`2000-01-01T${formData.start_time}:00`)
        if (isNaN(startTime.getTime())) return
        
        const totalMinutes = (formData.duration_hours || 0) * 60 + (formData.duration_minutes || 0)
        if (totalMinutes <= 0) return
        
        const endTime = new Date(startTime.getTime() + totalMinutes * 60000)
        const endTimeString = endTime.toTimeString().slice(0, 5)
        setFormData(prev => ({ ...prev, end_time: endTimeString }))
      } catch (error) {
        console.error('Error calculating end time:', error)
      }
    }
  }, [formData.start_time, formData.duration_hours, formData.duration_minutes, timeInputMethod])

  // Calculate duration when start and end time change
  useEffect(() => {
    if (timeInputMethod === 'start_end' && formData.start_time && formData.end_time) {
      try {
        const startTime = new Date(`2000-01-01T${formData.start_time}:00`)
        const endTime = new Date(`2000-01-01T${formData.end_time}:00`)
        
        if (isNaN(startTime.getTime()) || isNaN(endTime.getTime())) return
        
        const diffMs = endTime.getTime() - startTime.getTime()
        const diffMinutes = Math.floor(diffMs / 60000)
        
        if (diffMinutes > 0) {
          const hours = Math.floor(diffMinutes / 60)
          const minutes = diffMinutes % 60
          setFormData(prev => ({ 
            ...prev, 
            duration_hours: hours,
            duration_minutes: minutes
          }))
        }
      } catch (error) {
        console.error('Error calculating duration:', error)
      }
    }
  }, [formData.start_time, formData.end_time, timeInputMethod])

  const calculateEndTime = (startTime: string, durationMinutes: number) => {
    try {
      if (!startTime || !durationMinutes) return '09:30'
      const start = new Date(`2000-01-01T${startTime}:00`)
      if (isNaN(start.getTime())) return '09:30'
      const end = new Date(start.getTime() + durationMinutes * 60000)
      return end.toTimeString().slice(0, 5)
    } catch (error) {
      return '09:30'
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/auth/login')
      return
    }

    // Validate time inputs
    if (timeInputMethod === 'start_end') {
      const startTime = new Date(`2000-01-01T${formData.start_time}:00`)
      const endTime = new Date(`2000-01-01T${formData.end_time}:00`)
      if (endTime <= startTime) {
        alert('End time must be after start time')
        setLoading(false)
        return
      }
    }

    // Calculate total duration in minutes for backend
    const totalDurationMinutes = formData.duration_hours * 60 + formData.duration_minutes

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          duration_minutes: totalDurationMinutes
        }),
      })

      if (response.ok) {
        alert('Task updated successfully!')
        router.push('/dashboard')
      } else {
        const error = await response.json()
        alert(`Failed to update task: ${error.detail}`)
      }
    } catch (error) {
      console.error('Error updating task:', error)
      alert('Failed to update task. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }))
  }

  const handleTimeInputMethodChange = (method: TimeInputMethod) => {
    setTimeInputMethod(method)
    if (method === 'start_duration') {
      // Reset to current duration when switching
      const totalMinutes = formData.duration_hours * 60 + formData.duration_minutes
      const hours = Math.floor(totalMinutes / 60)
      const minutes = totalMinutes % 60
      setFormData(prev => ({ 
        ...prev, 
        duration_hours: hours,
        duration_minutes: minutes
      }))
    }
  }

  const formatTimeDisplay = (time: string) => {
    if (!time || time === 'NaN:undefined') return 'Invalid time'
    const [hours, minutes] = time.split(':')
    const hour = parseInt(hours)
    if (isNaN(hour)) return 'Invalid time'
    const ampm = hour >= 12 ? 'PM' : 'AM'
    const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour
    return `${displayHour}:${minutes} ${ampm}`
  }

  if (fetching) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Edit Task</h1>
            <p className="text-gray-600 mt-2">Update your task details</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Task Title */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Task Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter task title"
                value={formData.title}
                onChange={handleChange}
              />
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter task description (optional)"
                value={formData.description}
                onChange={handleChange}
              />
            </div>

            {/* Category */}
            <div>
              <label htmlFor="category_id" className="block text-sm font-medium text-gray-700 mb-2">
                Category *
              </label>
              <select
                id="category_id"
                name="category_id"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={formData.category_id}
                onChange={handleChange}
              >
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Time Input Method Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Time Setup *
              </label>
              <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4 mb-4">
                <button
                  type="button"
                  onClick={() => handleTimeInputMethodChange('start_duration')}
                  className={`px-4 py-3 rounded-md text-sm font-medium transition-colors ${
                    timeInputMethod === 'start_duration'
                      ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                      : 'bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200'
                  }`}
                >
                  Start Time + Duration
                </button>
                <button
                  type="button"
                  onClick={() => handleTimeInputMethodChange('start_end')}
                  className={`px-4 py-3 rounded-md text-sm font-medium transition-colors ${
                    timeInputMethod === 'start_end'
                      ? 'bg-blue-100 text-blue-700 border-2 border-blue-300'
                      : 'bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200'
                  }`}
                >
                  Start Time + End Time
                </button>
              </div>
            </div>

            {/* Time and Duration Section */}
            <div className="bg-gray-50 p-4 rounded-lg">
              {/* Start Time */}
              <div className="mb-4">
                <label htmlFor="start_time" className="block text-sm font-medium text-gray-700 mb-2">
                  Start Time *
                </label>
                <div className="flex items-center space-x-3">
                  <input
                    type="time"
                    id="start_time"
                    name="start_time"
                    required
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    value={formData.start_time}
                    onChange={handleChange}
                  />
                  <span className="text-sm text-gray-500">
                    {formatTimeDisplay(formData.start_time)}
                  </span>
                </div>
              </div>

              {/* Duration or End Time */}
              {timeInputMethod === 'start_duration' ? (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Duration *
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label htmlFor="duration_hours" className="block text-xs text-gray-600 mb-1">
                        Hours
                      </label>
                      <input
                        type="number"
                        id="duration_hours"
                        name="duration_hours"
                        min="0"
                        max="12"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        value={formData.duration_hours}
                        onChange={handleChange}
                      />
                    </div>
                    <div>
                      <label htmlFor="duration_minutes" className="block text-xs text-gray-600 mb-1">
                        Minutes
                      </label>
                      <input
                        type="number"
                        id="duration_minutes"
                        name="duration_minutes"
                        min="0"
                        max="59"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        value={formData.duration_minutes}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    Total: {formData.duration_hours}h {formData.duration_minutes}m
                  </div>
                </div>
              ) : (
                <div className="mb-4">
                  <label htmlFor="end_time" className="block text-sm font-medium text-gray-700 mb-2">
                    End Time *
                  </label>
                  <div className="flex items-center space-x-3">
                    <input
                      type="time"
                      id="end_time"
                      name="end_time"
                      required
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      value={formData.end_time}
                      onChange={handleChange}
                    />
                    <span className="text-sm text-gray-500">
                      {formatTimeDisplay(formData.end_time)}
                    </span>
                  </div>
                </div>
              )}

              {/* Time Summary */}
              <div className="bg-white p-3 rounded border">
                <div className="text-sm text-gray-600">
                  <div className="flex justify-between">
                    <span>Start:</span>
                    <span className="font-medium">{formatTimeDisplay(formData.start_time)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>End:</span>
                    <span className="font-medium">{formatTimeDisplay(formData.end_time)}</span>
                  </div>
                  <div className="flex justify-between border-t pt-1 mt-1">
                    <span>Duration:</span>
                    <span className="font-medium">
                      {formData.duration_hours > 0 && `${formData.duration_hours}h `}
                      {formData.duration_minutes}m
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Priority */}
            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                Priority
              </label>
              <select
                id="priority"
                name="priority"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={formData.priority}
                onChange={handleChange}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            {/* Recurring Task */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_recurring"
                name="is_recurring"
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                checked={formData.is_recurring}
                onChange={handleChange}
              />
              <label htmlFor="is_recurring" className="ml-2 block text-sm text-gray-900">
                Recurring task
              </label>
            </div>

            {formData.is_recurring && (
              <div>
                <label htmlFor="recurrence_pattern" className="block text-sm font-medium text-gray-700 mb-2">
                  Recurrence Pattern
                </label>
                <select
                  id="recurrence_pattern"
                  name="recurrence_pattern"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={formData.recurrence_pattern}
                  onChange={handleChange}
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
            )}

            {/* Submit Buttons */}
            <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-4 pt-6">
              <Link
                href="/dashboard"
                className="px-6 py-3 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base font-medium text-center"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 text-sm sm:text-base font-medium"
              >
                {loading ? 'Updating...' : 'Update Task'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
} 