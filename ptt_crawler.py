from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

EXPLORE_PAGE = 1
PUSH_SPEC = 10

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
            print("18禁網頁")
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
        
    def store_pic(self, url, pic_url_list):
        # 檢查看板是否為18禁,有些看板為18禁

        soup, _ = self.over18(url)
        # crawler_time = url.split('/')[-2] + crawler_time
        # 避免有些文章會被使用者自行刪除標題列
        try:
            title = soup.select('.article-meta-value')[2].text
        except Exception as e:
            title = "no title"

        # 抓取圖片URL(img tag )
        for img in soup.find_all("a", rel='nofollow'):
            img_url = self.image_url(img['href'])
            if img_url:
                pic_url_list.append(img_url)
        

    def craw_page(self, rs, url):

        url = 'https://www.ptt.cc' + url
        res = rs.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        
         
        soup_ = BeautifulSoup(res.text, 'html.parser')
        article_seq = []
        for r_ent in soup_.find_all(class_="r-ent"):
            try:
                # 先得到每篇文章的篇url
                link = r_ent.find('a')['href']
                if link:
                    # 確定得到url再去抓 標題 以及 推文數
                    title = r_ent.find(class_="title").text.strip()
                    rate = r_ent.find(class_="nrec").text
                    url = 'https://www.ptt.cc' + link
                    if rate:
                        if rate.startswith('爆'):
                            rate = 100
                        elif rate.startswith('X'):
                            rate = -1
                        else:
                            rate = int(rate)
                    else:
                        rate = 0
                    # 比對推文數
                    if int(rate) >= push_rate:
                        article_seq.append({
                            'title': title,
                            'url': url,
                            'rate': rate,
                        })
            except Exception as e:
                # print('crawPage function error:',r_ent.find(class_="title").text.strip())
                print('本文已被刪除', e)
        return article_seq

    def PushCnt_Calculte(self, push_cnt):

        if push_cnt == "爆":
            return 100
        elif push_cnt.find("X") > 0 :
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
        print(url_list)

        target_time = datetime.now() - timedelta(days=1)
        print("target_time={}".format(target_time))

        find = True
        while url_list and find :
            url = url_list.pop(0)
            res = rs.get(url, verify=False)
            soup = BeautifulSoup(res.text, 'html.parser')
            find = False # initial
            
            print("start crawler page {}".format(url))
            
            for r_ent in soup.find_all(class_="r-ent"):
                try:
                    subject = r_ent.find('div', class_="title")
                    if subject.a == None:
                        # print("本文已被刪除")
                        continue
                    print("subject={}".format(subject.a.string))                
                        
                    link = r_ent.find('a')['href']
                    print("link={}".format(link))

                    date_li = r_ent.find("div", class_="date").string.split('/')
                    print("dateli={}".format(date_li))

                    push_cnt = self.PushCnt_Calculte(r_ent.find(class_="nrec").text)

                    print("push_cnt={}".format(push_cnt))
                    
                    if int(date_li[0]) == target_time.month  and int(date_li[1]) == target_time.day and push_cnt > PUSH_SPEC:
                        print("Need process")
                        self.craw_page(rs, link)
                        find = True # has find target day, need continue
                    
                    if r_ent.next_sibling:
                        if r_ent.next_sibling.next_sibling:
                            next_class_type = r_ent.next_sibling.next_sibling.get('class')[0]
                            if next_class_type == "r-list-sep":
                                break

            #         print(type(r_ent))

                except Exception as e:
                    print('Error={}'.format(e))
                    print(r_ent)

                    
        print(url_list)






        all_page_url = soup.select('.btn.wide')[1]['href']
    
        # https://stackoverflow.com/questions/38395751/python-beautiful-soup-find-string-and-extract-following-string
        for td in soup.find_all("div",class_="date"):
            print(td.find_next_sibling("div",class_="r-list-sep"))


        start_page = self.get_page_number(all_page_url)
        page_term = 2  # crawler count
        push_rate = 10  # 推文
        index_list = []
        article_list = []
        url_list = []
        for page in range(start_page, start_page - page_term, -1):
            page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
            index_list.append(page_url)

        # 抓取 文章標題 網址 推文數
        while index_list:
            index = index_list.pop(0)
            res = rs.get(index, verify=False)
            # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
            if res.status_code != 200:
                index_list.append(index)
                # print u'error_URL:',index
                # time.sleep(1)
            else:
                article_list = self.craw_page(res, push_rate)
                # print u'OK_URL:', index
                # time.sleep(0.05)
        content = ''
        for article in article_list:
            data = '[{} push] {}\n{}\n\n'.format(article.get('rate', None), article.get('title', None),
                                                article.get('url', None))
            self.store_pic(article.get('url', None), url_list)

            content += data
        return content, url_list



if __name__ == "__main__" :
    ptt = ptt_craw()
    tmp, url_list = ptt.ptt_beauty(requests)
    print(tmp)
    print(url_list)