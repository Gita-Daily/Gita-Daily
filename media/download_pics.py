from icrawler.builtin import GoogleImageCrawler
image_search_queries = [
    "bhagavad gita krishna midjourney hd no text",
    "Krishna Arjuna hd no text",
    "Hindu philosophy cosmic form hd no text",
    "Indian spiritual art hd no text",
    "Bhagavad Gita paintings hd no text",
    "Mahabharata battlefield art hd no text",
    "Krishna deity concept art hd no text",
    "Dharma concept art hd no text",
    "meditation cosmic form hd no text",
    "Indian mythology art hd no text",
    "Hinduism cosmology cosmic form hd no text",
    "Indian temples cosmic midjourney hd no text",
    "Arjuna warrior midjourney hd no text",
    "Krishna teaching Arjuna midjourney hd no text",
    "Spiritual enlightenment cosmic form hd no text",
    "Kurukshetra war hd no text",
    "Divine incarnation Krishna cosmic form midjourney hd no text",
]

for query in image_search_queries:
    google_Crawler = GoogleImageCrawler(storage={'root_dir': 'images2/' + query})
    google_Crawler.crawl(keyword = query, max_num = 10, min_size=(500,500))






# import asyncio
# import aiohttp
# import aiofiles

# import pyfirefly
# from pyfirefly.utils import ImageOptions

# import openai
# openai.api_key = "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"

# import time
# import json

# token = 'eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2ODg2NjY0NzY0MjdfODVhYTVjM2QtM2MzNy00ZTA3LWFiYzMtOGQ3NmYwNzBjODI3X3V3MiIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJjbGlvLXBsYXlncm91bmQtd2ViIiwidXNlcl9pZCI6IkFCNDQyQTM0NjQyOTk4NjYwQTQ5NUZDN0BBZG9iZUlEIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJBQjQ0MkEzNDY0Mjk5ODY2MEE0OTVGQzdAQWRvYmVJRCIsImN0cCI6MCwiZmciOiJYU1pCVDQySVZQUDU0UDRLR01RVlpIQUFOTT09PT09PSIsInNpZCI6IjE2ODgzODQ3NzAzNzBfMjMwMTI1YzQtOWFmOC00NmUyLWEyMTMtNzc5ZWYwYjVhNThlX3V3MiIsIm1vaSI6IjgwMDc0MDExIiwicGJhIjoiTWVkU2VjTm9FVixMb3dTZWMiLCJleHBpcmVzX2luIjoiODY0MDAwMDAiLCJjcmVhdGVkX2F0IjoiMTY4ODY2NjQ3NjQyNyIsInNjb3BlIjoiQWRvYmVJRCxvcGVuaWQsZmlyZWZseV9hcGkifQ.ARaaBfUyzfJH1VUOdCGn9vlW4HXqM3SoJOUc6MDXfBJQagTxB-s20pYuscIJSRq7_lQgXH27Vf64_asiZKg4BZ2Iunf81pxuHYihWtcqJfZQK69X-316LpQQgDHmvIgv-FDCoVKH5NwQs6O9K1g5rqb6j23mVIVpuhuLk7fpybfeqGgCiQhfGy0kDkRjeGCn5tjF9vMqLCxr35zheWXbu_nVLQb25er00UJ3OtDSyh5Y7ZuBpsBpPClWwmplFn6LvE7yuQelwqL6_KbcFFSocfDlaTOrOmZf6Cjk_dIPT3GH-nI4qmbyCiHEy00Y_i0KjxvZ_TP_MQPRgxsWVCGjEA'

# async def create_save_image(a, prompt, img_options, num):
#     result = await a.text_to_image(prompt, **img_options)
#     async with aiofiles.open(f'{num}.{result.ext}', mode='wb+') as f:
#         await f.write(result.image)

# async def demo(prompt, num):
#     a = await pyfirefly.Firefly(token)
#     img = ImageOptions(image_styles = a.image_styles)
#     img.add_styles(['Art', 'Blurry background', 'Cyberpunk', 'Origami'])
#     img.set_aspect_ratio('portrait')
#     # img.set_aspect_ratio('widescreen')
#     task = create_save_image(a, prompt, img.options, num)

#     await asyncio.gather(task)

# def get_response(commentary):
#     functions = [
#         {
#             "name": "generate_picture",
#             "description": "Given the commentary of a bhagavad gita shloka, generates a picture description that can be used to find a relevant picture on google ",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "img_description": {
#                         "type": "string",
#                         "description": "what should be typed in google image search to get a relevant image for the shloka",
#                     },
#                 },
#                 "required": ["img_description"],
#             },
#         }
#     ]
#     while True:
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo-0613",
#                 messages=[
#                         {"role": "system", "content": "You are BhagavadGitaGPT."},
#                         {"role": "user", "content": "As BhagavadGitaReelGPT, an AI designed to help users imagine and visualise shlokas from the Bhagavad Gita, you have been tasked with generating an apt image search query on google that would capture the essence of the shloka well. Shloka Translation: \n\n" + commentary},
#                     ],
#                 functions = functions,
#                 function_call = {"name": "generate_picture"}

#             )
#             return response['choices'][0]['message']
#         except Exception as e:
#             print("An error occurred while generating response: " + str(e))
#             time.sleep(3)
#             continue


# with open('1/32.json', 'r') as json_file:
#     data = json.load(json_file)

# input_data = "Translation: " + data['translation']

# output = get_response(input_data)

# print(output)

# # args = json.loads(output['function_call']['arguments'])

# # # Printing the script lines and corresponding visual descriptions
# # for script_line, img_desc in zip(args['script'], args['image_description']):
# #     print(f"Script: {script_line}\nVisual Description: {img_desc}\n")

# # script_lines = args['script']
# # image_descriptions = args['image_description']

# # min_length = min(len(script_lines), len(image_descriptions))
# # script_lines = script_lines[:min_length]
# # image_descriptions = image_descriptions[:min_length]

# # import requests

# # url = "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld"
# # headers = {
# #     "accept": "audio/mpeg",
# #     "xi-api-key": "729ed03a74f8a6e365a1129f724a9b2b",
# #     "Content-Type": "application/json",
# # }

# # print("Ok we crossed that")
# # # data = '{"text":"The 1977 Philadelphia mayoral election saw Frank Rizzo win a second term, defeating challenger Ed Rendell by a narrow margin. "}'

# # # response = requests.post(url, headers=headers, data=data)

# # # with open("prompt_response.mp3", "wb") as f:
# # #     f.write(response.content)


# # from google.cloud import texttospeech
# # import os 

# # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/blackhole/.config/gcloud/application_default_credentials.json'

# # # Instantiates a client
# # client = texttospeech.TextToSpeechClient()

# # # Set the text input to be synthesized
# # synthesis_input = texttospeech.SynthesisInput(text="Hello World!")

# # # Build the voice request, select the language code ("en-US") and the ssml
# # # voice gender ("neutral")
# # voice = texttospeech.VoiceSelectionParams(
# #     language_code="en-US", name = "en-US-Neural2-C", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
# # )

# # # Select the type of audio file you want returned
# # audio_config = texttospeech.AudioConfig(
# #     audio_encoding="LINEAR16", speaking_rate=1.0, pitch=1.0
# # )

# # response = client.synthesize_speech(
# #     input=synthesis_input, voice=voice, audio_config=audio_config
# # )

# # print('hello')

# # # The response's audio_content is binary.
# # with open("output.mp3", "wb") as out:
# #     # Write the response to the output file.
# #     out.write(response.audio_content)
# #     print('Audio content written to file "output.mp3"')

# # for i in range(len(script_lines)):
# #     print("Generating audio for content: " + script_lines[i])
# #     # Create the data dictionary
# #     data = {"text": script_lines[i]}
    
# #     # Make the POST request
# #     # response = requests.post(url, headers=headers, data=json.dumps(data))

# #     # response = text_to_speech(content[i])
# #     synthesis_input = texttospeech.SynthesisInput(text=script_lines[i])
# #     response = client.synthesize_speech(
# #         input=synthesis_input, voice=voice, audio_config=audio_config
# #     )

# #     with open(f"audio_{i}.mp3", "wb") as out:
# #     # Write the response to the output file.
# #         out.write(response.audio_content)

    
# #     # Save the audio file
# #     # with open(f"audio_{i}.mp3", "wb") as f:
# #         # f.write(response.content)

# #     print("Audio saved successfully!")


# #     print("Generating image for image prompt: " + image_descriptions[i])
# #     asyncio.run(demo(image_descriptions[i], i))

# # import moviepy.editor as mp

# # def create_reel(n):
# #     clips = []

# #     for i in range(n):
# #         audio = mp.AudioFileClip(f"audio_{i}.mp3")
# #         image = mp.ImageClip(f"{i}.jpeg", duration=audio.duration).set_audio(audio)
# #         clips.append(image)

# #     final_video = mp.concatenate_videoclips(clips, method="compose")
# #     final_video.write_videofile("result.mp4", codec='libx264', audio_codec='aac', fps=24, temp_audiofile='/tmp/temp-audio.m4a')

# # create_reel(len(script_lines))