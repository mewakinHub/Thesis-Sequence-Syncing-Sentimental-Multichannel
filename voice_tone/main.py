import requests
import librosa
import soundfile as sf
from dotenv import load_dotenv
import os

# Function to get access token using OAuth2 client credentials
def get_access_token(api_key, api_secret):
    """Obtain an access token from Hume AI API."""
    url = "https://api.hume.ai/oauth2-cc/token"
    auth = (api_key, api_secret)
    data = {'grant_type': 'client_credentials'}
    
    try:
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        if not access_token:
            raise ValueError("Access token not found in the response.")
        return access_token
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        return None

def slice_and_analyze(audio_file, api_key, api_secret, slice_duration):
    """
    Slices an audio file into segments and analyzes each segment for emotions using the Hume AI API.

    Args:
        audio_file (str): Path to the audio file.
        api_key (str): Your Hume AI API key.
        api_secret (str): Your Hume AI API secret key.
        slice_duration (int, optional): Duration of each audio slice in seconds. Defaults to 1.

    Returns:
        list: A list of tuples, where each tuple contains a timestamp and the detected emotions.
    """
    # Get access token using the client credentials
    access_token = get_access_token(api_key, api_secret)
    if not access_token:
        print("Failed to obtain access token. Exiting.")
        return []

    # Load the audio file
    try:
        audio, sr = librosa.load(audio_file, sr=None)  # Load the audio at its original sample rate
    except Exception as e:
        raise ValueError(f"Error loading audio file: {e}")
    
    # Calculate the number of slices
    audio_duration = librosa.get_duration(y=audio, sr=sr)
    num_slices = int(audio_duration / slice_duration)

    results = []

    for i in range(num_slices):
        start_time = i * slice_duration
        end_time = (i + 1) * slice_duration

        # Slice the audio
        audio_slice = audio[int(start_time * sr):int(end_time * sr)]

        # Save the slice as a temporary WAV file
        temp_file = "temp_slice.wav"
        try:
            sf.write(temp_file, audio_slice, sr)
        except Exception as e:
            print(f"Error saving temporary slice: {e}")
            continue

        # Send the slice to Hume AI for analysis
        with open(temp_file, "rb") as f:
            try:
                response = requests.post(
                    url="https://api.hume.ai/v0/evi/analyze", 
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json; charset=utf-8"
                    },
                    files={"audio": f}
                )

                if response.status_code == 200:
                    # Parse emotions from the API response
                    emotions = response.json().get("emotions", "No emotions found")
                    results.append((start_time, emotions))
                else:
                    print(f"API error for slice at {start_time}s: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error sending request to Hume AI: {e}")

        # Remove the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return results


# Example usage
if __name__ == "__main__":
    load_dotenv()
    # Replace with your actual API key and secret
    api_key = os.getenv("API_KEY")  
    api_secret = os.getenv("API_SECRET")
    audio_file = "sound/negative (sad) - markiplier - sound.wav"  # Replace with the path to your audio file
    slice_duration = 1  # Duration of each audio slice in seconds

    try:
        results = slice_and_analyze(audio_file, api_key, api_secret, slice_duration)

        for timestamp, emotions in results:
            print(f"Timestamp: {timestamp:.2f}s, Emotions: {emotions}")
    except Exception as e:
        print(f"Error during analysis: {e}")
