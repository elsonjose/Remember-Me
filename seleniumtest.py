from selenium import webdriver
import getpass

from selenium.webdriver import DesiredCapabilities

emailtext = raw_input("ENTER EMAIL : ")
passwordtext = getpass.getpass(prompt="ENTER PASSWORD : ")

if len(emailtext)!=0 and len(passwordtext)!=0 :

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome('/home/ej/Downloads/chromedriver',chrome_options=chrome_options)
    driver.get("http://www.facebook.com")

    email = driver.find_element_by_name("email")
    email.clear()
    email.send_keys(emailtext)

    password = driver.find_element_by_name("pass")
    password.clear()
    password.send_keys(passwordtext)

    loginbtn = driver.find_element_by_id("loginbutton")
    loginbtn.click()

    profile = driver.find_element_by_id("userNav").click()
    friends = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/div[2]/div[2]/ul/li[3]/a").click
else :
    print("WRONG INOUT")