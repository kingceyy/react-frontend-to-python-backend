# Configuration Frontend

Ce guide explique comment configurer le frontend React pour se connecter au backend.

## 1. Supprimer les données mock

Dans le frontend, modifier `src/lib/api.ts`:

```typescript
// Remplacer isMockMode() pour ne pas utiliser les mocks en production
function isMockMode(): boolean {
  if (!BASE_URL) return true;
  // En production, toujours false
  return false;
}
```

## 2. Configurer la variable d'environnement

Créer/mettre à jour `.env.production`:

```
VITE_API_BASE_URL=https://your-koyeb-backend.app
```

Pour le développement local:

```
VITE_API_BASE_URL=http://localhost:8000
```

## 3. Variable VITE_API_BASE_URL

Le frontend utilise `VITE_API_BASE_URL` pour la base API. Par défaut:

```typescript
const BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");
```

## 4. Frontend React

Le frontend utilise déjà la bonne structure:

- `src/lib/api.ts` - Appels API (à adapter)
- `src/lib/auth-context.tsx` - Contexte d'authentification
- `src/lib/telegram.ts` - Intégration Telegram

Tous les endpoints du backend sont déjà mappés dans `ENDPOINTS`.

## 5. Déploiement sur Vercel

```bash
vercel env add VITE_API_BASE_URL
# Entrer: https://your-koyeb-backend.app
```

## 6. Vérifier la connexion

Une fois déployé:

1. Ouvrir le bot Telegram
2. Cliquer sur "🎮 Ouvrir l'app"
3. Vérifier que les données se chargent depuis le backend

## Endpoints disponibles

Tous les endpoints du backend sont:

- `POST /api/auth/telegram` - Auth
- `GET /api/me` - Profil
- `GET /api/coupons` - Coupons
- `GET /api/coupons/history` - Historique
- `GET /api/leaderboard` - Classement
- `GET /api/referees` - Filleuls
- `GET /api/vip` - VIP info
- `POST /api/admin/*` - Admin APIs

Le frontend utilise déjà tous ces endpoints via `api.*()`.

## Dépannage

**"API call failed"**
- Vérifier `VITE_API_BASE_URL`
- Vérifier les CORS sur le backend
- Vérifier que le backend est accessible

**"Invalid token"**
- Vérifier que `JWT_SECRET` est le même frontend/backend
- Vérifier que le token est bien envoyé

**"Database connection error"**
- Vérifier `DATABASE_URL` sur Koyeb
- Vérifier que la BD Neon est accessible
