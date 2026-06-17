// Market Intelligence Hub — AI Configuration
// Provider note: the app uses the internal key name "grok",
// but this config points to Groq's OpenAI-compatible API.
// Cache marker: groq-config-2026-06-17-03
(function () {
  const GROQ_STORAGE_KEY = 'MIH_GROQ_API_KEY';
  const OPENAI_STORAGE_KEY = 'MIH_OPENAI_API_KEY';

  window.MIH_CONFIG = {
    defaultProvider: 'grok',
    grok: {
      apiKey: localStorage.getItem(GROQ_STORAGE_KEY) || '',
      model: 'llama-3.3-70b-versatile',
      endpoint: 'https://api.groq.com/openai/v1/chat/completions'
    },
    openai: {
      apiKey: localStorage.getItem(OPENAI_STORAGE_KEY) || '',
      model: 'gpt-5',
      endpoint: 'https://api.openai.com/v1/chat/completions'
    }
  };

  window.MIH_CONFIG_READY = true;
  window.MIH_CONFIG_PROVIDER = 'groq';

  function persistKeysFromSettings() {
    const groqInput = document.getElementById('grok-key-input');
    const openaiInput = document.getElementById('openai-key-input');
    if (groqInput && groqInput.value.trim()) {
      localStorage.setItem(GROQ_STORAGE_KEY, groqInput.value.trim());
      window.MIH_CONFIG.grok.apiKey = groqInput.value.trim();
    }
    if (openaiInput && openaiInput.value.trim()) {
      localStorage.setItem(OPENAI_STORAGE_KEY, openaiInput.value.trim());
      window.MIH_CONFIG.openai.apiKey = openaiInput.value.trim();
    }
    window.MIH_CONFIG.grok.model = 'llama-3.3-70b-versatile';
    window.MIH_CONFIG.grok.endpoint = 'https://api.groq.com/openai/v1/chat/completions';
  }

  window.addEventListener('load', function () {
    const saveButton = document.querySelector('.modal-btn-primary');
    if (saveButton) saveButton.addEventListener('click', persistKeysFromSettings, true);
  });
})();
