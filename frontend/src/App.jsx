import { useState, useEffect } from 'react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { FaTrash, FaCheck, FaPlus, FaUndo } from 'react-icons/fa'
import './index.css'

function App() {
  const [todos, setTodos] = useState([])
  const [newTask, setNewTask] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    setIsLoading(true)
    try {
      const response = await axios.get('http://localhost:5000/todos')
      setTodos(response.data)
    } catch (error) {
      console.error('Error fetching todos:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const addTodo = async (e) => {
    e.preventDefault()
    if (!newTask.trim()) return
    try {
      const response = await axios.post('http://localhost:5000/todos', { task: newTask })
      setTodos([...todos, response.data])
      setNewTask('')
    } catch (error) {
      console.error('Error adding todo:', error)
    }
  }

  const toggleTodo = async (id, completed) => {
    try {
      // Optimistic update for instant feedback
      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, completed: !completed } : todo
      ))
      await axios.put(`http://localhost:5000/todos/${id}`, { completed: !completed })
    } catch (error) {
      console.error('Error updating todo:', error)
      // Revert if error
      fetchTodos()
    }
  }

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/todos/${id}`)
      setTodos(todos.filter(todo => todo.id !== id))
    } catch (error) {
      console.error('Error deleting todo:', error)
    }
  }

  return (
    <div className="app-container">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="todo-card"
      >
        <header>
          <h1>Task Master</h1>
          <p>Get things done, one at a time.</p>
        </header>

        <form onSubmit={addTodo} className="todo-form">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="Add a new task..."
            className="todo-input"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
            className="add-btn"
          >
            <FaPlus />
          </motion.button>
        </form>

        <ul className="todo-list">
          <AnimatePresence mode="popLayout">
            {todos.map(todo => (
              <motion.li
                key={todo.id}
                layout
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.2 }}
                className={`todo-item ${todo.completed ? 'completed' : ''}`}
              >
                <div
                  className="todo-content"
                  onClick={() => toggleTodo(todo.id, todo.completed)}
                >
                  <span className="check-icon">
                    {todo.completed ? <FaUndo /> : <FaCheck />}
                  </span>
                  <span className="todo-text">{todo.task}</span>
                </div>
                <motion.button
                  whileHover={{ scale: 1.2, color: '#ff4444' }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => deleteTodo(todo.id)}
                  className="delete-btn"
                >
                  <FaTrash />
                </motion.button>
              </motion.li>
            ))}
            {todos.length === 0 && !isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="empty-state"
              >
                <p>No tasks yet. Add one above! ✨</p>
              </motion.div>
            )}
          </AnimatePresence>
        </ul>
      </motion.div>
    </div>
  )
}

export default App
