import requests
import json
import sys

class CyberLLMAnalyst:
    """
    A local LLM client using Ollama to analyze security logs and alerts.
    This demonstrates the power of self-hosting LLMs (privacy-preserving) 
    to assist Security Operations Center (SOC) analysts.
    """
    
    def __init__(self, model="llama3.2"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.system_prompt = "You are an expert Cybersecurity Analyst. Review the following logs and provide a brief assessment of potential threats, prioritizing concise and actionable insights."
        
    def check_connection(self):
        try:
            requests.get(f"{self.base_url}/api/tags", timeout=5)
            return True
        except:
            return False

    def analyze_log(self, log_content):
        if not self.check_connection():
            print("[!] Cannot connect to local Ollama instance. Make sure it's running on localhost:11434.")
            return

        print(f"[*] Sending log to {self.model} for analysis...")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Analyze this log:\\n{log_content}"}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            analysis = data.get("message", {}).get("content", "")
            
            print("\\n=== LLM Analysis ===")
            print(analysis)
            print("====================\\n")
            
        except Exception as e:
            print(f"[!] Error analyzing log: {e}")

if __name__ == "__main__":
    analyst = CyberLLMAnalyst()
    
    suspicious_log = """
    Oct 07 10:15:32 server sshd[1234]: Failed password for root from 192.168.1.100 port 55432 ssh2
    Oct 07 10:15:34 server sshd[1234]: Failed password for root from 192.168.1.100 port 55432 ssh2
    Oct 07 10:15:36 server sshd[1234]: Failed password for root from 192.168.1.100 port 55432 ssh2
    Oct 07 10:15:38 server sshd[1234]: Accepted password for root from 192.168.1.100 port 55432 ssh2
    """
    
    print("Log to analyze:\\n", suspicious_log)
    analyst.analyze_log(suspicious_log)
