import requests
import csv

def grab_data(url):
    print(f"Fetching POST from: {url}...\n")
    
    # Modify the URL.
    json_url = url.rstrip('/') + '.json'
    
    # Set up the user agent.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Make the request.
    response = requests.get(json_url, headers=headers)
    
    
    if response.status_code != 200:
        print(f"Error: Failed to retrieve data! Status Code: {response.status_code}")
        return
    
    return response.json()

def extract_post(data):
    # Extract the post details.
    post_data = data[0]['data']['children'][0]['data']
    
    author = post_data.get('author', '[Deleted User]')
    content = post_data.get('selftext', '')
    media = post_data.get('url', '')
    
    return list((author, content, media))

def extract_comments(data):
    comments_data = data[1]['data']['children']
    comments = list()
    
    for item in comments_data:
        if item['kind'] == 't1':
            comments.append((item['data'].get('author', '[Deleted]'), item['data'].get('body', '')))
            
    return comments

def export_csv(post, comments, num):
    # path = f"Data/data{num}.csv"
    path = f"Data/data.csv"
    
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post Author', 'Post Content', 'Post Media Link'])
        writer.writerow([post[0], post[1], post[2]])
        writer.writerow([])
        writer.writerow(['Comment', 'Comment Author', 'Comment Content'])
        
        comment_count = 1
        for comment in comments:
            writer.writerow([comment_count, comment[0], comment[1]])
            comment_count += 1