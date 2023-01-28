# Thought Summarization App

## Overview
Code and notebook draft for my article: ["Building a Thought Summarization App with Whisper and GPT3"](https://towardsdatascience.com/building-a-thought-summarization-app-with-whisper-and-gpt-3-90c2d8653faa).

In this repo we implement the code for an app that can record audio, transcribe and sumarize its content.

You can upload an audio directly or record it using the app.

## Setup

# Setup

For setting up this project we will need to.

1. **Install OS-level dependencies (ffmpeg)**
   
On Linux:

```sudo apt update && sudo apt install ffmpeg```

```sudo apt install portaudio19-dev```

On MacOS

```brew install ffmpeg```

On Windows
```chco install ffmpeg```

1. **Create the conda environment**

```conda create -n thought_summarizer python==3.8```

3. Install Python dependencies (pytorch, whisper, pyaudio)

For installing pytorch, make sure that the cuda version is right for your machine,  see instructions [here](https://pytorch.org/). 

```conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia```


Then install the remaining dependencies by running:

```pip install -r requirements.txt```

## Running

To run the app do:

```streamlit run thought_summarization_app.py```



