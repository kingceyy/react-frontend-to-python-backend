# Guide FACILE: Créer un Repo GitHub (sans terminal!)

Si tu ne veux pas utiliser le terminal, tu peux le faire directement sur GitHub.com!

## Méthode 1: Upload ZIP directement (PLUS FACILE)

### Step 1: Créer le repo vide

1. Aller sur https://github.com/new
2. Remplir:
   - Name: `clubjm`
   - Description: `Bot Telegram Club JM`
   - Public
3. **NE PAS cocher** "Add .gitignore", "Add license", etc. (laisse vide)
4. Cliquer **"Create repository"**

### Step 2: Upload le ZIP

Après avoir créé le repo, tu verras une page avec:

```
Quick setup — if you've done this kind of thing before
```

En bas, tu verras:

```
...or upload an existing file
```

1. Cliquer le lien **"uploading an existing file"**
2. Drag & drop `clubjm-monorepo.zip` (ou cliquer pour sélectionner)
3. GitHub décompresse automatiquement! ✨

Attendre que GitHub traite... Voilà! 🎉

## Méthode 2: Upload fichiers individuels (Plus contrôlé)

### Step 1: Créer le repo

Même que ci-dessus.

### Step 2: Créer la structure

1. Sur la page du repo, cliquer **"Add file" → "Create new file"**
2. Créer les dossiers et fichiers comme tu veux

**Mais c'est très long...** La Méthode 1 est plus rapide!

## Méthode 3: GitHub Desktop (Interface graphique)

Si tu préfères une interface graphique:

1. Télécharger **GitHub Desktop**: https://desktop.github.com
2. Installer et log in avec ton compte GitHub
3. File → Clone Repository → créer repo d'abord
4. Puis ajouter les fichiers localement
5. Commit et Push

## Après upload: Configuration

Une fois le repo créé sur GitHub:

1. **Lire:** README.md (guide d'overview)
2. **Lire:** SETUP.md (instructions complet)
3. **Configurer:**
   - backend/.env.example → ton vrai .env
   - frontend/.env.example → ton vrai .env.local

4. **Déployer:**
   - Backend sur Koyeb (voir SETUP.md)
   - Frontend sur Vercel (voir SETUP.md)

## Troubleshooting

**Le ZIP n'upload pas?**
- Taille max: 25 MB (notre ZIP est 71 KB, pas de problème)
- Vérifier connexion internet

**Fichiers mal décompressés?**
- Télécharger le ZIP localement
- Décompresser: `unzip clubjm-monorepo.zip`
- Puis utiliser Méthode 3 (GitHub Desktop)

**Fichiers en double/mal organisés?**
1. Aller Settings (en haut du repo)
2. Danger Zone → Delete this repository
3. Recommencer proprement

## Structure finale attendue

Après upload, tu dois voir:

```
clubjm/
├── README.md
├── SETUP.md
├── .gitignore
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── .env.example
    └── src/
```

Si structure ressemble à ça → C'est bon! ✅

## Prochaines étapes

1. **Lire SETUP.md** pour instructions détaillées
2. **Créer fichiers .env** (Ne pas commit, ils contiennent secrets!)
3. **Déployer Backend** sur Koyeb
4. **Déployer Frontend** sur Vercel

---

**Questions?** Voir README.md ou SETUP.md
