# Digital Journey Logger

## An Intelligent Screenshot-Based Activity Tracker

![Digital Journey Logger](https://ibb.co/placeholder-image)


---

## 🚀 Overview

Digital Journey Logger is an innovative application that helps users track and recall their digital activities by automatically capturing screenshots at set intervals and providing an AI-powered query interface to search through them. It's like having a time machine for your digital life!

### Key Features

- **Automatic Screenshot Capture**: Easily capture screenshots with custom naming
- **AI-Powered Querying**: Ask natural language questions about your past activities
- **Intelligent Results**: Get contextual explanations about what you were doing at specific times
- **Visual Timeline**: Browse your digital journey through a visual gallery interface
- **Privacy-First**: All data stays on your local machine, with no cloud uploads

## 💻 Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python with Flask
- **AI Engine**: Groq LLM API (llama3-70b-8192 model)
- **Screenshot Utility**: PyAutoGUI
- **Data Storage**: Local JSON for metadata, filesystem for screenshots

## 📋 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 14+ (optional, for development only)
- Groq API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/digital-journey-logger.git
cd digital-journey-logger
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

1. Create a `.env` file in the project root (or set your Groq API key in app.py)
2. Add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Step 4: Run the Application

```bash
cd src
python app.py
```

The application will be available at: [http://localhost:5000](http://localhost:5000)

## 🖥️ How It Works

1. **Capture**: The application takes screenshots of your screen using PyAutoGUI
2. **Store**: Screenshots are saved locally with timestamps and metadata
3. **Query**: When you ask a question like "What was I doing yesterday at 6 PM?", the query is sent to the Groq LLM API
4. **Analyze**: The AI analyzes your query against the screenshot metadata
5. **Present**: Relevant screenshots and an explanation are presented in the user interface

## 🔍 Use Cases

- **Time Tracking**: Understand how you spend your time on digital devices
- **Project Documentation**: Automatically document your work process
- **Memory Aid**: "What was that website I was looking at last Tuesday?"
- **Productivity Analysis**: Identify patterns in your digital behavior

## 🏆 What Makes This Project Unique

- **Natural Language Interface**: No complex search parameters needed - just ask questions naturally
- **Contextual Understanding**: The AI provides explanations, not just search results
- **Minimalist Design**: Clean interface focused on quick capture and easy retrieval
- **Local-First Philosophy**: Your data stays on your machine for maximum privacy

## ⚙️ Project Structure

```
digital-journey-logger/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── screenshots/
│   └── [captured screenshots]
├── src/
│   └── app.py
├── metadata.json
├── requirements.txt
└── README.md
```

## 🔮 Future Enhancements

- **OCR Integration**: Extract and search text within screenshots
- **Activity Categorization**: Automatically categorize activities (work, entertainment, etc.)
- **Time Insights**: Generate reports on how time is spent across applications
- **Browser Extension**: Capture metadata directly from browser activity
- **Multi-device Sync**: Securely sync activity data across devices

## 👥 Team

- [vinay koushik] - Lead Developer
- [Yashaswini] - UI/UX Designer
- [mohanapriya] - AI Integration Specialist
- [lekha]  - screen capture integration
