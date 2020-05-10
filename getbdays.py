from selenium import webdriver
import getpass
from selenium.webdriver import DesiredCapabilities
import subprocess as sp
from selenium.common.exceptions import NoSuchElementException
import sys
import os
import socket

def is_connected():
    try:
        socket.create_connection(("www.facebook.com", 80))
        return True
    except OSError:
        pass
    return False


def getbirthdays(chrome_driver_path):
    if is_connected:
        emailtext = input("ENTER EMAIL : ")
        passwordtext = getpass.getpass(prompt="ENTER PASSWORD : ")

        chromedriver_path =  chrome_driver_path

        if len(emailtext)!=0 and len(passwordtext)!=0 :

            print('Info : Logging into Facebook')
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--incognito")
            driver = webdriver.Chrome(chromedriver_path,options=options)
            driver.get("https://www.facebook.com/events")

            email = driver.find_element_by_name("email")
            email.clear()
            email.send_keys(emailtext)

            password = driver.find_element_by_name("pass")
            password.clear()
            password.send_keys(passwordtext)

            loginbtn = driver.find_element_by_id("loginbutton")
            loginbtn.click()

            try:
                birthdays = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[1]/div/div/div[2]/div[3]/a')
                print('Info : Log In Successful')
                print('Info : Getting Birthdays')
                driver.execute_script("arguments[0].click();", birthdays)
                try:
                    birthday_user_list = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/ul')
                    birthday_user_items = birthday_user_list.find_elements_by_tag_name('li')
                    if len(birthday_user_items) ==0:
                        print('Result : 0 Birthdays Today !!')
                        sp.call(['notify-send','0 Birthdays Today'])
                    else:
                        print('Result :',len(birthday_user_items),'BIRTHDAYS TODAY !!')
                        user_data_list = []
                        for birthday_user_item in birthday_user_items:
                            user_data = birthday_user_item.text.split('old')
                            user_data_list.append(user_data[0])
                        sp_param_data = ""
                        for data_item in user_data_list:
                            data_item_list = data_item.split()
                            user_name = " ".join(data_item_list[0:(len(data_item_list)-2)])
                            user_age = data_item_list[-2]
                            print(user_name,'=>',user_age,'years')
                            sp_param_data+=user_name+'\n'

                        sp_param = str(len(birthday_user_items))+' Birthdays Today'
                        sp.call(['notify-send','-i','emblem-favorite',sp_param,sp_param_data])
                except NoSuchElementException:
                    print('Result : 0 Birthdays Today !!')
                    sp.call(['notify-send','0 Birthdays Today'])
            except NoSuchElementException:
                #sp.call(['notify-send','Login Failed','Wrong email or password.'])
                print('Info : Login Failed, wrong email or password')

        else :
            print("WRONG INPUT")
    else:
        print("No Internet. Please try again later.")


# main

if __name__ == "__main__":
    getbirthdays(os.path.abspath(sys.argv[1]))
