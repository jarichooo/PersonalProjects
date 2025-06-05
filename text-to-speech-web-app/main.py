import PyPDF2
import pyttsx3
import wave
import os
import lameenc

mp3_folder = "D:\\Git\\PersonalProjects\\text-to-speech-web-app\\static\\mp3s"
os.makedirs(mp3_folder, exist_ok=True) 

def convert_wav_to_mp3(wav_path, mp3_path):
    with wave.open(wav_path, 'rb') as wav_file:
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        pcm_data = wav_file.readframes(wav_file.getnframes())

    encoder = lameenc.Encoder()
    encoder.set_bit_rate(128)
    encoder.set_in_sample_rate(sample_rate)
    encoder.set_channels(channels)
    encoder.set_quality(2)  

    mp3_data = encoder.encode(pcm_data)
    mp3_data += encoder.flush()

    with open(mp3_path, 'wb') as f:
        f.write(mp3_data)


def extract_text(pdf, start, end, speed=210, fileName=""):
    reader = PyPDF2.PdfReader(pdf)
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    total_pages = len(reader.pages)
    end = min(end, total_pages)

    # pdf name
    pdf_name = os.path.splitext(os.path.basename(pdf))[0]
    fileName = f"{pdf_name}_output.mp3"


    temp_wav = "temp_output.wav"
    engine.setProperty("rate", speed)
    engine.setProperty("voice", voices[1].id)

    text = ""
    for i in range(start, end):
        page = reader.pages[i].extract_text()
        if page:
            text += page + "\n"

    if text:
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()

        path = os.path.join(mp3_folder, fileName)
        convert_wav_to_mp3(temp_wav, path)

        os.remove(temp_wav)