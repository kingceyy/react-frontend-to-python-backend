# 🚀 Guide d'Installation Complete - Club JM Backend

## 📋 Prérequis

- Python 3.9+
- PostgreSQL (ou accès Neon)
- Bot Telegram créé via @BotFather
- Git + GitHub (pour Koyeb)

## 🔧 Installation Locale

### 1. Cloner/Extraire le projet

```bash
unzip clubjm-backend.zip
cd clubjm-backend
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration Neon

Aller sur https://console.neon.tech et:

1. Créer un projet
2. Copier la connexion string PostgreSQL
3. Créer `.env`:

```bash
cp .env.example .env
```

Éditer `.env`:

```
DATABASE_URL=postgresql://neondb_owner:npg_WLh3ayUgxem5@ep-shiny-brook-ah4p4kz1-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_WEBHOOK_SECRET=random_secret_string
JWT_SECRET=openssl rand -base64 32
FRONTEND_URL=https://clubjm.vercel.app
TELEGRAM_CHANNEL_ID=-1002632653839
DEBUG=False
```

### 5. Démarrer le serveur

```bash
python main.py
```

Ou avec auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Tester: http://localhost:8000/health

## 🐳 Déploiement Koyeb

### 1. Préparer GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/clubjm-backend.git
git push -u origin main
```

### 2. Créer un compte Koyeb

https://app.koyeb.com

### 3. Connecter GitHub

1. Aller dans **Settings** → **Connected Services**
2. Connecter GitHub
3. Autoriser Koyeb

### 4. Créer une App

1. Cliquer **Create Web Service**
2. Sélectionner **GitHub**
3. Choisir le repo `clubjm-backend`
4. Branche: `main`

### 5. Configuration Service

**Build Settings:**
- Builder: `Buildpack`
- Root path: `/`

**Runtime Settings:**
- HTTP Port: `8000`
- Run command:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6. Variables d'environnement

Dans Koyeb, ajouter ces variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Neon string |
| `TELEGRAM_BOT_TOKEN` | Your bot token |
| `TELEGRAM_WEBHOOK_SECRET` | Random string |
| `JWT_SECRET` | `openssl rand -base64 32` |
| `FRONTEND_URL` | `https://clubjm.vercel.app` |
| `TELEGRAM_CHANNEL_ID` | `-1002632653839` |
| `DEBUG` | `False` |

### 7. Déployer

Cliquer **Deploy**. Koyeb va:
1. Cloner le repo
2. Installer les dépendances
3. Lancer le serveur

Attendre 2-3 minutes...

### 8. Copier l'URL de Koyeb

Une fois déployé, vous aurez une URL comme:
```
https://clubjm-backend-xxx.koyeb.app
```

## 🤖 Configuration Telegram Bot

### 1. Créer le bot

Aller sur Telegram et contacter @BotFather:
```
/newbot
Nom: Club JM
Username: clubjm_bot (doit être unique)
```

Copier le TOKEN.

### 2. Configurer le Webhook (optionnel)

Si vous utilisez le Webhook (pour les webhooks Telegram):

```bash
curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook \
  -d url=https://your-koyeb-url.app/webhook \
  -d secret_token=your_webhook_secret
```

Ou laisser en mode polling (le bot vérifie périodiquement).

## 🔗 Connecter le Frontend

### Configurer Vercel

1. Aller dans https://clubjm.vercel.app (settings)
2. Ajouter variable d'environnement:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://your-koyeb-backend.app`

3. Redéployer

### Vérifier la connexion

1. Ouvrir le bot Telegram
2. Cliquer "/start"
3. Cliquer "🎮 Ouvrir l'app"
4. Vérifier que ça charge les coupons, leaderboard, etc.

## 📱 Tester le Bot

### Commandes disponibles

```
/start      - Affiche le menu principal
/about      - À propos de Club JM
/ref        - Mon lien de parrainage
/help       - Aide
```

### Tester localement

Ouvrir https://web.telegram.org et:
1. Chercher votre bot
2. Cliquer /start
3. Cliquer sur le bouton "🎮 Ouvrir l'app"

## 🛠️ Dépannage

### "Connection refused"

Backend pas accessible. Vérifier:
- Koyeb déployé et running
- Firewall permettant les connexions
- Port 8000 ouvert

### "Database connection error"

BD inaccessible. Vérifier:
- `DATABASE_URL` correct
- Neon accessible
- Firewall Neon configuré

### "Invalid InitData"

Token Telegram invalide. Vérifier:
- `TELEGRAM_BOT_TOKEN` correct
- InitData valide (timestamp pas trop ancien)

### "CORS error"

Frontend n'a pas accès à l'API. Vérifier:
- `FRONTEND_URL` correct dans backend .env
- CORS middleware configuré
- URL Frontend correspond

## 📊 Monitoring

### Logs Koyeb

```bash
koyeb service logs --name clubjm-backend --follow
```

### Vérifier la santé

```bash
curl https://your-koyeb-backend.app/health
```

Réponse attendue:
```json
{"status": "ok"}
```

## 🔐 Sécurité

- ✅ JWT tokens pour l'authentification
- ✅ CORS configuré
- ✅ InitData Telegram validé
- ✅ Admin-only endpoints protégés
- ✅ HTTPS en production

## 📝 Prochaines étapes

1. **Ajouter des utilisateurs admin** via base de données:

```python
# À faire via Django shell ou script
UPDATE users SET is_admin = TRUE WHERE telegram_id = YOUR_ID;
```

2. **Configurer VIP channel** dans `bot.py`

3. **Ajouter le webhook Telegram** pour les mises à jour en temps réel

4. **Monitorer les logs** Koyeb

## 📞 Support

- Telegram: https://t.me/JMDAVEKKKK
- GitHub Issues: Pour les bugs
- Neon Support: Pour les problèmes BD

## 🎉 Succès!

Si vous voyez:
1. ✅ Bot répond à /start
2. ✅ Mini app s'ouvre
3. ✅ Les données chargent
4. ✅ Leaderboard visible
5. ✅ Coupons visibles

Alors c'est bon! 🚀
