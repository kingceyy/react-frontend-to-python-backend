# ⚡ Quick Start - Club JM Backend

## 🎯 En 5 minutes

### 1. Préparer Neon

- Aller https://console.neon.tech
- Créer projet
- Copier CONNECTION STRING

### 2. Créer le Bot Telegram

- Contacter @BotFather sur Telegram
- `/newbot`
- Copier le TOKEN

### 3. Générer des secrets

```bash
# Clé JWT
openssl rand -base64 32

# Secret webhook (optionnel)
openssl rand -base64 32
```

### 4. Fichier `.env`

```bash
cp .env.example .env
```

Éditer `.env`:
```
DATABASE_URL=postgresql://...         # Neon
TELEGRAM_BOT_TOKEN=...                 # BotFather
TELEGRAM_WEBHOOK_SECRET=...            # Généré
JWT_SECRET=...                         # Généré
FRONTEND_URL=https://clubjm.vercel.app
TELEGRAM_CHANNEL_ID=-1002632653839
DEBUG=False
```

### 5. Tester localement

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Vérifier: http://localhost:8000/health → `{"status": "ok"}`

### 6. Pousser sur GitHub

```bash
git init
git add .
git commit -m "Initial"
git remote add origin https://github.com/YOU/clubjm-backend
git push -u origin main
```

### 7. Déployer sur Koyeb

1. Aller https://app.koyeb.com
2. Connecter GitHub
3. **Create Web Service** → GitHub → `clubjm-backend`
4. Builder: `Buildpack`
5. Run: `uvicorn main:app --host 0.0.0.0 --port 8000`
6. Port: `8000`
7. Ajouter toutes les variables d'environnement (voir étape 4)
8. **Deploy** ✨

### 8. Configurer Frontend

Sur Vercel:
- Settings → Environment Variables
- `VITE_API_BASE_URL=https://xxx.koyeb.app`
- Redéployer

### 9. Test Bot

- Ouvrir Telegram
- Chercher votre bot
- `/start`
- Cliquer "🎮 Ouvrir l'app"
- ✅ Ça marche!

## 📚 Architecture

```
FastAPI Backend (Koyeb)
    ↓
SQLAlchemy + Neon PostgreSQL
    ↓
Aiogram Telegram Bot
    ↓
React Frontend (Vercel)
```

## 🔌 API Endpoints

### Auth
```
POST /api/auth/telegram
  ↓ InitData + start_param
  ← token + profile
```

### User
```
GET /api/me               → Profil utilisateur
GET /api/coupons          → Coupons disponibles
GET /api/coupons/history  → Historique
GET /api/leaderboard      → Top 100
GET /api/referees         → Mes filleuls
GET /api/vip              → Info VIP
POST /api/vip/purchase    → Acheter VIP
```

### Admin (is_admin=true required)
```
POST   /api/admin/coupons              → Créer coupon
GET    /api/admin/coupons              → Liste tous
PATCH  /api/admin/coupons/{id}/validate → Valider
GET    /api/admin/users                → Liste users
GET    /api/admin/users?search=...     → Chercher
PATCH  /api/admin/users/{id}           → Modifier
GET    /api/admin/stats                → Statistiques
```

## 🤖 Bot Commands

```
/start      Menu principal avec boutons
/about      À propos de Club JM
/ref        Mon lien de parrainage
/help       Aide
```

## 📊 Système de Classe

```
Starter: 0-29 parrainages    🟢
Loki:    30-49               🔵
Blaise:  50-79               🟣
Master:  80+                 🔴
```

## 🔄 Flux Utilisateur

1. User clique bot Telegram
2. Bot affiche `/start` avec boutons
3. Click "🎮 Ouvrir l'app" → Web App avec InitData
4. Frontend valide: `POST /api/auth/telegram`
5. Backend retourne token JWT
6. Frontend stocke token, fait appels avec `Authorization: Bearer <token>`
7. User voir coupons, leaderboard, etc.

## 🎟️ Système de Coupon

```
Coupon {
  id: string
  code: string
  image_url: string (s'adapte au format de l'image)
  text: string
  min_class: "Starter" | "Loki" | "Blaise" | "Master"
  expires_at: datetime (null = jamais)
  quantity_left: number (null = illimité)
  locked: boolean (true si user pas assez de classe)
}
```

Admin crée coupon → Appear pour users qualifiés → User clique → Valider coupon

## 👥 Système de Parrainage

1. Admin/user a referral_code: `JMXXXXXXX`
2. Invite ami avec `/start ref_JMXXXXXXX`
3. Backend détecte `start_param` = `ref_JMXXXXXXX`
4. Crée referral relationship
5. Referrer: `active_invites += 1`
6. Check si rank up (30/50/80 invites) → Mettre à jour class
7. Unlock coupons pour nouvelle class

## 🛡️ Sécurité

- ✅ InitData Telegram validé (HMAC-SHA256)
- ✅ JWT tokens (HS256, 30 jours)
- ✅ CORS pour Vercel origin seulement
- ✅ Admin-only endpoints vérifiés
- ✅ HTTPS en production
- ✅ Webhook secret pour bot (optionnel)

## 🔧 Dépannage rapide

**"Module not found"**
→ `pip install -r requirements.txt`

**"Database connection error"**
→ Vérifier DATABASE_URL dans .env

**"Bot pas répond"**
→ Vérifier TELEGRAM_BOT_TOKEN

**"CORS error"**
→ Vérifier FRONTEND_URL = https://clubjm.vercel.app

**"Koyeb stuck"**
→ Vérifier logs: `koyeb service logs --name clubjm-backend`

## 📁 Structure fichiers

```
clubjm-backend/
├── main.py              # Entry point
├── requirements.txt     # Dépendances
├── .env.example        # Config template
├── Dockerfile          # Pour Docker
├── docker-compose.yml  # Dev avec PostgreSQL local
├── start.sh            # Script de démarrage
└── app/
    ├── __init__.py
    ├── api.py          # Routes FastAPI
    ├── bot.py          # Handlers Aiogram
    ├── auth.py         # Auth & JWT
    ├── config.py       # Configuration
    ├── database.py     # SQLAlchemy
    ├── models.py       # ORM models
    ├── schemas.py      # Pydantic schemas
    └── crud.py         # Database operations
```

## 🚀 Prochaines étapes

1. **Admin** - Rendre users admin:
   ```sql
   UPDATE users SET is_admin = TRUE WHERE telegram_id = YOUR_ID;
   ```

2. **VIP Channel** - Configurer channel privé dans `bot.py`

3. **Webhook** - Configurer webhook Telegram pour real-time

4. **Analytics** - Ajouter monitoring/logs

5. **Email** - Notifications (optionnel)

## 📞 Support

- Docs: Voir README.md, INSTALLATION.md, DEPLOYMENT_CHECKLIST.md
- Telegram: @JMDAVEKKKK
- GitHub Issues: Pour les bugs

## ✨ Succès!

Si vous voyez:
- ✅ Bot répond à /start
- ✅ App web s'ouvre
- ✅ Leaderboard charge
- ✅ Coupons visibles

**Bravo, c'est en production!** 🎉
