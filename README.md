# 📱 Fast2SMS Bulk Sender - Web Application

A fully-featured web application for sending bulk SMS messages using the Fast2SMS service with multiple templates in various languages.

## ✨ Features

- **16 Pre-approved Templates** in multiple languages (English, Hindi, Kannada, Tamil, Bengali, Malayalam, Telugu, Marathi)
- **Easy File Upload** - CSV/XLSX support with drag-and-drop
- **Data Preview** - Review your data before sending
- **Template Validation** - Automatic validation of template IDs
- **Real-time Progress** - Track SMS sending status in real-time
- **Detailed Logging** - Excel log files with complete results
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Retry Logic** - Automatic retry for failed messages
- **Unicode Support** - Full support for regional language SMS

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Fast2SMS API key ([Get it here](https://www.fast2sms.com/))

### Installation

1. **Navigate to the web app folder:**
   ```bash
   cd fast2sms_webapp
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

3. **You should see the home page with all available templates!**

## 📖 Usage Guide

### Step 1: View Templates

The home page displays all 16 approved SMS templates with:
- Template ID
- Sender ID
- Number of variables
- DLT ID
- Message preview

### Step 2: Prepare Your Data

1. Click **"Download Sample"** to get a template CSV file
2. Open the CSV in Excel or any spreadsheet software
3. Fill in your data:
   - `mobile`: 10-digit mobile number (without +91)
   - `v1` to `v10`: Variable values for template placeholders
   - `template_id`: Choose from the approved template IDs

**Example:**
| mobile      | v1   | v2    | v3          | v4     | v5            | template_id |
|-------------|------|-------|-------------|--------|---------------|-------------|
| 9876543210  | John | 12345 | Health Plus | ABC123 | 1800-XXX-XXX  | 173865      |

### Step 3: Upload Data

1. Click **"Upload Data"** in the navigation
2. Select your CSV/XLSX file (or drag and drop)
3. Click **"Upload & Continue"**
4. The system will validate your file and show a preview

### Step 4: Preview & Validate

- Review the data summary (total rows, unique mobiles)
- Check for invalid template IDs
- View the first 10 rows of your data
- Click **"Continue to Send"** if everything looks good

### Step 5: Configure & Send

1. Enter your **Fast2SMS API key**
2. (Optional) Set a schedule time for delayed sending
   - Format: `YYYY-MM-DD-HH-MM`
   - Example: `2024-12-25-14-30` (Dec 25, 2024 at 2:30 PM)
3. Review the sending summary
4. Click **"Start Sending SMS"**
5. Confirm the action

### Step 6: View Results

- See real-time statistics (success/fail counts, duration)
- View detailed results for each message
- Download the complete Excel log file
- Start a new job or go back to home

## 📁 Project Structure

```
fast2sms_webapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── upload.html       # File upload page
│   ├── preview.html      # Data preview page
│   ├── send.html         # API configuration page
│   └── results.html      # Results page
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── script.js     # JavaScript functionality
├── uploads/              # Uploaded files (auto-created)
└── logs/                 # Log files (auto-created)
```

## 🔧 Configuration

### Environment Variables (Optional)

You can set your Fast2SMS API key as an environment variable:

**Windows:**
```cmd
set F2S_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export F2S_KEY=your_api_key_here
```

### Template Management

To add or modify templates, edit the `TEMPLATES` dictionary in `app.py`:

```python
TEMPLATES = {
    template_id: {
        "sender": "SENDER_ID",
        "vars": number_of_variables,
        "text": "Message template with {#var#} placeholders",
        "dlt_id": dlt_template_id
    },
    # Add more templates...
}
```

## 📊 File Format Requirements

### Required Columns
- `mobile`: 10-digit mobile number (e.g., 9876543210)
- `template_id`: Template ID from approved list
- `v1, v2, v3, ...`: Variables for template (up to v10)

### Supported Formats
- CSV (.csv)
- Excel (.xlsx)

### File Size Limit
- Maximum: 16MB

## 🛠️ Troubleshooting

### Common Issues

1. **"Module not found" error**
   - Make sure you've installed all requirements: `pip install -r requirements.txt`

2. **"File upload failed"**
   - Check file format (CSV/XLSX only)
   - Ensure file has required columns (`mobile`, `template_id`)
   - Check file size (max 16MB)

3. **"SMS sending failed"**
   - Verify your Fast2SMS API key is correct
   - Check your Fast2SMS account balance
   - Ensure template IDs match approved templates
   - Verify mobile numbers are valid 10-digit numbers

4. **"Invalid template ID"**
   - Use only template IDs from the approved list on the home page
   - Template IDs are case-sensitive and must be exact numbers

### Server Issues

If the server doesn't start:

1. Check if port 5000 is already in use
2. Try a different port:
   ```bash
   # In app.py, change the last line to:
   app.run(debug=True, host='0.0.0.0', port=8080)
   ```

## 🔒 Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive data
- The app uses Flask's built-in session management
- Uploaded files are stored securely in the `uploads/` folder
- Log files are stored in the `logs/` folder

## 📝 API Rate Limiting

The application includes:
- 0.2 second delay between messages to avoid rate limiting
- Automatic retry (3 attempts) for failed messages
- Exponential backoff for network errors

## 🌐 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Environment Variables for Production

```bash
export FLASK_ENV=production
export SECRET_KEY=your_secure_secret_key_here
export F2S_KEY=your_fast2sms_api_key
```

## 📞 Support

For issues with:
- **Fast2SMS API**: Visit [Fast2SMS Support](https://www.fast2sms.com/)
- **This Application**: Contact the M-SWASTH team

## 📄 License

Created for M-SWASTH Team | Fast2SMS Bulk Sender v2.0

## 🎯 Features Roadmap

- [ ] Bulk template management UI
- [ ] Scheduled sending with calendar picker
- [ ] SMS delivery status tracking
- [ ] Multi-user support with authentication
- [ ] API endpoint for programmatic access
- [ ] Dashboard with analytics

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 Additional Resources

- [Fast2SMS Documentation](https://docs.fast2sms.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Built with ❤️ for M-SWASTH Team**

For questions or support, please contact your system administrator.
