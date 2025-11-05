// Utility functions

// Parse CSV file
function parseCSV(text) {
    const lines = text.split('\n').filter(line => line.trim());
    if (lines.length === 0) return [];

    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const row = {};
        headers.forEach((header, index) => {
            row[header] = values[index] ? values[index].trim() : '';
        });
        data.push(row);
    }

    return data;
}

// Check if text contains non-ASCII characters (for Unicode detection)
function needUnicode(text) {
    return /[^\x00-\x7F]/.test(text);
}

// Generate sample CSV content
function generateSampleCSV() {
    const headers = ['mobile', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'template_id'];
    const sampleData = [
        ['9876543210', 'John', '12345', 'Health Plus', 'ABC123', '1800-XXX-XXX', '', '', '', '', '', '173865'],
        ['9876543211', 'Jane', '67890', 'Care Pro', 'XYZ456', '1800-YYY-YYY', '', '', '', '', '', '173865']
    ];

    let csv = headers.join(',') + '\n';
    sampleData.forEach(row => {
        csv += row.join(',') + '\n';
    });

    return csv;
}

// Download file
function downloadFile(content, filename, type = 'text/csv') {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Save data to localStorage
function saveToStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (e) {
        console.error('Failed to save to localStorage:', e);
        return false;
    }
}

// Load data from localStorage
function loadFromStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.error('Failed to load from localStorage:', e);
        return null;
    }
}

// Clear localStorage
function clearStorage(key) {
    localStorage.removeItem(key);
}

// Format timestamp
function formatTimestamp(date = new Date()) {
    return date.toISOString().replace(/[:.]/g, '-').slice(0, -5);
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Validate mobile number
function isValidMobile(mobile) {
    return /^[6-9]\d{9}$/.test(mobile.toString().trim());
}

// Validate template ID
function isValidTemplateId(templateId) {
    return TEMPLATES.hasOwnProperty(parseInt(templateId));
}

// Sleep/delay function
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Export data to Excel (CSV format)
function exportToExcel(data, filename) {
    if (data.length === 0) return;

    const headers = Object.keys(data[0]);
    let csv = headers.join(',') + '\n';

    data.forEach(row => {
        const values = headers.map(header => {
            let value = row[header] || '';
            // Escape commas and quotes
            if (value.toString().includes(',') || value.toString().includes('"')) {
                value = '"' + value.toString().replace(/"/g, '""') + '"';
            }
            return value;
        });
        csv += values.join(',') + '\n';
    });

    downloadFile(csv, filename, 'text/csv');
}
