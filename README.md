# 📄 CV Generator

Un générateur de CV **PDF professionnel** en Python. Décris ton parcours dans un fichier JSON structuré, lance le script, et obtiens un CV formaté d'une page impeccable — prêt à envoyer.

Conçu pour les CVs de finance/conseil au format standard (HEC, Goldman Sachs, McKinsey style) : layout une colonne, deux colonnes titre/date, bullets et sous-bullets.

## ✨ Fonctionnalités

- 📝 **Pilotage par JSON** — contenu 100% séparé du code
- 📏 **Contrainte une page** — le script refuse de générer si le contenu déborde (protection anti-débordement)
- 🔒 **Données personnelles isolées** — un fichier `personal.json` séparé (gitignore) pour ton adresse, email, téléphone
- 🎨 **Layout professionnel** — Times Roman, colonnes alignées, séparateurs horizontaux, bullets/sous-bullets
- ⚡ **Zéro dépendance cloud** — 100% local, aucune API externe

## 🚀 Quick Start

### Prérequis

```bash
pip install reportlab
```

### 1. Crée ton fichier CV JSON

Copie et adapte `file/demo.json` :

```json
{
  "summary": "Étudiant en dernière année à HEC Paris, spécialisation Finance...",
  "education": [
    {
      "university": "HEC Paris",
      "location": "Jouy-en-Josas, France",
      "degree": "Master Grande École — Majeure Finance",
      "date": "2023 – 2025",
      "bullets": [
        "Classement top 5% de promotion",
        "Membre du HEC Finance Club"
      ]
    }
  ],
  "experience": [
    {
      "company": "Goldman Sachs",
      "location": "Paris, France",
      "title": "Analyste Stagiaire — Investment Banking",
      "date": "Juin – Août 2024",
      "bullets": [
        "Modélisation financière (LBO, DCF) sur 3 transactions M&A (>500M€)",
        {
          "main": "Préparation de pitch books pour des clients CAC 40",
          "sub_bullets": [
            "Analyse sectorielle et benchmarking concurrentiel",
            "Valorisation par multiples de marché"
          ]
        }
      ]
    }
  ],
  "skills": {
    "Langues": "Français (natif), Anglais (C2), Espagnol (B2)",
    "Compétences techniques": "Excel VBA, Bloomberg, Python (pandas, numpy), SQL",
    "Centres d'intérêt": "Tennis (classé -15), Photographie"
  }
}
```

### 2. (Optionnel) Infos personnelles

Crée un fichier `personal.json` à la racine (ignoré par git) :

```json
{
  "name": "Jean Dupont",
  "email": "jean.dupont@hec.edu",
  "phone": "+33 6 12 34 56 78",
  "linkedin": "linkedin.com/in/jean-dupont",
  "location": "Paris, France"
}
```

### 3. Génère le PDF

```bash
python cv.py
```

Le script te demande :
1. Le nom du fichier JSON d'entrée (ex: `file/mon_cv.json`)
2. Le nom du PDF à générer (ex: `jean_dupont_cv.pdf`)

Si le contenu dépasse une page, le script l'indique et n'écrit rien — ajuste ton JSON.

## 📂 Structure

```
cv_generator/
├── cv.py              # Script principal — génération PDF (reportlab)
├── file/
│   └── demo.json      # Exemple de CV (HEC Finance, Goldman Sachs)
└── test.pdf           # PDF de démo généré à partir de demo.json
```

## 🗂️ Schéma JSON

| Champ | Type | Description |
|---|---|---|
| `summary` | `string` | Paragraphe d'introduction |
| `education` | `array` | Liste des formations |
| `education[].university` | `string` | Nom de l'école |
| `education[].degree` | `string` | Intitulé du diplôme |
| `education[].date` | `string` | Période (ex: `2023 – 2025`) |
| `education[].bullets` | `array` | Points clés (strings ou objets avec sous-bullets) |
| `experience` | `array` | Liste des expériences |
| `experience[].company` | `string` | Nom de l'entreprise |
| `experience[].title` | `string` | Intitulé du poste |
| `experience[].bullets` | `array` | Réalisations (strings ou `{main, sub_bullets}`) |
| `skills` | `object` | Catégories de compétences (clé → valeur) |

## 🔒 Confidentialité

Le `.gitignore` exclut automatiquement tous les fichiers `*.json` et `*.pdf` — **sauf** `file/demo.json` et `test.pdf`. Tes vrais CVs et tes infos personnelles ne seront jamais committés par accident.

## 🛠️ Stack technique

- **Python 3** — stdlib uniquement + `reportlab`
- **reportlab** — génération PDF (Times Roman, tables, paragraphes)
