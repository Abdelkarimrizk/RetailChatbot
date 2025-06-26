// src/components/FakeHomePage.jsx
import React from 'react'

const FakeHomePage = () => {
  return (
    <div className="min-h-screen bg-zinc-800 text-white flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-4xl font-bold mb-4">Welcome to FakeStore</h1>
      <p className="text-lg text-zinc-300 max-w-xl">
        <br />
        To learn how to use the site, please visit the{' '}
        <a
          href="https://github.com/Abdelkarimrizk/RetailChatbot#readme"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 underline hover:text-blue-300"
        >
          README
        </a>
        .
      </p>
    </div>
  )
}

export default FakeHomePage
