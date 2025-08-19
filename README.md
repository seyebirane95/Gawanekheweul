# Django E-commerce Starter

Un squelette minimal d'une boutique en ligne (catalogue, panier, commande) en **Django**.

## Lancer en local

```bash
cd django_ecommerce_starter
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # pensez à changer SECRET_KEY
python manage.py migrate
python manage.py createsuperuser  # pour accéder à /admin
python manage.py runserver
```

Ouvrez http://127.0.0.1:8000

## Ajouter des produits
- Allez sur `/admin` et créez d'abord des **Categories**, puis des **Products**.

## Déploiement (piste rapide)
- **Render** ou **Railway**: créez un service web, `Python 3.11`, commande `web: gunicorn config.wsgi`.
- Ajoutez les variables d'environnement de `.env.example`.
- Configurez un **nom de domaine** et HTTPS.
- Pour des fichiers statiques, WhiteNoise est déjà activé.

## Stripe (à brancher plus tard)
- Créez un compte Stripe et récupérez `STRIPE_PUBLIC_KEY` et `STRIPE_SECRET_KEY`.
- Implémentez un `Checkout Session` côté serveur dans `orders/views.py` (TODO).

## Structure
- `core`: pages d'accueil et à propos
- `products`: catalogue (Category, Product)
- `cart`: panier via sessions
- `orders`: commandes (Order, OrderItem), checkout simulé

Bon build !
