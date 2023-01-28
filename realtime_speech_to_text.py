#!/usr/bin/env python
# coding: utf-8

# # Building a Thought Summarization App
# 
# In this article I will show you how to build a simple app to transcribe and 
# summarize recordings of rambling thoughts directly from an audio file or in realtime.

# ![](thoughts_map.png)

# # Why Summarize Thoughts?
# 
# I often think about note taking, knowledge management, and topics that touch upon the topics of recording, transforming, and processing thoughts and ideas.
# 
# My interest in these topics is probably a mix of personal struggles with organizing my own thoughts, and partially related to my obsession with ever evolving
# 
# this ideal automation system for living, a sort of human learning automata that I often see myself becoming (in my wildest and childest dreams).
# 
# Now, as for the general importance of summarizing thoughts, I would argue the following. As far as bringing an idea into reality, the current methods we have to transcribe ultra fast flows
# 
# of thought are at best arcaic, they in no menas capture the speed and dynamics of the free flow nature of thinking, coming up with ideas and having them dance around in our minds.
# 
# Basically when we write by typing or hand writing, we slow everything down, which in one sense can be extremely beneficial, because it makes use reflect more carefully about what we are thinking, 
# however on the other side, it does what it does, makes us think slower, at a rate that our brains dont want to tolerate.
# 
# If I am solving a hard problem I indeed want to be slower, and taking notes and slowing down is the very opposite of a hindrance, however for bringin flows of ideas to life, we need something better.
# 
# Its not new this idea of recording your thoughts, many writes have done it. The new thing is that we the advent of large language models like chatgpt, we now have amazing tools to allow us to navigate these thoughts more efficiently than ever before.
# 
# ONe can just think and record these thoughts as they are spoken, and then, have a set of models take care of the storing, processing and indexing of those thoughts to make them quickly avialable upon request at later time when inspiration calls.
# 
# 
# So, let's look at how we could leverage current open source technologies plus Large Language Models made available by OpenAI, to build a tool to facilitate this workflow of streaming thoughts.
# 

# # Steps to Build a Thought Summarizer App
# 
# First things first, lets define the steps for building a thought summarization app.
# 
# 1. Setup
# 2. Import dependencies
# 3. Record audio
# 4. Transcribe audio
# 5. Summarize transcribed text
# 6. Organize and present thoughts

# Now, let's go through each of these steps in detail.

# # Setup
# 
# For setting up this project we will need to.
# 
# 1. **Install OS-level dependencies (ffmpeg)**
#    
# On Linux:
# 
# ```sudo apt update && sudo apt install ffmpeg```
# 
# On MacOS
# 
# ```brew install ffmpeg```
# 
# On Windows
# ```chco install ffmpeg```
# 
# 2. **Create the conda environment**
# 
# ```conda create -n thought_summarizer python==3.8```
# 
# 3. Install Python dependencies (pytorch, whisper, pyaudio)
# 
# For installing pytorch, make sure that the cuda version is right for your machine.
# 
# ```conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia```
# 
# Install Whisper:
# 
# ```pip install git+https://github.com/openai/whisper.git -q```
# 
# Install Pyaudio
# (On Linux do this first: 
# 
# ```sudo apt install portaudio19-dev```
# 
# Then,
# ```pip install pyaudio```

# 

# 2. Import dependencies:
# 
# Import whisper, pyaudio, wave and time.

# In[6]:


import pyaudio
import whisper
import time
import wave


# 3. Record audio:
# 
# Use PyAudio to open a stream and record audio for a specified amount of time and
# save the recorded audio as a wav file.

# In[11]:


CHANNELS = 1
FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 1024
# Record for 20 seconds
time_recording = 20

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
print("Start recording")
frames = []

seconds = 10
for i in range(0, int(RATE / CHUNK * seconds)):
    data = stream.read(CHUNK)
    frames.append(data)
    

print("Recording stopped")
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("output.wav", "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# 5. Transcribe audio:
# 
# Load a base model using `whisper.load_model()`, use the model to transcribe the recorded audio file and optionally write the transcribed text to a text file.

# In[7]:


# Load the whisper model
model = whisper.load_model("base.en")


# In[8]:


write_text_file = False
audio_file_path = "./output.wav"

result = model.transcribe(audio_file_path)
if write_text_file==True:    
    with open("captions.txt", "w+") as f:
        f.write(result["text"])

print(result["text"])


# 6. Summarize transcribed text:
# 
# Use GPT-3 or the ChatGPT demo (API coming soon!) to summarize the transcribed text and extract key thoughts. 
# 
# Below I show the output using the ChatGPT demo:

# ![](2023-01-26-19-14-30.png)

# And now, let's look at the GPT-3 output using the official OpenAI API.

# In[9]:


import openai

# Apply the API key
openai.api_key = "YOUR API KEY"

# Define the prompt for GPT-3
text = result["text"]
prompt = (f"summarize this text: {text}")

# Get a response from GPT-3
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1024,
    n =1,
    stop=None,
    temperature=0.5
)

# Get the summary from the response
summary = response.choices[0].text

# Print the summary
print(summary)


# As expected the summary produced by ChatGPT is far superior, but overall,
# the summary provided by both is quite usable.

# 7. Organize and present thoughts
# 
# As for the final step, this could be organizing these chunk thoughts into a database so that one could easily search them.  
# 
# Organize the thoughts and notes in a meaningful way
# Create an outline for the article or video
# Experiment with the thought-database/search idea (embedding?) (in context search of thoughts?)
# Using ChatGPT to suggest actionable things based on thoughts and notes.

# 8. Conclusion:
# 
# Summarize the steps taken to build the thought summarization app
# Explain the key takeaways and any future work to be done

# 
# 
# 
# Remaining tasks:
# - Do the gpt3 version of the summary and compare with the chatgpt one
# - Organize the setup and the parts of the article/video
# - Write the article outline
# - Experiment with the thought-database/search idea (embedding?) (in context search of thoughts?)
# - Using ChatGPT to suggest actionable things based on thoughts and notes. Something like "based of these notes I wrote" what you think I should write about next weekend that would encapsulate some of these ideas?
