import requests
import json
import sys

def check_ollama_status():
    """Check if Ollama is running and DeepSeek model is available"""
    print("Checking Ollama status...")
    
    try:
        # Try to get list of models from Ollama
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        
        models = response.json().get("models", [])
        
        print(f"Ollama is running. Available models:")
        for model in models:
            print(f"- {model['name']}")
        
        # Check if DeepSeek is available
        deepseek_available = any("deepseek" in model.get("name", "").lower() for model in models)
        
        if not deepseek_available:
            print("\nDeepSeek model not found. You need to pull it with:")
            print("ollama pull deepseek-r1:1.5b")
        else:
            print("\nDeepSeek model is available and ready to use.")
        
        return deepseek_available
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama server.")
        print("Make sure Ollama is installed and running with 'ollama serve' command.")
        return False
    except Exception as e:
        print(f"Error checking Ollama status: {e}")
        return False

if __name__ == "__main__":
    if check_ollama_status():
        print("\nSystem is ready for AI product search with DeepSeek model.")
    else:
        print("\nPlease ensure Ollama is running and DeepSeek model is installed.")
        sys.exit(1)