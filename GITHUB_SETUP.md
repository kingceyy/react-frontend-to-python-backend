# Guide: Créer un Repo GitHub pour Club JM

## Step 1: Créer un nouveau repo

1. Aller sur **https://github.com/new**
2. Remplir les champs:
   - **Repository name:** `clubjm` (ou `clubjm-bot`)
   - **Description:** Bot Telegram Club JM avec Web App React
   - **Public** ou **Private** (ta préférence)
   - **Add .gitignore:** Python
   - **License:** MIT (optionnel)

3. Cliquer **"Create repository"**

## Step 2: Télécharger le ZIP

1. Voir le bouton en haut à droite de cette page: `...` (trois points)
2. Cliquer **"Download ZIP"**
3. Tu auras `clubjm-monorepo.zip`

## Step 3: Extraire et initialiser

```bash
# Extraire
unzip clubjm-monorepo.zip
cd clubjm

# Initialiser Git
git init
git add .
git commit -m "Initial commit: Full stack Club JM Bot"
```

## Step 4: Connecter au repo GitHub

Remplace `YOUR_USERNAME` par ton username GitHub:

```bash
# Ajouter le remote
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/clubjm.git

# Push vers GitHub
git push -u origin main
```

## Step 5: Résultat

Tu devrais voir sur GitHub:

```
clubjm/
├── README.md
├── SETUP.md
├── .gitignore
├── .env.example
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── app/
│       ├── models.py
│       ├── api.py
│       ├── bot.py
│       └── ...
└── frontend/
    ├── package.json
    ├── src/
    ├── public/
    └── ...
```

## Troubleshooting

### Error: "fatal: not a git repository"

```bash
# Réinitialiser Git
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/clubjm.git
git push -u origin main
```

### Error: "Permission denied"

Utiliser SSH au lieu de HTTPS:

```bash
# Générer clé SSH (si tu ne l'as pas)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Ajouter à GitHub Settings → SSH Keys

# Puis utiliser:
git remote set-url origin git@github.com:YOUR_USERNAME/clubjm.git
git push -u origin main
```

### Error: "Authentication failed"

```bash
# Si tu utilises HTTPS, créer un Personal Access Token:
# 1. GitHub Settings → Developer settings → Personal access tokens
# 2. Generate new token (repo scope)
# 3. Utiliser token comme password quand git demande
```

## Prochaines étapes

Une fois le repo créé:

1. **Backend sur Koyeb:** Voir `backend/DEPLOYMENT_CHECKLIST.md`
2. **Frontend sur Vercel:** Voir `frontend/README.md`
3. **Configuration:** Voir `SETUP.md` à la racine

## Commandes Git utiles

```bash
# Voir le status
git status

# Voir les logs
git log --oneline

# Créer une branche feature
git checkout -b feature/ma-feature
git push origin feature/ma-feature

# Merger dans main
git checkout main
git pull origin main
git merge feature/ma-feature
git push origin main
```

---

**Besoin d'aide?** Voir le README.md ou SETUP.md
