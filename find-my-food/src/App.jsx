import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Layout from './components/Layout'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <Layout title="Find My Food">
      </Layout>
    </div>
  )
}

export default App
