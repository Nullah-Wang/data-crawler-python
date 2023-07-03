import re
from .utils import get_soup

def parse_page(url):
    if '/AR' in url:
        return parse_page_ar(url)
    return parse_page_basic(url)

def parse_content(soup,url):
    phrases = [p.text.strip() for p in soup.select('div[class=remainder-content] section div p')]
    if not phrases:
        # print("content is empty")
        # print(url)
        return ''
    return '\n'.join(phrases)

def parse_teaser(soup,url):
    phrases = [p.text.strip() for p in soup.select('div[class=teaser-content] section div p')]
    if not phrases:
        # print("teaser is empty")
        # print(url)
        return ''
    return '\n'.join(phrases)

def parse_pic_article(soup,url):
    phrases = [p.text.strip() for p in soup.select('div[data-qa=article-image] figure figcaption')]
    if not phrases:
        return ''
    return '\n'.join(phrases)

def parse_pic_lede(soup,url):
    div = soup.select('div[data-qa=lede-art] figure figcaption')
    if not div:
        return ''
    # print(div[0].text.strip())
    return div[0].text.strip()

def parse_author(soup,url):
    span = soup.select('*[data-qa=author-name]')
    if not span:
        # print("author is empty")
        # print(url)
        return ''
    # print(span[0].text.strip())
    return span[0].text.strip()

def parse_date(soup,url):
    div = soup.select('div[data-qa=timestamp]')
    if not div:
        # print("date is empty")
        # print(url)
        return ''
    # print(div[0].text.strip())
    return div[0].text.strip()

def parse_headline(soup,url):
    div = soup.select('div[data-qa=headline-text]')
    if not div:
        div = soup.select('span[data-qa=headline-opinion-text]')
        # print(div)
        if not div:
            div = soup.select('h1[id=main-content]')
            # print(div)
            if not div:
                # print("headline is empty")
                # print(url)
                return ''
        return "Opinion:"+div[0].text.strip()
    # print(div[0].text.strip())
    return div[0].text.strip()

def parse_category(soup,url):
    a = soup.select('div[data-qa=kicker] a')
    if not a:
        # print("category is empty")
        # print(url)
        return ''
    # print(a[0].text.strip())
    return a[0].text.strip()

def parse_page_basic(url):
    soup = get_soup(url)
    # print(soup)
    if soup is None:
        # print("none")
        return {}
    json_obj = {
        'url': url,
        'headline': parse_headline(soup, url),
        'author': parse_author(soup,url),
        'date': parse_date(soup,url),
        'category': parse_category(soup,url),
        'pic-desc-lede': parse_pic_lede(soup,url),
        'pic-desc-article': parse_pic_article(soup, url),
        'teaser-content': parse_teaser(soup, url),
        'content': parse_content(soup, url),
        'data_strf':parse_date_strf_from_url(url)
    }
    # print(json_obj['headline'])
    # date_strf = '-'.join(url.strip("/").split('/')[-4:-1])
    # json_obj['date_strf'] = date_strf
    return json_obj

def parse_author_date_ar(soup, url):
    try:
        ad = soup.select('div[id=article] font')
        if not ad:
            return '', ''
        byline = soup.select('div[id=byline]')
        if byline:
            author_ = byline[0].text.strip()
            if author_.split()[0].lower() == 'by':
                author = ' '.join(author_.split()[1:])
            else:
                author = author_
        else:
            author_ = ''
            author = ''

        if author_:
            date = ad[0].text.replace(author_, '').strip()
        else:
            date = ''
    except Exception as e:
        print('author_date exception: {}'.format(url))
        print(e)
        return '', ''

    return author, date

def parse_date_strf_from_url(url):
    datepattern = re.compile('\d{4}/\d{2}/\d{2}')
    date_strf = datepattern.findall(url)
    if date_strf:
        return date_strf[0].replace('/', '-')
    return ''

def parse_head_ar(soup):
    headline = soup.select('h1')
    if not headline:
        return ''
    return headline[0].text.strip()

def parse_content_ar(soup):
    content = [p.text.strip() for p in soup.select('div[id=article_body] p')]
    if not content:
        return ''
    return '\n'.join(content)

def parse_page_ar(url):
    soup = get_soup(url)
    author, date = parse_author_date_ar(soup, url)
    json_obj = {
        'url': url,
        'content': parse_content_ar(soup),
        'author': author,
        'date': date,
        'headline': parse_head_ar(soup),
        'category': '',
        'date_strf': parse_date_strf_from_url(url)
    }
    return json_obj
