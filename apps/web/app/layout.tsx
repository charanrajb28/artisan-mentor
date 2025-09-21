import AuthWrapper from '../components/AuthWrapper'; // New import

export const metadata = {
  title: 'Artisan Mentor', // Changed title
  description: 'Your personal creative guide', // Changed description
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthWrapper> {/* Wrap children with AuthWrapper */}
          {children}
        </AuthWrapper>
      </body>
    </html>
  )
}



