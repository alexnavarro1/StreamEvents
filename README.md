# StreamEvents

## ✨ Objectius
Sistema de gestió d'esdeveniments en streaming amb autenticació d'usuaris, perfils personalitzats i funcionalitats de seguiment entre usuaris.

## 🧱 Stack Principal
- **Backend**: Django 5.0.0
- **Base de dades**: MongoDB amb Djongo
- **Processament d'imatges**: Pillow

## 📂 Estructura Simplificada
- streamevents/
- ├── config/ # Configuració del projecte Django
- ├── users/ # App d'usuaris personalitzats
- │ ├── fixtures/ # Dades inicials
- │ │ ├── 01_groups.json
- │ │ └── 02_users.json
- │ ├── models.py # CustomUser i Follow
- │ └── admin.py # Panell d'administració
- ├── templates/ # Plantilles HTML
- ├── media/ # Arxius pujats (avatars)
- ├── static/ # CSS, JS, imatges
- ├── venv/ # Entorn virtual
- └── manage.py


## ✅ Requisits previs
- Python 3.10+
- MongoDB local (port 27017)
- Git

## 🚀 Instal·lació ràpida

1. **Clonar i preparar entorn**:
```bash
git clone (repositori)
cd streamevents
python -m venv venv
```

2.**Activar entorn virtual**:
```bash
venv\Scripts\activate
```

3.**Instalar dependecies**
```bash
pip install django==5.0.0
pip install djongo==1.3.6
pip install pymongo==3.12.3
pip install python-dotenv==1.0.0
pip install pillow==10.1.0
```

4.**Aplicar migracions**
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔐 Variables d'entorn (env.example)
SECRET_KEY=1234
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
MONGO_URL=mongodb://localhost:27017
DB_NAME=streamevents_db

## 👤 Superusuari
```bash
python manage.py createsuperuser
```
## 🗃️ Migrar a MongoDB
```bash
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
      'default': {
        'ENGINE': 'djongo',
        'NAME': 'streamevents_db',
        'ENFORCE_SCHEMA': True,
        'CLIENT': {
            'host': 'mongodb://localhost:27017'
        }
    }
}
```

## 🛠️ Comandes útils
```bash
# Executar servidor
python manage.py runserver

# Crear nova app
python manage.py startapp app_name
```
## 💾 Fixtures (exemple)
```bash
python manage.py loaddata users/fixtures/*.json
```
## 🌱 Seeds (exemple d'script)
...