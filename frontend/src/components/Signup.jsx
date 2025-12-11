{/*
###########################################################################
#     The Sound - The 1975
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-12
########################################################################### */};

{/*
###########################################################################
#
#   region Imports
#
########################################################################### */}
import { useState } from 'react';
import api from '../api/axios';
import { useNavigate, Link } from 'react-router-dom';

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

{/*
###########################################################################
#
#   region Class Definitions
#
########################################################################### */}

const Signup = () => {
  const [ email, setEmail ] = useState('');
  const [ password, setPassword ] = useState('');
  const [ error, setError ] = useState('');
  const [ success, setSuccess ] = useState( false );
  const navigate = useNavigate();

  const handleSubmit = async ( e ) => {
    e.preventDefault();
    setError('');

    try {
      // Send json data
      await api.post( '/signup', {
        email: email,
        password: password
      } );
      
      setSuccess( true );
      // redirect to login fallback
      setTimeout( () => navigate( '/login' ), 2000 );
      
    } catch ( err ) {
      // error if email already exists
      if ( err.response && err.response.data && err.response.data.detail ) {
        setError( err.response.data.detail );
      } else { // generic error
        setError( 'Signup failed. Please try again.' );
      }
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Sign Up</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>Account created! Redirecting to login...</p>}
      
      {!success && (
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label>Email:</label>
            <input 
              type="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              required 
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          
          <div style={{ marginBottom: '1rem' }}>
            <label>Password:</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
              style={{ width: '100%', padding: '8px' }}
            />
          </div>

          <button type="submit" style={{ padding: '10px 20px' }}>Create Account</button>
        </form>
      )}
      
      <p>
        SKIBIIDIIIIIIIII? <Link to="/login">Login</Link>
      </p>
    </div>
  );
};

export default Signup;