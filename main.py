import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

hideBrowser = True
URL = "your favorite site.com"
coupPrefix = "004"
trialCounter = 1001
goodCouponsArray = []

def createNextFullCoupon():
    global coupPrefix, trialCounter
    length = len(str(trialCounter))
    if length == 1:
        trialCounterStr = "000" + str(trialCounter)
    elif length == 2:
        trialCounterStr = "00" + str(trialCounter)
    elif length == 3:
        trialCounterStr = "0" + str(trialCounter)
    elif length == 4:
        trialCounterStr = str(trialCounter)
    elif length == 5:
        exit(0)
    trialCounter += 1
    return f"{coupPrefix}-{trialCounterStr}"


seleBrowserPath = "C:\Program Files (x86)\chromedriver.exe"
seleDriver = ""
if (hideBrowser):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    seleDriver = webdriver.Chrome(seleBrowserPath, options=chrome_options)
else:
    seleDriver = webdriver.Chrome(seleBrowserPath)

runProgram = True
if runProgram:
    while(True):
        seleDriver.get(URL)

        # add to cart
        seleLink = seleDriver.find_element_by_class_name("single_add_to_cart_button")
        seleLink.click()
        time.sleep(3)

        # add coupon
        seleLink = seleDriver.find_element_by_name("coupon_code")
        couponToTry = createNextFullCoupon()
        seleLink.send_keys(couponToTry)

        seleLink = seleDriver.find_element_by_name("apply_coupon")
        seleLink.click()

        # check coupon valid , page contains '  '
        pageHTML = str(str(seleDriver.page_source.encode('utf-8')))
        goodCoupon = False if pageHTML.find("does not exist!") == -1 else True
        if goodCoupon == True:
            goodCouponsArray.append(couponToTry)

        print(couponToTry, goodCoupon)
        time.sleep(3)

    seleDriver.close()
    f = open("coupons.txt", "a")
    for x in goodCouponsArray:
        f.write(x)
    f.close()
