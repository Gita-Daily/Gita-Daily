import requests

# Define URL and headers
url = "https://live-server-114563.wati.io/api/v1/sendSessionFile/6588646820"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0ZTk0YjdmYy01MDVlLTRkZjItYjMwYy0xOTlmNWE1NDhjODIiLCJ1bmlxdWVfbmFtZSI6ImthcnRoaWtAZG8ueW9nYSIsIm5hbWVpZCI6ImthcnRoaWtAZG8ueW9nYSIsImVtYWlsIjoia2FydGhpa0Bkby55b2dhIiwiYXV0aF90aW1lIjoiMDkvMDIvMjAyMyAwNTowNDo0NyIsImRiX25hbWUiOiIxMTQ1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6IkNsYXJlX0FJIiwiYXVkIjoiQ2xhcmVfQUkifQ.29IGlp4J9UKJ1G6vFxmbi2A12TRiFRCQB-lL-ew6vxQ"
}

# File path
file_path = "Audio/1_1.mp3"  # Replace with the actual file path

# Open the file
with open(file_path, 'rb') as f:
    file_data = f.read()

# Formulate multipart payload
files = {'file': ('file.mp3', file_data, 'audio/mpeg')}

# Perform the POST request
response = requests.post(url, headers=headers, files=files)

# Print the response
print(response.text)