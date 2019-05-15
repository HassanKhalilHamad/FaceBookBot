from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import argparse

class FacebookBot:
    def __init__(self,username,password,hashtag,status_report=False):
        self.username = username
        self.password = password
        self.hashtag = hashtag

        self.status_report = status_report

        options = Options()
        options.add_argument("--disable-notifications")

        if self.status_report: print("Opening chromedriver...")
        self.wd = webdriver.Chrome(chrome_options=options)
        if self.status_report: print("Logging in...")
        self.login()

    def login(self):
        self.wd.get("https://www.facebook.com/login")
        self.wd.find_element_by_id("email").send_keys(self.username)
        self.wd.find_element_by_id("pass").send_keys(self.password)
        self.wd.find_element_by_id("loginbutton").click()



    def get_posts(self):
        articles = self.wd.find_elements_by_xpath("//span[@data-testid='UFI2TopReactions/tooltip_LIKE']//a[@role='button']")
        return articles


    def scroll(self,page_end=100):
        find_elem = None
        scroll_from = 0
        scroll_limit = self.wd.execute_script("return document.body.scrollHeight")
        i = 0
        while not find_elem:
            self.wd.execute_script("window.scrollTo(%d, %d);" % (scroll_from, scroll_from + scroll_limit))
            scroll_from += scroll_limit
            i += 1
            if page_end and i >= page_end:
                break
            try:
                find_elem = self.wd.find_element_by_xpath("//span[@class='_38my']")
                find_elem.click()
            except exceptions.ElementNotVisibleException:
                find_elem = None
            except exceptions.NoSuchElementException:
                find_elem = None


    def search(self):
        if self.status_report: print("searshing for your Hashtag")
        self.wd.find_elements_by_css_selector('form input')[0].send_keys(self.hashtag)
        self.wd.find_element_by_css_selector("button[aria-label='Search']").click()
        if self.status_report: print("Waiting Page To Load")
        time.sleep(15)
        if self.status_report: print("Filtering All Public Posts")
        self.wd.find_element_by_xpath("(//span[contains(.,'Public')])[2]").click()
        if self.status_report: print("Waiting Page To Load")
        time.sleep(10)


    def automate(self,unlike=False,page_end=100):
        if self.status_report: print("Forcing Facebook to load the posts...")
        self.scroll(page_end)
        if self.status_report: print("Scrolled down %s times" % page_end)
        if self.status_report: print("%s posts..." % ("Unliking" if unlike else "Liking"))
        self.wd.execute_script("window.scrollTo(0,0);")
        posts = self.get_posts()
        num = 0
        for p in posts:
             p.click()
             time.sleep(8)
             L = self.wd.find_element_by_xpath("//a[@data-testid='UFI2ReactionLink']").click()
             B = self.wd.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
             time.sleep(4)

           


    def close(self):
        self.wd.close()
        


ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", required=True, help="your user name")
ap.add_argument("-p", "--pasw", required=True, help="your password")
ap.add_argument("-k", "--hashtag", required=True, help="your key word")
ap.add_argument("-l", "--like", required=True, help="number of likes")

args = vars(ap.parse_args())

username = args["user"]
password = args["pasw"]
hasht = args["hashtag"]
numLikes = int(args["like"])
bot = FacebookBot(username,password,hasht,status_report=True)
bot.search()
bot.automate(page_end=numLikes)
bot.close()
