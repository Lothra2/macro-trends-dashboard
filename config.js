// Market Intelligence Hub — AI Configuration
// ─────────────────────────────────────────────
// GROK (default): Replace YOUR_GROK_API_KEY with your x.ai key
// GPT-5: Leave blank here — enter in Settings UI when switching providers
// ─────────────────────────────────────────────
window.MIH_CONFIG = {
  defaultProvider: 'grok',
  grok: {
    apiKey: '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',
    model: 'llama-3.3-70b-versatile',
    endpoint: 'https://api.groq.com/openai/v1/chat/completions'
  },
  openai: {
    apiKey: '',
    model: 'gpt-5',
    endpoint: 'https://api.openai.com/v1/chat/completions'
  }
};
