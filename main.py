from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import cv2
import pytesseract

### for reading Captcha I use OpenCV and Tesseract

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

startDate = input('Enter the start date in dd/mm/yyyy formate - ')
endDate = input('Enter End date in dd/mm/yyyy formate - ')
search = {1:'Case Number', 2:'Complainant', 3:'Respondent', 4:'Comp-Advocate', 5:'Resp-Advocate', 6:'Judge/Member', 7:'Free Text', 8:'Sector', 9:'Between dates'}

searchB = input("Select one option number 1:'Case Number', 2:'Complainant', 3:'Respondent', 4:'Comp-Advocate', 5:'Resp-Advocate', 6:'Judge/Member', 7:'Free Text', 8:'Sector', 9:'Between dates'- ")

commision = {1:"NCDRC", 2:"Andaman Nicobar", 3:"Andhra Pradesh", 4:"Arunachal Pradesh",5:"Assam",6:"Bihar",7:"Chandigarh",8:"Chhattisgarh",
                  9:"Circuit Bench Amravati", 10:"Circuit Bench Asansol", 11:"Circuit Bench Aurangabad", 12:"Circuit Bench Bikaner",13:"Circuit Bench Jodhpur",
                   14:"Circuit Bench Kohlapur",15:"Circuit Bench Kota",16:"Circuit Bench Madurai",17:"Circuit Bench Nagpur",18:"Circuit Bench Nashik",
                   19:"Circuit Bench Pune",20:"Circuit Bench Siliguri",21:"Circuit Bench Udaipur",22:"Dadra and Nagar Haveli and Daman and Diu",23:"Delhi"
                   ,24:"Goa",25:"Gujarat",26:"Haryana",27:"Himachal Pradesh",28:"Jammu and Kashmir",29:"Jharkhand",30:"Karnataka",31:"Kerala",32:"Lakshadweep"
                   ,33:"Madhya Pradesh",34:"Maharashtra",35:"Manipur",36:"Meghalaya",37:"Mizoram",38:"Nagaland",39:"Odisha Bench II",40:"Orissa",41:"Pondicherry"
                   ,42:"Punjab",43:"Rajasthan",44:"Sikkim",45:"Srinagar Bench",46:"Tamil Nadu",47:"Telangana",48:"Tripura",49:"Uttar Pradesh",50:"Uttarakhand",51:"West Bengal"}

selectCommission = input(""" Select one option 1:"NCDRC", 2:"Andaman Nicobar", 3:"Andhra Pradesh", 4:"Arunachal Pradesh",5:"Assam",6:"Bihar",7:"Chandigarh",8:"Chhattisgarh",
                  9:"Circuit Bench Amravati", 10:"Circuit Bench Asansol", 11:"Circuit Bench Aurangabad", 12:"Circuit Bench Bikaner",13:"Circuit Bench Jodhpur",
                   14:"Circuit Bench Kohlapur",15:"Circuit Bench Kota",16:"Circuit Bench Madurai",17:"Circuit Bench Nagpur",18:"Circuit Bench Nashik",
                   19:"Circuit Bench Pune",20:"Circuit Bench Siliguri",21:"Circuit Bench Udaipur",22:"Dadra and Nagar Haveli and Daman and Diu",23:"Delhi"
                   ,24:"Goa",25:"Gujarat",26:"Haryana",27:"Himachal Pradesh",28:"Jammu and Kashmir",29:"Jharkhand",30:"Karnataka",31:"Kerala",32:"Lakshadweep"
                   ,33:"Madhya Pradesh",34:"Maharashtra",35:"Manipur",36:"Meghalaya",37:"Mizoram",38:"Nagaland",39:"Odisha Bench II",40:"Orissa",41:"Pondicherry"
                   ,42:"Punjab",43:"Rajasthan",44:"Sikkim",45:"Srinagar Bench",46:"Tamil Nadu",47:"Telangana",48:"Tripura",49:"Uttar Pradesh",50:"Uttarakhand",51:"West Bengal""")

def getCaptchaValue():
    #for reading catcha we need to install OPENCV and tesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Rakesh\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'   #exact location where
    img = cv2.imread('filename.png')
    img = cv2.resize(img, (390, 130))
    return pytesseract.image_to_string(img)

browser = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
browser.get("http://cms.nic.in/ncdrcusersWeb/search.do?method=loadSearchPub")
browser.maximize_window()
#select Date By Radio option
newsletter = browser.find_element(By.XPATH, value="//label[@for='dtof']")
newsletter.click()

#select start date
stDate = browser.find_element(By.ID, "stDate")
stDate.click()
stDate.send_keys(Keys.CONTROL, "a")
stDate.send_keys(Keys.BACKSPACE)
stDate.send_keys(startDate)

#select End date
enDate = browser.find_element(By.ID, "endDate")
enDate.click()
enDate.send_keys(Keys.CONTROL, "a")
enDate.send_keys(Keys.BACKSPACE)
enDate.send_keys(endDate)

#select Search Type
searchBy = browser.find_element(By.ID, "searchBy")
for option in searchBy.find_elements(By.TAG_NAME, "option"):
    if option.text == search[int(searchB)]:
        option.click()
        break

#select Commision
stateName = browser.find_element(By.ID, "stateId")
for option in stateName.find_elements(By.TAG_NAME, "option"):
    if option.text == commision[int(selectCommission)]:
        option.click()
        break

#select Branch
searchIn = browser.find_element(By.ID, "districtId")
for option in searchIn.find_elements(By.TAG_NAME, "option"):
    if commision[int(selectCommission)] == "NCDRC":
        if option.text == "NCDRC":
            option.click()
            break
    else:
        if option.text == "StateCommission":
            option.click()
            break

#code for reading capthcha
cpIm = browser.find_element(By.ID, "captchaId")
src = cpIm.get_attribute('src')
with open('filename.png', 'wb') as file:
    file.write(browser.find_element(By.ID, "captchaId").screenshot_as_png)
captchaVal = browser.find_element(By.NAME, "captchaText")
data =getCaptchaValue()
captchaVal.send_keys(data)
subButton = browser.find_element(By.ID, "searchImg")
subButton.click()

#added sleep, my location website is responding bit late
time.sleep(5)

#### <<<<< -------------------------------- Reading Data ------------------------------------ >>>>>>>>
s = BeautifulSoup(browser.page_source, "html.parser")
table = s.find_all('table')
headers = []

#code for creaditing DF and header values
for j in table[-2].find_all('th'):
    title = j.text
    headers.append(title)
    mydata = pd.DataFrame(columns=headers)
kk = len(table[-1].find_all('tr')[0].find_all('td'))


for i in range(kk-1):
    if i == 0:
        for k in table[-2].find_all('tr')[1:]:
            row_Data = k.find_all('td')
            row = [f.text for f in row_Data]
            caseId = '0/0/'+row[0].strip()
            row[-1] = {"url" : 'http://cms.nic.in/ncdrcusersWeb/servlet/search.GetJudgement', "caseidin":caseId, "dtofhearing" : row[6]}
            row[0] = row[0].strip()
            length = len(mydata)
            mydata.loc[length] = row
    else:
        s = BeautifulSoup(browser.page_source, "html.parser")
        table = s.find_all('table')
        for k in table[-2].find_all('tr')[1:]:
            row_Data = k.find_all('td')
            row = [f.text for f in row_Data]
            caseId = '0/0/'+row[0].strip()
            row[-1] = {"url" : 'http://cms.nic.in/ncdrcusersWeb/servlet/search.GetJudgement', "caseidin":caseId, "dtofhearing" : row[6]}
            row[0] = row[0].strip()
            length = len(mydata)
            mydata.loc[length] = row
    if i+1==kk:
        break
    else:
        #code for click on next button
        s = BeautifulSoup(browser.page_source, "html.parser")
        table = s.find_all('table')
        c = table[-2].find_all('tr')[0]
        if i+1<kk-1:
            clickVal = browser.find_element(By.LINK_TEXT, 'Next')
            clickVal.click()
            time.sleep(10)

mydata.to_csv('file.csv')




