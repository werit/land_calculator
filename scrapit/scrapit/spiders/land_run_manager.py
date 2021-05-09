import scrapy
import time
from datetime import date, datetime
import psycopg2
import json


class LandRunManager(scrapy.Spider):
    name = "land400-1200"

    def start_requests(self):
        start_urls = [
            'https://www.sreality.cz/api/cs/v2/clusters?category_main_cb=3&category_sub_cb=19&category_type_cb=1'
            '&estate_area=400|1200&leftBottomBounding=11.446373078124992|49.109722273228115&locality_region_id=11|10'
            f'&rightTopBounding=17.752525421874992|50.951394924112556&tms={self.get_time_in_ms()}&zoom=18'
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(f'Page is: {page}')
        conn_string = "host='192.168.99.100' dbname='admin' user='admin' password='koko'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        filename = f'quotes-{page}.json'
        res = []
        data = json.loads(response.body)
        datetime_processed = datetime.now()
        for cluster_item in data['clusters']:
            lat_lon_dct = cluster_item['center']
            for estate_id in cluster_item['estate_ids']:
                # TODO: I am missing something like processing batch_id
                res.append((estate_id, lat_lon_dct['lat'], lat_lon_dct['lon'], cluster_item['average'],
                            cluster_item['size'], datetime_processed, 'sreality'))
        args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in res)
        cursor.execute(b"INSERT INTO land VALUES " + args_str)
        conn.commit()
        self.log(f'Inputs committed')
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

    @staticmethod
    def get_postgre_cursor():
        conn_string = "host='192.168.99.100' dbname='admin' user='admin' password='koko'"
        conn = psycopg2.connect(conn_string)
        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        return conn.cursor()

    def manage_land(self):
        pass

    @staticmethod
    def get_time_in_ms():
        round(time.time() * 1000)


def test_method():
    tup = [(12345, 49.11, 14.2, 500, 1, date.today(), 'test'), (12346, 49.66, 14.25, 1500, 1, date.today(), 'test')]

    cursor = LandRunManager.get_postgre_cursor()
    a = cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", tup[0])
    b = [x for x in tup]
    # args_str = ','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
    filename = f'quotes-1.json'
    print(a)
    print(type(a))
    print(type(b))
    print(b)
    print(len(b))
    args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
    print(args_str)


if __name__ == '__main__':
    test_method()
