 import sys
import warnings
from pydub import AudioSegment
import os
import shutil
import torch
from TTS.api import TTS

# # Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# # Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
voice_dir = "voices"

LOGO = "images/IITJ_Logo.jpg"
ENGLISH_TIFF = "images/NotoSansMono_Condensed-Regular.ttf"
HINDI_TIFF = "images/NotoSerifDevanagari_Condensed-SemiBold.ttf"

if not sys.warnoptions:
    warnings.simplefilter("ignore")



def join_audio():
    sounds = dict()
    for path in sorted(os.listdir(voice_dir)):
        sounds[path] = AudioSegment.from_wav(os.path.join(voice_dir, path))

    combined_sounds = sum(sounds.values())
    final_file_path = f"{voice_dir}/finised_output.wav"
    combined_sounds.export(final_file_path, format="wav")
    return final_file_path

def clear_folder():
    if os.path.exists(voice_dir):
        shutil.rmtree(voice_dir)

def make_folder():
    if os.path.exists(voice_dir) == False:
        os.mkdir(voice_dir)


def save_voice(text, count, language=None):


    text = [txt["text"] for txt in text]

    words = " ".join(map(str, text))
    
    if language=="devanagari":
        tts.tts_to_file(text=words, speaker="Ana Florence", language="hi", file_path= f"{voice_dir}/{count}-hindi.wav")
    else:
        tts.tts_to_file(text=words, speaker="Ana Florence", language="en", file_path= f"{voice_dir}/{count}-english.wav")

    
def word_center(text):
    bbox = text['bbox']
    x,y,w,h = bbox['x'],bbox['y'], bbox['w'], bbox['h']
    x_center = x + (w // 2)
    y_center = y + (h // 2)

    return x_center, y_center

def get_coordinates(image):
    return image["center"][1], image["center"][0]

def get_sequence(texts):
    # for text in texts:
    #     x, y = word_center(text)
    #     text["center"] = (x, y)
    
    sequence = sorted(texts, key=lambda k: k['line'], reverse=True)
    # for i in range(len(sequence)):
    #     sequence[i]["count"] = i
    return sequence


def calculate_font_size(image_size, standard_image_size, bounding_box_area):
    # Define base font size relative to a standard image size
    base_font_size = 20  # Adjust this as a base font size for a standard image size

    # Calculate font size relative to the image size
    image_ratio = max(image_size) /standard_image_size
    font_size_relative_to_image = int(base_font_size * image_ratio)

    # Adjust font size based on bounding box area (customize this factor based on your requirements)
    bounding_box_factor = 1 + 0.8*(bounding_box_area / (image_size[0] * image_size[1]))  # Adjust this factor as needed
    final_font_size = int(font_size_relative_to_image * bounding_box_factor)

    return final_font_size