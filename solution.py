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

    month_mapping = {'января': '01',
                     'февраля': '02',
                     'марта': '03',
                     'апреля': '04',
                     'мая': '05',
                     'июня': '06',
                     'июля': '07',
                     'августа': '08',
                     'сентября': '09',
                     'октября': '10',
                     'ноября': '11',
                     'декабря': '12'}

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

            # date classification
            text = text.lower()
            search_text = text[:160] + text[-60:]
            
            # search max year
            years = re.findall(r'201\d', search_text)
            if not years:
                search_text = text
                years = re.findall(r'201\d', search_text)
            years = set(map(int, years))
            year = max(years) if years else '2014'
            
            # search date
            dates = re.findall(r'\d\d \w+ '+str(year), search_text)
            if dates:
                date = dates[-1]
                date = date.replace(' ', '.')
                for month, number in self.month_mapping.items():
                    date = date.replace(month, number)
            else:
                dates = re.findall(r'\d\d\.\d\d\.'+str(year), search_text)
                if dates:
                    date = dates[0]
                else:
                    date = '26.12.2014'

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


if __name__ == '__main__':
    S = Solution()
    S.train(None)
    texts = []
    for file in os.listdir('train/txts'):
        with open('train/txts/' + file) as f:
            texts.append(f.read())
    S.predict(texts)

