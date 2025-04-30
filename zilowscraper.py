import time,re
import requests

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from random import randrange

def getsource(url):
    clist =['US','AL', 'AZ', 'KG', 'BA', 'UZ', 'BI', 'XK', 'DE', 'AT','UK', 'GB', 'IE', 'IM', 'FR', 'ES', 'NL', 'IT', 'PT', 'BE', 'AD', 'MC', 'MA', 'LU', 'DK', 'FI', 'NO', 'EU', 'VA']
    content =''
    try:
        chooseip = randrange(len(clist))
        content =''
        SBR_WEBDRIVER = 'https://brd-customer-hl_2aa4f566-zone-referal2haziq-country-'+clist[chooseip].lower()+':kilai54qoc5l@brd.superproxy.io:9515'
        print(SBR_WEBDRIVER)
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            checkip ='https://geo.brdtest.com/mygeo.json'
            driver.get(checkip)
           # print('checking ip')
           # print(driver.page_source)
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(url)
            driver.implicitly_wait(5)
            content = driver.page_source
           
            
            driver.get_screenshot_as_file('mm.png')
    except Exception as e:
        print(e)
      #  input(e)
        if 'ip_forbidden' in str(e).lower():
            content =str(e).strip()
            print("brightdata ad ip")
        else:
            getsource(url)
        
    return content

def fetchzillow(agent_name):
    #agent_name = clean_name(agent_name)
    email=""
    phone=""
    link = ""
    found = 'False'
    noresult = 0
    if True:
        
           
        check = 0
        capt = 0
        while check < 17700:
            print('Scraping info for ' + agent_name)
            url = 'https://www.zillow.com/professionals/real-estate-agent-reviews/?name=' + agent_name.replace(' ', '+').strip()
            #print(url)

            content = getsource(url)
            
            check =len(content)
            print(check)
            if 'ip_forbidden' in str(content):
                noresult  = 1
                break
            #time.sleep(10)
    
        if noresult == 1:
            return(email,phone,link,'IP Blocked')
            
        try:
            flag = 0
            try:
                print('trying to search for agent card')
                link = content.split('"fullName":"'+agent_name+'"',1)[1].split('"profileLink":"/profile/',1)[1].split('"',1)[0]
                
                print(1,link)
            except:
                if len(agent_name.strip().split(' ')) > 2:
                    try:
                        fname = agent_name.split(' ')[0]+' '+agent_name.split(' ')[-1]
                        link = content.split('"fullName":"'+fname+'"',1)[1].split('"profileLink":"/profile/',1)[1].split('"',1)[0]
                        print(2,link)
                    except:
                        flag = 1
                else:
                    flag = 1
                
            if flag == 0:
                found = 'True'
                link = 'https://www.zillow.com/profile/'+link
                check = 0
                while check < 17700:
                    print("opening page",link)
                    content = getsource(link)
                    check =len(content)
                    print(check)
                    if 'ip_forbidden' in str(content):
                        noresult  = 1
                        break
                    #time.sleep(10)
                    
                if noresult == 1:
                    
                    return(email,phone,link,'IP Blocked')
                
           
                try:
                    email = content.split('"email":"',1)[1].split('"',1)[0]
                except:
                    email = ''
                try:
                    phonelist =  content.split('"phoneNumbers":{',1)[1].split('},',1)[0]                    
                    phonelist =phonelist.split('":"')[1:]                    
                    myphlist = []
                    for ph in phonelist:
                        ph = ph.split('"',1)[0]
                        if ph in myphlist:
                            continue
                        myphlist.append(ph)
                    phone = ', '.join(myphlist[0:])  
                        
                except:
                    phone = ''
                    
                
               
                        
                        
        except Exception as e:
            print(e)
            
            
        if flag == 1:
            link =email= cphone=bphone = ''
            found = 'False'
            print('Agent not found')
        print(email,phone,link,found)

    return email,phone,link,found

#print(fetchzillow('Katie Lewter Arvidson'))
