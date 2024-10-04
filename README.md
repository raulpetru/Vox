# Description
Vox is an open source web platform developed with Django for transcribing audio to text.

It uses Django Ninja to allow a client (using a valid API key) to obtain the audio files in order to generate and upload the transcription.

Vox will only host your user's audio files and transcriptions, you do need a client to process transcriptions.

# How to process transcriptions
[VoxComputeTranscription](https://github.com/raulpetru/VoxComputeTranscription) is an example of a simple client that will access the API and process the transcriptions requests. It utilizes WhisperX to generate the transcription from audio files.