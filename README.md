# SUS Sisters Pairing System 🌸

A desktop application for automatically pairing Big Sisters with Little Sisters based on shared interests, course, and year group. Built with Python and Tkinter.

## Overview

SUS Sisters lets coordinators upload two Excel spreadsheets — one for Big Sisters, one for Little Sisters — and automatically generates the best-matched pairs using a weighted scoring algorithm. Results are displayed in-app and can be exported to Excel.

## How the matching works

Each possible big/little combination is scored:

| Criteria | Points |
|---|---|
| Each shared interest | +3 |
| Same course | +2 |
| Same year group | +1 |

Little sisters are assigned to the big sister with whom they score highest. If there are more little sisters than big sisters, the algorithm runs a second pass and assigns remaining little sisters to whichever big sister is their best match — meaning one big sister may receive two little sisters.

## Features

- Upload Big Sister and Little Sister Excel files via a file picker
- Displays record count on load so you can verify the file was read correctly
- Runs interest-based matching and displays results in a sortable table
- Export matched pairs to a formatted Excel file
- Handles uneven group sizes — no one is left unmatched

## Project Structure

```
SUS-Sisters/
├── main.py                  # Entry point
├── requirements.txt
├── ui/
│   └── app_ui.py            # Tkinter GUI + results table
└── pairing/
    ├── file_handler.py      # Excel file loading
    ├── matcher.py           # Scoring and pairing algorithm
    └── exporter.py          # Excel export
```

## Excel File Format

Both input files must be `.xlsx` with the following columns (column names are case-insensitive):

| Column | Description | Example |
|---|---|---|
| `name` | Full name | Alice Johnson |
| `interests` | Comma-separated interests | football, reading, music |
| `course` | Course or degree name | Engineering |
| `year_group` | Year of study | Year 1 |

## Setup

**1. Clone the repo:**
```bash
git clone https://github.com/kelech1/SUS-Sisters.git
cd SUS-Sisters
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the app:**
```bash
python main.py
```

## Tech Stack

- Python 3.11
- Tkinter (GUI)
- pandas (data processing and matching)
- openpyxl (Excel reading and writing)