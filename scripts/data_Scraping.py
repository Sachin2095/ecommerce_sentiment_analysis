from selenium import webdriver
from selenium.webdriver import chrome 
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging 
import os        
from error_handling import EMPTYURLERROR , EMPTYREVIEW

         
### logging structure 
file_name="Data_scraping"
logging.basicConfig(
    filename=f"logs/{file_name}.log",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode="a"
)

# Amazon top products in last 30 days 
amazon_top_products = {
    "Electronics": ["iPhone", "Laptop"],
    "Mobiles & Accessories": ["AirPods", "Apple Watch"],
    "Books / Reading": ["Kindle", "Harry Potter Series"],
    "Gaming Consoles": ["Nintendo Switch", "PlayStation 5 (PS5)"],
    "Home & Kitchen": ["Coffee", "Water Bottle"],
    "Toys & Games": ["Lego", "Barbie Doll"],
    "Fashion (Clothing & Shoes)": ["Crocs", "Sneakers"],
    "Beauty & Personal Care": ["Makeup Kit", "Hair Dryer"],
    "Appliances": ["Smart TV", "Refrigerator"],
    "Stationery & Office": ["Desk", "Monitor"]
}

def amazon_products_reviews(product_name):
        """This is a function to scrap the review for above mentioned products {only 5 products}"""
        if product_name!="":
            options=webdriver.ChromeOptions()
            options.add_experimental_option("detach",True)
            driver=webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
            driver.get('https://www.amazon.in/')
            box=driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
            box.send_keys(product_name)
            box.send_keys(Keys.ENTER)
            urls=[]
            # link to go to page
            box=driver.find_elements(By.XPATH,"//a[@class='a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal']")
            print(box)
            for i in box:
                link=i.get_attribute('href')
                urls.append(link)
            print(f"creted url list for product_name {product_name}:",urls)
            if len(urls):
               review=[]
               sentiment=[]
               time.sleep(10)
               logging.info("Getting ready to scrap reviews")
               for url in urls:
                   driver.get(url)
                   box=driver.find_elements(By.XPATH,'//div[@class="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"]/span')
                   ratings = WebDriverWait(driver,5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@class="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"]'))
                    )
                   for r in ratings:
                       text=r.get_attribute("innerText")[0:3]
                       sentiment.append(text)
                   for i in box:
                       review.append(i.text)
                   if len(review) and len(sentiment):
                      logging.info("reviews and Rating has been fetched.")
                   else:
                        logging.info("No Review found or No Rating found")
                        raise EMPTYREVIEW("No Review found or No Rating found")
                   time.sleep(10)
               print(len(review),len(sentiment))
               mini=min(len(sentiment),len(review))
               df=pd.DataFrame({'Reviews':review[0:mini],'Ratings':sentiment[0:mini]})
               driver.close()
               logging.info("Dataframe has been created")
               df.to_csv(f"data/raw/{product_name}.csv", index=False)
               logging.info(f"✅ DataFrame saved to output_data/{product_name}.csv")
               return df
            else: 
                logging.info("No product url Found")
                raise EMPTYURLERROR("No product url Found")
            return


        
all_products_reviews=pd.DataFrame(columns=["Reviews", "Ratings"])
logging.info("SCRAPING HAS STARTED")
for cat,subcat in amazon_top_products.items():
    for product_name in subcat:
        logging.info(f"product name {product_name} has sent")
        amazon_products_reviews(product_name)
        time.sleep(10)
        logging.info(f"dataset has been created for {product_name}")

logging.info("SCRAPING ENDED")


# # Make sure directory exists
# os.makedirs("data/raw", exist_ok=True)
# # Save to CSV
# df.to_csv("data/raw/reviews.csv", index=False)
# logging.info("✅ DataFrame saved to output_data/reviews.csv")
