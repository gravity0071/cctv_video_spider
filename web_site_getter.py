# 爬取视频
# todo 现在可以爬到2016-02-03 再往前网页版本不一样，还要重写
import os

from selenium import webdriver
from time import sleep

import download_m3u8_video

video_name_full = ''
store_path = '/Users/shawnwan/Downloads/cctv_spider/'  # todo need to replace it to wherever you want to store the video to


# get the second page which contains the link of the video
def second_page(video_name, video_link):
    video_browser = webdriver.Chrome()
    try:
        video_browser.get(video_link)
        sleep(5)

        source_link_element = video_browser.find_element_by_xpath('//video[@id="_video_player_html5_api"]/source')
        source_link = source_link_element.get_property('src')
        # print(source_link)
        download_m3u8_video.ts_long(source_link, video_name, store_path)
        return

    finally:
        video_browser.quit()


def first_page(video_name_full):
    browser = webdriver.Chrome()
    url = 'https://tv.cctv.com/lm/xwlb/index.shtml'
    # browser = webdriver.Safari()
    try:
        browser.get(url)  # get into the link
        # browser.add_argument('blink-settings=imagesEnabled=false')
        sleep(5)
        select_year = browser.find_element_by_class_name('select_year')

        # select all the years interably
        years = browser.find_elements_by_xpath('//*[@class="swiper-slide cur"]')
        # test_count = 0 #todo delete
        for year in years:
            # if test_count < 8:
            #     test_count = test_count + 1
            #     continue
            # test_count = test_count + 1
            select_year.click()
            year.click()
            select_month = browser.find_elements_by_class_name('select')

            months = browser.find_elements_by_xpath('//*[@id="riliscrollbar2"]/div/ul/*[@class="swiper-slide"]')
            for month in months:
                select_month[1].click()
                if not month.is_displayed():
                    continue
                month.click()
                sleep(1)

                # get all the elements of the video
                table = browser.find_elements_by_xpath('//*[@id="idCalendar"]/tr/td')
                for i in table:
                    style_i = i.get_property('style')
                    if not len(style_i) == 0:
                        if style_i[0] == 'cursor':
                            break
                    class_i = i.get_attribute('class')
                    if not class_i == '':
                        if class_i == 'empty':
                            continue

                    i.click()
                    sleep(1)  # todo adjusting the sleep time according to the web speed
                    not_exists_video = browser.find_element_by_xpath('//*[@class="shadow_box"]/div/div[@class="btn"]')
                    if browser.find_element_by_class_name('lanmu19629_notjm_shadow').is_displayed():
                        not_exists_video.click()
                        continue

                    is_new_version = 0  # 0: new version 1: old version
                    # get the second page link
                    try:
                        video_element = browser.find_elements_by_xpath('//*[@class="rililist newsList"]/li/a')
                        video_element[0].get_property('title')
                    except:
                        is_new_version = 1
                        video_element = browser.find_elements_by_xpath('//*[@class="rililist newsList"]/ul/li/a')

                    # sleep in case of the delay of the network
                    if is_new_version == 0:
                        video_name_full_delay = video_element[0].get_property('title')
                    else:
                        video_name_full_delay = browser.find_element_by_xpath(
                            '//*[@class="rililist newsList"]/ul/li/a/div[@class="text"]/div[@class="title"]').text
                    if video_name_full_delay == video_name_full:
                        sleep(5)
                        video_element = browser.find_elements_by_xpath('//*[@class="rililist newsList"]/li/a')

                    if is_new_version == 0:
                        video_name_full = video_element[0].get_property('title')
                    else:
                        video_name_full = browser.find_element_by_xpath(
                            '//*[@class="rililist newsList"]/ul/li/a/div[@class="text"]/div[@class="title"]').text
                    video_name = video_name_full[7: 15]

                    # if the video exists, then it don't need to download again
                    if os.path.exists(store_path + video_name + '.mp4'):
                        continue
                    video_link = video_element[0].get_property('href')
                    print(video_name + " :" + video_link)
                    second_page(video_name, video_link)

                    if not class_i == '':
                        if class_i == 'current':
                            break
    finally:
        browser.quit()


if __name__ == '__main__':
    while True:
        try:
            first_page(video_name_full)
        except Exception as e:
            print("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + e)
