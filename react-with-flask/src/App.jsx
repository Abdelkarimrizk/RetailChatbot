import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [time, setTime] = useState(0)

  useEffect(() => {
    fetch('/api/time')
      .then((res) => res.json())
      .then(data => setTime(data.time))
      }, [])

  return (
    <>
      <div className="time">
        <p>The current time is {new Date(time * 1000).toLocaleString()}</p>
      </div>
    </>
  )
}

export default App
