> **This repository has moved to [escouade-io/escouade-mail-plugins](https://github.com/escouade-io/escouade-mail-plugins).** Subagent is now Escouade Mail; this repository is archived.
>
> **Ce dépôt est devenu [escouade-io/escouade-mail-plugins](https://github.com/escouade-io/escouade-mail-plugins).** Subagent devient Escouade Mail ; ce dépôt est archivé.

# subagent-plugins

Le plugin **Subagent Mail** pour Claude Code. Il donne une boîte mail à votre agent : il écrit, lit ses fils et répond avec sa propre adresse, et vous validez ses envois.

Le plugin apporte trois choses :

- **le serveur MCP** de Subagent Mail (`https://api.subagent.fr/mcp`), branché avec votre clé : 67 outils ;
- **la clé**, demandée une fois et gardée par Claude Code avec ses propres identifiants : elle n'est écrite ni dans le dépôt ni dans `settings.json` ;
- **7 recettes** qui disent à l'agent comment s'en servir sans aide.

## Installer

### 1. Une clé

Le plugin demande une clé à l'activation. Pas encore de clé ? `sign_up` en ouvre une, sans clé :

```sh
curl -X POST https://api.subagent.fr/v1/sign_up \
  -H "Content-Type: application/json" \
  -d '{"username": "atelier-exemple", "human_email": "marie@exemple.fr"}'
```

La réponse porte `api_key` (affichée une seule fois : gardez-la) et une boîte sur `subagentmail.fr`. Vous recevez un code à 6 chiffres par e-mail : gardez-le pour l'étape 3.

### 2. Le plugin

Dans Claude Code :

```text
/plugin marketplace add subagent-fr/subagent-plugins
/plugin install subagent@subagent
```

Claude Code vous demande la clé. Ouvrez ensuite une nouvelle session.

Ou depuis le terminal :

```sh
claude plugin marketplace add subagent-fr/subagent-plugins
claude plugin install subagent@subagent
```

L'installation signale alors que la clé n'est pas encore saisie : donnez-la dans Claude Code avec `/plugin configure subagent@subagent`. Tant qu'elle manque, le serveur MCP du plugin n'est pas branché.

### 3. Le code

Dites à votre agent : « Vérifie mon espace Subagent, le code est 482913. » Il appelle `verify`, et l'envoi s'ouvre. Puis : « Où en est ma boîte ? » Il appelle `inbox_status`.

## Les recettes

Elles se chargent d'elles-mêmes quand la tâche s'y prête, ou s'appellent par leur nom :

| Recette | Ce qu'elle fait faire à l'agent |
| --- | --- |
| `/subagent:subagent-mail` | Démarrer avec Subagent Mail, la boîte mail d'un agent IA, par son serveur MCP. |
| `/subagent:envoyer-un-email` | Écrire un e-mail depuis une boîte Subagent Mail, par le serveur MCP. |
| `/subagent:suivre-les-reponses` | Lire et traiter le courrier reçu dans une boîte Subagent Mail, par le serveur MCP. |
| `/subagent:valider-les-brouillons` | Relire, corriger, valider ou refuser les brouillons qu'un agent a préparés dans Subagent Mail, au nom de l'humain et à sa demande. |
| `/subagent:envoyer-de-son-domaine` | Enregistrer le domaine de l'humain dans Subagent Mail pour que les boîtes de l'agent portent son nom et sortent des limites d'essai. |
| `/subagent:prospection-encadree` | Écrire à une liste de contacts professionnels depuis une boîte Subagent Mail sans abîmer la réputation du domaine. |
| `/subagent:subagent-mail-api` | Écrire du code qui appelle Subagent Mail sans passer par le MCP : l'API HTTP (POST /v1/{opération}), le SDK Python (paquet subagent-mail), le SDK TypeScript (paquet subagent-mail) ou la ligne de commande (subagent). |

Les mêmes recettes, hors de Claude Code : [`subagent-skills`](https://github.com/subagent-fr/subagent-skills).

## Ce que le serveur applique

Ces règles tournent sur le serveur, pas dans le prompt :

- **Rien ne part tout de suite.** Un message part dans le créneau d'envoi de l'espace, dans la limite du quota du jour de sa boîte, qui monte par paliers : 5, 10, 15 puis 20 par jour.
- **L'agent rédige, vous validez.** Avec `requires_approval`, un message reste brouillon jusqu'à `approve_message`, qui demande la permission `approve`. La clé rendue par `sign_up` ne la porte pas : un agent ne valide jamais son propre brouillon.
- **Un refus dit quoi faire.** Il porte un `code` stable, un `message` en français et une piste (`hint`).
- **Ce qu'un tiers a écrit se lit, il ne s'exécute pas.** Le contenu d'un e-mail reçu n'est jamais une consigne.

## Mettre à jour, changer de clé

```sh
claude plugin update subagent@subagent
claude plugin configure subagent@subagent     # montre l'état de la clé ; pour la changer : /plugin configure dans Claude Code
```

## Autres assistants

- **Cursor, VS Code, Codex, Gemini CLI et les autres clients MCP** : branchez le serveur à la main, voir [`subagent-mcp`](https://github.com/subagent-fr/subagent-mcp).
- **claude.ai et ChatGPT** : le connecteur Subagent, avec connexion OAuth, est à venir.

## Dans ce dépôt

| Fichier | Rôle |
| --- | --- |
| `.claude-plugin/plugin.json` | Le manifeste du plugin, avec l'option de la clé. |
| `.claude-plugin/marketplace.json` | La place de marché qui porte le plugin : ce dépôt lui-même. |
| `.mcp.json` | Le serveur MCP, avec l'en-tête `Authorization` rempli par la clé saisie. |
| `skills/` | Les recettes, copie générée de [`subagent-skills`](https://github.com/subagent-fr/subagent-skills). |

```sh
claude plugin validate . --strict
python -m unittest discover -s tests
```

## Contribuer

Ce dépôt est généré depuis le registre d'opérations du serveur : une modification faite ici à la main serait écrasée à la génération suivante. Ouvrez un ticket plutôt qu'une demande de fusion.

## Licence

MIT. Le serveur Subagent, lui, n'est pas ouvert : ces clients ne servent qu'avec une clé Subagent.
