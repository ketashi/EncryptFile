#!/usr/bin/python3
import sys,signal,argparse,os,string,secrets,pdb,base64
from cryptography.fernet import Fernet
from pwn import *

#control C
def def_handler(sig,frame):
    log.info("Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

#validar
#if len(sys.argv) < 2:
 #   log.info("Uso: python3 %s -h" % sys.argv[0])
  #  sys.exit(1)

#validar input
#text = "Uso: python3 %s --encrypt <archivo_a_encryptar> or --decrypt <archivo_a_desencriptar> or --dencrypt <ruta_de_carpeta_encriptar>" % sys.argv[0] 
#parser = argparse.ArgumentParser(description = text)
#parser.add_argument("--encrypt", help = "archivo a encriptar")
#parser.add_argument("--decrypt", help = "archivo a desencriptar")
#parser.add_argument("--dencrypt", help = "ruta de directorio que desea encriptar")
#parser.add_argument("--ddecrypt", help = "ruta de directorio que desea desencriptar")
#args = parser.parse_args() 

#variables globales
#file_e = args.encrypt
#file_d = args.decrypt
#dir_e = args.dencrypt
#dir_d = args.ddecrypt

#Generar Claves
def key_gen():
    
    key = Fernet.generate_key()
    with open ("filekey.key", "wb") as file_key:
        file_key.write(key)

#Encriptar Archivo
def encryption_file(master,file_e):
    
    #obtener data de archivo original
    with open(file_e, "rb") as file:
        original = file.read()

    #obtener data encriptar
    encryption = master.encrypt(original)
    try:
        #encyptar archivo
        with open(file_e, "wb") as encrypt_file:
                encrypt_file.write(encryption)

        #renombrar del archivo
        os.rename(file_e,file_e + ".crypt")
        log.success("archivo encriptado con exito")
    
    except Exception as err:
        log.failure(err)

#Desencriptar Archivo
def decryption_file(master,file_d):
    
    #obtener data de archivo encriptado
    with open(file_d, "rb") as file:
        file_encrypt = file.read()
    
    #obtener data desencriptar
    decryption = master.decrypt(file_encrypt) 
    
    try:
        #descriptar archivo
        with open(file_d, "wb") as decrypt_file:
            decrypt_file.write(decryption)
       
        #renombrar archivo   
        os.rename(file_d,file_d.replace(".crypt",""))
        log.success("archivo desencriptado con exito")
    
    except Exception as err:  
        log.failure(err) 

#encriptar carpeta de archivos
def dencryption_file(master):
    
    for root, dirs, files in os.walk("./Prueba"):
        for file in files:
            file_path = os.path.join(root, file)
            encryption_file(master,file_path)

#desencriptar carpeta de archivo
def ddecryption_file(master):
     for root, dirs, files in os.walk(dir_d):
        for file in files:
            file_path = os.path.join(root, file)
            decryption_file(master,file_path)


if __name__ == "__main__":
        
    #Obtener o crear clave
    #if os.path.isfile("filekey.key"):
     #   with open("filekey.key", "rb") as read_key:
      #      key = read_key.read()
    #else:
     #   key_gen()
      #  with open("filekey.key", "rb") as read_key:
       #     key = read_key.read()
    key = "GEJ-94F-iE-kEMjk4iHptFYcTFxLS1lL_yTvAAagJtA="        
    #clave maestra
    master = Fernet(key)
    
    #Encriptar archivo 
    #if args.encrypt:
     #   encryption_file(master,file_e) 
    
    #Desencriptar archivo   
    #if args.decrypt:
     #   decryption_file(master,file_d)
    
    #Encriptar directorios
    #if args.dencrypt:
    dencryption_file(master)
    #Desencriptar directorios
    #if args.ddecrypt:
     #   ddecryption_file(master)

