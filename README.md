# SPORT LIVE — version finale (gratuite)

Site statique en français, thème sombre, responsive, avec résultats, classements et calendriers de :
- La Liga (API-Football, identifiant 140)
- Ligue 1 (API-Football, identifiant 61)
- Premier League (API-Football, identifiant 39)
- NBA (API-Basketball, identifiant 12)

Les données sont stockées dans `data/sports.json`. Le navigateur ne voit jamais la clé API.

## Source et limites
Le projet utilise API-SPORTS / API-Football et API-Basketball. Les offres gratuites annoncées comprennent 100 requêtes par jour pour chaque API, sous réserve de disponibilité/couverture de la saison demandée. Le script effectue environ 6 appels football + 2 appels basketball par synchronisation quotidienne. Les flux sont des données sportives de fournisseur tiers, pas une garantie contractuelle de données officielles.
Documentation : https://www.api-football.com/documentation_v3
Basketball : https://api-sports.io/documentation/basketball/basketball-v1.yaml
Tarifs : https://www.api-football.com/ et https://api-sports.io/sports/basketball

## Configuration nécessaire (à faire une fois)
1. Créer un compte gratuit sur https://dashboard.api-football.com/ (pas de carte bancaire annoncée pour le plan gratuit).
2. Copier la clé API-SPORTS depuis le tableau de bord.
3. Créer un dépôt GitHub et y envoyer tous les fichiers de ce dossier.
4. Dans GitHub : Settings → Secrets and variables → Actions → New repository secret.
   - Nom : `APISPORTS_KEY`
   - Valeur : la clé API-SPORTS (ne jamais la mettre dans `index.html`).
5. Dans GitHub : Settings → Pages → Build and deployment → Deploy from a branch → `main` → `/ (root)` → Save.
6. Dans Actions, ouvrir « SPORT LIVE — actualisation quotidienne à 7 h (Paris) » puis lancer « Run workflow » avec `force=true` pour faire le premier remplissage immédiat.

## Actualisation à 7 h heure de Paris
GitHub Actions déclenche le workflow à 05:00 et 06:00 UTC. Le script vérifie l'heure `Europe/Paris` et ne travaille que pendant la fenêtre 07:00–07:19 locale. Cela gère automatiquement le passage heure d'hiver/heure d'été. Les tâches cron de GitHub peuvent toutefois être retardées par la plateforme ; 7 h est donc l'heure programmée, pas une garantie à la minute près.
Le site affiche l'heure de la dernière synchronisation. Le bouton « Actualiser » recharge les données déjà publiées ; il ne lance pas un appel API depuis le navigateur.

## Tester en local
Ouvrir `index.html` avec un serveur statique local après avoir généré `data/sports.json` avec `APISPORTS_KEY` définie. Le fichier de données vide fourni au départ est volontairement sans faux scores.
