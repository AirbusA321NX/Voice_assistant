# info_handler.py
import subprocess
import json
import config

def is_information_query(text):
    """Simple check to identify information queries"""
    info_indicators = ["what", "who", "how", "why", "when", "where", "explain", "tell me", "define", "meaning of"]
    text_lower = text.lower().strip()
    return any(text_lower.startswith(indicator) for indicator in info_indicators)

def process_with_ai(text):
    """Send the query to AI for processing"""
    prompt = f"""
You are an intelligent assistant that can determine the best way to answer user queries.
For each query, determine if it requires a web search and generate an appropriate response.

If the query needs current information or factual data, respond with a web search command:
{{"action": "web_search", "query": "appropriate search terms"}}

If the query can be answered with general knowledge or the query is about system commands, respond with:
{{"action": "system_command", "command": "the user's original query"}}

Examples:
Input: "What is the weather today?"
{{"action": "web_search", "query": "current weather"}}

Input: "Who is Elon Musk?"
{{"action": "web_search", "query": "Elon Musk biography"}}

Input: "Open Notepad"
{{"action": "system_command", "command": "Open Notepad"}}

Input: "How to cook pasta?"
{{"action": "web_search", "query": "how to cook pasta step by step"}}

Input: "Define artificial intelligence"
{{"action": "web_search", "query": "definition of artificial intelligence"}}

Input: "What time is it?"
{{"action": "system_command", "command": "What time is it?"}}

Now process this query: "{text}"

Respond ONLY with the JSON format shown above.
"""
    
    try:
        result = subprocess.run(
            ["ollama", "run", config.OLLAMA_MODEL], 
            input=prompt.encode(), 
            capture_output=True,
            timeout=30
        )
        
        output = result.stdout.decode()
        
        # Extract JSON from the output
        try:
            first = output.index("{")
            last = output.rindex("}")
            json_part = output[first:last+1]
            return json.loads(json_part)
        except (ValueError, IndexError):
            # If we can't parse JSON, treat as system command
            return {"action": "system_command", "command": text}
            
    except Exception as e:
        # If AI processing fails, treat as system command
        return {"action": "system_command", "command": text}

def handle_information_request(text):
    """Handle information requests by sending them to AI for processing"""
    if is_information_query(text):
        # Send to AI for determination
        ai_response = process_with_ai(text)
        return ai_response
    return None