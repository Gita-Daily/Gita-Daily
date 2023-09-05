import json
import os
import glob

import openai
import time

openai.api_key = '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'

n = 0

def summarise(prompt, message_text):
    functions = [
        {
            "name": "summarise",
            "description": f"{prompt}",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Summarised output",
                    },
                },
                "required": ["summary"],
            },
        }
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are GitaGPT"}, {"role": "user", "content": message_text}],
            functions=functions,
            function_call={"name": "summarise"}
        )
        return json.loads(response['choices'][0]['message']["function_call"]["arguments"])["summary"]
    except Exception as e:
        print("An error occurred while generating response: " + str(e))
        time.sleep(3)
        return summarise(prompt, message_text) 

# # Loop through folders 1 to 18
# for folder_number in range(1, 19):
#     # Construct the folder path
#     folder_path = str(folder_number)

#     # Use glob to find all JSON files in the folder
#     json_files = glob.glob(f"{folder_path}/*.json")

#     # Iterate through the found JSON files
#     for file_path in json_files:
#         # Open the file
#         with open(file_path, 'r') as file:
#             contents = json.load(file)

#             commentary = contents["commentary"]
#             verse = contents["verse"]
#             translation = contents["translation"]

#             remaining_length = 1600 - len(verse) - len(translation) - 50

#             remaning_words = remaining_length // 5

#             if len(commentary) > remaining_length:
#                 prompt = f"Summarise the given commentary of shloka(s) from the bhagavad gita in {remaning_words} words: "
#                 msg_text = f"Summarise the given commentary of shloka(s) from the bhagavad gita in {remaning_words} words: \n\n{commentary}\n\n"
#                 summary = summarise(prompt, msg_text)
#                 contents["new_commentary"] = summary

#                 print("Changed summary from " + str(len(commentary)) + " to " + str(len(summary)) + " characters. Remaining: " + str(remaining_length - len(summary)) + " characters")

#                 with open(file_path, 'w') as file:
#                     json.dump(contents, file, indent=4)
#                     print("Wrote to " + file_path)
#             else:
#                 contents["new_commentary"] = commentary

#                 with open(file_path, 'w') as file:
#                     json.dump(contents, file, indent=4)
#                     print("Wrote to " + file_path)


# Loop through folders 1 to 18
for folder_number in range(1, 19):
    # Construct the folder path
    folder_path = str(folder_number)

    # Use glob to find all JSON files in the folder
    json_files = glob.glob(f"{folder_path}/*.json")

    # Iterate through the found JSON files
    for file_path in json_files:
        # Open the file
        with open(file_path, 'r') as file:
            contents = json.load(file)

            commentary = contents["new_commentary"]
            verse = contents["verse"]
            translation = contents["translation"]
            
            extra_fluff = "*Chapter 12 Verse 1*\n\n\n\n*Translation*\n\n*Commentary*\n\nCreated by www.gitadaily.in"

            remaining_length = 1600 - len(verse) - len(translation) - len(extra_fluff) - 25

            remaning_words = remaining_length // 5

            if len(commentary) > remaining_length:
                print(file_path)
                print(remaining_length)
                prompt = f"Summarise the given commentary of shloka(s) from the bhagavad gita in {remaning_words - 6} words: "
                msg_text = f"Summarise the given commentary of shloka(s) from the bhagavad gita in {remaning_words - 6} words: \n\n{commentary}\n\n"
                summary = summarise(prompt, msg_text)
                contents["new_commentary"] = summary  
                print(len(summary))     

                with open(file_path, 'w') as file:
                    json.dump(contents, file, indent=4)
                    print("Wrote to " + file_path)