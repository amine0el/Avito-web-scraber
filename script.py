import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.avito.ma/fr/tanger/bureaux_et_plateaux-%C3%A0_vendre"

dataset = []

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
for page in range(1, 3):
    if page > 1:
        url += f"?o={page}"
    response = requests.request("GET", url, headers=headers)
    
    if response.status_code != 200:
        break
    
    html_soup = BeautifulSoup(response.text, 'html.parser')
    items_list = html_soup.find(class_="sc-1nre5ec-1 fzpnun listing").find_all("div", class_="sc-jejop8-0 epNjzr")
    
    for item in items_list:
        item_url = item.find('a', href=True)['href']
        item_response = requests.get(item_url,headers=headers)
        
        if item_response.status_code != 200:
            break

        soup = BeautifulSoup(item_response.text, "html.parser")
        
        title_element = soup.find('h1', class_='sc-1g3sn3w-12 mnjON')
        title = title_element.text

        price_element = soup.find('p', class_='sc-1x0vz2r-0 kzRRVw sc-1g3sn3w-13 kliyMh')
        if price_element != None:
            price = int(''.join(re.findall(r'\d', price_element.text)))
        else:
            price = ''

        data_list = soup.find_all('li', class_= "sc-qmn92k-1 ldnQxr")

        data = {}
        data['title'] = title
        data['price'] = price
        for item in data_list:
            key_element = item.find('span', class_='sc-1x0vz2r-0 brylYP')
            value_element = item.find('span', class_='sc-1x0vz2r-0 jsrimE')
            if key_element and value_element:
                key = key_element.text.strip()
                value = value_element.text.strip()
                data[key] = value
        
        data['item_url'] = item_url

        dataset.append(data)


ds = pd.DataFrame(dataset)
# Save the DataFrame as an Excel file
ds.to_excel("Avito_Dataset.xlsx", index=False)