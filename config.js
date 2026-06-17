// Market Intelligence Hub — AI Configuration
// ─────────────────────────────────────────────
// GROK (default): Replace YOUR_GROK_API_KEY with your x.ai key
// GPT-5: Leave blank here — enter in Settings UI when switching providers
// ─────────────────────────────────────────────
window.MIH_CONFIG = {
  defaultProvider: 'grok',
  grok: {
    apiKey: 'YOUR_GROK_API_KEY_HERE',
    model: 'grok-3',
    endpoint: 'https://api.x.ai/v1/chat/completions'
  },
  openai: {
    apiKey: '',
    model: 'gpt-5',
    endpoint: 'https://api.openai.com/v1/chat/completions'
  }
};
