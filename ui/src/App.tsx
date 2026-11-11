import { AppStateProvider } from './context/AppStateContext'
import Home from './pages/Home'


export default function App() {
  return (
    <AppStateProvider>
      <Home />
    </AppStateProvider>
  )
}
