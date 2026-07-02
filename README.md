# Club JM Backend

Backend FastAPI + Aiogram pour le bot Telegram Club JM.

## Installation

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration de l'environnement

Copier `.env.example` en `.env` et remplir les variables:

```bash
cp .env.example .env
```

**Variables importantes:**

- `DATABASE_URL`: Lien Neon PostgreSQL
- `TELEGRAM_BOT_TOKEN`: Token du bot Telegram
- `JWT_SECRET`: Clé secrète JWT (générer: `openssl rand -base64 32`)
- `FRONTEND_URL`: URL du frontend (https://clubjm.vercel.app)

### 3. Base de données

La base de données se crée automatiquement au premier démarrage.

Pour réinitialiser:
```bash
python -c "from app.database import engine, Base; Base.metadata.drop_all(engine); Base.metadata.create_all(engine)"
```

### 4. Démarrage du serveur

```bash
python main.py
```

ou

```bash
bash start.sh
```

Le serveur démarre sur `http://localhost:8000`

## Endpoints API

### Authentification

- `POST /api/auth/telegram` - Authentifier avec InitData Telegram

### Utilisateur

- `GET /api/me` - Profil utilisateur actuel
- `GET /api/coupons` - Liste des coupons disponibles
- `GET /api/coupons/history` - Historique des coupons validés
- `GET /api/leaderboard` - Classement des utilisateurs
- `GET /api/referees` - Liste de mes filleuls
- `GET /api/vip` - Infos VIP
- `POST /api/vip/purchase` - Initiateur achat VIP

### Admin

- `POST /api/admin/coupons` - Créer un coupon
- `GET /api/admin/coupons` - Liste tous les coupons
- `PATCH /api/admin/coupons/{id}/validate` - Valider un coupon
- `GET /api/admin/users` - Liste les utilisateurs (avec recherche)
- `PATCH /api/admin/users/{id}` - Modifier un utilisateur
- `GET /api/admin/stats` - Statistiques

## Bot Telegram

### Commandes

- `/start` - Démarrer et voir boutons
- `/about` - À propos de Club JM
- `/ref` - Voir le lien de parrainage
- `/help` - Aide

### Features

- Mini app intégrée (lien Web App)
- Système de parrainage (start_param)
- Vérification d'adhésion au canal
- Support Aiogram 3.3

## Architecture

```
clubjm-backend/
├── main.py                 # Point d'entrée
├── requirements.txt        # Dépendances
├── .env.example           # Variables d'exemple
├── app/
│   ├── __init__.py
│   ├── api.py             # Routes FastAPI
│   ├── bot.py             # Handlers Aiogram
│   ├── auth.py            # Auth & JWT
│   ├── config.py          # Configuration
│   ├── database.py        # Connexion BD
│   ├── models.py          # Modèles SQLAlchemy
│   ├── schemas.py         # Schémas Pydantic
│   └── crud.py            # Operations BD
```

## Déploiement Koyeb

### 1. Créer un projet Koyeb

https://app.koyeb.com

### 2. Connecter le Git

Pousser ce repo sur GitHub et connecter Koyeb.

### 3. Configuration Koyeb

- **Builder**: `python-wsgi`
- **Run command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **HTTP port**: `8000`

### 4. Variables d'environnement

Ajouter toutes les variables du `.env.example` dans Koyeb settings:

- `DATABASE_URL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`
- `JWT_SECRET`
- `FRONTEND_URL`
- `TELEGRAM_CHANNEL_ID`
- `DEBUG=False`

### 5. Webhook Telegram

Une fois déployé, configurer le webhook:

```bash
curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook \
  -d url=https://<KOYEB_URL>/webhook
```

## Frontend Connection

Le frontend sur Vercel se connecte au backend avec:

```typescript
const BASE_URL = "https://<KOYEB_URL>";
```

À configurer dans `.env.example` du frontend.

## Support

Contact: https://t.me/JMDAVEKKKK

## License

Proprietary
