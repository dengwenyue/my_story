# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import threading
import os
import Queue

URL = "https://www.qu.la"

url_queue = Queue.Queue()


def retry(max_times=3, slient=True):
    def wrapper(func):
        def decorate(*args, **kwargs):
            for _ in range(max_times):
                try:
                    result = func(*args, **kwargs)
                    if result:
                        return result
                except Exception as e:
                    if not slient:
                        raise e
        return decorate
    return wrapper


@retry()
def crawler(book_id):
    url = URL + "/book/" + book_id
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.content, "html.parser")
    dds = soup.find_all("dd")
    for i, dd in enumerate(dds):
        name = dd.a.string
        dd_url = dd.a['href']
        print i
        url_queue.put((name, dd_url))
    return "ok"


def get_content():
    while 1:
        try:
            name, url = url_queue.get(block=False, timeout=3)
        except Exception as e:
            print e
            break
        url = URL + url
        res = requests.get(url, verify=False)
        soup = BeautifulSoup(res.content, "html.parser")
        content = soup.find("div", id="content")
        filename = name.split()[0] + '.txt'
        filename = os.path.join("/tmp", filename)
        with open(filename, 'w') as f:
            f.write(str(content))
        url_queue.task_done()


if __name__ == "__main__":
    crawler('11517')
    t = threading.Thread(target=get_content, args=())
    t.start()
    t.join()
