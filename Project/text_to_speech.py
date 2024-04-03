import requests

def tts_deepgram(text, voice_option, api_key ):
    # Define the API endpoint
    url = f"https://api.deepgram.com/v1/speak?model=aura-{voice_option}-en"


    # Define the headers
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }

    text = f"""{text}"""
    escaped_text = text.replace('"', '\\"')  # Escape double quotes
    escaped_text = escaped_text.replace(".", "...") # adding ellipses inserts a long pause.
    escaped_text = escaped_text.replace("?", "...") 
    # Define the payload
    payload = {
        "text": escaped_text
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content to a file
        with open("your_output_file.mp3", "wb") as f:
            f.write(response.content)
        print("File saved successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

