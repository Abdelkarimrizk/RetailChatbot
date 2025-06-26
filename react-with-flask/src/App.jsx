import ChatPopup from './components/ChatPopup'
import FakeHomePage from './components/FakeHome'

function App() {
  return (
    <div className="relative min-h-screen bg-gray-100">
      <FakeHomePage />
      <ChatPopup />
    </div>
  )
}

export default App