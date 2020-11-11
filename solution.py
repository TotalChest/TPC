from typing import List, Tuple
import os
import re


class Solution:
    Types = ['федеральный закон',
             'постановление',
             'приказ',
             'распоряжение',
             'закон',
             'указ']

    month_mapping = {'декабря': '12',
                     'ноября': '11',
                     'октября': '10',
                     'сентября': '09',
                     'августа': '08',
                     'июля': '07',
                     'июня': '06',
                     'мая': '05',
                     'апреля': '04',
                     'марта': '03',
                     'февраля': '02',
                     'января': '01'}

    def __init__(self):
        self.flag = 0

    def train(self, train: List[Tuple[str, dict]]) -> None:
        pass

    def predict(self, test: List[str]) -> List[dict]:
        results = []
        author = 'Глава Республики Карелия'
        date = '26.12.2014'
        T = 'федеральный закон'
        number = '831'
        name = 'о полиции'

        for text in test:

            
            text = text.lower().replace(' ', '')
            #split_text = text.split('\n')
            search_text = text[:140] + text[-60:]
            #search_text = '\n'.join(split_text[:8] + split_text[-5:])
            
            # search max year
            years = set(re.findall(r'201\d', search_text))
            if not years:
                search_text = text
                years = set(re.findall(r'201\d', search_text))
            years = set(map(int, years))

            # drop years without data
            years_with_data = set()
            for year in years:
                if self.year2data(year, search_text):
                    years_with_data.add(year)
            if years_with_data:
                year = max(years_with_data)
            else:
                year = max(years)
            
            # search date
            dates = re.findall(r'\d\d[а-я]{3,8}'+str(year), search_text)
            if dates:
                date = dates[-1]
                date = date[:2] + '.' + date[2:-4] + '.' + date[-4:]
                for month, number in self.month_mapping.items():
                    date = date.replace(month, number)
            else:
                dates = re.findall(r'\d\d\.\d\d\.'+str(year), search_text)
                if dates:
                    date = dates[0]
                else:
                    date = '26.12.2014'
            print(date)

            prediction = {"type": T,
                          "date": date,
                          "number": number,
                          "authority": author,
                          "name": name
                         }

            results.append(prediction)

        return results

    def _prepare_data():
        pass

    def year2data(self, year, search_text):
        return len(re.findall(r'\d\d[а-я]{3,8}'+str(year), search_text) + \
                   re.findall(r'\d\d\.\d\d\.'+str(year), search_text))


if __name__ == '__main__':
    S = Solution()
    S.train(None)
    texts = []
    for file in os.listdir('train/txts'):
        with open('train/txts/' + file) as f:
            texts.append(f.read())
    S.predict(texts) 
    

