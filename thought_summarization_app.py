import streamlit as st
import whisper
import pyaudio
import wave
import openai


openai.api_key = "Your API KEY"
st.title("Thought Summarization App")

model = whisper.load_model("base")

st.write("Whisper Model Loaded!")

# upload audio file with streamlit
# audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

CHANNELS = st.sidebar.number_input(label="Channels")
FORMAT = pyaudio.paInt16
RATE = st.sidebar.number_input(label="Rate")
CHUNK = st.sidebar.number_input(label="Chunk")
THOUGHT_DELAY = st.sidebar.number_input(label="Thought Delay (s)")
temp_audio_file_path = "./audo_sample.m4a"

if st.sidebar.button("Record Audio"):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    print("Recording thoughts...")
    frames = []


    for i in range(0, int(RATE / CHUNK * THOUGHT_DELAY)):
        data = stream.read(CHUNK)
        frames.append(data)
        

    print("Recording stopped. Now starting transcription...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(temp_audio_file_path, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    
if st.sidebar.button("Transcribe/Summarize Audio"):
    result = model.transcribe(temp_audio_file_path)
    st.write("Thought Summaries:")
    text = result["text"]
    prompt = (f"summarize this text: {text}")

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
    st.write(summary)

    #st.write(result["text"])
    
    







