# 🔍 Resume Matcher App

An intelligent AI-powered resume matching application that uses Google Gemini embeddings to find the best candidates for job descriptions. Built with Streamlit for a modern, user-friendly interface.

## ✨ Features

### 🎯 Core Functionality
- **Multi-format Support**: Upload PDF and DOCX resume files
- **AI-Powered Matching**: Uses Gemini embeddings for semantic similarity
- **Smart Ranking**: Cosine similarity algorithm ranks candidates by relevance
- **Top 10 Results**: Displays the most relevant candidates with similarity scores

### 🚀 Performance Optimizations
- **Parallel Processing**: ThreadPoolExecutor for faster resume parsing
- **Lazy Loading**: AI summaries generated only when viewing candidate profiles
- **Efficient File Handling**: Optimized text extraction and caching
- **Comprehensive Logging**: Performance monitoring and debugging

### 🎨 User Experience
- **Clean Table Layout**: Professional ranking display with clear metrics
- **Interactive Profiles**: Click-to-view detailed candidate information
- **File Preview**: PDF embedding + DOCX text view
- **Download Functionality**: Easy access to original resume files
- **Responsive Design**: Wide layout optimized for better viewing

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.35.0
- **AI/ML**: Google Gemini API (embeddings + summaries)
- **Similarity**: scikit-learn (cosine similarity)
- **File Processing**: PyMuPDF (PDF), python-docx (DOCX)
- **Configuration**: python-dotenv

## 📦 Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-matcher-app.git
   cd resume-matcher-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🚀 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Resume Matcher App"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select the `resume-matcher-app` repository
   - Set the main file path: `app.py`

3. **Configure Environment Variables**
   - In Streamlit Cloud dashboard, go to "Settings"
   - Add environment variable:
     - **Key**: `GEMINI_API_KEY`
     - **Value**: Your Gemini API key
   - Deploy the app

### Alternative Deployment Options

- **Heroku**: Use the Procfile and requirements.txt
- **Docker**: Build with the provided Dockerfile
- **Local Server**: Run with `streamlit run app.py --server.port 8501`

## 📁 Project Structure

```
resume-matcher-app/
├── app.py                 # Main Streamlit application
├── matcher.py             # Cosine similarity & ranking logic
├── gemini_api.py          # Gemini API wrapper
├── utils.py               # File processing utilities
├── logger.py              # Shared logging configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### Supported File Formats

- **PDF**: Full text extraction with PyMuPDF
- **DOCX**: Text extraction with python-docx
- **File Size**: Recommended < 10MB per file

## 📊 Performance

### Optimization Features
- **Parallel Resume Parsing**: ~3x faster with ThreadPoolExecutor
- **Lazy Summary Generation**: Only generates AI summaries when viewing profiles
- **Efficient Embeddings**: Batch processing for multiple resumes
- **Memory Management**: Proper file handling and cleanup

### Expected Performance
- **Small Batch (5-10 resumes)**: 10-30 seconds
- **Medium Batch (10-20 resumes)**: 30-60 seconds
- **Large Batch (20+ resumes)**: 60+ seconds

## 🐛 Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**
   - Ensure `.env` file exists and contains your API key
   - Check for typos in the environment variable name

2. **PDF not displaying**
   - Verify PDF file is not corrupted
   - Check file size (should be < 10MB)
   - Ensure proper file permissions

3. **"No readable text found in uploaded resumes"**
   - Occurs when text parsing returns empty results (e.g., scanned images or corrupted files)
   - Verify file integrity or upload text-based PDF/DOCX files

4. **Slow performance**
   - Check internet connection (for Gemini API calls)
   - Reduce number of simultaneous uploads
   - Monitor logs for specific bottlenecks

5. **Import errors**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Logging

The app includes comprehensive logging for debugging:
- Performance timing for each operation
- File processing status
- API call success/failure
- Error details with stack traces

View logs in the terminal where you run the app.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for AI embeddings and summaries
- **Streamlit** for the web framework
- **PyMuPDF** for PDF processing
- **scikit-learn** for similarity calculations

---

**Built for efficient resume matching and candidate evaluation** 🚀
