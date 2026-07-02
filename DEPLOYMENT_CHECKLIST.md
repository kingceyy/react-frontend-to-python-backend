# ✅ Checklist de Déploiement - Club JM

## 📝 Avant de déployer

### Neon PostgreSQL
- [ ] Créer un projet Neon sur https://console.neon.tech
- [ ] Copier la DATABASE_URL complète
- [ ] Tester la connexion localement avec `psql`

### Telegram Bot
- [ ] Créer un bot via @BotFather
- [ ] Copier le TELEGRAM_BOT_TOKEN
- [ ] Générer une clé JWT secrète: `openssl rand -base64 32`
- [ ] Générer une clé webhook: `openssl rand -base64 32`

### GitHub
- [ ] Créer un repo GitHub privé
- [ ] Pousser le code du backend
- [ ] Ajouter `.env` à `.gitignore`

### Vercel (Frontend)
- [ ] Frontend déjà déployé sur https://clubjm.vercel.app
- [ ] Prêt à ajouter `VITE_API_BASE_URL`

## 🔧 Configuration locale

```bash
# 1. Cloner et préparer
unzip clubjm-backend.zip
cd clubjm-backend
python -m venv venv
source venv/bin/activate

# 2. Créer .env
cp .env.example .env
# Éditer .env avec vos valeurs

# 3. Tester localement
pip install -r requirements.txt
python main.py

# 4. Vérifier /health
curl http://localhost:8000/health
```

## 🚀 Déploiement sur Koyeb

### Étape 1: GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USER/clubjm-backend.git
git push -u origin main
```

### Étape 2: Koyeb
- [ ] Créer compte sur https://app.koyeb.com
- [ ] Connecter GitHub (Settings → Connected Services)
- [ ] Create Web Service → GitHub → clubjm-backend
- [ ] Branche: `main`
- [ ] Builder: Buildpack
- [ ] Run command: `uvicorn main:app --host 0.0.0.0 --port 8000`
- [ ] HTTP Port: `8000`

### Étape 3: Variables d'environnement Koyeb

Ajouter dans Koyeb App Settings:

```
DATABASE_URL=postgresql://...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_WEBHOOK_SECRET=...
JWT_SECRET=...
FRONTEND_URL=https://clubjm.vercel.app
TELEGRAM_CHANNEL_ID=-1002632653839
DEBUG=False
```

### Étape 4: Déployer
- [ ] Cliquer **Deploy**
- [ ] Attendre build (2-3 min)
- [ ] Vérifier logs pour erreurs
- [ ] Copier l'URL Koyeb: `https://xxx.koyeb.app`

## ✅ Après déploiement

### Vérifications

```bash
# 1. Health check
curl https://your-koyeb-backend.app/health
# Réponse attendue: {"status": "ok"}

# 2. Logs
koyeb service logs --name clubjm-backend

# 3. Admin panel
# Modifier un utilisateur en admin via SQL:
# UPDATE users SET is_admin = TRUE WHERE telegram_id = YOUR_ID;
```

### Configurer Frontend

Sur Vercel:
1. Aller dans Settings → Environment Variables
2. Ajouter: `VITE_API_BASE_URL=https://your-koyeb-backend.app`
3. Redéployer

### Tester le Bot

1. Ouvrir Telegram
2. Chercher votre bot
3. Cliquer /start
4. Cliquer "🎮 Ouvrir l'app"
5. Vérifier que ça charge

## 🔐 Sécurité

- [ ] `DEBUG=False` en production
- [ ] JWT_SECRET changé (pas la valeur par défaut)
- [ ] DATABASE_URL sécurisée (jamais en .env public)
- [ ] CORS configuré correctement
- [ ] Webhook secret configuré
- [ ] Admin users définis

## 📊 Monitoring

### Logs Koyeb
```bash
koyeb service logs --name clubjm-backend --follow
```

### Erreurs courants

| Erreur | Solution |
|--------|----------|
| `Connection refused` | Vérifier Koyeb déployé |
| `Database error` | Vérifier DATABASE_URL |
| `Invalid token` | Vérifier JWT_SECRET |
| `CORS error` | Vérifier FRONTEND_URL |

## 🎯 Fonctionnalités à tester

### Auth
- [ ] `/api/auth/telegram` - Se connecter
- [ ] Token JWT reçu
- [ ] Token envoyé dans Authorization header

### User
- [ ] `GET /api/me` - Profil charge
- [ ] Coupons affichent
- [ ] Historique visible
- [ ] Leaderboard load

### Referral
- [ ] Link de parrainage copie
- [ ] /ref command fonctionne
- [ ] Nouveau user via lien compte

### Admin
- [ ] Créer coupon fonctionne
- [ ] Modifier user fonctionne
- [ ] Stats affichent
- [ ] Recherche user fonctionne

### Bot
- [ ] /start affiche menu
- [ ] /about affiche infos
- [ ] /ref affiche lien
- [ ] /help affiche aide
- [ ] Boutons travaillent

## 🎉 Prêt!

Si tout est ✅, votre backend est prêt! 🚀

**URL de production:** `https://your-koyeb-backend.app`

Partagez le bot avec les utilisateurs!

## 📞 Support

- Documentation: README.md
- Installation: INSTALLATION.md
- Frontend: FRONTEND_SETUP.md
- Issues: GitHub
