import re
import sys
from scraper import scrape_all
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


"""the stopwords are taken from glasgows school of computing
resources here: http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words

mention: some words are added specifically for retrieaval of the words of
Nerdwriters1' video 'The Secret of Sexism'. Please remove these words if
you wanna obey glasgows stopwords completely.
words: the words at the top of the array that are not in alphabetical order
"""
stopwords = ['t', 'm', 'just', 'like', 'think', 'don', 'want', 'say', 'really']
stopwords += ['way', 'make', 'know']
stopwords += ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']


def strip_non_alpha(text):
    # turn unicode to ascii
    text = text.encode('ascii', 'ignore').lower()
    # replace all non-alphabetical characters
    wordlist = re.compile(r'\W+').split(text)

    return wordlist


def remove_stopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]


def word_list_to_freq_dict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist, wordfreq))


def sort_freq_dict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


def main():
    """Main entry point for the script."""
    # the "developer" option specifices the key that uniquely
    # identifies your google account for accesing youtubes data API
    argparser.add_argument("--developerkey", help="Required key" +
                           "for accessing youtubes data API.")
    # The "videoid" option specifies the YouTube video ID that uniquely
    # identifies the video for which the comments will be fetched.
    argparser.add_argument("--videoid", help="Required ID for video" +
                           "for which the comments will be fetched.")
    args = argparser.parse_args()

    if not args.developerkey:
        exit("Please specify key using the --developerkey= parameter.")
    if not args.videoid:
        exit("Please specify videoid using the --videoid= parameter.")

    try:
        service = build('youtube', 'v3', developerKey=args.developerkey)
        result = scrape_all(service, args.videoid)
        comments, replies, unique_count = result[0], result[1], result[2]

        # Convert all comments and replies into something
        # comprehensible to a word counter
        fullwordlist = strip_non_alpha(comments+replies)
        wordlist = remove_stopwords(fullwordlist, stopwords)
        dictionary = word_list_to_freq_dict(wordlist)
        sorteddict = sort_freq_dict(dictionary)

        # Gives us the top 10 words from frequency:
        for word, freq in sorteddict[:10]:
            print word, freq

        print "comment count: %d" % unique_count

    except HttpError, e:
        print "An HTTP error %d occured:\n%s" % (e.resp.status, e.content)
    else:
        print "Done fetching data."


if __name__ == '__main__':
    sys.exit(main())
