from google.cloud import speech_v1p1beta1 as speech
#from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

def transcribe_audio(audio_path):
    client = speech.SpeechClient()

    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    response = client.recognize(config=config, audio=audio)

    # Extract and format the results
    formatted_text = ""
    for result in response.results:
        speaker_tag = result.alternatives[0].transcript
        for word in result.alternatives[0].words:
            speaker_label = "Person {}".format(word.speaker_tag)
            formatted_text += "{}: {}\n".format(speaker_label, speaker_tag)
            break

    return formatted_text

if __name__ == "__main__":
    audio_file_path = "conversation_audio.wav"
    transcription = transcribe_audio(audio_file_path)
    with open("transcription.txt", "w") as file:
        file.write(transcription)
