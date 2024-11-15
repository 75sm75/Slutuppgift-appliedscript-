
from cryptography.fernet import Fernet ##  Kryptera och dekrypterar data
import argparse ##  Detta hanterar kommandoargument i terminalen 
import os ## Detta bibliotek med oprativsystemet tex kontrollerar om en fil existerar 
 
def generate_key():     ## Skapar nyckel för att kryptera och dekryptera  sedan för att spara i en fil 
    key = Fernet.generate_key()
    with open("nyckel.key", "wb") as key_file:
        key_file.write(key)
    print(f"Genererad nyckel: {key}")
 
def load_key():         ## ladda nyckel ,om det inte finns se till att generera nyckeln först
    if not os.path.exists("nyckel.key"):
        print("Nyckelfilen saknas. Generera en nyckel först.")
        return None
    with open("nyckel.key", "rb") as key_file:
        key = key_file.read()
        print(f"Nyckel laddad: {key}")
    return key
 
def encrypt_file(file_path):      ## kryptera nyckeln och spara filen med enc 
    key = load_key()
    if key is None:
        return
    if not os.path.exists(file_path):
        print(f"Filen {file_path} saknas.")
        return
    with open(file_path, "rb") as file_to_encrypt:
        file_data = file_to_encrypt.read()
 
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(file_data)
 
    enc_file_path = f"{file_path}.enc"  
    with open(enc_file_path, "wb") as enc_file:
        enc_file.write(cipher_text)
    print(f"Filen är krypterad och sparad som: {enc_file_path}")
 
def decrypt_file(file_path):      ## Dekrypterafilen och spara den utan enc
    key = load_key()
    if key is None:
        return
    if not os.path.exists(file_path):
        print(f"Filen {file_path} saknas.")
        return
    with open(file_path, "rb") as file:
        encrypted_message = file.read()
 
    cipher_suite = Fernet(key)
    try:
        plain_text = cipher_suite.decrypt(encrypted_message)
    except Exception as e:
        print(f"Fel vid dekryptering: {e}")
        return
 
    decrypted_file_name = os.path.splitext(os.path.basename(file_path))[0]  
    if decrypted_file_name.endswith(".enc"):  
        decrypted_file_name = decrypted_file_name[:-4]  
    final_decrypted_name = f"decrypted_{decrypted_file_name}"  
    
    directory = os.path.dirname(file_path)
    final_decrypted_path = os.path.join(directory, final_decrypted_name)  
 
    
    with open(final_decrypted_path, "wb") as decrypted_file:
        decrypted_file.write(plain_text)
    print(f"Filen är avkrypterad och sparad som '{final_decrypted_path}'")
 
parser = argparse.ArgumentParser(description="Sellas krypteringsprogram")       ## Skapar en parser för kommandoradsargument.
parser.add_argument("action", choices=["nyckel", "kryptera", "dekryptera"], help="Välj en åtgärd") ## Definierar vilka argument som kan användas.
parser.add_argument("--file", help="Välj en fil")  ## Tolkar argumenten som skickas via kommandoraden.
 
args = parser.parse_args()
 
if args.action == "nyckel": ## Utför åtgärder baserat på det valda argumentet
    generate_key()
elif args.action == "kryptera":
    if not args.file:
        print("Ingen fil angiven för kryptering.")
    else:
        encrypt_file(args.file)
elif args.action == "dekryptera":
    if not args.file:
        print("Ingen fil angiven för dekryptering.")
    else:
        decrypt_file(args.file)

