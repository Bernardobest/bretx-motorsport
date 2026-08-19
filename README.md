# BretX Motorsport — Site vitrine

Site statique (HTML/CSS/JS, aucun framework) prêt à déployer sur Netlify.

## 1. Mettre le site en ligne (le plus rapide)

**Option A — Sans GitHub (5 minutes) :**
1. Va sur https://app.netlify.com et crée un compte gratuit.
2. Sur la page d'accueil, fais glisser tout le dossier `bretx-motorsport` (celui qui contient `index.html`) dans la zone "Drag and drop your site output folder here".
3. Le site est en ligne immédiatement sur une URL type `random-name-123.netlify.app`. Tu peux la renommer dans Site settings > Change site name.

**Option B — Avec GitHub (recommandé pour pouvoir mettre à jour facilement) :**
1. Crée un nouveau repo sur https://github.com/new (ex: `bretx-motorsport`), sans README ni .gitignore.
2. Dans le dossier du projet, sur ta machine ou ici :
   ```
   git remote add origin https://github.com/TON-COMPTE/bretx-motorsport.git
   git branch -M main
   git push -u origin main
   ```
3. Sur Netlify : "Add new site" > "Import an existing project" > connecte GitHub > choisis le repo. Build command : laisser vide. Publish directory : `.` (racine).
4. Chaque `git push` mettra le site à jour automatiquement.

Un fichier `netlify.toml` est déjà inclus avec la config de base.

## 2. Nom de domaine

Une fois le site en ligne, dans Netlify : Domain settings > Add a domain. Si tu as déjà un nom de domaine (ex: bretx-motorsport.fr), tu peux le connecter là (Netlify te donne les enregistrements DNS à mettre chez ton registrar, ex: OVH, Gandi).

## 3. Calendrier de réservation (Cal.com — gratuit, façon Doctolib)

1. Crée un compte gratuit sur https://cal.com
2. Configure tes disponibilités (jours/horaires où tu peux intervenir).
3. Crée un type d'événement (ex: "Diagnostic & reprogrammation moteur", durée 2h par exemple).
4. Dans Cal.com, active la demande du **numéro de téléphone** comme champ obligatoire (Event type > Advanced > Booking questions), et ajoute un champ texte pour "Véhicule (marque/modèle/année)".
5. Récupère le lien de ton événement (format `ton-pseudo/nom-evenement`).
6. Ouvre `js/main.js`, ligne ~55 :
   ```js
   const CAL_LINK = "bretx-motorsport/reprogrammation-moteur"; // <-- À CONFIGURER
   ```
   Remplace par ton vrai lien Cal.com.
7. Cal.com envoie automatiquement un email de confirmation au client ET à toi à chaque réservation — rien d'autre à configurer.

## 4. Acompte 25% via Stripe

1. Connecte-toi à ton compte Stripe existant : https://dashboard.stripe.com
2. Va dans Payment Links > Créer un lien de paiement.
3. Crée un produit "Acompte réservation à domicile" avec un montant (tu peux faire un lien à montant variable, le client indique le montant demandé, ou plusieurs liens à montants fixes selon tes forfaits).
4. Copie le lien généré (`https://buy.stripe.com/...`).
5. Ouvre `js/main.js`, ligne ~93 :
   ```js
   const STRIPE_LINK = "https://buy.stripe.com/REMPLACER_PAR_TON_LIEN"; // <-- À CONFIGURER
   ```
   Remplace par ton vrai lien.

**Fonctionnement actuel :** le client réserve sur Cal.com, tu confirmes le montant exact de l'acompte par email/téléphone, puis il clique sur le bouton "Verser mon acompte via Stripe" sur le site. Si tu veux automatiser complètement (montant exact déjà pré-rempli selon le véhicule), il faudra passer à une intégration Stripe Checkout sur-mesure — dis-le moi si tu veux qu'on fasse évoluer le site dans cette direction plus tard.

## 5. Formulaire de contact (déjà fonctionnel, aucune config technique requise)

Le formulaire utilise **Netlify Forms**, inclus gratuitement dès que le site est déployé sur Netlify (jusqu'à 100 soumissions/mois gratuites). Rien à configurer côté code.

Pour recevoir les notifications par email à chaque nouveau message :
1. Netlify > ton site > Forms > "contact" > Settings > Add notification > Email notification.
2. Renseigne ton adresse email.

Les messages restent aussi consultables dans Netlify > Forms.

## 6. Adresse email de contact affichée sur le site

Le site affiche actuellement `contact@bretx-motorsport.fr` (placeholder). Remplace-la dans `index.html` (recherche `contact@bretx-motorsport.fr`, 2 occurrences) par ton adresse réelle si différente, ou crée cette adresse via ton hébergeur de domaine / Google Workspace.

## 7. Logo

Le logo fourni est déjà intégré (`img/logo.png`).

## 8. Ce qu'il reste à personnaliser / vérifier avant le lancement

- [ ] Configurer `CAL_LINK` (étape 3)
- [ ] Configurer `STRIPE_LINK` (étape 4)
- [ ] Vérifier/mettre à jour l'adresse email de contact
- [ ] Ajouter les notifications email sur Netlify Forms (étape 5)
- [ ] Remplacer les tarifs "sur devis" par tes prix réels une fois affinés vs concurrence
- [ ] Vérifier que le numéro de téléphone est bien demandé comme champ obligatoire dans Cal.com
- [ ] (Optionnel) Ajouter un vrai nom de domaine
- [ ] (Optionnel) Ajouter des photos réelles de tes interventions/véhicules au fil du temps

## Structure du projet

```
bretx-motorsport/
├── index.html          Page principale
├── success.html         Page de confirmation après envoi du formulaire
├── css/style.css        Toute la charte graphique
├── js/main.js           Menu mobile, animations, embed Cal.com, lien Stripe
├── img/logo.png          Logo BretX Motorsport
└── netlify.toml          Config de déploiement Netlify
```
