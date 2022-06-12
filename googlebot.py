from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from censor import censor_words
import time
import warnings
warnings.filterwarnings("ignore")

def newline():
    ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

def get_current_chat():
    print("printing current chat...")
    current_chat_xpath = '//span[@class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr"]'
    current_chat_elements = driver.find_elements_by_xpath(current_chat_xpath)
    current_chat_name = current_chat_elements[-1].get_attribute("title")
    print(">Current chat = "+current_chat_name)
    return current_chat_name

def go_to_chat(chat_name):
    search_xpath = '//div[@class="_13NKt copyable-text selectable-text"][@data-tab="3"]'
    search_box = driver.find_element_by_xpath(search_xpath)
    print(">Going to chat "+chat_name)
    search_box.send_keys(chat_name+Keys.ENTER)

def get_latest_message():
    messages = driver.find_elements_by_xpath('//span[@class="i0jNr selectable-text copyable-text"]')
    latest_message = messages[len(messages)-1].get_attribute("innerText")
    return latest_message

def send_message(string):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'#'//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    input_box.send_keys("_*GoogleBot:*_ "+string + Keys.ENTER)
    print(">Message sent")

def send_link(url, x):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]' #'//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    input_box.send_keys('_*GoogleBot:*_')
    newline()
    input_box.send_keys('Link for '+x)
    newline()
    input_box.send_keys(url)
    input_box.send_keys(Keys.ENTER)

def send_intro():
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]' #'//div[@class="_13NKt copyable-text selectable-text"][@data-tab="9"]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    input_box.send_keys('_*GoogleBot:*_')
    newline()
    input_box.send_keys('bot get <search terms>')
    input_box.send_keys(Keys.ENTER)

def fetch_url(x):
    driver.switch_to.window(driver.window_handles[1])
    search_box_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'#'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input' #'//div[@class="YacQv gsfi"]'
    feeling_lucky_xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[2]'#'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[2]'
    search_box = driver.find_element_by_xpath(search_box_xpath)
    search_box.send_keys(x)
    print(x)
    
    feeling_lucky_button = driver.find_element_by_xpath(feeling_lucky_xpath)
    feeling_lucky_button.click()
    time.sleep(0.1)
    url = driver.current_url
    driver.get('https://google.com')
    driver.switch_to.window(driver.window_handles[0])
    return url

def convert(lst):
    return (lst.split())

def censor_check(x):
    words = convert(x)
    flag = True
    for i in words:
        print(i)
        if i in censor_words:
            flag = False
            break
    return flag

def functionality(x):
    print(">Latest message = "+x)
    if(x.startswith("bot get ")):
        x = x.replace('bot get ', '')
        if(True):
            print(x)
            url = fetch_url(x)
            # url = "ok"
            print(url)
            send_link(url, x)
        else:
            send_message("https://giphy.com/gifs/giphyqa-LAKIIRqtM1dqE", x)
        
    elif(x == "go home bot"):
        send_message("bye")
        go_to_chat(home_chat)
        send_intro()

    elif(x.startswith("bot go to ")):
        chat_name = x.replace('bot go to ', '')
        current_chat = get_current_chat()
        if(current_chat==home_chat):
            send_message("I am going to "+chat_name)
            go_to_chat(chat_name)
            send_intro()
        else:
            send_message("You can't ask me to go to "+chat_name+" from "+current_chat)

def initialize():
    opt = Options()
    opt.add_experimental_option("debuggerAddress","localhost:8989")
    func_driver = webdriver.Chrome(chrome_options=opt)
    func_driver.switch_to.window(func_driver.window_handles[0])
    print(">Keep the tab active till your home chat appears")
    return func_driver

print(">Starting Bot...")
home_chat = 'bot home chat' # set your private chat
print("Home chat = "+home_chat)
print(">Initializing driver...")
driver = initialize()
go_to_chat(home_chat)
print(">Driver initialized.")
old = ""
while(True):
    try:
        x = get_latest_message().lower()
        if old==x:
            continue
        old = x
        functionality(x)
    except:
        send_message("Something went wrong")
        print(">ERROR")
    time.sleep(1)
