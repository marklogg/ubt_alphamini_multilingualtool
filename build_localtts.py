"""
该模块用于创建Mni-Open-Sdk.jar中VoicePool.playLocalTTs()使用的多语言环境mp3文件;
需要客户使用自己的文本转语音接口,将这些文本合成为mp3文件
This module is used to create a multi-language environment mp3 file used by VoicePool.playLocalTTs(...) in Mni-Open-Sdk.jar;

Customers need to use their own text-to-speech interface to synthesize these texts into mp3 files.
"""
import pandas as pd

from build_res_apks import language


def text_to_speech(file: str, text: str) -> bool:
    """
    Customers need to use their own text-to-speech interface to synthesize these texts into mp3 files.

    Take google text-to-speech api as an example: https://cloud.google.com/text-to-speech/docs/libraries?hl=zh_CN#command-line

    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("./build/localTts/output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "./build/localTts/output.mp3"')

    :param file: File name saved to
    :param text: Text to be synthesized
    :return:
    """
    return False


def create_localtts_files(it):
    text = it[language[0]]
    file_name = it["音频文件名称"]
    if text:
        if text_to_speech(file=file_name, text=text):
            print(f"\"{text}\" to speech-file:{file_name}  success!")
        else:
            print(f"failure! Please implement the text-to-speech interface yourself.")


def main():
    t = pd.read_excel(f"./excels/language_localTts.xlsx", header=1)
    print(t.info)
    t.apply(create_localtts_files, axis=1)


if __name__ == '__main__':
    main()
