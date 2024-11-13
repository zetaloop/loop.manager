import requests

def get_titles(rss_url):
    '''rss_url: like https://github.com/zetaloop/PowerToys-CN/releases.atom'''
    response = requests.get(rss_url)
    if response.status_code == 200:
        content = response.text.split('\n')
        titles = [i.strip()[7:-8] for i in content if '<title>' in i]
        return titles[1:]
    raise ConnectionError('Unable to access github.com')