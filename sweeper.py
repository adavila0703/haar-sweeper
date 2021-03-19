import time
import requests
from requests.api import request
from requests.exceptions import MissingSchema, InvalidSchema, SSLError
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, StaleElementReferenceException
import cv2



def sweep_sweep(keyword, pics, headless) -> None:
    search = keyword.replace(' ', '%20')
    site_url = f'https://www.bing.com/images/search?q={search}&qft=+filterui:aspect-square&form=IRFLTR&first=1&tsc=ImageBasicHover'
    
    #cascades
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    
    if headless == True:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('chromedriver.exe')

    driver.get(site_url)

    pic_urls = set()
    
    images = driver.find_elements_by_tag_name('img')
    for image in images:
        if image.get_attribute('alt') == f'Image result for {keyword}':
            image.click()
            break

    driver.switch_to.frame('OverlayIFrame')

    pic_num = 0
    for pic in range(0, pics + 1):
        try:
            images = driver.find_elements_by_tag_name('img')
            for image in images:
                if image.get_attribute('alt') == 'See the source image' and image.get_attribute('tabindex') == '0':
                    # gray = cv2.cvtColor(face_check, cv2.COLOR_BGR2RGB)
                    # faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
                    # if faces != []:
                    #     pic_urls.add(image.get_attribute('src'))
                    url = image.get_attribute('src')
                    
                   
                    if url.endswith('png') == False and url.endswith('jpg') == False and url.endswith('ImgRaw') == False and url.endswith('jpeg') == False:
                        print('continue', url)
                        continue

                    try:
                        request = requests.get(url)
                    except SSLError:
                        continue                  

                    file = open('pics/' + str(pic_num) + '.png', 'wb')
                    file.write(request.content)
                    file.close()
                    face_pic = cv2.imread(f'pics/{str(pic_num)}.png')
                    gray = cv2.cvtColor(face_pic, cv2.COLOR_BGR2RGB)
                    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
                    
                    
                    time.sleep(1)
                    pic_num += 1
                    if len(faces) == 0 and pic_num != 0:
                        print('no faces', url)
                        pic_num -= 1
                        

                   


            icons = driver.find_elements_by_class_name('icon')
            for icon in icons:
                if icon.get_attribute('title') == 'Next image result':
                    icon.click()
        except StaleElementReferenceException:
            pass
        
    # for t in enumerate(pic_urls):
    #     try:
    #         request = requests.get(t[1])
    #         file = open('pics/' + str(t[0]) + '.png', 'wb')
    #         file.write(request.content)
    #         file.close()
    #     except InvalidArgumentException:
    #         pass
    #     except MissingSchema:
    #         pass
    #     except IndexError:
    #         pass
    #     except InvalidSchema:
    #         pass
    # return None

if __name__ == '__main__':
    sweep_sweep('faces', 100, False)
