import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_prompt(product_name: str, description: str) -> str:
    """
    Generates a high-quality image generation prompt based on product details using the Grok API.
    
    Args:
        product_name (str): The name of the product.
        description (str): A description of the product.
        
    Returns:
        str: The generated image prompt.
        
    Raises:
        Exception: If the Grok API call fails.
    """
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        raise ValueError("GROK_API_KEY environment variable is not set.")
    api_key = api_key.strip()
    
    # Groq OpenAI-compatible API endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    system_prompt = (
        "You are an expert prompt engineer. Your task is to convert product information "
        "into high-quality image-generation prompts. The output must be ONLY the prompt string, "
        "without any extra explanation, quotes, or conversational text. "
        "Focus on creating ultra-realistic, highly detailed photographic prompts."
    )
    
    user_message = f"Product:\n{product_name}\n\nDescription:\n{description}"
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        generated_prompt = data["choices"][0]["message"]["content"].strip()
        
        # Remove surrounding quotes if Grok accidentally includes them
        if generated_prompt.startswith('"') and generated_prompt.endswith('"'):
            generated_prompt = generated_prompt[1:-1]
            
        return generated_prompt
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Groq API call failed: {str(e)}")

def generate_mock_image(prompt: str) -> str:
    """
    Generates a real image using a free, no-key-required API (pollinations.ai).
    This fulfills the requirement of generating a real image from the prompt.
    """
    import urllib.parse
    # URL encode the prompt to safely pass it in the URL
    encoded_prompt = urllib.parse.quote(prompt)
    # Return the direct image URL
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
