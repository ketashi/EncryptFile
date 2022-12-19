#!/usr/bin/python3

from pwn import *
from selenium import webdriver
import sys,requests,pdb,time,signal,argparse,os,pandas,shutil

#CTRl C
def def_handler(sig,frame):
    log.info("Saliendo...")
    sys.exit(1)
signal.signal(signal.SIGINT,def_handler)
#Validation
if len(sys.argv) < 2:
    log.info("Uso: py %s -h" %sys.argv[0])
    sys.exit(1)

#arguments
parser = argparse.ArgumentParser(description= "Description")
parser.add_argument('--file', help='Lista de url')
args = parser.parse_args()
#get information of arguments
files = args.file
s= requests.session()
dirs="./Capture"
#create dir
def create():
    if not (os.path.isdir("./Capture")):
        os.mkdir("Capture")
    else:
        shutil.rmtree("./Capture/")
        os.mkdir("Capture")

def main():
    #create directory
    create()
    #verification file
    if (os.path.exists(files)):
        #read file excel
        data = pandas.read_excel(files)
        target_url = data["target_url"].values
        #bucle
        p1 = log.progress("Iniciando Scanning...")
        for i in range(len(target_url)):
            #send requests https
            try:
                list_url = target_url[i]
                list_url = list_url.replace("domain","https")
                p1.status("Probando pagina %s" %list_url)
                r = s.get(list_url,timeout=1)
                time.sleep(1)
                if r.status_code == 200:
                    log.success("[%d] -> %s Pagina habilitada" %(i,list_url))
                    options = webdriver.ChromeOptions()
                    options.add_argument('--window-size=1024,768')
                    options.add_argument('--headless')
                    options.add_argument('--disable-gpu')

                    browser = webdriver.Chrome(options=options)
                    browser.get(list_url)
                    browser.save_screenshot("./Capture/%i.png" %(i))
                    browser.close()
                    continue
                else:
                    #log.info("Page %s esta habilitada" %list_url)
                    pass
            except:
                #log.failure("Page %s no responde" %list_url)
                continue
    else:
        log.failure("El archivo no existe")

if __name__ == "__main__":
    main()
