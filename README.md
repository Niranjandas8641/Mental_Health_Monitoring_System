# 💜 MindCare – AI Mental Health Monitoring System

MindCare is a web-based mental wellness application that helps users track their daily moods, record personal reflections, and understand their mood patterns over time.

The application uses Python, Flask, and TextBlob for mood logging and text sentiment analysis, with an interactive dashboard for visualizing mood trends.

## ✨ Features

- **Daily Mood Tracking:** Record mood scores from 1 to 5.
- **Journal Entries:** Write optional notes about daily feelings and experiences.
- **Sentiment Analysis:** Analyze journal text using TextBlob.
- **Mood Summary:** View average mood and total recorded entries.
- **30-Day Mood Trends:** Visualize recorded mood scores using charts.
- **Weekly Mood Analysis:** Calculate weekly average mood and total entries.
- **Daily Mood Chart:** Display daily average mood scores for the last seven days.
- **Mood History:** Review recent mood entries and journal notes.
- **Interactive Dashboard:** Simple, responsive interface with a purple theme.
- **Data Persistence:** Store mood records in a local JSON file.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application and REST API |
| TextBlob | Text sentiment analysis |
| HTML5 | Dashboard structure |
| CSS3 | Styling and responsive layout |
| JavaScript | Frontend interactions and API integration |
| Chart.js | Mood trend visualizations |
| JSON | Local mood data storage |

## 📂 Project Structure

```text
MindCare/
│
├── app.py
├── requirements.txt
├── .gitignore
├── mental_health_data.json
│
└── templates/
    └── index.html
```

**Note:** `mental_health_data.json` is created or updated by the application and should not be committed if it contains personal mood records or journal entries. The file is shown above to explain the local project structure.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MindCare-AI-Mental-Health-Monitoring.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Navigate to the project folder

```bash
cd MindCare-AI-Mental-Health-Monitoring
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should include:

```text
Flask
textblob
```

If your project uses additional Python libraries, add them to the requirements file.

### 6. Run the application

```bash
python app.py
```

Open the application in your browser:

http://127.0.0.1:5000/

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Displays the MindCare dashboard |
| `/api/log_mood` | POST | Saves a mood entry and analyzes journal text |
| `/api/summary` | GET | Returns mood summary and recent entries |
| `/api/weekly-analysis` | GET | Returns weekly mood statistics and daily averages |

### Example: Save a mood

**Request:**

```http
POST /api/log_mood
Content-Type: application/json
```

```json
{
  "mood": 4,
  "note": "Today was a good day."
}
```

The exact response format depends on the backend implementation.

### Example: Weekly analysis response

```json
{
  "weekly_average": 2.44,
  "total_entries": 9,
  "trend": "Not enough data",
  "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  "daily_averages": [null, null, null, null, null, 2.67, 2.0],
  "daily_entry_counts": [0, 0, 0, 0, 0, 6, 3]
}
```

This example illustrates the API response structure. Actual results depend on recorded mood entries and the backend's trend calculation.

## 📊 How It Works

1. The user selects a mood score between 1 and 5.
2. The user optionally writes a journal note.
3. Flask receives and stores the mood entry.
4. TextBlob analyzes the journal text for sentiment.
5. The dashboard retrieves mood summaries and recent entries.
6. Chart.js visualizes mood scores and daily averages.
7. The weekly analysis endpoint calculates statistics for the seven-day period.

## 🔮 Future Improvements

- AI-powered personalized mood insights.
- Weekly and monthly reports.
- Mood reminders and notifications.
- Downloadable mood reports.
- Improved data privacy and secure user authentication.
- More advanced mood pattern analysis.

## 🔒 Privacy and Disclaimer

MindCare is an educational project designed for mood tracking and self-reflection.

- Mood scores and journal notes may contain sensitive personal information.
- Do not upload private mood data, passwords, API keys, or environment files to a public repository.
- Text sentiment analysis is not a clinical assessment.
- MindCare does not diagnose, treat, or replace professional mental health care.

## 👨‍💻 Author

**Niranjan Das**

BSc Artificial Intelligence and Machine Learning Graduate

Interested in Artificial Intelligence, Machine Learning, Python, and Generative AI.

## 📄 License

This project can be distributed under the MIT License if you choose to add an MIT `LICENSE` file to the repository.
