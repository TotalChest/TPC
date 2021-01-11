from typing import List, Tuple
import os
import re


class Solution:
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
        pass

    def train(self, train: List[Tuple[str, dict]]) -> None:
        pass

    def predict(self, test: List[str]) -> List[dict]:
        results = []
        Author = 'Глава Республики Карелия'
        Date = '26.12.2014'
        Type = 'федеральный закон'
        Number = '831'
        Name = 'о полиции'

        for text in test:

            if 'ПРИКАЗ' in text or 'приказываю' in text:
                Type = 'приказ'
                Numbers = re.findall(r'№ (\d+/?\d*-?[а-яА-Я]*)', text[40:])
                Authors = re.findall(r'^(.*?)\n\n', text, re.S)
            elif 'РАСПОРЯЖЕНИЕ' in text:
                Type = 'распоряжение'
                Numbers = re.findall(r'№ (\d{2,4}-?р?.?)', text)
                Authors = re.findall(r'^РАСПОРЯЖЕНИЕ\n(.*?)\n', text) if text.startswith('РАСПОРЯЖЕНИЕ') \
                                                                      else re.findall(r'^(.*?)\n', text)
                if '' in Authors:
                    Authors = ['Президент Российской Федерации']
            elif 'ФЕДЕРАЛЬНЫЙ ЗАКОН' in text[:50]:
                Type = 'федеральный закон'
                Numbers = re.findall(r'№ (\d{1,4}-ФЗ)', text)[::-1]
                Authors = ['Государственная Дума Федерального собрания Российской Федерации']
            elif 'УКАЗ' in text or 'каз вступает в силу' in text:
                Type = 'указ'
                Numbers = re.findall(r'№ (\d{1,4}-?[уУ]?[гГ]?)', text)[::-1]
                Authors = ['Президент Российской Федерации']
            elif 'ЗАКОН ' in text or 'ЗАКОН\n' in text:
                Type = 'закон'
                Numbers = re.findall(r'№ ([-\dа-яА-Я/]*)', text)[::-1]
                Authors = re.findall(r'Принят (.*?)\n', text)
            else:
                Type = 'постановление'
                Numbers = re.findall(r'№ (\d+-?[а-яА-Я]{0,2})', text)
                Authors = re.findall(r'^(.*?)\n', text)
     
            names = re.findall(r'\n(О .*?|Об .*?)\n\n', text, re.S)
            Name = names[0] if names else ''
            Author = Authors[0] if Authors else 'Правительство Российской Федерации'
            Number = Numbers[0] if Numbers else '96'

            ###################################################################
            ###  DATE without type
            ###################################################################    

            text = text.lower().replace(' ', '')
            search_text = text[:150] + text[-70:]
            
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
            Date = date
            ###################################################################
                
            prediction = {"type": Type,
                          "date": Date,
                          "number": Number,
                          "authority": Author,
                          "name": Name
                         }

            results.append(prediction)

        return results

    def year2data(self, year, search_text):
        return len(re.findall(r'\d\d[а-я]{3,8}'+str(year), search_text) + \
                   re.findall(r'\d\d\.\d\d\.'+str(year), search_text))


# local testing
if __name__ == '__main__':
    S = Solution()
    S.train(None)
    texts = []
    for file in os.listdir('train/txts'):
        with open('train/txts/' + file) as f:
            texts.append(f.read())
    print(S.predict(texts))
    

