# 🚀 AI-Powered DDR Report Generator

## 📌 Overview

This project is an AI-powered Streamlit application that automates the generation of a **Detailed Diagnostic Report (DDR)** from technical documents such as **site inspection reports** and **thermal imaging reports**.

Traditionally, engineers manually analyze these reports, correlate observations with thermal data, and prepare a final document — a process that is time-consuming and error-prone.

This system automates the entire workflow and generates a **structured, client-ready dashboard**.

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **PDF Processing:** PyMuPDF
* **AI Model:** Google Gemini 1.5 Pro (Multimodal)
* **Image Processing:** PIL / OpenCV (if used)

---

## 🔄 Workflow

### 1️⃣ Data Extraction

* Upload inspection and thermal PDF reports
* Extract:

  * Text data (observations, notes)
  * Embedded images (thermal visuals)
* Tool used: **PyMuPDF**

---

### 2️⃣ AI Processing

* Extracted data is sent to **Gemini 1.5 Pro**
* Uses structured prompting to:

  * Identify issues
  * Determine root causes
  * Map images to observations
* Output is generated in **structured JSON format**

---

### 3️⃣ Dashboard Rendering

* JSON output is visualized using **Streamlit**
* Features:

  * Color-coded severity levels
  * Structured report sections
  * Relevant thermal images alongside insights

---

## 📊 DDR Output Structure

The generated report includes:

* Property Issue Summary
* Area-wise Observations
* Probable Root Cause
* Severity Assessment (with reasoning)
* Recommended Actions
* Additional Notes
* Missing / Unclear Information

---

## ⚠️ Limitations

* Works only with **PDF files**
* Performance depends on **PDF structure quality**
* Large documents may hit **token limits**
* Image extraction may fail for poorly formatted PDFs

---

## 🔮 Future Improvements

* Implement **RAG (Retrieval-Augmented Generation)** for better accuracy
* Add **Database & Authentication system**
* Enable **PDF export of final report**
* Support for **multiple document formats (Word, Excel)**

---

## 🔐 Environment Variables

Create a `.env` file and add:

```
API_KEY=your_api_key_here
```

---

## 💡 Key Highlights

* End-to-end AI workflow automation
* Multimodal AI (text + images)
* Real-world problem solving
* Clean and structured output generation

---

## 🎯 Conclusion

This project demonstrates how **multimodal AI + document processing + real-time dashboards** can automate complex technical workflows and significantly reduce manual effort.

---

