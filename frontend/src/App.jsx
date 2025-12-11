import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// We will create these components next
const Login = () => <h2>Login Page Placeholder</h2>;
const Signup = () => <h2>Signup Page Placeholder</h2>;
const Dashboard = () => <h2>Dashboard Placeholder</h2>;

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          {/* default redirect to login */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;