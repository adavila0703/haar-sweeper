import time
import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import cv2
import os
import numpy as np

def set_options(*args, **kwargs) -> webdriver.Chrome:
    if kwargs['headless']:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('chromedriver.exe')
    return driver

def sweep_sweep(keyword, pics, headless, size) -> None:
    search = keyword.replace(' ', '%20')
    site_url = f'https://www.bing.com/images/search?q={search}&qft=+filterui:aspect-square&form=IRFLTR&first=1&tsc=ImageBasicHover'
    driver = set_options(headless=headless)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    driver.get(site_url)

    images = driver.find_elements_by_tag_name('img')
    for image in images:
        if image.get_attribute('alt') == f'Image result for {keyword}':
            image.click()
            break

    driver.switch_to.frame('OverlayIFrame')

    for pic in range(0, pics + 1):
        try:
            image_path = driver.find_element_by_xpath('//*[@id="mainImageWindow"]/div[2]/div/div/div/img')
            url = image_path.get_attribute('src')
            request = requests.get(url, stream=True).raw

            if request.headers['Content-Type'] != 'image/png' and request.headers['Content-Type'] != 'image/jpeg':
                print('continue', url)
                raise(Exception, 'Not Img')  

            image = np.array(bytearray(request.read()), dtype='uint8')
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            resize = cv2.resize(image, size)
            faces = faceCascade.detectMultiScale(resize, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
            
            time.sleep(0.5)
            if len(faces) == 0 and pic != 0:
                raise(Exception, 'No face') 

            cv2.imwrite(f'pics/{str(pic)}.png', resize)          
            icons = driver.find_element_by_xpath('//*[@id="navr"]/span')
            icons.click()

        except Exception as e:
            print('error', e)
            time.sleep(1)
            icons = driver.find_element_by_xpath('//*[@id="navr"]/span')
            icons.click()

def rescale():
    files = os.listdir('pics')

    for file in files:
        img_path = str(file)
        img = cv2.imread('pics/' + file, cv2.IMREAD_GRAYSCALE)
        resize = cv2.resize(img, (100, 100))
        cv2.imwrite(img_path, resize)


if __name__ == '__main__':
    sweep_sweep('faces', 50, False, (100, 100))
