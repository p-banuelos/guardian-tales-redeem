import json
import requests
from bs4 import BeautifulSoup

class GuardianTales:
    def __init__(self, user_id, region = 'EU'):
        self.user_id = user_id
        self.region = region
        self.url = 'https://www.guardiantales.com'
        self.url_redeem = f'{self.url}/coupon/redeem'
        self.request_headers = { 
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        }
        self.form_headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        }
        self.old_coupons = self.load_old()
        self.data = {
            "region": self.region,
            "userId": self.user_id,
            "code": None
        }

    def redeem(self, coupon):
        if coupon not in self.old_coupons:
            self.data['code'] = coupon
            try:
                with requests.post(
                    url=self.url_redeem, 
                    data=self.data, 
                    headers=self.form_headers,
                    timeout=60
                ) as response:
                    if response.status_code == 200:
                        if f'Something unexpected has occurred' in response.text:
                            print(f'Seems the coupon {coupon}, is no longer valid')
                        elif f'already expired' in response.text:
                            print(f'Seems the coupon {coupon}, is expired')                            
                        else:
                            print(f'Coupon {coupon} redeemed')
                        self.store_old(coupon)
                    else:
                        print(f'Error redeeming coupon {coupon}, check the html for error: {response.text}')
            except Exception as e:
                print(f'Error redeeming coupon {coupon}, error: {e}')


    def list_codes(self):
        coupons = []
        with requests.get(
            url='https://www.pockettactics.com/guardian-tales/code',
            headers=self.request_headers
        ) as response:
            if response.status_code == 200:            
                soup = BeautifulSoup(response.text, features='html.parser')
                for list_coupon in soup.find_all('ul'):
                    if any(
                        x for x in ['active', 'expired']
                        if x in format(list_coupon.previous.previous).lower()
                    ):
                        coupons += self.parse_codes(list_coupon)
                        
        with requests.get(
            url='https://ucngame.com/codes/guardian-tales-coupon-codes',
            headers=self.request_headers
        ) as response:
            if response.status_code == 200:            
                soup = BeautifulSoup(response.text, features='html.parser')
                for list_coupon in soup.find_all('tbody')[0]:
                    coupons.append(list_coupon.contents[0].text)

        return list(set(coupons))

    @staticmethod
    def parse_codes(rows):
        return [
            row.text.split(' ')[0]
            for row in rows.contents
            if row != f'\n'
        ]
    
    @staticmethod
    def load_old():
        with open('./guardian_tales/old_coupons.json', 'r') as file:
            array_str = file.read()
        return json.loads(array_str)      
    
    def store_old(self, coupon):
        self.old_coupons.append(coupon)
        with open('./guardian_tales/old_coupons.json', 'w') as file:
            json.dump(self.old_coupons, file, indent=4)