import os
import time
import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['LOG_FOLDER'] = 'logs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx'}

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)

# Template definitions - Same as notebook
TEMPLATES = {
    173865: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "Dear {#var#} customer {#var#}, you are covered with policy {#var#}, https://c0i.in/MSWAST/{#var#}. Find your nearest clinic https://mswast-map.glitch.me/map2.html  -MSWASTH -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    173903: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "प्रिय {#var#} ग्राहक {#var#}, आप {#var#} बीमा के अंतर्गत आते हैं, https://c0i.in/MSWAST/{#var#}. अधिक जानकारी के लिए कृपया {#var#} पर कॉल करें -MSWASTH",
        "dlt_id": 1107172768969047732
    },
    173904: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "ಆತ್ಮೀಯ {#var#} ಗ್ರಾಹಕ {#var#}, ನೀವು {#var#} ವಿಮೆಯಡಿ ಒಳಗಾಗಿದ್ದೀರಿ, https://c0i.in/MSWAST/{#var#}. ಯಾವುದೇ ವಿವರಗಳಿಗಾಗಿ ದಯವಿಟ್ಟು {#var#} ಗೆ ಕರೆ ಮಾಡಿ -MSWASTH -MSWASTH",
        "dlt_id": 1107172768964776740
    },
    174779: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "அன்புள்ள {#var#} வாடிக்கையாளர்களே {#var#}, உங்கள் {#var#} கொள்கையின் கீழ் பாதுகாக்கப்படுகிறீர்கள், https://c0i.in/MSWAST/{#var#}. பற்றிய விவரங்களுக்கு {#var#} ஜ அழைக்கவும் -MSWASTH",
        "dlt_id": 1107172768960388249
    },
    174780: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "প্রিয় {#var#} গ্রাহক {#var#}, আপনি  {#var#} স্কিমের অধীনে আবৃত, https://c0i.in/MSWAST/{#var#}. যেকোন বিবরণের জন্য অনুগ্রহ করে কল করুন {#var#} -MSWASTH",
        "dlt_id": 1107172768955025536
    },
    174781: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "പ്രിയപ്പെട്ട {#var#} ഉപഭോക്താവേ {#var#}, നിങ്ങൾ {#var#} പോളിസിയിൽ ഉൾപ്പെട്ടിരിക്കുന്നു, https://c0i.in/MSWAST/{#var#}. ഏതെങ്കിലും വിശദാംശങ്ങൾക്ക് ദയവായി വിളിക്കുക {#var#} -MSWASTH",
        "dlt_id": 1107172768941070312
    },
    175561: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "ప్రియమైన {#var#} కస్టమర్ {#var#}, మీరు {#var#} పాలసీ కింద కవరై ఉన్నారు, https://c0i.in/MSWAST/{#var#} సందర్శించండి లేదా {#var#} కి కాల్ చేయండి -MSWASTH",
        "dlt_id": 1107173165717883763
    },
    175562: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "प्रिय {#var#} ग्राहक {#var#}, तुम्ही {#var#} विमा अंतर्गत आहात, https://c0i.in/MSWAST/{#var#}. कोणत्याही तपशिलांसाठी कृपया {#var#} वर कॉल करा -MSWASTH",
        "dlt_id": 1107173165711431532
    },
    181629: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "Dear {#var#} customer {#var#}, you are covered with policy {#var#}, https://c0i.in/MSWAST/{#var#}. Find your nearest clinic {#var#} -MSWASTH",
        "dlt_id": 1107174185289525526
    },
    183078: {
        "sender": "MSWAST",
        "vars": 4,
        "text": "Dear {#var#} customer {#var#}, you are covered with policy {#var#}, https://c0i.in/MSWAST/{#var#}. Find your nearest clinic https://mswast-map.glitch.me/map2.html  -MSWASTH -MSWASTH",
        "dlt_id": 1107174410935731322
    },
    201352: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "ಆತ್ಮೀಯ {#var#} ಗ್ರಾಹಕರೇ {#var#}, ನೀವು {#var#}ನಲ್ಲಿ M-Swasth ನಿಂದ ಟೆಲಿ ಹೆಲ್ತ್ ಸೇವೆಗಳಿಂದ ಒಳಗೊಳ್ಳಲ್ಪಟ್ಟಿದ್ದೀರಿ. ಚಂದಾದಾರಿಕೆ ಐಡಿ {#var#}. ನಮ್ಮ ವೈದ್ಯರೊಂದಿಗೆ ಸಂಪರ್ಕ ಸಾಧಿಸಲು ನೀವು {#var#} ಗೆ ಕರೆ ಮಾಡಬಹುದು, 24*7 ಅಥವಾ ಲಿಂಕ್‌ನೊಂದಿಗೆ ಮೊಬೈಲ್ ಅಪ್ಲಿಕೇಶನ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201353: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "ప్రియమైన {#var#} వినియోగధారులు {#var#}, మీరు {#var#}లో M-Swasth ద్వారా టెలి హెల్త్ సర్వీసెస్‌తో కవర్ చేయబడ్డారు. సబ్‌స్క్రిప్షన్ ఐడి {#var#}. మీరు మా వైద్యులతో కనెక్ట్ అవ్వడానికి {#var#} కు కాల్ చేయవచ్చు, 24*7 లేదా లింక్‌తో మొబైల్ యాప్‌ను డౌన్‌లోడ్ చేసుకోవచ్చు - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201354: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "அன்புள்ள {#var#} வாடிக்கையாளர் {#var#}, {#var#}இல் M-Swasth வழங்கும் டெலி ஹெல்த் சர்வீசஸ் மூலம் நீங்கள் பாதுகாக்கப்படுகிறீர்கள். சந்தா ஐடி {#var#}. எங்கள் மருத்துவர்களுடன் தொடர்பு கொள்ள {#var#} 24*7 என்ற எண்ணை நீங்கள் அழைக்கலாம் அல்லது https://play.google.com/store/apps/details?id=in.m_insure.patient_app என்ற இணைப்பில் மொபைல் செயலியைப் பதிவிறக்கலாம் -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201355: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "പ്രിയപ്പെട്ട {#var#} ഉപഭോക്താവേ {#var#}, {#var#}ൽ M-Swasth-ന്റെ ടെലി ഹെൽത്ത് സർവീസസ് നിങ്ങൾക്ക് ലഭ്യമാണ്. സബ്‌സ്‌ക്രിപ്‌ഷൻ ഐഡി {#var#}. ഞങ്ങളുടെ ഡോക്ടർമാരുമായി ബന്ധപ്പെടാൻ നിങ്ങൾക്ക് {#var#} 24*7 എന്ന നമ്പറിൽ വിളിക്കാം അല്ലെങ്കിൽ https://play.google.com/store/apps/details?id=in.m_insure.patient_app എന്ന ലിങ്ക് ഉപയോഗിച്ച് മൊബൈൽ ആപ്പ് ഡൗൺലോഡ് ചെയ്യാം -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201356: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "प्रिय {#var#} ग्राहक {#var#}, आप {#var#} में M-Swasth द्वारा टेली हेल्थ सेवाओं के अंतर्गत संरक्षित हैं। आपकी सदस्यता आईडी {#var#} है। आप हमारे डॉक्टरों से 24*7 जुड़ने के लिए {#var#} पर कॉल कर सकते हैं या इस लिंक से मोबाइल ऐप डाउनलोड कर सकते हैं - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201357: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "Dear {#var#} client {#var#}, you are covered with Tele Health Services by M-Swasth in {#var#}. Subscription Id {#var#}. You can call on {#var#} to get connected with our doctors, 24*7 or download mobile app with the link - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    }
}

BASE_URL = "https://www.fast2sms.com/dev/bulkV2"


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def need_unicode(txt):
    """Check if text contains non-ASCII characters"""
    return any(ord(c) > 127 for c in txt)


def send_with_retry(payload, api_key, tries=3, base_pause=1.0):
    """Send SMS with retry logic"""
    for n in range(tries):
        try:
            r = requests.post(
                BASE_URL,
                json=payload,
                headers={"authorization": api_key},
                timeout=12
            )
            js = r.json()
            if js.get("return") is True:
                return True, js.get("request_id"), "Success", js
            else:
                err = js.get("message", str(js))
                return False, None, err, js
        except requests.exceptions.Timeout:
            err = "Request timeout"
        except requests.exceptions.RequestException as e:
            err = f"Network error: {str(e)}"
        except Exception as e:
            err = f"Error: {str(e)}"

        if n < tries - 1:
            time.sleep(base_pause * (2**n))

    return False, None, err, {"error": err}


@app.route('/')
def index():
    """Home page - Display templates"""
    tpl_data = []
    for tpl_id, info in TEMPLATES.items():
        tpl_data.append({
            "id": tpl_id,
            "sender": info["sender"],
            "vars": info["vars"],
            "dlt_id": info["dlt_id"],
            "text": info["text"]
        })
    return render_template('index.html', templates=tpl_data, total=len(TEMPLATES))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload data file"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Load and validate file
            try:
                ext = Path(filename).suffix.lower()
                if ext == ".xlsx":
                    df = pd.read_excel(filepath, dtype=str).fillna("")
                else:
                    df = pd.read_csv(filepath, dtype=str).fillna("")

                # Normalize column names
                df.columns = [c.strip().lower() for c in df.columns]

                # Check required columns
                if 'mobile' not in df.columns or 'template_id' not in df.columns:
                    flash('File must contain "mobile" and "template_id" columns', 'error')
                    os.remove(filepath)
                    return redirect(request.url)

                # Ensure all v1-v10 columns exist
                for i in range(1, 11):
                    col = f"v{i}"
                    if col not in df.columns:
                        df[col] = ""

                # Reorder columns
                df = df[["mobile"] + [f"v{i}" for i in range(1, 11)] + ["template_id"]]

                # Save processed file
                df.to_csv(filepath, index=False)

                # Store filename in session
                session['uploaded_file'] = filename
                session['total_rows'] = len(df)
                session['unique_mobiles'] = df['mobile'].nunique()

                flash(f'File uploaded successfully! {len(df)} rows loaded.', 'success')
                return redirect(url_for('preview'))

            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'error')
                if os.path.exists(filepath):
                    os.remove(filepath)
                return redirect(request.url)
        else:
            flash('Invalid file type. Only CSV and XLSX files are allowed.', 'error')
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/download_sample')
def download_sample():
    """Generate and download sample CSV file"""
    columns = ["mobile"] + [f"v{i}" for i in range(1, 11)] + ["template_id"]
    sample_data = pd.DataFrame([
        ["9876543210", "John", "12345", "Health Plus", "ABC123", "1800-XXX-XXX", "", "", "", "", "", "173865"],
        ["9876543211", "Jane", "67890", "Care Pro", "XYZ456", "1800-YYY-YYY", "", "", "", "", "", "173865"]
    ], columns=columns)

    sample_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_sms_data.csv')
    sample_data.to_csv(sample_path, index=False)

    return send_file(sample_path, as_attachment=True, download_name='sample_sms_data.csv')


@app.route('/preview')
def preview():
    """Preview uploaded data"""
    if 'uploaded_file' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('upload'))

    filename = session['uploaded_file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(filepath):
        flash('Uploaded file not found. Please upload again.', 'error')
        return redirect(url_for('upload'))

    # Load file
    df = pd.read_csv(filepath, dtype=str).fillna("")

    # Validate template IDs
    invalid_templates = []
    for idx, row in df.iterrows():
        try:
            tid = int(float(str(row['template_id']).strip()))
            if tid not in TEMPLATES:
                invalid_templates.append((idx + 1, tid))
        except:
            invalid_templates.append((idx + 1, row['template_id']))

    # Get preview data (first 10 rows)
    preview_data = df.head(10).to_dict('records')

    return render_template('preview.html',
                           preview_data=preview_data,
                           total_rows=len(df),
                           unique_mobiles=df['mobile'].nunique(),
                           invalid_templates=invalid_templates[:10],
                           invalid_count=len(invalid_templates))


@app.route('/send', methods=['GET', 'POST'])
def send():
    """Send SMS messages"""
    if 'uploaded_file' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('upload'))

    if request.method == 'POST':
        api_key = request.form.get('api_key', '').strip()
        schedule_time = request.form.get('schedule_time', '').strip()

        if not api_key:
            flash('API key is required', 'error')
            return redirect(request.url)

        # Store in session for the sending process
        session['api_key'] = api_key
        session['schedule_time'] = schedule_time

        return redirect(url_for('process'))

    return render_template('send.html')


@app.route('/process')
def process():
    """Process and send SMS messages"""
    if 'uploaded_file' not in session or 'api_key' not in session:
        flash('Session expired. Please start over.', 'error')
        return redirect(url_for('upload'))

    filename = session['uploaded_file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    api_key = session['api_key']
    schedule_time = session.get('schedule_time', '')

    # Load data
    df = pd.read_csv(filepath, dtype=str).fillna("")

    results = []
    start_time = datetime.now()

    for idx, row in df.iterrows():
        row_num = idx + 1
        mobile = str(row["mobile"]).strip()

        # Validate and get template
        try:
            msg_id = int(float(str(row["template_id"]).strip()))
        except:
            results.append({
                "row": row_num,
                "mobile": mobile,
                "template_id": row['template_id'],
                "status": "FAIL",
                "request_id": "",
                "message": f"Invalid template_id: {row['template_id']}",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            continue

        tpl = TEMPLATES.get(msg_id)
        if not tpl:
            results.append({
                "row": row_num,
                "mobile": mobile,
                "template_id": msg_id,
                "status": "FAIL",
                "request_id": "",
                "message": f"Template {msg_id} not found",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            continue

        # Build variables
        nvars = tpl["vars"]
        vals = []
        for i in range(1, nvars + 1):
            val = str(row[f"v{i}"]).strip()
            if val.lower() in {"n/a", "na", "none", "null"}:
                val = ""
            vals.append(val)
        vars_pipe = "|".join(vals)

        # Build payload
        payload = {
            "route": "dlt",
            "sender_id": tpl["sender"],
            "message": str(msg_id),
            "variables_values": vars_pipe,
            "numbers": mobile,
            "flash": "0"
        }

        if schedule_time:
            payload["schedule_time"] = schedule_time

        if need_unicode(tpl["text"] + vars_pipe):
            payload["language"] = "unicode"

        # Send SMS
        ok, req_id, message, raw = send_with_retry(payload, api_key)

        results.append({
            "row": row_num,
            "mobile": mobile,
            "template_id": msg_id,
            "status": "SUCCESS" if ok else "FAIL",
            "request_id": req_id or "",
            "message": message,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "raw_response": str(raw)
        })

        # Small delay to avoid rate limiting
        time.sleep(0.2)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Save results to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"sms_log_{timestamp}.xlsx"
    log_path = os.path.join(app.config['LOG_FOLDER'], log_filename)

    log_df = pd.DataFrame(results)
    log_df.to_excel(log_path, index=False, engine='openpyxl')

    # Calculate stats
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    fail_count = len(results) - success_count

    # Store results in session
    session['log_filename'] = log_filename
    session['success_count'] = success_count
    session['fail_count'] = fail_count
    session['duration'] = duration

    # Clean up
    session.pop('api_key', None)

    return redirect(url_for('results'))


@app.route('/results')
def results():
    """Display results"""
    if 'log_filename' not in session:
        flash('No results available', 'warning')
        return redirect(url_for('index'))

    log_filename = session['log_filename']
    log_path = os.path.join(app.config['LOG_FOLDER'], log_filename)

    # Load results
    log_df = pd.read_csv(log_path.replace('.xlsx', '.csv')) if not os.path.exists(log_path) else pd.read_excel(log_path)

    # Get stats from session
    success_count = session.get('success_count', 0)
    fail_count = session.get('fail_count', 0)
    duration = session.get('duration', 0)
    total_rows = session.get('total_rows', 0)

    # Get preview of results (first 20 rows)
    results_preview = log_df.head(20).to_dict('records')

    return render_template('results.html',
                           log_filename=log_filename,
                           success_count=success_count,
                           fail_count=fail_count,
                           total=total_rows,
                           duration=duration,
                           results_preview=results_preview)


@app.route('/download_log/<filename>')
def download_log(filename):
    """Download log file"""
    log_path = os.path.join(app.config['LOG_FOLDER'], secure_filename(filename))
    if os.path.exists(log_path):
        return send_file(log_path, as_attachment=True, download_name=filename)
    else:
        flash('Log file not found', 'error')
        return redirect(url_for('index'))


@app.route('/reset')
def reset():
    """Reset session and start over"""
    session.clear()
    flash('Session cleared. You can start a new bulk SMS job.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
