# Install the Deepgram Python SDK
# pip install deepgram-sdk

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from deepgram_captions import DeepgramConverter, srt

# AUDIO_FILE = "./your_output_file.mp3"


def transcribe_audio(AUDIO_FILE):
    try:
        deepgram = DeepgramClient("20207dc1ad783424a8d45ad34d28a9af532a1314")

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # print(response.to_json(indent=4))

        # with open("output.json", "w") as file:
        #     file.write(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

    return response

def srt_from_transcription(dg_response):   
    transcription = DeepgramConverter(dg_response)
    captions = srt(transcription)
    # print(captions)
    with open("subtitling.txt", "w") as file:
        file.write(captions)


# dg_response = transcribe_audio(AUDIO_FILE)
# srt_from_transcription(dg_response)


