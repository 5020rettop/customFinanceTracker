{/*
###########################################################################
#     It's Not Living (If It's Not With You) - The 1975
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

const Login = () => {
  const [ email, setEmail ] = useState('');
  const [ password, setPassword ] = useState('');
  const [ error, setError ] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // create form data
    const formData = new FormData();
    formData.append( 'username', email ); // OAuth2 standard uses 'username' field
    formData.append( 'password', password );

    try {
      // send POST req
      const response = await api.post( '/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      } );

      // save token and redirect to dashboard
      localStorage.setItem( 'token', response.data.access_token );
      navigate( '/dashboard' );
      
    } catch ( err ) {
      setError( 'Invalid email or password' );
      console.error( err );
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto' }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
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

        <button type="submit" style={{ padding: '10px 20px' }}>Login</button>
      </form>
      
      <p>
        REGISTER HERE!@!!!!? <Link to="/signup">Sign up</Link>
      </p>
    </div>
  );
};

export default Login;