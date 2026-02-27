import MethodLibrary as ML

test_url = "https://www.reddit.com/r/transvoice/comments/1r7ojng/how_is_my_lazy_everyday_voice/"
postNum = 1
prompt = "Please provide a URL, or enter 'E' to exit.\n"
url = ""


#### Main application loop ####

while url != "E" and url != "e":
    if postNum == 2:
        prompt = "Please provide another URL, or enter 'E' to exit.\n"
    
    url = input(prompt)
    
    if url == "E" or url == "e":
        break
    elif url == "":
        url = test_url
    
    data = ML.fetch_post(url)
    post = ML.extract_post(data, url)
    comments = ML.extract_comments(data)
    
    ML.extract_media(url, postNum)
    ML.export_csv(post, comments, postNum)
    
    postNum += 1
    
    print("\n")