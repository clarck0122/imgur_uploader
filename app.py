from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta
import time
import logging
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import os
import sys
from uploader import *
from time import sleep

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

EXPLORE_PAGE = 5
PUSH_SPEC = 30
UPLOAD_LIMIT = 100

class ptt_craw():
    def get_page_number(self, content):
        start_index = content.find('index')
        end_index = content.find('.html')
        page_number = content[start_index + 5: end_index]
        return int(page_number) + 1

    def over18(self, url):
        res = requests.get(url, verify=False)
        # 先檢查網址是否包含'over18'字串 ,如有則為18禁網站
        if 'over18' in res.url:
            logger.debug("18禁網頁")
            # 從網址獲得版名
            board = url.split('/')[-2]
            load = {
                'from': '/bbs/{}/index.html'.format(board),
                'yes': 'yes'
            }
            res = requests.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
        return BeautifulSoup(res.text, 'html.parser'), res.status_code

    def image_url(self, link):
        # 符合圖片格式的網址
        image_seq = ['.jpg', '.png', '.gif', '.jpeg']
        for seq in image_seq:
            if link.endswith(seq):
                return link
        # 有些網址會沒有檔案格式， "https://imgur.com/xxx"
        if 'imgur' in link:
            return '{}.jpg'.format(link)
        return ''
        
    # def store_pic(self, url, pic_url_list):
    #     # 檢查看板是否為18禁,有些看板為18禁

    #     soup, _ = self.over18(url)
    #     # crawler_time = url.split('/')[-2] + crawler_time
    #     # 避免有些文章會被使用者自行刪除標題列
    #     try:
    #         title = soup.select('.article-meta-value')[2].text
    #     except Exception as e:
    #         title = "no title"

    #     # 抓取圖片URL(img tag )
    #     for img in soup.find_all("a", rel='nofollow'):
    #         img_url = self.image_url(img['href'])
    #         if img_url:
    #             pic_url_list.append(img_url)
        

    def craw_page(self, rs, url, pic_url_list):

        url = 'https://www.ptt.cc' + url
        res = rs.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')


        soup, _ = self.over18(url)
        # crawler_time = url.split('/')[-2] + crawler_time
        # 避免有些文章會被使用者自行刪除標題列
        try:
            title = soup.select('.article-meta-value')[2].text
        except Exception as e:
            title = "no title"

        i = 1
        # 抓取圖片URL(img tag )
        for img in soup.find_all("a", rel='nofollow'):
            img_url = self.image_url(img['href'])
            if img_url:
                objurl = []
                objurl.append(title + "_" + str(i))
                objurl.append(img_url)
                pic_url_list.append(objurl)
                logger.debug(objurl)
                i += 1


    def PushCnt_Calculte(self, push_cnt):

        if push_cnt == "爆":
            return 100
        elif push_cnt.startswith("X") :
            return -1
        elif push_cnt == "":
            return 0
        else:
            return int(push_cnt)
            

    def ptt_beauty(self, requests):
        rs = requests.session()
        res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)

        page_option = soup.find(id="action-bar-container")
        tag = page_option.find_all(class_="btn wide")[1]
        link = tag.get('href')
        index = int(link[link.find('index')+5:link.find('.html')])

        url_list = []
        for i in range(EXPLORE_PAGE):
            url_list.append("https://www.ptt.cc/bbs/Beauty/index{}.html".format(index-i))
        # print(url_list)

        target_time = datetime.now() - timedelta(days=1)
        # print("target_time={}".format(target_time))

        pic_url_list = []
        find = True
        while url_list and find :
            url = url_list.pop(0)
            res = rs.get(url, verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            find = False # initial
            
            logger.debug("start crawler page {}".format(url))
            
            for r_ent in soup.find_all(class_="r-ent"):
                try:
                    subject = r_ent.find('div', class_="title")
                    if subject.a == None:
                        # print("本文已被刪除")
                        continue
                    # print("subject={}".format(subject.a.string))                
                        
                    link = r_ent.find('a')['href']
                    # print("link={}".format(link))

                    date_li = r_ent.find("div", class_="date").string.split('/')
                    # print("dateli={}".format(date_li))

                    push_cnt = self.PushCnt_Calculte(r_ent.find(class_="nrec").text)

                    # print("push_cnt={}".format(push_cnt))
                    
                    logger.debug("subject={}, link={}, dateli={}, push_cnt={}".format(subject.a.string, link, date_li, push_cnt))

                    if int(date_li[0]) == target_time.month  and int(date_li[1]) == target_time.day and push_cnt > PUSH_SPEC:
                        logger.debug("Need process, {}".format(link))
                        self.craw_page(rs, link, pic_url_list)
                        
                    
                    page_time = datetime.strptime( str(target_time.year) + '/' + str(int(date_li[0])) + '/' +  str(int(date_li[1])), '%Y/%m/%d')
                    if page_time.date() >= target_time.date() :
                        find = True # has find target day, need continue

                    if r_ent.next_sibling:
                        if r_ent.next_sibling.next_sibling:
                            next_class_type = r_ent.next_sibling.next_sibling.get('class')[0]
                            if next_class_type == "r-list-sep":
                                break

            #         print(type(r_ent))

                except Exception as e:
                    logger.debug('Error={}'.format(e))
                    logger.debug(r_ent)

                    
        logger.debug(url_list)
        return pic_url_list



if __name__ == "__main__" :

    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.DEBUG)
    # add a rotating handler
    if os.path.isdir("./Log") == False:
        os.mkdir("./Log")
    handler = RotatingFileHandler('./Log/myapp.log', maxBytes=2*1024*1024,
                                  backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    ptt = ptt_craw()
    pic_url_list = ptt.ptt_beauty(requests)
    # print(tmp)
    # logger.debug(pic_url_list)
    
    imgur = uploader()
    imgur.logger = logger
    cnt = 0

    while pic_url_list:
        cnt += 1
        objurl = pic_url_list.pop(0)
        logger.debug("Cnt={}, upload... {}, {}".format(cnt, objurl[0], objurl[1]))

        if not imgur.upload_photo(objurl[1], imgur.album_id,objurl[0]):
            logger.debug("Occur Error, stop upload.")
            break
        
        if cnt >= UPLOAD_LIMIT:
            logger.debug("Reach UPLOAD_LIMIT. stop upload.")
            break
        
        sleep(1)
    # print("upload... {}".format(url))