# PDF_JS_Injector

A Python-based tool to create malicious PDFs with embedded JavaScript, inject payloads into existing PDFs, or extract JavaScript from suspicious files. Built for security researchers and analysts working with PDF-based attack vectors.

---

## ⚙️ Features

- 🆕 **Create** blank PDFs with embedded JavaScript payloads
- 💉 **Inject** JavaScript into existing PDF files
- 🔍 **Extract** JavaScript from potentially malicious PDFs
- 📜 Supports both inline payloads and external JS files
- 🛠 Built on PyPDF2 (v1.3 compatible)

---

## ✅ Prerequisites

Before running the script, make sure you have the following:

- **Python 3.6 or later**
- **PyPDF2 version 1.3.0**

Install the required dependency using:

```bash
pip install PyPDF2==1.3.0
```

---

## 🧪 Examples

Create a new PDF with a JS alert payload
```bash
python PDF_JS_Injector.py --payload "app.alert('JavaScript Executed!');"
```
Create using JS from a file
```bash
python PDF_JS_Injector.py --payload-file payload.js --output exploit.pdf
```
Inject JS into an existing PDF
```bash
python PDF_JS_Injector.py --inject input.pdf --payload-file payload.js --output exploit.pdf
```
Extract embedded JS from a PDF
```bash
python PDF_JS_Injector.py --extract suspicious.pdf
```
