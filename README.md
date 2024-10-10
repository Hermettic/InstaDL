# InstaDL 📸

**InstaDL** es una aplicación escrita en Python que permite descargar contenido de cuentas de Instagram, incluidas aquellas privadas a las que sigues. Con esta herramienta puedes elegir qué elementos descargar (fotos, videos, historias, etc.), todo en un entorno controlado y personalizado.

## 🚀 Instalación rápida

### 1. Pre-requisitos

Antes de comenzar, asegúrate de tener Python instalado en tu sistema. Si no lo tienes, puedes instalarlo utilizando [Homebrew](https://brew.sh/) en macOS con el siguiente comando:

```bash
brew install python
```

### 2. Crear un entorno virtual

Para mantener tu entorno de trabajo limpio, vamos a crear un entorno virtual donde instalaremos todas las dependencias.

```bash
python3 -m venv InstaDL
```

### 3. Activar el entorno virtual

Una vez creado, es hora de activarlo. Dependiendo de tu sistema operativo, usa uno de los siguientes comandos:

- **En macOS/Linux**:

```bash
source InstaDL/bin/activate
```

- **En Windows**:

```bash
InstaDL\Scripts\activate
```

Tu terminal mostrará el nombre del entorno virtual (InstaDL) para indicar que está activado. Ahora todas las dependencias que instales estarán dentro de este entorno aislado.

### 4. Instalar dependencias 🔧

Con el entorno activado, instala todas las dependencias necesarias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

> Si prefieres instalar los paquetes manualmente, aquí está la lista completa de requerimientos:
>
> - `certifi==2024.8.30`
> - `cffi==1.17.1`
> - `charset-normalizer==3.4.0`
> - `cryptography==43.0.1`
> - `idna==3.10`
> - `instaloader==4.13.1`
> - `pycparser==2.22`
> - `requests==2.32.3`
> - `tqdm==4.66.5`
> - `urllib3==2.2.3`

### 5. ¡Descarga los perfiles que quieras! 🎉

Con todo configurado, ya puedes ejecutar el script y descargar perfiles de Instagram:

```bash
python InstaDL.py
```

## ⚠️ Importante: Evitar la suspensión de tu cuenta

Instagram podría detectar actividad inusual si descargas demasiado contenido o accedes a demasiados perfiles en poco tiempo. Te recomendamos utilizar una **cuenta secundaria** para evitar posibles bloqueos o suspensiones de tu cuenta principal.

## Contribuciones 🤝

Si tienes ideas para mejorar **InstaDL** o encuentras algún problema, ¡no dudes en crear un issue o un pull request.

---

### ¡Gracias por usar InstaDL! 🙌
