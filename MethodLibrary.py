import PackageHandler as PH


#### DEPENDENCIES ####

PH.ensure_installed("csv")
import csv
PH.ensure_installed("os")
import os
PH.ensure_installed("requests")
import requests
PH.ensure_installed("yt_dlp")
import yt_dlp

######################



def export_csv(post, comments, postNum, folder="DataSheets"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = f"{folder}/Post#{postNum}.csv"

    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post Name', 'Post Author', 'Post Content', 'Post Media Link'])
        writer.writerow([post[0], post[1], post[2], post[3]])
        writer.writerow(['----', '----', '----', '----'])
        writer.writerow(['Comment #', 'Comment Author', 'Comment Content', '----'])

        comment_count = 1
        for comment in comments:
            writer.writerow([comment_count, comment[0], comment[1]])
            comment_count += 1



def extract_comments(data):
    comments_data = data[1]['data']['children']
    comments = list()

    for item in comments_data:
        if item['kind'] == 't1':
            comments.append((item['data'].get('author', '[Deleted]'), item['data'].get('body', '')))

    return comments



def extract_media(url, post_num, folder="Media"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    print("Attempting to fetch media.")

    valid_direct_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.mp3', '.wav', '.ogg', '.flac')
    filename = f"Post#{post_num}"

    if url.endswith(valid_direct_extensions):
        filepath = os.path.join(folder, filename)

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Media file saved to: {filepath}\n")
            else:
                print(f"Download FAILED due to error: {response.status_code}\n")
        except Exception as e:
            print(f"Download FAILED due to error: {e}\n")

    elif any(domain in url for domain in ['v.redd.it', 'reddit.com', 'youtube.com', 'youtu.be', 'soundcloud.com', 'vocaroo.com']):
        print("Split media detected at host. Attempting to merge...")
        ydl_opts = {
            'outtmpl': f'{folder}/{filename}.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Media file saved to: {folder}\n")
        except Exception as e:
            print(f"Download FAILED due to error: {e}\n")

    else:
        print("No media detected at host.\n")



def extract_post(data, url):
    # Extract the post details.
    post_data = data[0]['data']['children'][0]['data']
    
    postName = post_data.get('title')
    author = post_data.get('author', '[Deleted User]')
    content = post_data.get('selftext', '')
    media = post_data.get('url', '')
    
    if post_data.get('is_video'):
        print("Native video detected.")
        media = url
    elif post_data.get('secure_media') and post_data['secure_media'].get('oembed'):
        print("Embedded video detected.")
        media = post_data['secure_media']['oembed'].get('url', url)
    
    return list((postName, author, content, media))



def fetch_post(url):
    print(f"Fetching POST from: {url}...\n")

    # Modify the URL to bypass Reddit API restrictions.
    json_url = url.rstrip('/') + '.json'

    # Set up the user agent.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Make the access request.
    response = requests.get(json_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Failed to retrieve data! \nStatus Code: {response.status_code}\n")
        return

    return response.json()