# Spiritual Coach App

A personal spiritual wellness application built with FastAPI, Streamlit, SQLAlchemy, and SQLite.

The app helps users maintain a daily spiritual routine through affirmations, sankalp (intentions), gratitude practice, and journaling.

---

## Features

### Morning Routine

* Daily affirmations
* View affirmation history
* Track spiritual practice

### Sankalp

* Create personal intentions
* Store and retrieve sankalp entries

### Gratitude Journal

* Record gratitude notes
* View gratitude history
* Timestamped entries

### Journal

* Write daily reflections
* Store spiritual and personal observations
* View journal history

### Dashboard

* Central navigation hub
* Quick access to all spiritual activities
* Future support for progress tracking and insights

---

## Technology Stack

### Frontend

* Streamlit
* Python

### Backend

* FastAPI
* Pydantic
* Uvicorn

### Database

* SQLite

### ORM

* SQLAlchemy

### Development Tools

* VS Code
* Git
* GitHub
* Conda Environment

---

## Project Structure

```text
spiritual-coach-app/
│
├── backend/
│   ├── UI.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/Swetapatharkar/spiritual-coach-app.git
cd spiritual-coach-app
```

### Create Conda Environment

```bash
conda create -n spiritual_coach python=3.12
conda activate spiritual_coach
```

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Run Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Run Streamlit UI

Open a new terminal:

```bash
cd backend
streamlit run UI.py
```

Streamlit URL:

```text
http://localhost:8501
```

---

## Future Enhancements

* User authentication
* Progress tracking dashboard
* Spiritual streak tracking
* Daily inspirational quotes
* Meditation tracker
* Audio affirmations
* Cloud database support
* Mobile responsive UI
* Deployment to cloud platforms

---

## Author

Shweta Patharkar

---

## License

This project is intended for learning, personal development, and spiritual wellness purposes.
