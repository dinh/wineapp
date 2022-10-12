# README.md

- [README.md](#readmemd)
- [Wine Review API](#wine-review-api)
    - [A propos du dataset](#a-propos-du-dataset)
    - [La stack technique](#la-stack-technique)
        - [Pourquoi MongoDB ?](#pourquoi-mongodb-)
    - [Installation](#installation)
        - [Lancer l'application](#lancer-lapplication)
    - [Documentation](#documentation)
    - [Annexes](#annexes)
        - [Description des champs](#description-des-champs)
        - [Champs ayant une valeur nulle](#champs-ayant-une-valeur-nulle)
        - [JsonSchema](#jsonschema)


# Wine Review API

**Wine Review API** fournit des données et des scores qualifiés sur les vins du monde entier.

Les données proviennent de [Kaggle](https://www.kaggle.com/datasets/zynicide/wine-reviews) et sont issues d’un `webscraping` du site **WineEnthusiast** en juin 2017. L'API permet les faire des opérations standards telles que la création, la lecture, la mise à jour et la suppression. Elle permet également de faire des recherches par titre et par score.

## A propos du dataset

Le dataset obtenu contient trois fichiers :

- `winemag-data-130k-v2.csv` contient 10 colonnes et 130k lignes de critiques de vins.
- `winemag-data_first150k.csv` contient 10 colonnes et 150k lignes d'évaluations de vins.
- `winemag-data-130k-v2.json` contient 6919 noeuds de critiques de vin.

La version 2 des données est la plus récente . Elle est proposée aux formats `JSON` et `CSV`.

Pour le projet, nous avons choisi le format `JSON.`

## La stack technique

- FastAPI
- MongoDB
- Docker et Docker Compose

### Pourquoi MongoDB ?

Comme il a été précisé précédemment, les données sont issues d’un `webscraping`  du site **WineEnthusiast**. ****Nous n’avons donc aucune garantie d’un schéma strict pour ces données. En effet, le site web va évoluer, avoir de nouvelles pages, de nouvelles fonctionnalités. Si nous voulons suivre l'utilisation de ces nouvelles fonctionnalités, vous devons peut-être mettre à jour le schéma de notre base de données.

Pour ce cas d’usage, une base de données de type document comme **MongoDB** est appropriée. Les documents d'une collection Mongo sont sans schéma et n'ont aucune relation entre eux. Cela signifie que nous pouvons introduire de nouveaux champs à tout moment sans avoir besoin de réviser votre schéma de table au préalable, ce qui vous permet d'itérer plus rapidement.

## Installation

- Installer ou mettre à jour Docker et Docker Compose pour disposer des dernières versions
- Cloner le repo

### Lancer l'application

- Aller dans le répertoire racine et exécuter `docker-compose up -d`
-
- Pour arrêter, taper `docker-compose down`

## Documentation

La documentation de l'API est accessible à l'adresse suivante: `http://127.0.0.1:9090/docs`

## Annexes

### Description des champs

|  | Description |
| --- | --- |
| country  | Pays de provenance du vin |
| description |  Quelques phrases d'un sommelier décrivant le goût, l'odeur, l'aspect, le toucher, etc. du vin |
| designation  | Appellation : Le vignoble de l'établissement vinicole d'où proviennent les raisins qui ont donné naissance au vin |
| points | Le nombre de points que WineEnthusiast a attribué au vin sur une échelle de 1 à 100 (bien qu'ils disent qu'ils ne publient des critiques que pour les vins qui obtiennent une note supérieure à 80). |
| price  |  Le coût d'une bouteille de vin |
| province  | La province ou l'état d'où provient le vin |
| region_1 | La région viticole d'une province ou d'un état (par exemple Napa) |
| region_2 | Parfois, des régions plus spécifiques sont spécifiées dans une zone viticole (par exemple Rutherford dans la vallée de Napa), mais cette valeur peut parfois être vide |
| taster_name | Nom de la personne qui a goûté et évalué le vin. |
| taster_twitter_handle | Identifiant Twitter de la personne qui a dégusté et évalué le vin |
| title | Le titre de la critique du vin, qui contient souvent le millésime si vous souhaitez extraire cette caractéristique |
| variety | e type de raisin utilisé pour produire le vin (par exemple, Pinot Noir) |
| winery |  |

### Champs ayant une valeur nulle

Une analyse du fichier`winemag-data-130k-v2.json`avec `jq` permet d’identifier les champs pouvant contenir des valeurs nulles

```
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

Cela nous permet de créer un JsonSchema pour le dataset et nous permet de définir le modèle `Pydantic`

### JsonSchema

```bash
{
    "$schema": "http://json-schema.org/draft-06/schema#",
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