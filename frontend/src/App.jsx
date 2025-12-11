{/*
###########################################################################
#     I'm In Love With You - The 1975
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-11
########################################################################### */};

{/*
###########################################################################
#
#   region Imports
#
########################################################################### */}

import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';

{/*
###########################################################################
#
#   region Helpers
#
########################################################################### */}

{/*
###########################################################################
#
#   region Program Specific Globals
#
########################################################################### */}

const Dashboard = () => <h2>Dashboard Placeholder</h2>;

{/*
###########################################################################
#
#   region Class Definitions
#
########################################################################### */}

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