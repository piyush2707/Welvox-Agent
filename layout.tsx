'use client';

import React, { ReactNode } from 'react';
import { ClerkProvider } from '@clerk/nextjs';
import '../styles/globals.css';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="description" content="WelvoxAgent - Universal AI Operating System" />
        <title>WelvoxAgent - One AI. Infinite Skills.</title>
      </head>
      <body className="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">
        <ClerkProvider>
          <div className="flex flex-col min-h-screen">
            <header className="border-b border-gray-200 dark:border-gray-800">
              <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg" />
                  <h1 className="text-2xl font-bold">WelvoxAgent</h1>
                </div>
                <div className="flex items-center gap-4">
                  <a href="/docs" className="text-sm font-medium hover:text-blue-600">
                    Docs
                  </a>
                  <a href="/github" className="text-sm font-medium hover:text-blue-600">
                    GitHub
                  </a>
                </div>
              </nav>
            </header>
            <main className="flex-1">{children}</main>
            <footer className="border-t border-gray-200 dark:border-gray-800 py-8">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-600 dark:text-gray-400">
                <p>&copy; 2024 Welvox AI. All rights reserved.</p>
              </div>
            </footer>
          </div>
        </ClerkProvider>
      </body>
    </html>
  );
}
