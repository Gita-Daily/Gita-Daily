import urllib.request


def download_gita_audio():
    shlok_num = 1
    for chp_num in range(1, 19):
        while (shlok_num < 81):
            try:
                url = f"https://www.gitasupersite.iitk.ac.in/sites/default/files/audio/CHAP{chp_num}/{chp_num}-{shlok_num}.MP3"
                file_name = f"Audio/{chp_num}_{shlok_num}.mp3"
                urllib.request.urlretrieve(url, file_name)
                print(f"Downloaded {chp_num}_{shlok_num}.mp3")
                shlok_num += 1
            except:
                print('Shloks in chapter were ', shlok_num - 1)
                chp_num += 1
                shlok_num = 1
                continue

download_gita_audio()