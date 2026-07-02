# 🚀 COMMENCER ICI - Club JM Bot

Bienvenue! Tu as un monorepo complet avec Backend + Frontend.

## 📦 Étape 1: Télécharger le ZIP

1. En haut à droite, clique les **3 points** (•••)
2. Clique **Download ZIP**
3. Attends que le ZIP se télécharge (~71 KB)

## 🗂️ Étape 2: Extraire le ZIP

```bash
# Sur Mac/Linux:
unzip clubjm-monorepo.zip
cd clubjm

# Sur Windows:
# - Clic droit sur clubjm-monorepo.zip
# - "Extraire tout..."
# - Ouvrir le dossier clubjm
```

## 📖 Étape 3: Lire les guides (TRÈS IMPORTANT!)

Ouvre les fichiers dans cet ordre:

### 🟢 Si tu veux juste déployer rapidement:

1. **README.md** ← Commence ici! (5 min)
2. **SETUP.md** ← Instructions étape par étape (10 min)
3. **backend/QUICKSTART.md** ← Setup backend rapide

### 🔵 Si tu veux tous les détails:

1. **README.md** - Vue d'ensemble
2. **SETUP.md** - Instructions complètes
3. **backend/INSTALLATION.md** - Installation détaillée backend
4. **backend/DEPLOYMENT_CHECKLIST.md** - Checklist complet
5. **GITHUB_WEB_UPLOAD.md** - Créer repo GitHub

### 🟠 Guides par sujet:

- **GitHub:** `GITHUB_WEB_UPLOAD.md` (FACILE!) ou `GITHUB_SETUP.md` (Terminal)
- **Koyeb:** `backend/DEPLOYMENT_CHECKLIST.md`
- **Vercel:** `SETUP.md` section "Frontend"
- **Frontend React:** `frontend/README.md`

## 🔑 Étape 4: Créer repo GitHub

### Option A: Web (PLUS FACILE - recommandé!)

Voir: `GITHUB_WEB_UPLOAD.md`

Résumé rapide:
1. Aller https://github.com/new
2. Créer repo `clubjm` (vide)
3. Cliquer "uploading an existing file"
4. Drag & drop le ZIP
5. GitHub décompresse automatiquement! ✨

### Option B: Terminal

Voir: `GITHUB_SETUP.md`

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/clubjm.git
git push -u origin main
```

## ⚙️ Étape 5: Configurer

```bash
# Backend
cd backend
cp .env.example .env
# Éditer .env avec tes variables (Database, Bot Token, etc)

# Frontend
cd ../frontend
cp .env.example .env.local
# Éditer .env.local avec API_BASE_URL
```

## 🚀 Étape 6: Déployer

Voir: `SETUP.md` pour instructions complètes

**Backend sur Koyeb:**
1. https://koyeb.com
2. Connecter GitHub repo
3. Select: clubjm repo, root: `backend/`
4. Build: `pip install -r requirements.txt`
5. Run: `python main.py`
6. Ajouter env vars
7. Deploy!

**Frontend sur Vercel:**
1. https://vercel.com
2. Connecter GitHub repo
3. Root directory: `frontend/`
4. Build: `npm run build`
5. Ajouter VITE_API_BASE_URL
6. Deploy!

## 📁 Structure du projet

```
clubjm/
├── README.md               ← Lire en premier
├── SETUP.md                ← Instructions détaillées
├── GITHUB_WEB_UPLOAD.md    ← Créer repo (facile)
├── GITHUB_SETUP.md         ← Créer repo (terminal)
│
├── backend/                ← FastAPI + Aiogram Bot
│   ├── main.py             ← Point d'entrée
│   ├── requirements.txt     ← Dépendances Python
│   ├── .env.example        ← Configuration (copier à .env)
│   ├── Dockerfile          ← Pour Koyeb
│   ├── QUICKSTART.md       ← Setup rapide
│   ├── INSTALLATION.md     ← Installation détaillée
│   ├── DEPLOYMENT_CHECKLIST.md ← Checklist production
│   └── app/                ← Code Python
│       ├── models.py       ← Database models
│       ├── schemas.py      ← Data validation
│       ├── crud.py         ← Database operations
│       ├── api.py          ← API endpoints
│       ├── bot.py          ← Telegram bot
│       ├── auth.py         ← Telegram auth
│       ├── database.py     ← DB connection
│       └── config.py       ← Configuration
│
└── frontend/               ← React + Vite App
    ├── package.json        ← Dependencies
    ├── vite.config.ts      ← Vite config
    ├── .env.example        ← Configuration (copier à .env.local)
    ├── vercel.json         ← Vercel config
    └── src/
        ├── pages/          ← Pages React
        ├── components/     ← Components réutilisables
        ├── lib/            ← Utilities
        └── App.tsx         ← App principal
```

## 🎯 Checklist rapide

- [ ] Téléchargé clubjm-monorepo.zip
- [ ] Extrait le ZIP
- [ ] Créé repo GitHub
- [ ] Poussé le code: `git push`
- [ ] Configuré backend/.env
- [ ] Configuré frontend/.env.local
- [ ] Créé Neon database (PostgreSQL)
- [ ] Créé Telegram Bot Token
- [ ] Déployé Backend sur Koyeb
- [ ] Déployé Frontend sur Vercel
- [ ] Configuré variables d'environnement
- [ ] Testé bot Telegram
- [ ] Vérified web app

## 🔗 Ressources utiles

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Aiogram Docs](https://docs.aiogram.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Neon Docs](https://neon.tech/docs)
- [Koyeb Docs](https://koyeb.com/docs)
- [Vercel Docs](https://vercel.com/docs)

## 💬 Support

- Bot Support: https://t.me/JMDAVEKKKK
- Channel: https://t.me/+gpImJ4tj2BUxMzE0

## ⚡ Pro Tips

1. **Commencer avec SETUP.md** - c'est le plus important
2. **Ne pas commit .env files** - ils contiennent secrets! (.gitignore les ignore déjà)
3. **Tester localement d'abord** - avant de déployer
4. **Garder tokens secrets** - ne jamais les montrer ou commit
5. **Lire les README.md** - vraiment important!

---

**Besoin d'aide?** Lire le fichier correspondant dans le dossier du projet.

**Prêt?** Commençons! 🚀

→ Ouvre maintenant: **README.md**
