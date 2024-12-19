import { createRoot } from 'react-dom/client'
import './index.css'
import AppWithRouter from './App.jsx'
import { AuthProvider } from "./Views/AuthContext"; // Import the provider

createRoot(document.getElementById('root')).render(

  <AuthProvider>
    <AppWithRouter />
  </AuthProvider>,

)
