# 🎯 LIRE D'ABORD - Club JM Backend

Bienvenue! Tu as reçu le backend complet pour ton bot Telegram Club JM.

## 📦 Ce que tu as

✅ **Backend FastAPI complet**
- 10 fichiers Python
- Tous les endpoints nécessaires
- Intégration Neon PostgreSQL
- Bot Aiogram configuré

✅ **Documentation complète**
- QUICKSTART.md → Démarrer en 5 min
- INSTALLATION.md → Installation détaillée
- DEPLOYMENT_CHECKLIST.md → Checklist de déploiement
- README.md → Documentation API complète
- FRONTEND_SETUP.md → Configurer le frontend

✅ **Prêt pour production**
- Docker + docker-compose
- Configuration de sécurité
- CORS configuré
- JWT tokens

## 🚀 Les 3 étapes principales

### 1️⃣ Préparation (15 min)
```
1. Créer projet Neon (DB)
2. Créer bot @BotFather
3. Générer JWT secret
4. Créer .env
```

### 2️⃣ Test local (5 min)
```
python -m venv venv
pip install -r requirements.txt
python main.py
→ http://localhost:8000/health
```

### 3️⃣ Déployer Koyeb (10 min)
```
1. GitHub repo
2. Connecter Koyeb
3. Ajouter variables env
4. Deploy!
```

## 📚 Par où commencer?

**Si tu es pressé:** → **QUICKSTART.md**
**Installation détaillée:** → **INSTALLATION.md**
**Déploiement:** → **DEPLOYMENT_CHECKLIST.md**
**API complète:** → **README.md**
**Frontend React:** → **FRONTEND_SETUP.md**

## 🎯 Architecture

```
┌─────────────────────────────────────────────┐
│         TELEGRAM (Bot Aiogram)              │
│   /start, /about, /ref, /help + Webhook   │
└────────────────┬────────────────────────────┘
                 │
                 ├─ InitData (authentication)
                 │
┌────────────────▼────────────────────────────┐
│        FASTAPI BACKEND (Koyeb)              │
│  ✓ Auth JWT                                 │
│  ✓ User Management                          │
│  ✓ Coupons                                  │
│  ✓ Leaderboard + Referral                  │
│  ✓ Admin Panel                              │
└────────────────┬────────────────────────────┘
                 │
                 └─ PostgreSQL (Neon)
                    Users, Coupons, Usage
                 
┌────────────────┬────────────────────────────┐
│    REACT FRONTEND (Vercel)                  │
│    https://clubjm.vercel.app                │
│  Receives API token → Displays everything   │
└─────────────────────────────────────────────┘
```

## 🔑 Prérequis

✅ Python 3.9+
✅ PostgreSQL (ou Neon account)
✅ Bot Telegram créé
✅ GitHub (pour Koyeb)
✅ Koyeb account (gratuit)
✅ Neon account (gratuit)

## ⚙️ Variables d'environnement à avoir

```
DATABASE_URL              # Neon PostgreSQL
TELEGRAM_BOT_TOKEN        # BotFather token
TELEGRAM_WEBHOOK_SECRET   # Random secret
JWT_SECRET                # Random secret
FRONTEND_URL              # https://clubjm.vercel.app
TELEGRAM_CHANNEL_ID       # -1002632653839
DEBUG                     # False (production)
```

## 🎮 Fonctionnalités incluses

✅ Authentification Telegram (InitData)
✅ JWT tokens (30 jours)
✅ Système de classe (Starter → Master)
✅ Système de parrainage (referral)
✅ Coupons avec classe minimum
✅ Historique utilisateur
✅ Leaderboard (top 100)
✅ VIP management
✅ Admin panel complet
✅ Recherche utilisateur
✅ Statistics

## 📊 API Endpoints

**Public:**
- `POST /api/auth/telegram` - Se connecter

**User (token required):**
- `GET /api/me` - Profil
- `GET /api/coupons` - Coupons
- `GET /api/coupons/history` - Historique
- `GET /api/leaderboard` - Classement
- `GET /api/referees` - Mes filleuls
- `GET /api/vip` - Info VIP

**Admin (is_admin required):**
- `POST /api/admin/coupons` - Créer coupon
- `GET /api/admin/coupons` - Liste coupons
- `GET /api/admin/users` - Liste users
- `PATCH /api/admin/users/{id}` - Modifier user
- `GET /api/admin/stats` - Stats

## 🤖 Commands Bot

```
/start      Menu principal
/about      À propos de Club JM
/ref        Mon lien de parrainage
/help       Aide
```

## 📋 Fichiers expliqués

```
clubjm-backend/
├── main.py              # Point d'entrée FastAPI
├── requirements.txt     # Dépendances pip
├── .env.example        # Variables template
├── Dockerfile          # Image Docker
├── docker-compose.yml  # Dev avec BD locale
├── start.sh            # Script de démarrage
│
├── 📖 DOCUMENTATION
│   ├── 00-LIRE-DABORD.md (ce fichier)
│   ├── QUICKSTART.md
│   ├── INSTALLATION.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── README.md
│   └── FRONTEND_SETUP.md
│
└── app/
    ├── main.py           # Entry point
    ├── __init__.py       # Package init
    ├── config.py         # Configuration
    ├── database.py       # SQLAlchemy setup
    ├── models.py         # ORM models (User, Coupon, etc.)
    ├── schemas.py        # Pydantic schemas
    ├── auth.py           # JWT + Telegram auth
    ├── crud.py           # Database operations
    ├── api.py            # Routes FastAPI
    └── bot.py            # Handlers Aiogram
```

## ⚡ Démarrage rapide (5 min)

```bash
# 1. Setup
unzip clubjm-backend.zip
cd clubjm-backend
cp .env.example .env

# 2. Éditer .env (remplir variables)
nano .env

# 3. Installer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Tester
python main.py

# 5. Vérifier
curl http://localhost:8000/health
# Réponse: {"status": "ok"}

# 6. GitHub
git init
git add .
git commit -m "Initial"
git push...

# 7. Koyeb → Deploy!
```

## 🐛 Problèmes courants

| Problème | Solution |
|----------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Connection refused | Backend pas accessible |
| CORS error | Vérifier FRONTEND_URL |
| Invalid token | JWT_SECRET incorrect |
| DB connection error | DATABASE_URL incorrect |

## 🔒 Sécurité

- ✅ Tokens JWT (30 jours)
- ✅ InitData Telegram validé
- ✅ CORS configuré
- ✅ Admin-only endpoints
- ✅ HTTPS en production
- ✅ Pas de secrets en git

## 📞 Support

- Telegram: @JMDAVEKKKK
- Documentation: Lire les .md
- Erreurs: Vérifier les logs

## ✅ Checklist avant production

- [ ] `.env` rempli correctement
- [ ] Neon BD accessible
- [ ] Bot Telegram créé
- [ ] Test local: `python main.py`
- [ ] GitHub repo créé
- [ ] Koyeb account créé
- [ ] Déploiement Koyeb réussi
- [ ] Variables env sur Koyeb
- [ ] Frontend VITE_API_BASE_URL configuré
- [ ] Bot teste dans Telegram

## 🎉 Prêt?

1. **Ouvre QUICKSTART.md**
2. **Suis les étapes**
3. **Déploie sur Koyeb**
4. **Teste le bot Telegram**
5. **C'est en prod!** 🚀

---

**Questions?** Lire la documentation ou contacter @JMDAVEKKKK sur Telegram.

**Bon codage!** ✨
