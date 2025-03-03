import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from '@components/Layout';
import Home from '@pages/Home';
import Login from '@pages/Login';
import Register from '@pages/Register';
import Profile from '@pages/Profile';
import CreatePost from '@pages/CreatePost';
import ProtectedRoute from '@components/ProtectedRoute';

// Create a client
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/profile/:username" element={<Profile />} />
              <Route path="/create" element={<CreatePost />} />
            </Route>
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
