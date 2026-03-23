import MethodLibrary as ML

print("\n")
subName = input("Please provide a subreddit name: ")
desiredPosts = int(input("Please provide a number of posts to collect: "))
queryLimit = desiredPosts
postType = input("Would you like to skip posts which do not include attached audio or video files?\n")

print("\n")

postIndex = 0
difference = 0

if postType[0] == 'Y' or postType[0] == 'y':
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
    urls = ML.FetchURLs(subName, queryLimit)
    print("Fetching all discovered posts...")
    
    while postIndex < queryLimit:
        data = ML.FetchPost(urls[postIndex])
        post = ML.ExtractPost(data, urls[postIndex])
        comments = ML.ExtractComments(data)

        ML.ExtractMedia(urls[postIndex], postIndex + 1)
        ML.ExportCSV(post, comments, postIndex + 1)

        postIndex += 1

        print("\n\n")

print("Operation complete.")