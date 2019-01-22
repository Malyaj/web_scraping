import os
from selenium import webdriver
import urllib
import time

#download_dir = r"D:\Users\703143501\Downloads"
chromedriver_path = r"D:\Users\703143501\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"
sc_url = "http://supportcentral.ge.com/products/sup_products.asp?prod_id=285102"
# https://sites.google.com/a/chromium.org/chromedriver/
# keep chromedriver.exe in PATH
# "D:\Users\703143501\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"

def download_workflow(wf, sso, key, download_dir, chromedriver_path=chromedriver_path, base_url = sc_url):
    ### instantiate the driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": download_dir,
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "safebrowsing.enabled": True
                                              }
                                    )
    
    #options.add_argument(f"download.default_directory={download_dir}")
    driver = webdriver.Chrome(options=options)

    ### login to support central
    driver.get(base_url)
    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys(sso)
    password_field.send_keys(key)
    submit_field = driver.find_element_by_name("submitFrm")
    submit_field.click()


    # here we can repeat the download process for many workflows
    ### navigate to url of the wf
    url = f"https://supportcentral.ge.com/caseforms/sup_myforms.asp?form_doc_id={wf}"
    driver.get(url)

    # switch to frame
    frame_id = driver.find_element_by_id('mycase')
    driver.switch_to.frame(frame_id)

    # find file name
    # http://libraries.ge.com/systemfiledownload?fileid=945315793101
    xpath = """//*[@id="divCond_13756759"]/td[2]/a"""
    elem = driver.find_element_by_xpath(xpath)
    #print(dir(elem))
    filename = driver.find_element_by_xpath(xpath).text
    print(f"filename: {filename}")

    # download file
    ## issue: the target href changes with workflows
    ## possible solution : check the element's attributes using the xpath
    href="https://libraries.ge.com/systemfiledownload?fileid=942004535101"
    driver.get(href)

    ### need to keep function waiting while the download happends
    filepath = download_dir + r"/" + filename
    #print(f"filepath: {filepath}")

    # ideal file name: "1326706_890138_CostFile_Closeout.xlsx"
    # however file may be saved with some modification in name like
    # 1326706_890138_CostFile_Closeout_rev12.xlsx
    
    ofs = filename.split("_")[0]
    esn = filename.split("_")[1]
    filename_without_extension = filename.split(".")[0] #1326706_890138_CostFile_Closeout
    filename_stem = "_".join(filename.split(".")[0].split("_")[:3]) #1326706_890138_CostFile

    def partial_match(name, filename):
        ofs = filename.split("_")[0]
        esn = filename.split("_")[1]
        filename_without_extension = filename.split(".")[0] #1326706_890138_CostFile_Closeout
        filename_stem = "_".join(filename.split(".")[0].split("_")[:3]) #1326706_890138_CostFile

        if (ofs in name) and (esn in name) and ((in name) or (in name))

        

    
    while True:
        files_at_location = list(os.walk(download_dir))[0][2]
        exact_match = filename in files_at_location
        
        #fuzzy_match
        print(f"file created: {file_created}")
        if exact_match or fuzzy_match:
            print(f"file {filename} downloaded at location {donwload_dir}")
            break
        else:
            print("Downloading file ...")
            time.sleep(3)


##############################################################################################################
##############################################################################################################
import PySimpleGUI as sg
#sg.ChangeLookAndFeel('DarkBlue')
  
sg.SetOptions(text_justification='right', tooltip_time= 1)

###
menu_def = [['&File', ['&Open', ['Train set', 'Unseen Data'], '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', ['&About'],]]


layout = [#[sg.Menu(menu_def, tearoff=False)],
          #[sg.FileBrowse(), sg.InputText('Select Workflow list', key='_wf_list_')],
          [sg.FolderBrowse(), sg.InputText('Select Download location', key='_down_')],
          [sg.Text('Enter Workflow Number'.ljust(50, ' ')), sg.InputText('', key='_wf_')],
          [sg.Text('Enter SSO'.ljust(50, ' ')), sg.InputText('', key='_sso_')],
          [sg.Text('Enter password'.ljust(50, ' ')), sg.InputText('', password_char="*", key='_key_')], 
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
    if event is None or event == 'Exit':      
        break      
    if event == 'Submit':
        # pass the WF#, download location, and the SSO, key to the function
        download_dir = values['_down_']
        wf = values['_wf_']
        sso = values['_sso_']
        key = values['_key_']

        #print(download_dir)
        
        download_workflow(wf, sso, key, download_dir)
        #filename = "1364670_298402_CostFile_Closeout_Rev12.xlsx"
        #filepath = download_dir + r"/" + filename
        #print("-+-" * 15)
        #print(filepath)
        #os.path.isfile(filepath)
        sg.Popup(f'File download at {download_dir}')

window.Close()
