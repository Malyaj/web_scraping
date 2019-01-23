import PySimpleGUI as sg
import os
from selenium import webdriver
#import urllib
import time
import xlrd


chromedriver_path = r"D:\Users\703143501\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"
##sc_url = "http://supportcentral.ge.com/products/sup_products.asp?prod_id=285102"
sc_url = "https://supportcentral.ge.com/products/sup_products.asp?prod_id=285102"
# https://sites.google.com/a/chromium.org/chromedriver/
# keep chromedriver.exe in PATH
# "D:\Users\703143501\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"


def download_workflow(wfs, sso, key, download_dir, chromedriver_path=chromedriver_path, base_url = sc_url):
    ### create the wf_list
    wf_list = [x.strip() for x in wfs.split(',')]
    print(wf_list)

    options = webdriver.ChromeOptions()

    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') # 
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

    
    #driver.get("http://google.com/")
    #print ("Headless Chrome Initialized on Windows OS")

    
    ### instantiate the driver
    #options = webdriver.ChromeOptions()
    #options.headless = True
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    options.add_experimental_option("prefs", {"download.default_directory": download_dir,
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "safebrowsing.enabled": True
                                              }
                                    )

    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    #driver = webdriver.Chrome(options=options)

    
    ### login to support central
    driver.get(base_url)
    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys(sso)
    password_field.send_keys(key)
    submit_field = driver.find_element_by_name("submitFrm")
    submit_field.click()


    for wf in wf_list:
        # here we can repeat the download process for many workflows
        ### navigate to url of the wf
        url = f"https://supportcentral.ge.com/caseforms/sup_myforms.asp?form_doc_id={wf}"
        driver.get(url)
        # switch to frame
        frame_id = driver.find_element_by_id('mycase')
        driver.switch_to.frame(frame_id)
        # find relevant xpath
        xpath = """//*[@id="divCond_13756759"]/td[2]/a"""
        elem = driver.find_element_by_xpath(xpath)
        # download href
        href = elem.get_attribute("href")
        print(href)
        # filename
        filename = driver.find_element_by_xpath(xpath).text
        ## the 'http' in href extracted from elem needs to be replaced with 'https'
        href = href[:4] + 's' + href[4:]

        # download file
        driver.get(href)

        ### need to keep function waiting while the download happends
        filepath = download_dir + r"/" + filename
    
        #ofs = filename.split("_")[0]
        #esn = filename.split("_")[1]
    
        while True:
            file_created = filename in list(os.walk(download_dir))[0][2]
        
            #print(f"file created: {file_created}")
            if file_created:
                print(f"file {filename} downloaded at location {download_dir}")
                # remove wf from wf_list
                #wf_list.remove(wf)
                break
            else:
                print("Download in progress ...")
                time.sleep(5)

    # all wf processed, close the driver
    #driver.close()
    driver.quit()


###########################################################################################################################################################
def app():
    sg.SetOptions(text_justification='right', tooltip_time= 1)

    menu_def = [['&Download', ['&Sample workflow list']],
                ['&Import', ['workflow list']],
                #['Download sample workflow list'], 
                ['&Help', ['&About', ['base url', 'Chromedriver path']],],
                ]


    layout = [[sg.Menu(menu_def, tearoff=False)],
              #[sg.FileBrowse(), sg.InputText('Select Workflow list', key='_wf_list_')],
              [sg.FolderBrowse(), sg.InputText('Select Download location', key='_down_')],
              [sg.Text('Enter Workflow Number'.ljust(40, ' ')), sg.InputText('', key='_wf_')],
              [sg.Text('Enter SSO'.ljust(40, ' ')), sg.InputText('', key='_sso_')],
              [sg.Text('Enter password'.ljust(40, ' ')), sg.InputText('', password_char="*", key='_key_')], 
              [sg.RButton('Submit', size=(100,1))],
              [sg.Exit(size=(100,1))],
              ]


    window = sg.Window('Cost File download tool', grab_anywhere=True).Layout(layout)

    #window.BackgroundColor = 'black'
    window.Resizable = True
    window.TextJustification = True


    ### event loop
    while True:
        event, values = window.Read()

        if event == 'Chromedriver path':
            sg.Popup(chromedriver_path)

        if event == 'base url':
            sg.Popup(sc_url)
        
        if event is None or event == 'Exit':    
            break
        
        if event == 'Submit':
            # pass the WF#, download location, and the SSO, key to the function
            download_dir = values['_down_']
            wf = values['_wf_']
            sso = values['_sso_']
            key = values['_key_']
            
            download_workflow(wf, sso, key, download_dir)
            sg.Popup(f'Files download at {download_dir}')

    window.Close()
###########################################################################################################################################################


if __name__ == "__main__":
    # run app
    app()


