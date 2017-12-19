# -*- coding: utf-8 -*-
import time
from multiprocessing.dummy import Pool as Threadpool
import sys
import requests #请求
from lxml import etree #数据解析
import pymongo
import json

# lllllllllllllllllllllllllllllllllllll
def get_response(url):
    html = requests.get(url,headers = headers) #发送一次请求
    selector = etree.HTML(html.text)
    product_list = selector.xpath('//*[@id="J_goodsList"]/ul/li')
    #print product_list
    for product in product_list:
        try:
            sku_id = product.xpath('@data-sku')[0]
            product_url = 'https://item.jd.com/{}.html'.format((str(sku_id)))
            get_data(product_url)
        except Exception as e:
            print(e)

def get_data(product_url):
    '''
    获取商品详情
    ：param url:
    :return
    '''
    product_dict = {}
    html = requests.get(product_url,headers = headers)
    selector = etree.HTML(html.text)
    product_infos = selector.xpath('//ul[@class="parameter2 p-parameter-list"]')
    for product in product_infos:
        product_number = product.xpath('li[2]/@title')[0]
        product_price = get_product_price(product_number)
        product_dict['商品名称'] = product.xpath('li[1]/@title')[0]
        product_dict['id'] = product_number
        product_dict['商品产地'] = product.xpath('li[4]/@title')[0]
        product_dict['商品价格'] = product_price

    # for key,items in product_dict.items():
    # 	print key,items
    # print product_dict
    save(product_dict)

def get_product_price(sku_id):
    '''获取价格
    ：param sku:
    : return:
    '''
    price_url = 'https://p.3.cn/prices/mgets?&skuIds=J_{}'.format(str(sku_id))
    response = requests.get(price_url, headers = headers).content
    response_json = json.loads(response)

    for info in response_json:
        # print info
        return info.get('p')


def save(product_list):
    '''
    保存数据
    '''
    client = pymongo.MongoClient()
    db = client['product_dict'] #数据库
    content = db['jd'] #表
    print(product_list)
    content.insert(product_list)

if __name__ == '__main__':
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    urls = ['https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.T04&wq=shouji&cid2=653&cid3=655&ev=exbrand_%E5%B0%8F%E8%BE%A3%E6%A4%92%40&uc=0#J_searchWrap']
    # urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.T04&wq=shouji&cid2=653&cid3=655&page={}&s=241&click=0'.format(page) for page in range(1,10,2)]
    # urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.T04&wq=shouji&cid2=653&cid3=655&page=1&s=241&click=0']

    pool = Threadpool(2)
    start_time = time.time()
    # print(start_time)
    pool.map(get_response,urls)
    pool.close()
    pool.join()
    end_time = time.time()
    print("%d second" % (end_time - start_time))

