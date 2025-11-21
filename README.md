# Elanco Tick Sighting Backend (Placement Task)

This is a simple backend MVP for displaying and analysing UK tick sightings.  
It loads the provided dataset, stores it in a SQLite database, and exposes API endpoints for searching and aggregated statistics.

---

## How to Run

### 1. Create virtual environment

python -m venv venv

### 2. Activate it (If using Windows PowerShell)

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

### 4. Load the dataset into the database

python -m app.load_dataset

### 5. Run the server

python -m app.main

## The API will be available at:

http://127.0.0.1:5000


---

## API Endpoints

### `/sightings`
Returns tick sightings.

**Optional query parameters:**
- `location`
- `species`
- `start_date=YYYY-MM-DD`
- `end_date=YYYY-MM-DD`
- `limit`
- `offset`

Example:
/sightings?location=London&limit=10


---

### `/stats/locations`
Count of sightings per location.

---

### `/stats/monthly`
Monthly sighting trends (YYYY-MM).

---

### `/stats/weekly` *(optional extension implemented)*
Weekly sighting trends (YYYY-WW).

---

### `/stats/species`
Sightings grouped by species, ordered by count.

---

## Architecture Used

- **Flask** for the API  
- **SQLAlchemy ORM** for interacting with the database  
- **SQLite** as a simple local database for the MVP  
- **Pandas** to clean and load the provided dataset  
- Data validation and duplicate handling are performed during ingestion

---

## Optional Enhancements Implemented
- Pagination (`limit` and `offset`) for `/sightings`
- Weekly trend statistics (`/stats/weekly`)

---

## Video Demonstration
A short walkthrough video is attached below:

https://github.com/user-attachments/assets/d69f3986-bde7-4694-bf74-08fdc11c1da0
