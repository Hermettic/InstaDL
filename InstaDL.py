import instaloader
import os
from getpass import getpass
from tqdm import tqdm
from cryptography.fernet import Fernet
from instaloader.exceptions import ProfileNotExistsException, ConnectionException, BadCredentialsException

CONFIG_DIR = '.config'
PERFILES_DIR = 'perfiles'
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'credenciales.txt')
KEY_FILE = os.path.join(CONFIG_DIR, 'clave.key')

L = instaloader.Instaloader()

L.download_comments = False
L.save_metadata = False
L.download_video_thumbnails = False
L.post_metadata_txt_pattern = ""

def clear_screen():
    # Limpia la pantalla según el sistema operativo
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def cargar_clave():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            clave = key_file.read()
    else:
        clave = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(clave)
    return clave

def cifrar_texto(texto, clave):
    fernet = Fernet(clave)
    texto_cifrado = fernet.encrypt(texto.encode())
    return texto_cifrado

def descifrar_texto(texto_cifrado, clave):
    fernet = Fernet(clave)
    texto_descifrado = fernet.decrypt(texto_cifrado).decode()
    return texto_descifrado

def guardar_credenciales(username, password):
    clave = cargar_clave()
    with open(CREDENTIALS_FILE, 'wb') as cred_file:
        cred_file.write(cifrar_texto(username, clave) + b'\n')
        cred_file.write(cifrar_texto(password, clave))

def cargar_credenciales():
    if os.path.exists(CREDENTIALS_FILE):
        clave = cargar_clave()
        with open(CREDENTIALS_FILE, 'rb') as cred_file:
            username_cifrado = cred_file.readline().strip()
            password_cifrado = cred_file.readline().strip()
            username = descifrar_texto(username_cifrado, clave)
            password = descifrar_texto(password_cifrado, clave)
            return username, password
    return None, None

def verificar_perfil(profile_name):
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
        return profile
    except ProfileNotExistsException:
        print(f"El perfil '{profile_name}' no existe. Inténtalo de nuevo.")
        return None
    except ConnectionException:
        print("Error de conexión. Inténtalo de nuevo.")
        return None

def crear_subcarpetas(perfil_path):
    publicaciones_path = os.path.join(perfil_path, "Publicaciones")
    historias_path = os.path.join(perfil_path, "Historias")
    highlights_path = os.path.join(perfil_path, "Highlights")

    if not os.path.exists(publicaciones_path):
        os.makedirs(publicaciones_path)
    if not os.path.exists(historias_path):
        os.makedirs(historias_path)
    if not os.path.exists(highlights_path):
        os.makedirs(highlights_path)

    return publicaciones_path, historias_path, highlights_path

def descargar_contenido(profile_name):
    profile = verificar_perfil(profile_name)
    while profile is None:
        profile_name = input("Ingresa un nombre de usuario válido del perfil del cual deseas descargar contenido: ")
        profile = verificar_perfil(profile_name)

    if not os.path.exists(PERFILES_DIR):
        os.makedirs(PERFILES_DIR)

    perfil_path = os.path.join(PERFILES_DIR, profile_name)
    if not os.path.exists(perfil_path):
        os.makedirs(perfil_path)

    publicaciones_path, historias_path, highlights_path = crear_subcarpetas(perfil_path)

    opciones = input("¿Qué deseas descargar? (1: Publicaciones, 2: Historias, 3: Highlights, 4: Todo): ")

    total_items = 0
    publicaciones = []
    historias = []
    destacados = []

    if opciones in ['1', '4']:
        publicaciones = list(profile.get_posts())
        total_items += len(publicaciones)

    if opciones in ['2', '4']:
        historias = list(L.get_stories(userids=[profile.userid]))
        for story in historias:
            total_items += len(list(story.get_items()))

    if opciones in ['3', '4']:
        try:
            destacados = list(L.get_highlights(profile))
            for highlight in destacados:
                total_items += len(list(highlight.get_items()))
        except KeyError as e:
            print(f"Error al obtener los highlights: {e}")

    with tqdm(total=total_items, desc="Descargando contenido", unit="archivo") as pbar:
        
        if opciones in ['1', '4']:
            for post in publicaciones:
                L.dirname_pattern = publicaciones_path
                L.download_post(post, target='.')
                pbar.update(1)

        if opciones in ['2', '4']:
            for story in historias:
                for item in story.get_items():
                    L.dirname_pattern = historias_path
                    L.download_storyitem(item, target='.')
                    pbar.update(1)

        if opciones in ['3', '4']:
            for highlight in destacados:
                try:
                    for item in highlight.get_items():
                        L.dirname_pattern = highlights_path
                        L.download_storyitem(item, target='.')
                        pbar.update(1)
                except KeyError as e:
                    print(f"Error al descargar el highlight: {e}")

    print("Descarga completada.")

def iniciar_sesion():
    while True:
        username, password = cargar_credenciales()
        
        if username is not None and password is not None:
            usar_guardado = input(f"¿Quieres usar el usuario guardado ({username})? (s/n): ").lower()
            if usar_guardado == "s":
                try:
                    print(f"Iniciando sesión como {username}")
                    L.login(username, password)
                    return
                except BadCredentialsException:
                    print("Contraseña incorrecta, por favor ingrésala nuevamente.")
            else:
                print("Iniciar sesión con un nuevo usuario.")
        
        username = input("Ingresa tu nombre de usuario de Instagram: ")
        password = getpass("Ingresa tu contraseña de Instagram: ")
        
        try:
            L.login(username, password)
            guardar_credenciales(username, password)
            return
        except BadCredentialsException:
            print("Contraseña incorrecta, por favor intenta de nuevo.")

def main():
    iniciar_sesion()
    
    while True:
        clear_screen()
        profile_name = input("Ingresa el nombre de usuario del perfil del cual deseas descargar contenido: ")
        descargar_contenido(profile_name)

        continuar = input("¿Deseas descargar de otro perfil? (s/n): ").lower()
        if continuar != 's':
            break

        clear_screen()

    print("Programa terminado.")

main()
