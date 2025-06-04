import { ThemeToggle } from '@/components/ui/theme-toggle'

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      {/* Header with theme toggle */}
      <header className="flex justify-between items-center mb-8 py-4">
        <h1 className="text-3xl font-bold text-foreground">
          Visual Prompting Studio
        </h1>
        <ThemeToggle />
      </header>

      {/* Main content */}
      <main className="space-y-6">
        <div className="bg-card text-card-foreground rounded-lg p-6 shadow-sm border">
          <h2 className="text-2xl font-semibold mb-4">Welcome to Visual Prompting Studio</h2>
          <p className="text-muted-foreground">
            AI-powered structured prompt generation for visual media. Use the theme toggle button 
            in the top right to switch between light and dark modes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-card text-card-foreground rounded-lg p-6 shadow-sm border">
            <h3 className="text-xl font-semibold mb-2">Light Mode</h3>
            <p className="text-muted-foreground">
              Clean and bright interface for comfortable daytime use.
            </p>
          </div>
          
          <div className="bg-card text-card-foreground rounded-lg p-6 shadow-sm border">
            <h3 className="text-xl font-semibold mb-2">Dark Mode</h3>
            <p className="text-muted-foreground">
              Easy on the eyes for extended usage and low-light environments.
            </p>
          </div>
        </div>
      </main>
    </div>
  )
} 