'use client'

import { useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'

interface AuthWrapperProps {
  children: React.ReactNode;
}

const publicPaths = ['/login', '/register']; // Paths that don't require authentication

const AuthWrapper: React.FC<AuthWrapperProps> = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    
    // If on a public path, no redirection needed
    if (publicPaths.includes(pathname)) {
      return;
    }

    // If no token and not on a public path, redirect to login
    if (!token) {
      router.push('/login');
    }
    // If token exists and on login/register, redirect to dashboard
    else if (token && (pathname === '/login' || pathname === '/register')) {
      router.push('/dashboard');
    }
  }, [pathname, router]);

  return <>{children}</>;
};

export default AuthWrapper;
