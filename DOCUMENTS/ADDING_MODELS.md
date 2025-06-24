# How to Add AI Models to Jarvis-X

This guide explains how to add new AI models, providers, and customize the model selection system.

## 🔧 Adding New Models

### Step 1: Add Model Configuration

Open `/assistant/ai_engine.py` and find the `self.available_models` dictionary. Add your new model:

```python
"Your Model Name (Provider)": {
    "provider": "provider_name",           # openrouter, openai, huggingface, etc.
    "model_id": "actual/model/identifier", # The API model ID
    "endpoint": "https://api.url/endpoint", # API endpoint URL
    "price": "$0.001/1K tokens",           # Pricing info
    "free_tier": "Description of free tier" # Free tier details
}
```

### Step 2: Add Provider Support (if new)

If you're adding a new provider, create a new method in the `JarvisAI` class:

```python
def _chat_newprovider(self, message, system_prompt, model_config):
    """Handle NewProvider API calls"""
    if not self.newprovider_key:
        return "Error: NewProvider API key not found. Please add it to your .env file."
        
    headers = {
        "Authorization": f"Bearer {self.newprovider_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_config["model_id"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(model_config["endpoint"], headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
```

### Step 3: Update the Chat Method

Add your new provider to the `chat` method:

```python
elif model_config["provider"] == "newprovider":
    return self._chat_newprovider(message, system_prompt, model_config)
```

### Step 4: Add API Key Support

Add the API key to your `.env` file:
```
NEWPROVIDER_API_KEY=your_key_here
```

And load it in the `__init__` method:
```python
self.newprovider_key = os.getenv('NEWPROVIDER_API_KEY')
```

## 🏢 Current Providers

### OpenRouter (Recommended)
- **Pros**: Many free models, single API key, consistent format
- **Cons**: Some models have usage limits
- **Setup**: Get key from https://openrouter.ai/
- **Models**: 50+ models including Llama, Gemma, Phi-3, etc.

### OpenAI (Direct)
- **Pros**: Latest GPT models, high quality
- **Cons**: Paid after trial, more expensive
- **Setup**: Get key from https://platform.openai.com/
- **Models**: GPT-3.5, GPT-4, GPT-4o Mini

### How to Add More Providers:

#### Hugging Face
```python
"Llama-2 7B (HuggingFace)": {
    "provider": "huggingface",
    "model_id": "meta-llama/Llama-2-7b-chat-hf",
    "endpoint": "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf",
    "price": "FREE",
    "free_tier": "Rate limited"
}
```

#### Anthropic Claude
```python
"Claude 3 Sonnet (Anthropic)": {
    "provider": "anthropic",
    "model_id": "claude-3-sonnet-20240229",
    "endpoint": "https://api.anthropic.com/v1/messages",
    "price": "$0.003/1K tokens",
    "free_tier": "Trial credits"
}
```

#### Local Models (Ollama)
```python
"Llama-3 8B (Local)": {
    "provider": "ollama",
    "model_id": "llama3:8b",
    "endpoint": "http://localhost:11434/v1/chat/completions",
    "price": "FREE",
    "free_tier": "Completely free (local)"
}
```

## 📋 Model Categories

### Completely FREE Models:
- Llama-3.1 8B (OpenRouter)
- Llama-3 8B (OpenRouter)
- Gemma 2 9B (OpenRouter)
- Phi-3 Mini (OpenRouter)
- Qwen 2 7B (OpenRouter)

### Free Credits Models:
- OpenHermes 2.5 Mistral (OpenRouter)
- Gemini Pro (OpenRouter)
- Claude 3 Haiku (OpenRouter)
- GPT-3.5 Turbo (OpenAI)
- GPT-4o Mini (OpenAI)

### Local Models (Setup Required):
- Any Ollama model
- Any LM Studio model
- Any llama.cpp model

## 🎯 Model Selection Strategy

### For Beginners:
1. Start with **Llama-3.1 8B** (completely free)
2. Try **Phi-3 Mini** for faster responses
3. Use **Gemma 2 9B** for balanced performance

### For Advanced Users:
1. **OpenHermes 2.5** for uncensored responses
2. **Claude 3 Haiku** for reasoning tasks
3. **GPT-4o Mini** for best quality (paid)

### For Developers:
1. Set up **Ollama** for local development
2. Use **Hugging Face** for experimentation
3. Multiple providers for redundancy

## 🔍 Finding New Models

### OpenRouter Discovery:
1. Visit https://openrouter.ai/models
2. Look for models marked "Free"
3. Copy the model ID and add to Jarvis-X

### Hugging Face Discovery:
1. Visit https://huggingface.co/models
2. Filter by "Text Generation"
3. Look for models with API inference enabled

### Local Model Discovery:
1. Check https://ollama.ai/library
2. Run `ollama list` to see available models
3. Use `ollama run model_name` to test

## ⚙️ Advanced Configuration

### Custom Model Parameters:
```python
"Custom Model": {
    "provider": "custom",
    "model_id": "custom-model-id",
    "endpoint": "https://api.custom.com/v1/chat",
    "price": "Custom pricing",
    "free_tier": "Custom tier",
    "max_tokens": 2000,        # Custom max tokens
    "temperature": 0.8,        # Custom temperature
    "custom_headers": {        # Custom headers if needed
        "X-Custom-Header": "value"
    }
}
```

### Model Aliases:
You can create shorter names for models:
```python
"Llama-3": "Llama-3.1 8B (OpenRouter)",  # Alias
```

### Model Descriptions:
Add detailed descriptions:
```python
"description": "Fast, efficient model for general chat and coding tasks"
```

## 🚀 Testing New Models

1. **Add the model** to `available_models`
2. **Restart Jarvis-X**: `python main.py`
3. **Type `models`** to see your new model
4. **Test basic chat**: "Hello, who are you?"
5. **Test personalities**: Switch modes and test responses
6. **Test error handling**: Try invalid requests

## 📝 Model Documentation Template

When adding models, document them:

```markdown
### Model Name (Provider)
- **Type**: Chat/Instruct/Code/etc.
- **Size**: 7B/13B/70B parameters
- **Strengths**: What it's good at
- **Weaknesses**: What to avoid
- **Use Cases**: Best scenarios
- **Cost**: Free/Paid pricing
- **Speed**: Response time
- **Quality**: Output quality rating
```

## 🛠️ Troubleshooting

### Model Not Appearing:
- Check syntax in `available_models`
- Restart Jarvis-X completely
- Check for Python errors in terminal

### API Errors:
- Verify API key in `.env` file
- Check model ID spelling
- Verify endpoint URL
- Test with curl/Postman first

### Response Issues:
- Check model provider documentation
- Verify request format matches API
- Test with minimal example first

---

**Remember**: Always test new models thoroughly before adding them to production!
