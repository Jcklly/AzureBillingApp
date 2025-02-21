import React from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  // Dummy login handler; in production, call your auth API.
  const handleLogin = () => {
    // Do authentication logic here
    // On success, redirect to dashboard:
    navigate('/dashboard');
  };

  return (
    <div style={styles.container}>
      <h1>Login</h1>
      <p>Please enter your credentials to sign in.</p>
      <button onClick={handleLogin} style={styles.button}>Login</button>
    </div>
  );
};

const styles = {
  container: {
    textAlign: 'center',
    padding: '2rem'
  },
  button: {
    padding: '10px 20px',
    background: '#4e54c8',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  }
};

export default Login;