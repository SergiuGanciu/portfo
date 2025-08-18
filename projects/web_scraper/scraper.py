import requests
from bs4 import BeautifulSoup

res_news_main = requests.get('https://news.ycombinator.com/news')
soup_main = BeautifulSoup(res_news_main.text, 'html.parser')
more_link = soup_main.select('.morelink')[0]['href']
res_news_p2 = requests.get('https://news.ycombinator.com/news' + more_link)
soup_p2 = BeautifulSoup(res_news_p2.text, 'html.parser')
# print(more_link)
links = soup_main.select('.titleline') + soup_p2.select('.titleline')
subtexts = soup_main.select('.subtext') + soup_p2.select('.subtext')

def get_news_post_list(links, subtexts):
    """
    Collect posts with more than 100 votes from news.ycombinator.com/news main page.
    links: list of Tag objects
    subtexts: list of Tag objects
    return: Sorted list of dictionaries
    """
    posts_info = []

    for i in range(len(links)):
        score = subtexts[i].select('.score')

        if len(score):
            points = int(score[0].text.split()[0])

            if points >= 100:
                posts_info.append({
                    'title': links[i].find('a').text,
                    'link': links[i].find('a')['href'],
                    'votes': points
                })

    #Sort by votes DESC
    sorted_posts = sorted(posts_info, key=lambda k: k['votes'] , reverse=True)
    return sorted_posts

print(get_news_post_list(links, subtexts))