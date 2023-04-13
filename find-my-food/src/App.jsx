import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Layout from './components/Layout'
import Typography from '@mui/material/Typography'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <Layout>
        <Typography variant="h1" color="primary">
          Find My Food
        </Typography>
      </Layout>
    </div>
  )
}

export default App
