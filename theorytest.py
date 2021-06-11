import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

TODAY = date.today()
START_DATE = TODAY + timedelta(days=1)
INTERVAL = 12
LOOP = 5
DEBUG = False 
BASEURL = "https://eu-proscheduler.prometric.com/?prg=DTT&nopri=T&path=schd&cntry=irl"

class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printer(message, color=None):
    if not color:
        color=bc.OKBLUE
    print(color + message + bc.ENDC)

def parse_appointments(selector):
    cities = selector.find_elements_by_css_selector("div.row > .col-md-12 > .marginBottom")
    if not cities:
        printer("There is nothing in this week :( ", bc.FAIL)

    for city in cities:
        city_name = city.find_element_by_tag_name("strong").text
        month = city.find_element_by_class_name("test-center-month").text
        day = city.find_element_by_class_name("testCenterDay").text

        print(f"{bc.BOLD}{bc.HEADER}{city_name}{bc.ENDC} -> {bc.OKGREEN}{month} {day}{bc.ENDC}")
    
    print()
    printer("="*30, bc.FAIL)


def date_changer(selector):
    address="/html/body/app-root/app-scheduling/div/div[1]/app-schedule-location/div/app-location-selector/div/div[2]/div/app-geo-locator/input"
    start_date_xpath="/html/body/app-root/app-scheduling/div/div[1]/app-schedule-location/div/app-location-selector/div/div[3]/div[1]/label/datepicker-demo/div/input"
    end_date_xpath="/html/body/app-root/app-scheduling/div/div[1]/app-schedule-location/div/app-location-selector/div/div[3]/div[2]/label[1]/datepicker-demo/div/input"
    printer("-"*20, bc.WARNING)

    printer("Today:" + TODAY.strftime("%m/%d/%Y"), bc.HEADER)


    selector.find_element_by_xpath(address).send_keys("Nenagh, Ireland")
    selector.find_element_by_xpath(start_date_xpath).send_keys(START_DATE.strftime("%m/%d/%Y"))


    first_new_date = START_DATE + timedelta(days=INTERVAL)
    selector.find_element_by_xpath(end_date_xpath).clear()
    selector.find_element_by_xpath(end_date_xpath).send_keys(first_new_date.strftime("%m/%d/%Y"))
    printer("="*30, bc.FAIL)
    printer(f"Checking {START_DATE} - {first_new_date}   0/{LOOP}", bc.OKBLUE)
    printer("-"*20, bc.WARNING)

    time.sleep(2)

    selector.find_element_by_id("nextBtn").click()
    time.sleep(3)

    parse_appointments(selector=selector)

    for i in range(LOOP):
        second_new_date = first_new_date + timedelta(days=INTERVAL)

        printer(f"Checking {first_new_date} - {second_new_date}   {i+1}/{LOOP}", bc.OKBLUE)
        printer("-"*20, bc.WARNING)

        selector.find_element_by_css_selector("input[type=text]").clear()
        selector.find_element_by_css_selector("input[type=text]").send_keys(f"{first_new_date.strftime('%m/%d/%Y')} - {second_new_date.strftime('%m/%d/%Y')}")
        time.sleep(3)

        parse_appointments(selector=selector)

        first_new_date = second_new_date

def main():
    if not DEBUG:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
    else:
        driver = webdriver.Firefox()

    driver.get(BASEURL)

    print(driver.title)
    time.sleep(2)

    driver.find_element_by_id("nextBtn").click()
    time.sleep(2)

    driver.find_element_by_id("No").click()
    #driver.find_element_by_name("options_PreApprovedSelect")[1].click()
    time.sleep(1)

    driver.find_element_by_xpath("//select[@name='selectedExam']/option[3]").click()

    driver.find_element_by_id("nextBtn").click()

    time.sleep(2)
    driver.find_element_by_id("nextBtn").click()

    date_changer(selector=driver)

    driver.close()

if __name__ == "__main__":
    main()
