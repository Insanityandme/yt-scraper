"""Script to gather comments from a youtube video."""


# Call the API's commentThreads.list method to list the existing comments.
def scrape(service, video_id, pageToken=None):
    results = service.commentThreads().list(
             pageToken=pageToken,
             part="snippet",
             videoId=video_id,
             maxResults=100,
             textFormat="plainText",
             fields="items, nextPageToken"

     ).execute()

    return results


# Call the API's comments.list method to list the existing comment replies.
def get_comments(service, parent_id):
    results = service.comments().list(
        part="snippet",
        parentId=parent_id,
        textFormat="plainText",
        maxResults=100
    ).execute()

    return results


def fetch_all_comment_threads(service, video_id):
    comment_threads = []
    video_comment_threads = scrape(service, video_id)
    # pageToken = video_comment_threads['nextPageToken']

    while True:
        if 'nextPageToken' in video_comment_threads:
            pageToken = video_comment_threads['nextPageToken']
            video_comment_threads = scrape(service, video_id,
                                           pageToken=pageToken)
            comment_threads.append(video_comment_threads)
        else:
            comment_threads.append(video_comment_threads)
            break

    return comment_threads


def fetch_all_comments_and_ids(service, video_id):
    count = 0
    id_array = []
    comments = ""
    all_comments_threads = fetch_all_comment_threads(service, video_id)

    for comment_thread in all_comments_threads:
        comment_thread_items = comment_thread['items']
        for item in comment_thread_items:
            id_array.append(comment_thread_items[count]['id'])
            count += 1
            if count >= len(comment_thread_items):
                count = 0

            comment = item['snippet']['topLevelComment']
            text = comment['snippet']['textDisplay']
            comments += text + " "

    return (comments, id_array)


def scrape_all(service, video_id):
    comment_threads = fetch_all_comments_and_ids(service, video_id)
    id_array = comment_threads[1]
    count = 0
    replies = ""
    unique_count = 0

    for item in range(0, len(id_array)):
        parent_id = id_array[count]
        get_comment_results = get_comments(service, parent_id)
        count += 1
        unique_count += len(get_comment_results['items'])
        if get_comment_results['items']:
            for item in get_comment_results['items']:
                comments = item['snippet']['textDisplay']
                replies += comments + " "

    return (comment_threads[0], replies, unique_count+len(id_array))


def main():
    print "Data fetching done."

if __name__ == '__main__':
    main()
