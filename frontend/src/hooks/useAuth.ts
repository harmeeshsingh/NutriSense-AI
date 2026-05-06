import { useState, useEffect } from 'react';
import { initGoogleAuth } from '../services/gcip';

export const useAuth = () => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('auth_token'));
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!token);

  useEffect(() => {
    if (!token) {
      initGoogleAuth((response: any) => {
        if (response.credential) {
          // Store token securely. For simplicity in this demo, using localStorage.
          // In production, consider httpOnly cookies.
          localStorage.setItem('auth_token', response.credential);
          setToken(response.credential);
          setIsAuthenticated(true);
        }
      });
    }
  }, [token]);

  const logout = () => {
    localStorage.removeItem('auth_token');
    setToken(null);
    setIsAuthenticated(false);
  };

  return { token, isAuthenticated, logout };
};
