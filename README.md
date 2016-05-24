##What is this poorly written code?
I'm glad you asked, this is my first attempt on a project that teaches me HTTP requests and to work against an API in python.

The idea came from a request by [https://www.youtube.com/user/Nerdwriter1]: Nerdwriter1, a Youtuber that creates video essays on various topics of his interest.

[request]

##Usage
`python word_frequency.py --developerkey="my_google_developer_api_key" --videoid="youtube video_ID"`

###Requirements
####Python 2.7.x
I have been running this script on python 2.7.10, it should work on other 2.7.x versions. 

####google-api-python-client 
you can use pip:  
`$ pip install --upgrade google-api-python-client

A google account and a developer key, you don't need to set up a OAuth, just make a project and create a new Public API access key. 
More instructions here: [https://developers.google.com/youtube/v3/getting-started]

[request]: http://i.imgur.com/kz58Knr.png "nerd writer request"