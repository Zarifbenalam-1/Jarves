# API Keys Setup Guide

This document explains what each API key is for, how to get it, and how to add it to your `.env` file. Only use your real keys—never share them publicly!

## 1. OPENAI_API_KEY
- **Purpose:** For smart chat, answers, and advanced AI features.
- **How to get:** Sign up at https://platform.openai.com/ and create a free account. Go to API Keys and generate a new key.
- **How to use:** Add to your `.env` file like this:
  OPENAI_API_KEY=your_openai_key_here

## 2. OPENROUTER_API_KEY
- **Purpose:** For using free and community AI models (like GPT-3.5, Mixtral, etc) via OpenRouter.
- **How to get:** Go to https://openrouter.ai/ and sign up. Generate a free API key from your dashboard.
- **How to use:** Add to your `.env` file like this:
  OPENROUTER_API_KEY=your_openrouter_key_here

## 3. DUCKDUCKGO_API_KEY
- **Purpose:** For web search and research features.
- **How to get:** Visit https://duckduckgo.com/developers and follow the instructions for a free API key.
- **How to use:** Add to your `.env` file like this:
  DUCKDUCKGO_API_KEY=your_duckduckgo_key_here

## 4. YTMUSIC_API_KEY
- **Purpose:** For music search and playback.
- **How to get:** See https://ytmusicapi.readthedocs.io/en/latest/ for instructions.
- **How to use:** Add to your `.env` file like this:
  YTMUSIC_API_KEY=your_ytmusic_key_here

---

**Never share your API keys in public repos!**
