import React from 'react';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  // Check for a simple auth token in localStorage (customize as needed)
  const isAuthenticated = localStorage.getItem('authToken');
  if (!isAuthenticated) {
    return <Navigate to='/' />;
  }
  return children;
}

export default ProtectedRoute;
