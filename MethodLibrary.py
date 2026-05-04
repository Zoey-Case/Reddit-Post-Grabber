import PackageHandler as PH


#### DEPENDENCIES ####

PH.EnsureInstalled("csv")
import csv
PH.EnsureInstalled("os")
import os
PH.EnsureInstalled("requests")
import requests
PH.EnsureInstalled("yt_dlp")
import yt_dlp
PH.EnsureInstalled("time")
import time
PH.EnsureInstalled("ffmpeg")
PH.EnsureInstalled("audio_extract")
import audio_extract as AE

######################


def ExportCSV(post, comments, postNum, folder="DataSheets"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = f"{folder}/Post#{postNum}.csv"

    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post Name', 'Post Author', 'Post Content', 'Post Media Link'])
        writer.writerow([post[0], post[1], post[2], post[3]])
        writer.writerow(['----', '----', '----', '----'])
        writer.writerow(['Comment #', 'Comment Author', 'Comment Content', '----'])

        commentCount = 1
        for comment in comments:
            writer.writerow([commentCount, comment[0], comment[1]])
            commentCount += 1


def ExtractComments(data):
    commentsData = data[1]['data']['children']
    comments = list()

    for item in commentsData:
        if item['kind'] == 't1':
            comments.append((item['data'].get('author', '[Deleted]'), item['data'].get('body', '')))

    return comments


def ExtractMedia(url, postNum, generateAudioFile = False, folder ="Media"):
    succeeded = False
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    print("Attempting to fetch media.")

    validExtensions = ('.jpg', '.jpeg', '.png', '.gif', '.mp3', '.wav', '.ogg', '.flac')
    filename = f"Post#{postNum}"

    if url.endswith(validExtensions):
        filepath = os.path.join(folder, filename)

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                succeeded = True
        except Exception as e:
            print(f"Download FAILED due to error: {e}")

    elif any(domain in url for domain in ['v.redd.it', 'reddit.com', 'youtube.com', 'youtu.be', 'soundcloud.com', 'vocaroo.com']):
        print("Media Detected. Downloading...")
        ydl_opts = {
            'outtmpl': f'{folder}/{filename}.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            succeeded = True
        except Exception as e:
            print(f"Download FAILED due to error: {e}")

    # Pause for 5 seconds to avoid being blocked by Reddit's anti-DDOS.
    time.sleep(5)

    if (succeeded and generateAudioFile):
        print("Generating AUDIO FILE from VIDEO FILE...")
        GenerateAudioFileFromVideoFile(f"Post#{postNum}", folder)
        
    return succeeded


def ExtractPost(data, url):
    # Extract the post details.
    postData = data[0]['data']['children'][0]['data']
    
    postName = postData.get('title')
    author = postData.get('author', '[Deleted User]')
    content = postData.get('selftext', '')
    media = postData.get('url', '')
    
    if postData.get('is_video'):
        media = url
    elif postData.get('secure_media') and postData['secure_media'].get('oembed'):
        media = postData['secure_media']['oembed'].get('url', url)
    
    # Pause for 1 second to avoid being blocked by Reddit's anti-DDOS.
    time.sleep(1)
    return list((postName, author, content, media))


def FetchPost(url):
    print(f"Fetching POST from: {url}...")

    # Modify the URL to bypass Reddit API restrictions.
    jsonURL = url.rstrip('/') + '.json'

    # Set up the user agent.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Make the access request.
    response = requests.get(jsonURL, headers=headers)

    if response.status_code != 200:
        return

    return response.json()


def FetchURLs(subReddit, queryLimit):
    
    print(f"Fetching posts from r/{subReddit}...")

    # Set up the user agent.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    urls = []
    afterToken = None

    # Keep looping until we reach our target count or the end of the subreddit.
    while len(urls) < queryLimit:
        url = f"https://www.reddit.com/r/{subReddit}/hot.json?t=all&limit=100"

        # If we have a token from a previous loop, add it to go to the next page.
        if afterToken:
            url += f"&after={afterToken}"

        # Make the access request
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            break

        data = response.json()
        posts = data['data']['children']
        
        # Check if at end of subreddit.
        if not posts:
            break

        # Extract the data for each post on this page.
        for post in posts:
            fullURL = f"https://www.reddit.com{post['data'].get('permalink')}"

            urls.append(fullURL)

            # Stop if we hit the query limit during this loop.
            if len(urls) >= queryLimit:
                break

        # Get the token for the next page
        afterToken = data['data'].get('after')
        print(f"Collecting URLs...")

        # If there is no next page, stop the loop
        if not afterToken:
            break

        # Pause for 2 seconds to avoid being blocked by Reddit's anti-DDOS.
        time.sleep(2)

    print(f"URLs collected.")

    return urls


def GenerateAudioFileFromVideoFile(fileName, oldFolder, newFolder ="ConvertedMedia"):
    if not os.path.exists(f"{oldFolder}/{fileName}.mp4"):
        return
    
    if not os.path.exists(newFolder):
        os.makedirs(newFolder)
    
    AE.extract_audio(input_path = f"{oldFolder}/{fileName}.mp4", output_path = f"{newFolder}/{fileName}.wav", output_format = "wav")