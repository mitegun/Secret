from time import sleep
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
import json 
import requests
import art

def check_exists_by_xpath(xpath):
    
    try:
        browser.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def write_json(new_data, filename='product.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 7)
        
def write_json_var(id, var, filename='product.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        for obj in file_data:
            if obj['productId']==id:
                obj['variants'].append(var)

        # Join new_data with file_data inside emp_details
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 7)

def check_json(id, filename='product.json'):
    with open(filename,'r+') as file:
        file_data=json.load(file)
        a=0
        for obj in file_data:
            if(obj['productId'] == id):
                a=a+1
        if a>0:
            return True
        else:
            return False


def  off_json(nom,taille,brand, filename='product.json'):
    with open(filename,'r+') as file:
        file_data=json.load(file)
        for obj in file_data:
            if(obj['name']==nom and obj['brand']==brand):
                for variants in obj['variants']:
                    if(variants['europeanSize']==taille):
                        return(variants['MinAcceptOfferPrice'])
                                
                    

def obj_list(filename='product.json'):
    with open(filename,'r+') as file:
        file_data=json.load(file)
        i=1
        for obj in file_data:
            print(str(i) + "-" + obj['brand'] + " " + obj['name']+"\n")
            j=1
            for variants in obj['variants']:
                print(str(j) + "-" + variants['europeanSize'] + "\n")
                j=j+1
            i=i+1


def json_find_name(i,filename='product.json'):
    with open(filename,'r+') as file:
        file_data=json.load(file)
        return file_data[i]['name']

def json_find_size(i, j, filename='product.json'):
    with open(filename,'r+') as file:
        file_data=json.load(file)
        return file_data[i]['variants'][j]['europeanSize']

def delete_from_json(i, j):           
    with open('product.json') as file:
        file_data=json.load(file)
    del file_data[i]['variants'][j]
    if not 'variants' in file_data[i] or len(file_data[i]['variants']) == 0:
        del file_data[i]      
    with open('product.json','w') as file:
        file_data = json.dump(file_data, file, indent=7)
    
def update_json(i, j, prix, prixoff, count):
    with open('product.json') as file:
        file_data=json.load(file)
    file_data[i]['variants'][j]['price']=prix
    file_data[i]['variants'][j]['MinAcceptOfferPrice']=prixoff
    file_data[i]['variants'][j]['count']=count   
    with open('product.json','w') as file:
        file_data = json.dump(file_data, file, indent=7)



def offres():
    browser.get(("https://sell.wethenew.com/fr/offers"))
    sleep(1)
    printit()


def printit():
    threading.Timer(5.0, printit).start()
    xpath= '//span[contains(text(),"L\'offre wethenew :")]'
    a=check_exists_by_xpath(xpath)
    if(a==False):
        print("vous n'avez pas d'offre")
    else:        
        prixwtn=browser.find_element(By.XPATH, '//span[contains(text(),"L\'offre wethenew :")]').get_attribute("innerText")
        brand=browser.find_element(By.XPATH, '//div[@class="OfferCardstyled__Detail-sc-x3ap27-9 ecdxIl"]//span[1]').get_attribute("innerText")
        nom=browser.find_element(By.XPATH, '//div[@class="OfferCardstyled__Detail-sc-x3ap27-9 ecdxIl"]//span[2]').get_attribute("innerText")
        taille=browser.find_element(By.XPATH, '//div[@class="OfferCardstyled__Detail-sc-x3ap27-9 ecdxIl"]//span[3]').get_attribute("innerText")
        taille=taille[:taille.find(' EU')]
        print("Marque:"+brand+"\n")
        print("Modèle:"+nom+"\n")
        print("Taille:"+taille+"\n")
        prixwtn=prixwtn[prixwtn.find(':')+2:prixwtn.find('€')]
        a=prixwtn.find(': ')
        b=prixwtn.find('€')
        print("L'offre WTN:"+prixwtn+"\n")
        prix=off_json(nom, taille, brand)
        print("Ton prix à accepter:"+prix+"\n")
        if(int(prixwtn)<int(prix)):
            refus=browser.find_element(By.XPATH,'//button[contains(.,"Je refuse")]').get_attribute("innerText")
            refus.click()
            print("Offre refusée")
        else:
            accepter=browser.find_element(By.XPATH,'//button[contains(.,"J\'accepte")]').get_attribute("innerText")
            accepter.click()
            print("Offre acceptée")
    a=0
    browser.refresh()

def listing():    
    sku=input("Donne le SKU du produit:\n")
    offre=browser.find_element(By.XPATH,'//input[@name="productSearch"]')
    offre.send_keys(sku)
    sleep(3)
    xpath='//div[contains(@class, "ProductCard_ProductCard__LQccE")]'
    a=check_exists_by_xpath(xpath)
    print(a)
    sleep(3)
    if(a==True):
        browser.find_element(By.XPATH, xpath).click()
        sleep(1)
        b=browser.current_url
        b=b[45:len(b)]
        json_brand=browser.find_element(By.XPATH, '//p[@class="ProductTemplate_BrandModel__mfvat"]').get_attribute("innerText")
        json_nom=browser.find_element(By.XPATH, '//p[@class="ProductTemplate_NameModel__zw99y"]').get_attribute("innerText")
        json_img=browser.find_element(By.XPATH, '//img[@class="ProductTemplate_ImgProduct__yQX82"]').get_attribute("src")
        taille=input("Taille eu du produit:\n")        
        a=browser.find_elements(By.XPATH,'//ul[@class="VariantsList_VariantsListSquare__f2Ivd"]/li')
        tab=[]
        for res in a:
            txt=res.text
            tab.append(txt)
        for k in range(len(tab)):
            if(tab[k]==taille or tab[k]== "WTB\n"+str(taille)):
                g=k
                a[g].click()
                idd=a[k].get_attribute("id")
                break

                   
        sleep(1)        
        prix=input("Prix sur WeTheNew:\n")
        price=browser.find_element(By.XPATH,'//input[@name="price"]')
        price.send_keys(prix)
        prixmin=input("Prix minimum à accepter:\n")
        count=input("Quantité du produit:\n")
        q=browser.find_element(By.XPATH,'//input[@name="quantity"]')
        if(int(count)>1):
            q.send_keys("+")
            q.send_keys(count)
        sleep(1)
        producttype="shoe"          
        browser.find_element(By.XPATH,'//button[@class="Buttonstyled__Button-sc-x94gu-0 ivepvE ModalListingForm_Submit__rVCbD"]').click()
        browser.find_element(By.XPATH,'//a[@class="ProductTemplate_Button__aAz_w"]').click()
        if(check_json(b)==False):
            choix=input("Choisis ton mode d'expédition:\n 1- Shipping \n 2- Remise en main propre\n")   
            if(choix==1):  
                browser.find_element(By.XPATH,'//label[@class="InputRadiostyles__StyledInputRadio-sc-az2tte-0 jucWRQ ConfirmDealTemplate_ShippingInput__6xMZX"]').click()
            else:
                browser.find_element(By.XPATH,'//label[@class="InputRadiostyles__StyledInputRadio-sc-az2tte-0 jucWRQ ConfirmDealTemplate_DepositInput__BnEq6"]').click()
        sleep(3)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(1)
        browser.find_element(By.XPATH,'//span[@class="jsx-3820211865 Control"]').click()
        sleep(1)
        browser.find_element(By.XPATH,'//button[@class="Buttonstyled__Button-sc-x94gu-0 kwcLFQ ConfirmDealTemplate_Save__pYsFp"]').click()
        sleep(3)
        if(browser.current_url=="https://sell.wethenew.com/fr/stock/listing"):
            if(check_json(b)==True):
                variants= {
                        "id": a[k].get_attribute("id"),
                        "europeanSize": taille,
                        "price": prix,
                        "count": count,
                        "MinAcceptOfferPrice": prixmin
                    
                    }
                
                write_json_var(b, variants)
        
            else:
                object={"productId": b,
                "brand": json_brand,
                "name": json_nom,
                "productType": producttype,
                "image": json_img,
                "count": count,
                "variants": [
                    {
                        "id": idd,
                        "europeanSize": taille,
                        "price": prix,
                        "count": count,
                        "MinAcceptOfferPrice": prixmin
                    
                    }
                ]

                } 
                write_json(object)
        print("C'est listé bg.")
       
def listing2():
    sku=input("Donne le SKU du produit:\n")
    offre=browser.find_element(By.XPATH,'//input[@name="productSearch"]')
    offre.send_keys(sku)
    sleep(3)
    xpath='//div[contains(@class, "ProductCard_ProductCard__LQccE")]'
    a=check_exists_by_xpath(xpath)
    print(a)
    sleep(3)
    if(a==True):
        browser.find_element(By.XPATH, xpath).click()
        sleep(1)
        b=browser.current_url
        b=b[45:len(b)]
        json_brand=browser.find_element(By.XPATH, '//p[@class="ProductTemplate_BrandModel__mfvat"]').get_attribute("innerText")
        json_nom=browser.find_element(By.XPATH, '//p[@class="ProductTemplate_NameModel__zw99y"]').get_attribute("innerText")
        json_img=browser.find_element(By.XPATH, '//img[@class="ProductTemplate_ImgProduct__yQX82"]').get_attribute("src")
        taille=input("Taille eu du produit:\n")        
        a=browser.find_elements(By.XPATH,'//ul[@class="VariantsList_VariantsListSquare__f2Ivd"]/li')
        tab=[]
        for res in a:
            txt=res.text
            tab.append(txt)
        for k in range(len(tab)):
            if(tab[k].lower()==taille.lower() or tab[k].lower()== "WTB\n"+str(taille).lower()):
                g=k
                a[g].click()
                idd=a[k].get_attribute("id")
                break        
            sleep(1)     
            prix=input("Prix sur WeTheNew:\n")
            price=browser.find_element(By.XPATH,'//input[@name="price"]')
            price.send_keys(prix)
            prixmin=input("Prix minimum à accepter:\n")
            count=input("Quantité du produit:\n")
            q=browser.find_element(By.XPATH,'//input[@name="quantity"]')
            if(int(count)>1):
                q.send_keys("+")
                q.send_keys(count)
            sleep(1)
            producttype="accessory"           
            browser.find_element(By.XPATH,'//button[@class="Buttonstyles__Button-sc-1hzj9nz-0 ebgyWj wide"]').click()
            browser.find_element(By.XPATH,'//a[@class="ProductTemplate_Button__aAz_w"]').click()
            if(check_json(b)==False):
                choix=input("Choisis ton mode d'expédition:\n 1- Shipping \n 2- Remise en main propre\n")   
                if(choix==1):  
                    browser.find_element(By.XPATH,'//label[@class="InputRadiostyles__StyledInputRadio-sc-az2tte-0 jucWRQ ConfirmDealTemplate_ShippingInput__6xMZX"]').click()
                else:
                    browser.find_element(By.XPATH,'//label[@class="InputRadiostyles__StyledInputRadio-sc-az2tte-0 jucWRQ ConfirmDealTemplate_DepositInput__BnEq6"]').click()
            sleep(3)
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(1)
            browser.find_element(By.XPATH,'//span[@class="jsx-3820211865 Control"]').click()
            sleep(1)
            browser.find_element(By.XPATH,'//button[@class="Buttonstyled__Button-sc-x94gu-0 kwcLFQ ConfirmDealTemplate_Save__pYsFp"]').click()
            sleep(3)
            if(browser.current_url=="https://sell.wethenew.com/fr/stock/listing"):
                if(check_json(b)==True):
                    variants= {
                            "id": a[k].get_attribute("id"),
                            "europeanSize": taille,
                            "price": prix,
                            "count": count,
                            "MinAcceptOfferPrice": prixmin
                        
                        }
                    
                    write_json_var(b, variants)
            
                else:
                    object={"productId": b,
                    "brand": json_brand,
                    "name": json_nom,
                    "productType": producttype,
                    "image": json_img,
                    "count": count,
                    "variants": [
                        {
                            "id": idd,
                            "europeanSize": taille,
                            "price": prix,
                            "count": count,
                            "MinAcceptOfferPrice": prixmin
                        
                        }
                    ]

                    } 
                    write_json(object)
            print("C'est listé bg")          
                 
     
                


def delete():
    obj_list()
    a=input("Choisis ton item:\n")
    b=input("Choisis ta taille:\n")
    browser.find_element(By.XPATH, '//a[@href="/fr/my-listings"]').click()
    name=json_find_name(int(a)-1)
    sleep(2)
    offre=browser.find_element(By.XPATH,'//input[@name="productSearch"]') 
    offre.send_keys(name)
    print(name)
    sleep(5)
    browser.find_element(By.XPATH, '//div[@class="StockProduct_StockProduct__BFJlM"]').click()
    size=json_find_size(int(a)-1,int(b)-1)
    print(size)
    z=int(input("Que veux tu faire ?\n 1- Delete le listing\n 2-Update le listing \n"))
    if z==1:
        browser.find_element(By.XPATH, '//li['+b+'][@class="ListingSummary_ListingSummaryItem__vktH1"]//button[@class="ListingSummary_EditButton__4o6D_"]').click()
        delete_from_json(int(a)-1,int(b)-1)
        browser.find_element(By.XPATH,'//button[@class="Buttonstyles__Button-sc-1hzj9nz-0 fINGIH wide"]').click()
    if (z==2): 
        browser.find_element(By.XPATH, '//li['+b+'][@class="ListingSummary_ListingSummaryItem__vktH1"]//button[@class="ListingSummary_EditButton__4o6D_"]').click()
        count=input("Nouvelle quantité:\n")
        q=browser.find_element(By.XPATH,'//input[@name="quantity"]')
        q.send_keys("+")
        q.send_keys(count)
        price1=browser.find_element(By.XPATH,'//input[@name="price"]').get_attribute("value")
        print("Ton ancien prix était:"+price1)
        prixcons=browser.find_element(By.XPATH, '//p[@class="ModalListingForm_ParamsInfo__a254j"]').get_attribute("innerText")
        print(prixcons)
        prix=input("Ton nouveau prix:\n")
        prixoff=input("Offre minimum à accepter:")
        price=browser.find_element(By.XPATH,'//input[@name="price"]')
        price.clear()
        price.send_keys(prix)
        browser.find_element(By.XPATH, '//button[@class="Buttonstyles__Button-sc-1hzj9nz-0 ebgyWj wide"]').click()
        update_json(int(a)-1,int(b)-1, prix, prixoff, count)
       
def menu():
    browser.get("https://sell.wethenew.com/fr/listing")
    sleep(2)
    choix=input("Que veux tu faire bg? \n 1- Lister un vêtement\n 2- Lister sneakers\n 3- Monitor vente\n 4- Update un listing\n")
    if int(choix)==1:
        listing2()
        menu()
    if int(choix)==2:
        listing()
        menu() 
        
    if int(choix)==3:
        offres()
    if int(choix)==4:
        delete()
        menu()                    



if __name__ == "__main__":
    with open("setting.json", "r") as read_file:
        data = json.load(read_file)
        usernameStr = data["weTheNew_EMAIL"]
        passwordStr = data["weTheNew_PASSWORD"]
    """ options = uc.ChromeOptions()
    options.add_argument('--headless')
    ajouter options=options dans uc.Chrome()"""
    art.tprint("FUCK WTN\n")
    print("by Gratin\n\n\n")
    key = data["key"]
    print("KEY:"+key)
    service = ChromeService(executable_path="H:\Desktop\stage\chromedriver.exe")
    browser = uc.Chrome(service=service)
    
    try:
        browser.implicitly_wait(10)
        browser.get(('https://sell.wethenew.com/login'))
        sleep(5)
        test = browser.find_element(By.ID, "didomi-notice-agree-button")
        webdriver.ActionChains(browser).move_to_element(test).click(test).perform()
        sleep(3)
        username=browser.find_element(By.XPATH,'//input[@name="email" or contains(@placeholder,"Compléter ici...")]')
        username.send_keys(usernameStr)
        password=browser.find_element(By.XPATH,'//input[@name="password" or contains(@placeholder,"Compléter ici...")]')
        password.send_keys(passwordStr)
        sleep(2)
        login=browser.find_element(By.XPATH,'//button[contains(@class,"LoginTemplate_Button")]')
        login.click()    
        sleep(2)
        menu()
        
    except Exception as e:
        print(f"There was an error: {e}")

    sleep(10000)