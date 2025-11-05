# 📱 Fast2SMS Bulk Sender - Static Web App

A lightweight, static web application for sending bulk SMS messages using Fast2SMS service. No server required - runs entirely in your browser!

## ✨ Features

- **16 Pre-approved Templates** in 8+ languages (English, Hindi, Kannada, Tamil, Bengali, Malayalam, Telugu, Marathi)
- **100% Client-Side** - All processing happens in your browser, your data stays private
- **No Server Needed** - Pure HTML/CSS/JavaScript static site
- **Easy Deployment** - Works on GitHub Pages, Netlify, Vercel, or any static hosting
- **CSV File Support** - Upload and process CSV files directly in browser
- **Real-time Progress** - Live updates while sending SMS
- **Detailed Logging** - Download results as CSV/Excel format
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Retry Logic** - Automatic retry for failed messages
- **Unicode Support** - Full support for regional language SMS

## 🚀 Quick Start

### Option 1: Open Locally (Easiest!)

1. **Download or clone this repository**
2. **Open `index.html` in your web browser**
3. **That's it!** No installation, no dependencies, no server needed.

### Option 2: Deploy to Free Hosting

**GitHub Pages (Recommended):**
- Already configured! Enable in Settings → Pages
- Your site: `https://yourusername.github.io/Fast2SMS_001`

**Netlify/Vercel:**
- Drag and drop the entire folder
- Or connect your GitHub repo
- Instant deployment!

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
Fast2SMS_001/
├── index.html           # Home page with templates
├── upload.html          # File upload page
├── send.html            # Sending page
├── results.html         # Results page
├── css/
│   └── style.css        # Complete styling
├── js/
│   ├── templates.js     # Template definitions
│   ├── utils.js         # Utility functions
│   └── sms.js           # SMS sending logic
├── data/                # (Empty - for user data)
├── logs/                # (Empty - for logs)
└── uploads/             # (Empty - for uploads)
```

## 🔧 Configuration

### Template Management

To add or modify templates, edit the `TEMPLATES` object in `js/templates.js`:

```javascript
const TEMPLATES = {
    template_id: {
        sender: "SENDER_ID",
        vars: number_of_variables,
        text: "Message template with {#var#} placeholders",
        dlt_id: dlt_template_id,
        language: "Language Name"
    },
    // Add more templates...
};
```

## 📊 File Format Requirements

### Required Columns
- `mobile`: 10-digit mobile number (e.g., 9876543210)
- `template_id`: Template ID from approved list
- `v1, v2, v3, ...`: Variables for template (up to v10)

### Supported Formats
- CSV (.csv)

## 🛠️ Troubleshooting

### Common Issues

1. **CSV Upload Fails**
   - Ensure file is in CSV format
   - Check required columns exist: `mobile`, `template_id`
   - Remove any special characters from headers

2. **SMS Sending Fails**
   - Verify your Fast2SMS API key is correct
   - Check your Fast2SMS account balance
   - Ensure template IDs match approved templates
   - Verify mobile numbers are valid 10-digit numbers

3. **"Invalid Template ID" Error**
   - Use only template IDs from the home page list
   - Template IDs must be exact numbers (173865, not "173865")

4. **Results Not Showing**
   - Don't close browser tab during sending
   - Check browser console for errors (F12)
   - Clear browser cache and try again

### Browser Compatibility

| Browser | Minimum Version |
|---------|----------------|
| Chrome  | 60+ |
| Firefox | 60+ |
| Safari  | 12+ |
| Edge    | 79+ |

## 🔒 Privacy & Security

- Your CSV data is processed locally in your browser
- Data is temporarily stored in browser's localStorage
- API key is never saved permanently
- No data sent to any server except Fast2SMS API for sending SMS
- Clear browser data to remove all temporary information

## 📝 API Rate Limiting

The application includes:
- 0.2 second delay between messages to avoid rate limiting
- Automatic retry (3 attempts) for failed messages
- Exponential backoff for network errors

## 🌐 Deployment Options

### 1. GitHub Pages (Free & Easy)
1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/` (root)
4. Save → Your site is live!

### 2. Netlify (Free)
1. Drag & drop entire folder to Netlify
2. Or connect your GitHub repository
3. No build configuration needed
4. Instant deployment!

### 3. Vercel (Free)
1. Import your GitHub repository
2. Framework Preset: Other
3. Build command: (leave empty)
4. Output directory: (leave empty)
5. Deploy!

### 4. Any Web Host
- Upload all files to web server
- Point domain to `index.html`
- No special configuration needed
- Works on shared hosting, VPS, anywhere!

## 📞 Support

For issues with:
- **Fast2SMS API**: Visit [Fast2SMS Support](https://www.fast2sms.com/)
- **This Application**: Contact the M-SWASTH team

## 📄 License

Created for M-SWASTH Team | Fast2SMS Bulk Sender v3.0 (Static)

## 🆕 What's New in v3.0

- ✅ Converted from Flask to pure static HTML/CSS/JS
- ✅ No backend server needed
- ✅ Deployable on any static hosting (GitHub Pages, Netlify, Vercel)
- ✅ Improved privacy (client-side processing)
- ✅ Faster initial load time
- ✅ Mobile-responsive design
- ✅ Real-time sending progress
- ✅ Better error handling

## 🎯 Advantages Over Server-Based Version

✅ **No Server Required** - Pure static hosting
✅ **Free Hosting** - GitHub Pages, Netlify, Vercel
✅ **Faster Deployment** - No dependencies to install
✅ **Better Privacy** - Data stays in browser
✅ **Lower Cost** - No server costs
✅ **Simpler Setup** - Just open HTML file

## 📚 Additional Resources

- [Fast2SMS Documentation](https://docs.fast2sms.com/)
- [Fast2SMS Dashboard](https://www.fast2sms.com/dashboard)

---

**Ready to send bulk SMS? Just open `index.html` in your browser!** 🚀

**Built with ❤️ for M-SWASTH Team**
