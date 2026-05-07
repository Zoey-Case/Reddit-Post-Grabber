# Reddit Post Grabber

<p>This is a Python 3 terminal application I built to fetch reddit posts (along with any attached media and comments) en masse, as this was required for my senior thesis research. </p>
<p>This app allows the user to supply the name of a given subreddit and automatically grabs however many posts the user requests - in order from the "Hot" list, with an option to skip posts which do not include AV files and an option to also generate audio files from any video files fetched.</p>

## Prerequisites
1) [FFMPEG Codec](https://ffmpeg.org/download.html), for processing AV files.


## Instructions
1) Either download the .zip and extract it, or pull the repo with git.
2) Open a terminal in the application's root folder.
3) Enter the following command:
> python3 PostGrabber.py
