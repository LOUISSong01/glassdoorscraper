import undetected_chromedriver as uc
import random
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium.common.exceptions import (ElementNotVisibleException,
                                        ElementNotSelectableException)
ignore_list = [ElementNotVisibleException, ElementNotSelectableException,NoSuchElementException]
import re



usr_agents = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.3"
]
french_letters_pattern = re.compile(r'[àâçéèêëîïôùûüÿñæœ·]')

# checking for french characters in the company name
def check_french(str):
    letters = french_letters_pattern.findall(str)
    if(len(letters) != 0):
        return True
    return False

def get_random_usr_agents():
    return random.choice(usr_agents)

# Set up the ChromeOptions object with the proxy server information
chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--proxy-server={}".format(proxy_server))

chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=" + get_random_usr_agents())

# undetected chromedriver 
driv = uc.Chrome() 

scrap_result = []

# getting links of each company Overviews
def job_links(html):
    link = html.find("a", {"data-test": "cell-Jobs-url"})
    back = link['href']
    return back

#extract id from the job link in order to get link for overview of company
def extract_id(links):
    num = ""
    for c in links.split("Jobs-E")[1]:
        if c.isdigit():
            num = num + c
    return num

# when there is french letter
def special_case(html):
    company_name = html.find("h2", {"data-test": "employer-short-name"}).text
    company_size = html.find("span", {"data-test": "employer-size"}).text
    company_industry = html.find("span", {"data-test": "employer-industry"}).text

    return {    'company': company_name, 
                'company type': "N/A", 
                'hq': "N/A",
                'industry': company_industry, 
                'size': company_size, 
                'revenue': "N/A", 
                'ovr_rating': "N/A", 
                'rating_CV': "N/A",
                'rating_DI' : "N/A",
                'rating_WLB' : "N/A",
                'rating_SM' : "N/A",
                'rating_CB' : "N/A",
                'rating_CO' : "N/A",
                'link': "N/A"}

# check there is any missing sections
def missing_sec(path):
    try: 
        driv.find_element(By.XPATH, path)
    except NoSuchElementException:
        return True
    return False

#extract company name from info section
def name_extract(str):
    str = str.split(" Overview")[0]
    str = str.replace("[", "").replace("]", "").replace(".", "")
    return str

wait = WebDriverWait(driv, timeout=100, poll_frequency=1, ignored_exceptions=ignore_list)

# for each company...
def extract_company(company_website):
    # overview page scraping using selenium 
    try:
        driv.get(company_website)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-test="employerOverviewHeader"]')))

        company_name = name_extract(driv.find_element(By.XPATH, '//*[@data-test="employerOverviewHeader"]').text)

        if(company_name == "MISSING VALUE"):
            return 
        else:
            if(missing_sec('//div[@data-test="employer-size"]')):
                company_size = "N/A"
            else:
                company_size = driv.find_element(By.XPATH, '//*[@data-test="employer-size"]').text

            if(missing_sec('//div[@data-test="employer-type"]')):
                company_type = "N/A"
            else:
                company_type = driv.find_element(By.XPATH, '//div[@data-test="employer-type"]').text

            if(missing_sec('//a[@data-test="employer-website"]')):
                link = 'N/A'
            else:
                link = driv.find_element(By.XPATH, '//a[@data-test="employer-website"]').text

            if(missing_sec('//*[@data-test="employer-industry"]')):
                company_industry = "N/A"
            else:
                company_industry = driv.find_element(By.XPATH, '//*[@data-test="employer-industry"]').text

            if(missing_sec('//*[@data-test="employer-headquarters"]')):
                hq = "N/A"
            else: 
                hq = driv.find_element(By.XPATH, '//div[@data-test="employer-headquarters"]').text

            if(missing_sec('//*[@data-test="employer-revenue"]')):
                revenue = "N/A"
            else: 
                revenue = driv.find_element(By.XPATH, '//div[@data-test="employer-revenue"]').text

    except NoSuchElementException:
        time.sleep(15)
        company_name = name_extract(driv.find_element(By.XPATH, '//*[@data-test="employerOverviewHeader"]').text)

        if(missing_sec('//div[@data-test="employer-size"]')):
            company_size = "N/A"
        else:
            company_size = driv.find_element(By.XPATH, '//*[@data-test="employer-size"]').text

        if(missing_sec('//div[@data-test="employer-type"]')):
            company_type = "N/A"
        else:
            company_type = driv.find_element(By.XPATH, '//div[@data-test="employer-type"]').text

        if(missing_sec('//a[@data-test="employer-website"]')):
            link = 'N/A'
        else:
            link = driv.find_element(By.XPATH, '//a[@data-test="employer-website"]').text

        if(missing_sec('//*[@data-test="employer-industry"]')):
            company_industry = "N/A"
        else:
            company_industry = driv.find_element(By.XPATH, '//*[@data-test="employer-industry"]').text

        if(missing_sec('//*[@data-test="employer-headquarters"]')):
            hq = "N/A"
        else: 
            hq = driv.find_element(By.XPATH, '//div[@data-test="employer-headquarters"]').text

        if(missing_sec('//*[@data-test="employer-revenue"]')):
            revenue = "N/A"
        else: 
            revenue = driv.find_element(By.XPATH, '//div[@data-test="employer-revenue"]').text
        
    def check_inflate_reviews():
        try:
            time.sleep(3)
            driv.find_element(By.XPATH, '//*[@data-test="employerReviewsModule"]/div[1]/div[2]/strong')
        except NoSuchElementException:
            return False
        return True
    # checking for inflated reviews
    if(check_inflate_reviews()):
       wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@data-test="employerReviewsModule"]/div[2]/div[2]')))
       driv.find_element(By.XPATH, '//*[@data-test="employerReviewsModule"]/div[2]/div[2]').click()
       time.sleep(5)
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@data-test="employerReviewsModule"]/div[1]/div[2]')))
        driv.find_element(By.XPATH, '//*[@data-test="employerReviewsModule"]/div[1]/div[2]').click()
        time.sleep(3)
    '''
        except:
            time.sleep(15)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@data-test="employerReviewsModule"]/div[1]/div[2]')))
            driv.find_element(By.XPATH, '//*[@data-test="employerReviewsModule"]/div[1]/div[2]').click()
    '''

     
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/span')))
        overall_rating = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/span').text
        rating_CV = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[3]').text
        rating_DI = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[3]/div/div[3]').text
        rating_WLB = driv.find_element(By.XPATH,'//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[4]/div/div[3]').text
        rating_SM = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[5]/div/div[3]').text
        rating_CB = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]').text
        rating_CO = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[7]/div/div[3]').text
    except NoSuchElementException:
        time.sleep(15)
        overall_rating = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[1]/div/div[3]/span').text
        rating_CV = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div[3]').text
        rating_DI = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[3]/div/div[3]').text
        rating_WLB = driv.find_element(By.XPATH,'//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[4]/div/div[3]').text
        rating_SM = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[5]/div/div[3]').text
        rating_CB = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[6]/div/div[3]').text
        rating_CO = driv.find_element(By.XPATH, '//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div[7]/div/div[3]').text
    finally:
        return {'company': company_name, 
                'company type': company_type, 
                'hq': hq,
                'industry': company_industry, 
                'size': company_size, 
                'revenue': revenue, 
                'ovr_rating': overall_rating, 
                'rating_CV': rating_CV,
                'rating_DI' : rating_DI,
                'rating_WLB' : rating_WLB,
                'rating_SM' : rating_SM,
                'rating_CB' : rating_CB,
                'rating_CO' : rating_CO,
                'link': link}



def extract_companies(url):

    company_links = []
    driv.get(url)
    time.sleep(2)
    page_source = driv.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    companies = soup.find_all("div", {"data-test": "employer-card-single"})
    for company in companies:
        company_name = company.find("h2", {"data-test": "employer-short-name"}).text
        company_name = name_extract(company_name)
        if(check_french(company_name)):
            scrap_result.append(special_case(company))
            continue
        nospace_name = company_name.replace(" ", "")
        id = extract_id(job_links(company))
        company_website = f"https://www.glassdoor.com/Overview/Working-at-{nospace_name}-EI_IE{id}.htm"
        company_links.append(company_website)

    for link in company_links:
        scrap_result.append(extract_company(link))
        print(f"scrapped {len(scrap_result)} companies!! :>")
        print(scrap_result)
        

def scrap(page, until):
    if (page <= until):
        print(f'scrapping page {page} :)')
        extract_companies(f'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page={page}')
        time.sleep(2)
        scrap(page + 1, until)
    else:
        print(f"successfully scraped {len(scrap_result)} compaies!")
        df = pd.DataFrame(scrap_result)
        df.to_csv('glassdoor2.csv', index=False)

# put beginning page and last page to scrape
scrap(989,999)
#386 scrape해
#393
#526
#636
#683

'''
 #need to build the sign-in option
def google_sign_in(url):
    driv.get(url)
    # Wait for the sign-in button to become clickable
    sign_in_path = "//div[@id='SignInButton']/button[text()='Sign In']"
    wait.until(EC.element_to_be_clickable((By.XPATH, sign_in_path)))
    sign_in_path.click()

# Click the sign-in button

google_sign_in('https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page=102')
'''








 

