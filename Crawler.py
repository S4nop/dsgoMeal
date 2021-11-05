from bs4 import BeautifulSoup
import requests


class DsgoMealCrawler:
    def get_meal_info(self, date):
        page = requests.get(f"http://www.dsgo.kr/meal/formList.do?menugrp=050602&searchYM={date['year']}{date['month']}&searchDay={date['day']}")
        soup = BeautifulSoup(page.content, 'html.parser')

        info_list = soup.select('.textBox')
        return self.__post_process(info_list)

    def __post_process(self, info_html_list):
        lunch_html, dinner_html = info_html_list
        lunch_text = lunch_html.text.replace('\n', '').replace(',', '\n')
        dinner_text = dinner_html.text.replace('\n', '').replace(',', '\n')

        return lunch_text, dinner_text