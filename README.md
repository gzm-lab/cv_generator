# 📄 CV Generator

> 🧒 **In plain English:** You write your school, jobs, and skills in a simple text file, run the script, and it creates a beautiful professional CV as a PDF — like magic!

A **Python-based PDF résumé generator**. Describe your background in a structured JSON file, run the script, and get a clean one-page PDF — ready to send.

Designed for finance/consulting-style CVs (HEC, Goldman Sachs, McKinsey format): single-column layout, two-column title/date rows, bullets and sub-bullets.

## ✨ Features

- 📝 **JSON-driven** — content is 100% separated from the code
- 📏 **One-page enforcement** — the script rejects generation if content overflows (overflow protection)
- 🔒 **Isolated personal data** — a separate `personal.json` file (gitignored) for your address, email, and phone
- 🎨 **Professional layout** — Times Roman, aligned columns, horizontal dividers, bullets/sub-bullets
- ⚡ **Zero cloud dependency** — 100% local, no external APIs

## 🚀 Quick Start

### Prerequisites

```bash
pip install reportlab
```

### 1. Create your CV JSON file

Copy and adapt `file/demo.json`:

```json
{
  "summary": "Final-year student at HEC Paris, Finance specialization...",
  "education": [
    {
      "university": "HEC Paris",
      "location": "Jouy-en-Josas, France",
      "degree": "Master Grande École — Finance Major",
      "date": "2023 – 2025",
      "bullets": [
        "Top 5% of graduating class",
        "Member of the HEC Finance Club"
      ]
    }
  ],
  "experience": [
    {
      "company": "Goldman Sachs",
      "location": "Paris, France",
      "title": "Investment Banking Analyst Intern",
      "date": "Jun – Aug 2024",
      "bullets": [
        "Financial modeling (LBO, DCF) on 3 M&A transactions (>€500M)",
        {
          "main": "Prepared pitch books for CAC 40 clients",
          "sub_bullets": [
            "Sector analysis and competitive benchmarking",
            "Market multiple valuation"
          ]
        }
      ]
    }
  ],
  "skills": {
    "Languages": "French (native), English (C2), Spanish (B2)",
    "Technical Skills": "Excel VBA, Bloomberg, Python (pandas, numpy), SQL",
    "Interests": "Tennis (ranked), Photography"
  }
}
```

### 2. (Optional) Personal info

Create a `personal.json` file at the root (gitignored):

```json
{
  "name": "John Doe",
  "email": "john.doe@hec.edu",
  "phone": "+33 6 12 34 56 78",
  "linkedin": "linkedin.com/in/john-doe",
  "location": "Paris, France"
}
```

### 3. Generate the PDF

```bash
python cv.py
```

The script will prompt you for:
1. Input JSON filename (e.g. `file/my_cv.json`)
2. Output PDF name (e.g. `john_doe_cv.pdf`)

If the content exceeds one page, the script will report the overflow and write nothing — just trim your JSON and try again.

## 📂 Project Structure

```
cv_generator/
├── cv.py              # Main script — PDF generation (reportlab)
├── file/
│   └── demo.json      # Sample CV (HEC Finance, Goldman Sachs)
└── test.pdf           # Demo PDF generated from demo.json
```

## 🗂️ JSON Schema

| Field | Type | Description |
|---|---|---|
| `summary` | `string` | Introduction paragraph |
| `education` | `array` | List of education entries |
| `education[].university` | `string` | School name |
| `education[].degree` | `string` | Degree title |
| `education[].date` | `string` | Period (e.g. `2023 – 2025`) |
| `education[].bullets` | `array` | Key points (strings or objects with sub-bullets) |
| `experience` | `array` | List of work experiences |
| `experience[].company` | `string` | Company name |
| `experience[].title` | `string` | Job title |
| `experience[].bullets` | `array` | Achievements (strings or `{main, sub_bullets}`) |
| `skills` | `object` | Skill categories (key → value) |

## 🔒 Privacy

The `.gitignore` automatically excludes all `*.json` and `*.pdf` files — **except** `file/demo.json` and `test.pdf`. Your real CVs and personal info will never be accidentally committed.

## 🛠️ Tech Stack

- **Python 3** — stdlib only + `reportlab`
- **reportlab** — PDF generation (Times Roman, tables, paragraphs)
