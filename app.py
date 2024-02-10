import requests
import gradio as gr
from PIL import ImageDraw, ImageFont, Image

import gradio_utils as ut
from theme import Seafoam
import timeit


def get_response(img):

	url = "http://10.6.0.36:8000/endtoend/"  
	file = {'images': open(img, "rb")}

	starttime = timeit.default_timer()
	response = requests.post(url, files=file)

	time_response = timeit.default_timer() - starttime
	jresponse = response.json()
	

	count = 1
	all_words = []
	hindi_words = []
	english_words = []
	ut.clear_folder()
	ut.make_folder()

	for regions in jresponse[0]["regions"]:
		
		if regions['lang'] == "devanagari":
			if len(regions["label"]) != 0:
				entry = {
					"text": regions["label"],
					"language": "devanagri",
					"count": count,
					"line": regions["line"]
					}

				hindi_words.append(entry)
			else: continue


		else:	

			if len(regions["label"]) != 0:
				entry = {
					"text": regions["label"],
					"language": "English",
					"count": count,
					"line": regions["line"]
					}

				english_words.append(entry)
			else: continue
	h_words = []
	e_words = []

	starttime = timeit.default_timer()
	if len(hindi_words) != 0:
		h_words = ut.get_sequence(hindi_words)
		ut.save_voice(h_words, count, "devanagari")
		count += 1
	
	if len(english_words) != 0:
		e_words = ut.get_sequence(english_words)
		ut.save_voice(e_words, count)
	
	tts_time = timeit.default_timer() - starttime


	words = h_words + e_words
	words = [text["text"] for text in words]
	words = " ".join(words)
	timings = f"detection_time = {time_response} \ntts_time = {tts_time}"

	file_path = ut.join_audio()
	return words, file_path
	# return image, h_words+e_words 



if __name__ == "__main__":
	server = "0.0.0.0"
	port = 7865
	seafoam = Seafoam()

	interface_html = """
    <div style="text-align: center;">
        <img src="https://iitj.ac.in/uploaded_docs/IITJ%20Logo__big.jpg" alt="Logo" style="width: 100px; height: 100px; float: left;">
		<img src="https://play-lh.googleusercontent.com/_FXSr4xmhPfBykmNJvKvC0GIAVJmOLhFl6RA5fobCjV-8zVSypxX8yb8ka6zu6-4TEft=w240-h480-rw" alt="Right Image" style="width: 100px; height: 100px; float: right;">
    </div>

	"""


	custom_css = """
	.custom-textbox textarea{font-size: 40px; !important}
	"""

	demo = gr.Interface(fn=get_response,
	                    inputs=gr.Image(type = 'filepath', image_mode="RGB"),
						outputs=[gr.Textbox( elem_classes = "custom-textbox" ), gr.Audio(type = "filepath")],
						title = "API DEMO - Indic Text Recogniser",
						description = interface_html,
						theme = seafoam,
						css = custom_css
						)
	
	demo.launch(server_name = server,
					server_port = port,
					favicon_path = ut.LOGO)

