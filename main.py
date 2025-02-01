import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = ""
FLOW_ID = ""
APPLICATION_TOKEN = os.environ.get("APP_TOKEN", "") # Added default empty string
ENDPOINT = "customer" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    # Construct the API URL for the flow endpoint
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    # Prepare the payload with message and chat configuration
    payload = {
        "input_value": message,
        "output_type": "chat", 
        "input_type": "chat",
    }

    # Set up headers with authentication token
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    # Make POST request to API
    #response = requests.post(api_url, json=payload, headers=headers)
    #return response.json()
    
    # Return parsed JSON response
    return {
        "outputs": [
            {
                "outputs": [
                    {
                        "results": {
                            "message": {
                                "text": "Sample response text"  # This will be replaced with actual API response
                            }
                        }
                    }
                ]
            }
        ]
    }

def main():
    st.title("Chat Interface")
    
    # Add secret key authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        
    if not st.session_state.authenticated:
        secret_key = st.text_input("Enter secret key:", type="password")
        if secret_key == "512":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Please enter the correct secret key to access the chat")
            return
    
    message = st.text_area("Message", placeholder="Ask something...")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()