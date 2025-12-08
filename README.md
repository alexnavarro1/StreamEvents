# StreamEvents

## ✨ Objectius
Sistema de gestió d'esdeveniments en streaming amb autenticació d'usuaris, perfils personalitzats i funcionalitats de seguiment entre usuaris.  
Aquest projecte està completament documentat en català.

## 🧱 Stack Principal
- **Backend**: Django 5.0
- **Base de dades**: MongoDB amb Djongo
- **Processament d'imatges**: Pillow
- **Frontend**: HTML5, CSS3, Bootstrap 5

## 📂 Estructura del Projecte
- `streamevents/`
  - `config/`: Configuració global del projecte Django.
  - `users/`: App de gestió d'usuaris (CustomUser) i sistema de seguidors.
  - `events/`: App de gestió d'esdeveniments (CRUD complet, filtratge, visualització).
    - `templates/events/`: Plantilles HTML per a llistats, detalls i formularis.
    - `static/events/`: Scripts JS i estils específics.
  - `media/`: Arxius pujats pels usuaris (avatars, miniatures).
  - `static/`: Arxius estàtics globals.

## 🌟 Funcionalitats Principals

### 📅 Gestió d'Esdeveniments (App `events`)
- **CRUD Complet**: Crear, llegir, actualitzar i eliminar esdeveniments.
- **Estats d'Esdeveniment**: Programat, En Directe, Finalitzat, Cancel·lat.
- **Incrustació de Streaming**: Suport automàtic per a **Twitch** i **YouTube**.
- **Filtratge**: Cerca per títol, categoria, estat i rang de dates.
- **Imatges**: Redimensionament automàtic de miniatures a 600x600px.
- **Tauler de Control**: Vista "Els meus esdeveniments" per gestionar creacions pròpies.

### 👤 Gestió d'Usuaris (App `users`)
- Registre i autenticació d'usuaris personalitzats.
- Perfils d'usuari editables amb avatar.
- Sistema de "Follow" (seguir altres usuaris).

## ✅ Requisits previs
- Python 3.10+
- MongoDB local (port 27017 per defecte)
- Git

## 🚀 Instal·lació i Configuració

1. **Clonar el repositori**:
   ```bash
   git clone (repositori)
   cd streamevents
   ```

2. **Crear i activar l'entorn virtual**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Instal·lar dependències**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la Base de Dades**:
   Assegura't que MongoDB està corrent a `mongodb://localhost:27017`.

5. **Aplicar migracions**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Carregar dades d'exemple (Fixtures)**:
   ```bash
   python manage.py loaddata users/fixtures/01_groups.json
   python manage.py loaddata users/fixtures/02_users.json
   python manage.py loaddata events/fixtures/events.json
   ```

7. **Crear superusuari (Opcional)**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Executar el servidor**:
   ```bash
   python manage.py runserver
   ```
   Accedeix a: `http://127.0.0.1:8000/events/`

## 🛠️ Comandes de Manteniment
- **Actualitzar estats d'esdeveniments automàticament**:
  ```bash
  python manage.py update_event_status
  ```

## � Documentació
El codi font inclou comentaris detallats en **català** explicant la lògica de les vistes, models i formularis per facilitar l'aprenentatge i manteniment.