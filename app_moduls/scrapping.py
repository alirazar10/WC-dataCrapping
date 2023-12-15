from bs4 import BeautifulSoup, SoupStrainer
import  requests
import pandas as pd
from time import sleep
class ScrapWebPage(BeautifulSoup):
    
    def init(self):
        super().init()
    
    def get_product_links(self, page_url):
        response_result = requests.get(page_url)
        page_resource = response_result.content
        soup = BeautifulSoup(page_resource, 'lxml')
        div = soup.find_all(attrs={'class' : 'product'})
        porduct_links = {}

        for index, element in enumerate(div):
            links = element.div.find_all(attrs={'class': 'woocommerce-LoopProduct-link woocommerce-loop-product__link'}, href=True)
            porduct_links[index] = links[0].attrs['href']

        next_page_number = soup.find(attrs = {'class' : 'woocommerce-pagination'}) # this is for pagination it is not complete 

        pageULR = ''
        if page_url.endswith('/'):
            pageULR = page_url[:-1]
        else:
            pageULR=page_url

        if next_page_number is not None:
            next_page_number_link = next_page_number.find(attrs = {'class': 'next page-numbers'})
            if next_page_number_link is not None:
                next_page_number_link = next_page_number_link.attrs['href']
                next_page_link = pageULR + next_page_number_link
                number_of_pages = next_page_number.find_all('li')[-2].text
                products_and_next_page_number = {'next_page_number_link':  next_page_link, 'number_of_pages': number_of_pages, 'products_links': porduct_links}
            else:
                products_and_next_page_number = {'next_page_number_link': None, 'number_of_pages': None, 'products_links': porduct_links}
        else:
                products_and_next_page_number = {'next_page_number_link': None, 'number_of_pages': None, 'products_links': porduct_links}
        
        return products_and_next_page_number

    def loop_pagination_and_all_links(self, links):
        pass

    def get_product_info(self, product_link):        
        number_of_pages = int(product_link['number_of_pages'])
        new_page_link = product_link['next_page_number_link']
        product = []
        for x in  range(0, number_of_pages):
            print(x)
            new_pro_links = self.get_product_links(new_page_link)
            new_page_link = new_pro_links['next_page_number_link']
            product_data = {}
            for index, link in enumerate(product_link['products_links']):
                # sleep(1) #delay for one sec to not down the server
                response_result = requests.get(product_link['products_links'][link])
                product_page_resource = response_result.content
                parsed_result = BeautifulSoup(product_page_resource, 'lxml')
                product_title = parsed_result.find(attrs = {'class' :'product_title entry-title'})
                stock_info = parsed_result.find(class_ = 'stock in-stock')
                short_description = parsed_result.find(class_ = 'woocommerce-product-details__short-description')
                product_price = parsed_result.find(class_ = 'woocommerce-Price-amount amount')

                product_image = parsed_result.find(class_ = 'woocommerce-product-gallery__wrapper').find('a', href=True)
                
                product_description = parsed_result.find(class_ ='electro-description')
                product_category = parsed_result.find(class_ ='posted_in')
                product_tag = parsed_result.find(class_ ='tagged_as')
                product_sku =  parsed_result.find(class_ = 'sku')
                short_desc= ""
                stock = 0
                if stock_info is not None:
                    split_stock = stock_info.string.split(' ')
                    stock = split_stock[0]
                    instock = 1
                else:
                    stock = 0
                    instock = 0
                if product_title is not None:
                    product_title = product_title.text
                else:
                    product_title = None
                if short_description is not None:
                    short_desc = '\n'.join(short_description.prettify().split('\n')[1:-1])
                else:
                    short_desc = None

                if product_image is not None and product_image.attrs['href'] != 'https://refurbish.ae/wp-content/uploads/2020/08/Refurbish.ae_.png':
                    product_image = product_image.attrs['href'] 
                else:
                    product_image = 'https://refurbished.ae/wp-content/uploads/2021/06/logo-vertical.png'
                if product_price is not None:
                    price = product_price.find('bdi').contents[1]
                    
                else: 
                    price = None
                    
                if product_description is not None:
                    product_description
                    description = '\n'.join(product_description.prettify().split('\n')[1:-1])
                else:
                    description = None
                
                if product_sku is not None:
                    sku = product_sku.text
                else:
                    sku = None
                if product_category is not None:
                    category = product_category
                    category = ''
                    for i, cat in enumerate(product_category.find_all('a', href=True)):
                        category += cat.text+ ', '
                else:
                    category = None
                
                if product_tag is not None:
                    tags = ''
                    for j, tag in enumerate(product_tag.find_all('a', href=True)):
                        tags += tag.text+ ', '
                else: 
                    tags = None
                
                product_data = {
                    'sku': sku,
                    'post_status': '1',
                    'product_title': product_title,
                    'short_description' : short_desc,
                    'description' : description,
                    'featured_image': product_image,
                    'price': price,
                    'sale_price': None,
                    'in_stock' : instock,
                    'Stock': stock,
                    'sale_price_dates_from': None,
                    'sale_price_dates_to' : None,
                    "In stock?": 0,
                    "Stock": None,
                    "Low stock amount": None,
                    "Backorders allowed?": 0,
                    "Sold individually?": 0,
                    "Weight": None,
                    "Length": None,
                    "Width":None,
                    "Height (cm)": None,
                    "category" : category,
                    "tag": tags
                }
                product.append(product_data)
            product_link['products_links'] = new_pro_links['products_links']   
            # print(product_link['products_links'])
            if new_page_link is None:
                break  
        products = pd.DataFrame(product)
        products.to_csv('products.csv', mode='a')
        
        print(type(product))
        print(len(product))
        return '123'
        

