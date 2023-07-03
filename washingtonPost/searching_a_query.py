import argparse
import json
import time
import os
import re
import random
from washingtonpost_scraper import get_urls_from_a_search_page
from washingtonpost_scraper import parse_page
import multiprocessing
from multiprocessing import Pool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--sleep', type=float, default=3, help='Sleep time for each submission (post)')
    parser.add_argument('--begin_num', type=int, default=0, help='Number of scrapped articles')
    parser.add_argument('--max_num', type=int, default=20, help='Number of scrapped articles')
    parser.add_argument('--query', type=str, default='chinese', help='Number of scrapped articles')
    parser.add_argument('--force', dest='force', default='true', action='store_true')


    args = parser.parse_args()
    directory = args.directory
    sleep = args.sleep
    begin_num = args.begin_num
    max_num = args.max_num
    max_num = max(max_num, 50000)
    query = args.query
    force = args.force

    # create output directory
    directory += '/%s' % query
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open("{}/no_date_url.txt".format(directory), "r") as f:
        urls = f.readlines()

    # n_exceptions = 0
    # stop = False
    # for startat in range(begin_num, begin_num+max_num, 20):
    for startat in range(begin_num, len(urls), 20):
        # if stop :
        #     print("stop")
        #     break
        # # exception
        # if n_exceptions > 50:
        #     print('{} exceptions. stop scraping'.format(n_exceptions))

        print('start to scrap article {}'.format(startat))

        # scrap article urls
        # urls, urls_no_date = get_urls_from_a_search_page(query, startat)
        # if not urls:
        #     print("No more urls.stop scraping.")
        #     break
        # # output wrong urls
        # if urls_no_date:
        #     with open('{}/no_date_url.txt'.format(directory), 'a', encoding='utf-8') as f:
        #         for url in urls_no_date:
        #             f.write(url + "\n")
        # urls=['https://www.washingtonpost.com/sports/olympics/olympic-ski-halfpipers-crank-up-the-tunes-before-their-runs/2022/02/18/e19a67ca-90a5-11ec-8ddd-52136988d263_story.html','https://www.washingtonpost.com/sports/olympics/olympic-ski-halfpipers-crank-up-the-tunes-before-their-runs/2022/02/18/e19a67ca-90a5-11ec-8ddd-52136988d263_story.html']

        # scrap article details (multiprocessing method)
        t1 = time.time()
        MAX_WORKER_NUM = multiprocessing.cpu_count()
        p = Pool(MAX_WORKER_NUM)
        for i in range(20):
            p.apply_async(parse_task, args=(urls[startat+i].strip(),directory,force,))
            # parse_task(urls[2],directory,force)
        p.close()
        p.join()
        print("spent：",time.time()-t1)

        # sleep every 100 articles
        if (startat % 100) ==0 and startat != 0:
            time.sleep(15)
            print("sleep")
            # break


def parse_task(url,directory,force):

    # # check file has been already scraped
    # date_strf = '-'.join(url.strip("/").split('/')[-4:-1])
    # last_part = url.strip("/").split('/')[-1].split('.')[0]
    # filepath1 = './output/china_2018/{}_{}.json'.format(date_strf, last_part)
    # filepath = '{}/{}_{}.json'.format(directory, date_strf, last_part)


    # get article detail
    json_obj = parse_page(url)

    # check empty soup
    # if not json_obj:
    #     # n_exceptions += 1
    #     print("n_exceptions" + str(n_exceptions))
    #     return 0

    # output wrong urls
    if not json_obj['content']:
        with open("{}/wrong_url.txt".format(directory), 'a', encoding='utf-8') as f:
            f.write(json_obj['url']+"\n")
            print(url)
            return 0

    last_part = url.strip("/").split('/')[-1].split('.')[0]
    print(last_part)
    filepath = '{}/{}_{}.json'.format(directory, json_obj['data_strf'], last_part)
    filepath1 = './output/china/{}_{}.json'.format(json_obj['data_strf'], last_part)
    if os.path.exists(filepath1):
        if not force:
            return 0
        print('Already scraped from {}'.format(url))
        return 0

    # save article detail
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=2)
        # print("ok")

    # print('url = {}'.format(url))
    # print('file path = {}'.format(filepath), end='\n\n')
    # time.sleep(random.uniform(sleep - 1, sleep + 2))

if __name__ == '__main__':
    main()
