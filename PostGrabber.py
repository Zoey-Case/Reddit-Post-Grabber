import MethodLibrary as ML

print("\n")
subName = input("Please provide a subreddit name: ")
desiredPosts = int(input("Please provide a number of posts to collect: "))
queryLimit = desiredPosts

onlyVideoInput = input("Would you like to skip posts which do not include attached audio or video files?\n")
print("\n")

postIndex = 0
difference = 0

if onlyVideoInput[0] == 'Y' or onlyVideoInput[0] == 'y':
    print("Skipping posts which do not contain media...")
    
    urls = ML.FetchURLs(subName, queryLimit * 20)
    postNum = 0
    
    while postIndex < queryLimit:
        fetchSucceeded = ML.ExtractMedia(urls[postIndex], postNum + 1)
    
        if fetchSucceeded:
            data = ML.FetchPost(urls[postIndex])
            post = ML.ExtractPost(data, urls[postIndex])
            comments = ML.ExtractComments(data)
            
            ML.ExportCSV(post, comments, postNum + 1)
            postNum += 1
    
        postIndex += 1
        
        if postIndex == queryLimit - 1 and postIndex > postNum + difference:
            difference = postIndex - postNum
            queryLimit += desiredPosts - postNum
    
        print("\n\n")
else:
    skipVideoInput = input("Would you like to only grab text content from posts?\n")
    print("\n")
    
    urls = ML.FetchURLs(subName, queryLimit)
    
    skipVideos = (skipVideoInput[0] == 'Y' or skipVideoInput[0] == 'y')
    
    if skipVideos:
        print("Fetching only text content from discovered posts...")
    else:
        print("Fetching all content from discovered posts...")
    
    while postIndex < queryLimit:
        data = ML.FetchPost(urls[postIndex])
        post = ML.ExtractPost(data, urls[postIndex])
        comments = ML.ExtractComments(data)

        if not skipVideos:
            ML.ExtractMedia(urls[postIndex], postIndex + 1)
            
        ML.ExportCSV(post, comments, postIndex + 1)

        postIndex += 1

        print("\n\n")

print("Operation complete.")