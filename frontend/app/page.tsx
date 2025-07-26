"use client";

import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await fetch("http://localhost:8003/kyc", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !loading) {
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full space-y-8">
        <div className="text-center">
          <pre className="text-orange-600 font-mono text-xs sm:text-sm leading-tight mb-8">
{`
    ███████╗████████╗███████╗██╗   ██╗███████╗
    ██╔════╝╚══██╔══╝██╔════╝██║   ██║██╔════╝
    ███████╗   ██║   █████╗  ██║   ██║█████╗  
    ╚════██║   ██║   ██╔══╝  ╚██╗ ██╔╝██╔══╝  
    ███████║   ██║   ███████╗ ╚████╔╝ ███████╗
    ╚══════╝   ╚═╝   ╚══════╝  ╚═══╝  ╚══════╝
`}
          </pre>
          <h1 className="text-2xl sm:text-3xl font-light text-orange-800 mb-4">
            Your AI Assistant
          </h1>
        </div>

        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-orange-200 p-6">
          <div className="space-y-4">
            <label htmlFor="prompt" className="block text-sm font-medium text-orange-700">
              What can I help you with today?
            </label>
            <div className="relative">
              <input
                id="prompt"
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter client name for KYC analysis..."
                className="w-full px-4 py-3 rounded-lg border border-orange-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent outline-none transition-all duration-200 text-gray-800 placeholder-gray-400"
                disabled={loading}
              />
              <button
                onClick={handleSubmit}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-md transition-colors duration-200 text-sm font-medium disabled:opacity-50"
                disabled={!prompt.trim() || loading}
              >
                {loading ? "..." : "Analyze"}
              </button>
            </div>
          </div>
        </div>

        {/* Results Section */}
        {(result || error) && (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-orange-200 p-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <h3 className="text-red-800 font-medium">Error</h3>
                </div>
                <p className="text-red-700 mt-1">{error}</p>
              </div>
            )}
            
            {result && (
              <div>
                <h3 className="text-lg font-medium text-orange-800 mb-4">KYC Analysis Result</h3>
                <div className="bg-gray-50 rounded-lg p-4 border">
                  <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">{result}</pre>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
