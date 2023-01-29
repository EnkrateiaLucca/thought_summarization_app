import os
import streamlit as st
import whisper
import pyaudio
import wave
import openai

# get environment path variable OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]
st.title("Thought Summarization App")

model = whisper.load_model("base")

st.write("Whisper Model Loaded!")

# upload audio file with streamlit
# audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

CHANNELS = int(st.sidebar.number_input(label="Channels"))
FORMAT = pyaudio.paInt16
RATE = int(st.sidebar.number_input(label="Rate"))
CHUNK = int(st.sidebar.number_input(label="Chunk"))
THOUGHT_DELAY = int(st.sidebar.number_input(label="Thought Delay (s)"))
temp_audio_file_path = "./output.wav"

if st.sidebar.button("Record Audio"):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    print("Recording thoughts...")
    frames = []


    for i in range(0, int(RATE / CHUNK * THOUGHT_DELAY)):
        data = stream.read(CHUNK)
        frames.append(data)
        

    print("Recording stopped. Writing audio file")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(temp_audio_file_path, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    st.write(f"Audio file written at: {temp_audio_file_path}")
    
    
    
if st.sidebar.button("Transcribe/Summarize Audio"):
    st.write("Transcribing Audio...")
    result = model.transcribe(temp_audio_file_path)
    st.write("Thought Summaries:")
    text = result["text"]
    st.write("Transcription finished, original text: ")
    st.write(text)
    prompt = (f"summarize this text: {text}")
    st.write("Summarizing...")

    # Get a response from GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n =1,
        stop=None,
        temperature=0.5
    )

    # Get the summary from the response
    summary = response.choices[0].text

    # Print the summary
    st.write("Final Summary:")
    st.write(summary)
    
    







