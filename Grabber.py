import MethodLibrary as ML

test_url = 'https://www.reddit.com/r/transvoice/comments/1r7ojng/how_is_my_lazy_everyday_voice/'

url = input("Please provide a URL.\n")
if url == '':
    url = test_url

data = ML.grab_data(url)
post = ML.extract_post(data)
comments = ML.extract_comments(data)

ML.export_csv(post,comments, 0)