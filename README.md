- [Wine Review API](#wine-review-api)
    - [A propos du dataset](#a-propos-du-dataset)
    - [La stack technique](#la-stack-technique)
        - [Pourquoi MongoDB ?](#pourquoi-mongodb-)
    - [Installation](#installation)
        - [Prérequis](#prérequis)
        - [Cloner le repository](#cloner-le-repository)
        - [Lancement de l'application](#lancement-de-lapplication)
        - [Arrêter l’application](#arrêter-lapplication)
    - [Documentation](#documentation)
    - [Annexes](#annexes)
        - [Description des champs](#description-des-champs)
        - [Champs ayant une valeur nulle](#champs-ayant-une-valeur-nulle)
        - [Json Schema](#json-schema)

# Wine Review API

**Wine Review API** fournit des données et des scores qualifiés sur les vins du monde entier. Les données proviennent de [Kaggle](https://www.kaggle.com/datasets/zynicide/wine-reviews) et ont été collectées en juin 2017 grâce au **webscraping** du site WineEnthusiast. L'API permet de réaliser des opérations standards telles que la création, la lecture, la mise à jour et la suppression, ainsi que des recherches simples sur les prix et les notes.

## À propos du dataset

Le dataset obtenu contient trois fichiers :

- `winemag-data-130k-v2.csv` contient 10 colonnes et 130 000 lignes de critiques de vins.
- `winemag-data_first150k.csv` contient 10 colonnes et 150 000 lignes d'évaluations de vins.
- `winemag-data-130k-v2.json` contient 6 919 noeuds de critiques de vin.

La version 2 des données est la plus récente. Elle est proposée aux formats `JSON` et `CSV`.

Pour le projet, nous avons choisi le format `JSON`.

## La stack technique

- FastAPI
- MongoDB
- Docker et Docker Compose

### Pourquoi MongoDB ?

Comme mentionné précédemment, les données proviennent d'un `webscraping` du site **WineEnthusiast**. Nous n'avons donc aucune garantie quant à un schéma strict pour ces données. En effet, le site web va évoluer, avoir de nouvelles pages et de nouvelles fonctionnalités. Si nous voulons utiliser ces nouvelles fonctionnalités, il faudra peut-être mettre à jour le schéma de notre base de données.

Pour ce cas d'utilisation, une base de données de type document comme **MongoDB** est appropriée. Les documents d'une collection Mongo sont sans schéma et sans relation entre eux. Cela signifie que nous pouvons introduire de nouveaux champs à tout moment sans avoir besoin de réviser le schéma de notre table au préalable, ce qui nous permet d'itérer plus rapidement.

## Installation

### Prérequis

Pour disposer des dernières versions, il est nécessaire d'installer ou de mettre à jour `docker` et `docker-compose`.

### Cloner le repository

Exécutez la commande suivante pour cloner le repository :

`$>git clone <https://github.com/dinh/wineapp.git`>

### Lancement de l'application

Allez dans le répertoire racine et exécutez la commande suivante pour lancer l'application :

```
$>cd wineapp
$>docker-compose up -d

```

💡 Les données sont importées au démarrage. Si la base de données existe, l'import est annulé.

### Arrêter l'application

Pour arrêter l'application, entrez la commande suivante dans la ligne de commande :

`$>docker-compose down`

## Documentation

La documentation interactive de l'API est accessible à l'adresse suivante : `http://127.0.0.1:9090/api/docs`

### /api/reviews

### Pagination

En raison du grand nombre d'enregistrements dans la base de données, l'appel à l'endpoint `/api/reviews` renvoie par défaut les 20 premiers résultats. Il est cependant possible de contrôler le nombre de résultats obtenus avec les paramètres suivants :

- `limit` permet de spécifier le nombre maximal de résultats souhaités.
- `offset` permet d'effectuer un décalage sur l'ensemble des résultats.

Par exemple, la requête ci-dessous affichera les 50 résultats de la deuxième page :

`http://127.0.0.1/api/reviews?offset=2&limit=50`

Pour obtenir tous les enregistrements :

`http://127.0.0.1/api/reviews?limit=0`

### Filtrage

Il est possible de filtrer sur le prix (price) et la note (points) en utilisant les clés de filtrage au format mongodb telles que '$lt', '$gt', '$lte', '$gte', '$eq'.

La requête ci-dessous va retourner tous les vins dont le prix est compris entre 86 et 90 $ :

`http://127.0.0.1:9090/api/reviews?limit=0&price=$gt:86,$lt:90`

La requête suivante va retourner tous les vins ayant obtenu une note supérieure ou égale à 87 et dont le prix est égal à 19 $ :

`http://127.0.0.1:9090/api/reviews?limit=0&offset=1&points=$gte:87&price=$eq:19`
```

## Annexes

### Description des champs

|                       |                                                                                       Description                                                                                      |
|:---------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| country               | Le pays d'origine du vin                                                                                                                                                               |
| description           | Quelques phrases d'un sommelier décrivant le goût, l'odeur, l'aspect, le toucher, etc. du vin                                                                                          |
| designation           | L'appellation : le vignoble de l'établissement vinicole d'où proviennent les raisins qui ont donné naissance au vin                                                                    |
| points                | Le nombre de points que WineEnthusiast a attribués au vin sur une échelle de 1 à 100 (bien qu'ils ne publient des critiques que pour les vins qui reçoivent une note supérieure à 80). |
| price                 | Le coût d'une bouteille de vin                                                                                                                                                         |
| province              | La province ou l'État d'où provient le vin                                                                                                                                             |
| region_1              | La région viticole d'une province ou d'un État (par exemple Napa)                                                                                                                      |
| region_2              | Parfois, des régions plus spécifiques sont spécifiées dans une zone viticole (par exemple Rutherford dans la vallée de Napa), mais cette valeur peut parfois être vide                 |
| taster_name           | Le nom de la personne qui a goûté et évalué le vin                                                                                                                                     |
| taster_twitter_handle | L'identifiant Twitter de la personne qui a goûté et évalué le vin                                                                                                                      |
| title                 | Le titre de la critique du vin, qui contient souvent le millésime si vous souhaitez extraire cette caractéristique                                                                     |
| variety               | Le type de raisin utilisé pour produire le vin (par exemple, Pinot Noir)                                                                                                               |
| winery                | Le nom du domaine producteur de vin                                                                                                                                                    |

### Champs ayant une valeur nulle

Une analyse du fichier`winemag-data-130k-v2.json`avec `jq` permet d’identifier les champs pouvant contenir des valeurs nulles

```bash
$>jq . winemag-data-130k-v2.json | grep -E -i null,$ | sort | uniq -c

63        "country": null,
37465     "designation": null,
8996      "price": null,
63        "province": null,
21247     "region_1": null,
79460     "region_2": null,
26244     "taster_name": null,
31213     "taster_twitter_handle": null,
1         "variety": null,
```

Cela nous permet de créer un JsonSchema pour le dataset. Ce shéma sera utilisé pour générer le modèle `Pydantic`.

### Json Schema

JSON Schema est un format d'échange de données léger qui permet de générer une documentation claire et facile à comprendre. Il facilite ainsi la validation et les tests. Il est utilisé pour décrire la structure et les contraintes de validation des documents JSON. Dans notre cas, nous pourrions l'utiliser pour vérifier si les données scrappées évoluent dans le temps. Nous pouvons également l'utiliser pour générer le schéma Pydantic.

```json
{
  "$schema": "<http://json-schema.org/draft-06/schema#>",
  "$ref": "#/definitions/Wine",
  "definitions": {
    "Wine": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "points": {
          "type": "string",
          "format": "integer"
        },
        "title": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "taster_name": {
          "type": "string"
        },
        "taster_twitter_handle": {
          "type": "string"
        },
        "price": {
          "type": "number"
        },
        "designation": {
          "type": "string"
        },
        "variety": {
          "type": "string"
        },
        "region_1": {
          "type": "string"
        },
        "region_2": {
          "type": "string"
        },
        "province": {
          "type": "string"
        },
        "country": {
          "type": "string"
        },
        "winery": {
          "type": "string"
        }
      },
      "required": [
        "description",
        "points",
        "title",
        "winery"
      ],
      "title": "Wine"
    }
  }
}
```
