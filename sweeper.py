import time
import requests
from requests.api import request
from requests.exceptions import MissingSchema, InvalidSchema
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options



def sweep_sweep(keyword, pics, headless) -> None:
    search = keyword.replace(' ', '%20')
    site_url = f'https://www.bing.com/images/search?q={search}&qft=+filterui:aspect-square&form=IRFLTR&first=1&tsc=ImageBasicHover'
    
    if headless == True:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('chromedriver.exe')

    driver.get(site_url)

    pic_urls = []
    
    images = driver.find_elements_by_tag_name('img')

    for image in images:
        if image.get_attribute('alt') == f'Image result for {keyword}':
            image.click()
            break

    driver.switch_to.frame('OverlayIFrame')

    for pic in range(0, pics + 1):
        try:
            images = driver.find_elements_by_tag_name('img')
            for image in images:
                if image.get_attribute('alt') == 'See the source image' and image.get_attribute('tabindex') == '0':
                    pic_urls.append(image.get_attribute('src'))
            icons = driver.find_elements_by_class_name('icon')
            for icon in icons:
                if icon.get_attribute('title') == 'Next image result':
                    icon.click()
        except StaleElementReferenceException:
            pass
        
    for t in enumerate(pic_urls):
        try:
            request = requests.get(t[1])
            file = open('pics/' + str(t[0]) + '.png', 'wb')
            file.write(request.content)
            file.close()
        except InvalidArgumentException:
            pass
        except MissingSchema:
            pass
        except IndexError:
            pass
        except InvalidSchema:
            pass
    return None

if __name__ == '__main__':
    sweep_sweep('', 50, False)
