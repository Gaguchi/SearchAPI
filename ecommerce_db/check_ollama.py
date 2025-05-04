import requests
import json
import sys

def check_ollama_status():
    """Check if Ollama is running and Gemma 3 model is available"""
    print("Checking Ollama status...")
    
    try:
        # Try to get list of models from Ollama
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        
        models = response.json().get("models", [])
        
        print(f"Ollama is running. Available models:")
        for model in models:
            print(f"- {model['name']}")
        
        # Check if Gemma 3 is available (check both "gemma:3" and "gemma3:latest")
        gemma3_available = any(("gemma:3" in model.get("name", "") or "gemma3" in model.get("name", "")) for model in models)
        
        if not gemma3_available:
            print("\nGemma 3 model not found. You need to pull it with:")
            print("ollama pull gemma:3")
        else:
            print("\nGemma 3 model is available and ready to use.")
        
        return gemma3_available
        
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to Ollama server.")
        print("Make sure Ollama is installed and running with 'ollama serve' command.")
        return False
    except Exception as e:
        print(f"Error checking Ollama status: {e}")
        return False

if __name__ == "__main__":
    if check_ollama_status():
        print("\nSystem is ready for AI product search with Gemma 3.")
    else:
        print("\nPlease ensure Ollama is running and Gemma 3 model is installed.")
        sys.exit(1)