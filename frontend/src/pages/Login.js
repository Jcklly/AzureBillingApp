import React from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // For now, simulate login by navigating directly to the dashboard.
    navigate('/dashboard');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Login</h1>
      <p>Please click the button below to simulate login.</p>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;
