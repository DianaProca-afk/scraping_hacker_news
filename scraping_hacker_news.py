'''
This code selects the title, link and score of the articles with votes above 100.
'''
import requests
from bs4 import BeautifulSoup
import pprint

# we get the response from the website
response = requests.get('https://news.ycombinator.com/news')
response2 = requests.get(
    'https://news.ycombinator.com/newest?next=42498446&n=31')

# we parse the response with BeautifulSoup and make it into a beautifulsoup object so we can work with it.
soup_object = BeautifulSoup(response.text, 'html.parser')
soup_object2 = BeautifulSoup(response2.text, 'html.parser')
# titleline is the class where all the links are stored. We need to select that class, using the .select method from the BeautifulSoup module. This method returns a list of all items with of the class titleline.
title_line = (soup_object.select('.titleline'))
title_line2 = (soup_object2.select('.titleline'))
# score is the class where all scores are stored. Similar to the titleline, we need to select that class using the .select method from the BeautifulSoup module. Returns a list of all items of the class score.
subtext = (soup_object.select('.subtext'))
subtext2 = (soup_object2.select('.subtext'))

# we concatinate the two lists of the title_line and subtext by making a biger list.
mega_title_line = title_line + title_line2
mega_subtext = subtext + subtext2


def create_custom_hm(hmlist):
    return sorted(hmlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(title_line, subtext):
    hm = []

    # here we only enumerate the links, but we use enumerate so we match title and link with the score.
    for index, item in enumerate(title_line):

        # we get the text from the title
        title = item.getText()

        # titl_line[index] is the same as item, we used this instead to see that they are the same, which are the items inside  the list of title_link

        href = title_line[index].get('href', None)

        # here we cannot replace the subtext[index] with item because we do not loop, but uses the index from the enumerate funtion from the loop to mathc the index of link and title
        # we not that we get back a list of the scores, since we use the .select method
        vote = subtext[index].select('.score')
        if len(vote):
            # from the class score we get the text
            # index of 0 because wote is a list with one element, the score, but we need to grab the text of it
            points = int(vote[0].getText().split()[0])
            if points > 99:
                hm.append({'title': title, 'link': href, 'votes': points})

    return create_custom_hm(hm)


pprint.pprint((create_custom_hn(mega_title_line, mega_subtext)))
