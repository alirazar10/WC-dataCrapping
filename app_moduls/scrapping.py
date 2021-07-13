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
        if next_page_number is not None:
            next_page_number_link = next_page_number.find(attrs = {'class': 'next page-numbers'})
            if next_page_number_link is not None:

                next_page_number_link = next_page_number_link.attrs['href']
                number_of_pages = next_page_number.find_all('li')[-2].text
                products_and_next_page_number = {'next_page_number_link': next_page_number_link, 'number_of_pages': number_of_pages, 'products_links': porduct_links}
            else:
                products_and_next_page_number = {'next_page_number_link': None, 'number_of_pages': None, 'products_links': porduct_links}
        else:
                products_and_next_page_number = {'next_page_number_link': None, 'number_of_pages': None, 'products_links': porduct_links}
        
        return products_and_next_page_number


    def get_product_info(self, product_list):
        number_of_pages = int(product_list['number_of_pages'])
        # print(product_list)
        # return product_list
        new_page_link = product_list['next_page_number_link']
        product = []

        for x in  range(1, number_of_pages):
            print(x)
            pro_links = self.get_product_links(new_page_link)
            new_page_link = pro_links['next_page_number_link']
            print(pro_links['next_page_number_link'])
           
        # return '123'
        # return product_list['number_of_pages']

            product_data = {}
            for index, link in enumerate(product_list['products_links']):
                sleep(1) #delay for one sec to not down the server
                response_result = requests.get(product_list['products_links'][link])
                product_page_resource = response_result.content
                parsed_result = BeautifulSoup(product_page_resource, 'lxml')
                product_title = parsed_result.find(attrs = {'class' :'product_title entry-title'}).text
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
                    product_title = product_title
                else:
                    product_title = None
                if short_description is not None:
                    short_desc = '\n'.join(short_description.prettify().split('\n')[1:-1])
                else:
                    short_desc = None

                if product_image is not None and product_image != 'https://refurbish.ae/wp-content/uploads/2020/08/Refurbish.ae_.png':
                    product_image = product_image
                else:
                    product_image= 'https://refurbished.ae/wp-content/uploads/2021/06/logo-vertical.png'
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
                
               
        products = pd.DataFrame(product)
            # return product_page_resource
        products.to_csv('products.csv', mode='a')
        print(type(product))
        print(len(product))
        return '123'
        # ID,Type,SKU,Name,Published,"Is featured?",
        # "Visibility in catalog","Short description",Description,
        # "Date sale price starts","Date sale price ends","Tax status",
        # "Tax class","In stock?",Stock,"Low stock amount","Backorders allowed?",
        # "Sold individually?","Weight (kg)","Length (cm)","Width (cm)","Height (cm)",
        # "Allow customer reviews?","Purchase note","Sale price","Regular price",Categories,
        # Tags,"Shipping class",Images,"Download limit","Download expiry days",Parent,"Grouped products",
        # Upsells,Cross-sells,"External URL","Button text",Position,"Attribute 1 name","Attribute 1 value(s)",
        # "Attribute 1 visible","Attribute 1 global","Attribute 2 name","Attribute 2 value(s)","Attribute 2 visible",
        # "Attribute 2 global","Attribute 3 name","Attribute 3 value(s)","Attribute 3 visible","Attribute 3 global"

