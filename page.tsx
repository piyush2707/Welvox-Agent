'use client';

import React, { useState } from 'react';
import { Button, Card, Input, Spinner } from '@welvox/ui';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function HomePage() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Send to API
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h2 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          One AI. Infinite Skills.
        </h2>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
          WelvoxAgent is a Universal AI Operating System that understands your requests, breaks them
          into subtasks, and executes them with infinite skills.
        </p>
      </motion.div>

      {/* Main Chat Interface */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-2xl mx-auto mb-12"
      >
        <Card className="shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">What can I help you with?</label>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Tell me what you need... (e.g., 'Build my startup website', 'Analyze this CSV file', 'Write a blog post about AI')"
                className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700"
              />
            </div>
            <div className="flex gap-2">
              <Button type="submit" disabled={loading || !input.trim()} className="flex-1">
                {loading ? (
                  <>
                    <Spinner size="sm" />
                    <span className="ml-2">Processing...</span>
                  </>
                ) : (
                  'Submit'
                )}
              </Button>
              <Button variant="secondary" className="flex-1">
                <Link href="/conversations">View Conversations</Link>
              </Button>
            </div>
          </form>
        </Card>
      </motion.div>

      {/* Features Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="grid md:grid-cols-3 gap-8 mb-12"
      >
        {[
          {
            icon: '🤖',
            title: 'Universal Intelligence',
            description: 'Understands any request and routes it to the perfect skill',
          },
          {
            icon: '⚙️',
            title: 'Infinite Skills',
            description: '22+ specialized skills for coding, research, content, and more',
          },
          {
            icon: '🧠',
            title: 'Memory & Context',
            description: 'Maintains conversation history and learns from interactions',
          },
        ].map((feature, i) => (
          <Card key={i} className="text-center">
            <div className="text-5xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
            <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
          </Card>
        ))}
      </motion.div>

      {/* CTA Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-center"
      >
        <div className="bg-gradient-to-r from-blue-600/10 to-purple-600/10 rounded-lg p-8">
          <h3 className="text-2xl font-bold mb-4">Ready to experience infinite AI?</h3>
          <div className="flex gap-4 justify-center">
            <Button>
              <Link href="/dashboard">Launch Dashboard</Link>
            </Button>
            <Button variant="secondary">
              <a href="https://github.com/welvox/agent" target="_blank" rel="noopener noreferrer">
                View on GitHub
              </a>
            </Button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
