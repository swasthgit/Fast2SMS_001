// SMS sending functionality

// Send SMS with retry logic
async function sendSMSWithRetry(payload, apiKey, retries = 3) {
    for (let attempt = 1; attempt <= retries; attempt++) {
        try {
            const response = await fetch(BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'authorization': apiKey
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.return === true) {
                return {
                    success: true,
                    requestId: data.request_id,
                    message: 'Success',
                    raw: data
                };
            } else {
                const errorMsg = data.message || JSON.stringify(data);
                if (attempt === retries) {
                    return {
                        success: false,
                        requestId: null,
                        message: errorMsg,
                        raw: data
                    };
                }
            }
        } catch (error) {
            if (attempt === retries) {
                return {
                    success: false,
                    requestId: null,
                    message: `Network error: ${error.message}`,
                    raw: { error: error.message }
                };
            }
            // Wait before retry (exponential backoff)
            await sleep(1000 * Math.pow(2, attempt - 1));
        }
    }

    return {
        success: false,
        requestId: null,
        message: 'Max retries exceeded',
        raw: {}
    };
}

// Send bulk SMS
async function sendBulkSMS(data, apiKey, scheduleTime = '', onProgress = null) {
    const results = [];
    const startTime = new Date();

    for (let i = 0; i < data.length; i++) {
        const row = data[i];
        const rowNum = i + 1;
        const mobile = row.mobile.toString().trim();

        // Validate mobile number
        if (!isValidMobile(mobile)) {
            results.push({
                row: rowNum,
                mobile: mobile,
                template_id: row.template_id,
                status: 'FAIL',
                request_id: '',
                message: 'Invalid mobile number',
                timestamp: new Date().toISOString()
            });
            if (onProgress) onProgress(rowNum, data.length, 'FAIL', mobile);
            continue;
        }

        // Get and validate template
        const templateId = parseInt(row.template_id);
        if (!isValidTemplateId(templateId)) {
            results.push({
                row: rowNum,
                mobile: mobile,
                template_id: row.template_id,
                status: 'FAIL',
                request_id: '',
                message: `Invalid template ID: ${row.template_id}`,
                timestamp: new Date().toISOString()
            });
            if (onProgress) onProgress(rowNum, data.length, 'FAIL', mobile);
            continue;
        }

        const template = TEMPLATES[templateId];

        // Build variables
        const vars = [];
        for (let j = 1; j <= template.vars; j++) {
            const val = (row[`v${j}`] || '').toString().trim();
            vars.push(val === 'N/A' || val === 'n/a' || val === 'null' ? '' : val);
        }
        const varsString = vars.join('|');

        // Build payload
        const payload = {
            route: 'dlt',
            sender_id: template.sender,
            message: templateId.toString(),
            variables_values: varsString,
            numbers: mobile,
            flash: '0'
        };

        // Add schedule time if provided
        if (scheduleTime) {
            payload.schedule_time = scheduleTime;
        }

        // Check if unicode is needed
        if (needUnicode(template.text + varsString)) {
            payload.language = 'unicode';
        }

        // Send SMS
        const result = await sendSMSWithRetry(payload, apiKey);

        results.push({
            row: rowNum,
            mobile: mobile,
            template_id: templateId,
            status: result.success ? 'SUCCESS' : 'FAIL',
            request_id: result.requestId || '',
            message: result.message,
            timestamp: new Date().toISOString(),
            raw_response: JSON.stringify(result.raw)
        });

        if (onProgress) {
            onProgress(rowNum, data.length, result.success ? 'SUCCESS' : 'FAIL', mobile);
        }

        // Small delay to avoid rate limiting
        await sleep(200);
    }

    const endTime = new Date();
    const duration = (endTime - startTime) / 1000;

    return {
        results: results,
        duration: duration,
        total: data.length,
        success: results.filter(r => r.status === 'SUCCESS').length,
        failed: results.filter(r => r.status === 'FAIL').length
    };
}
