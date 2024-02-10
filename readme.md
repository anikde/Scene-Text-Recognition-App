# Introduction
This repository shows the use of [Gradio](https://github.com/gradio-app/gradio) as interface to demostrate scene text recognition API developed at IITJ.

**Gradio is very simple to use and it's quite moduler so that anyone can introduce complexity**

# Installation
Create a virtual environment and install necessary pip packages. I have used [coqui-ai's tts](https://github.com/coqui-ai/TTS) for text to speech and it works excelent . 
```
conda create -n stg_app python=3.9
pip install gradio
pip install TTS
```

# Working

Clone the repository
```
cd Scene-Text-Recognition-App
conda activate stg-app
python app.py
```

and the server will start localhost at port 7865. Make to sure to open the port if you are using linux.


