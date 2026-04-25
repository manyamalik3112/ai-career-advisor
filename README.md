# 📊 AI Career Advisor Dashboard

## 🚀 Overview

This project is an interactive **data analytics + career recommendation system** that analyzes Data Science job trends in India and suggests personalized career paths based on user skills.

It combines **data analysis, visualization, and rule-based AI logic** to simulate how real-world career recommendation systems work.

---

## 🎯 Problem Statement

Students often struggle to:

* Understand salary trends across data roles
* Identify which role matches their skills
* Know what skills they are missing

This project solves that by providing **data-driven career insights + recommendations**.

---

## ⚙️ Features

### 📊 Data Analysis Dashboard

* Salary distribution across roles
* Average salary comparison by job title
* Experience vs salary trends

### 🤖 AI Career Advisor

* Skill-based role recommendation
* Weighted skill matching algorithm
* Top 5 career suggestions

### 📚 Skill Gap Analysis

* Identifies missing skills for each role
* Helps users plan learning roadmap

### 🎯 Smart Filtering

* Filter by:

  * Experience level
  * Salary range
  * Job roles

---

## 🛠️ Tech Stack

* **Python**
* **Pandas** – data processing
* **Matplotlib** – data visualization
* **Streamlit** – interactive dashboard

---

## 🧠 How It Works

1. **Data Cleaning**

   * Removes unnecessary columns
   * Converts salary strings → numeric values

2. **Exploratory Analysis**

   * GroupBy operations for salary insights
   * Aggregation by job roles & experience

3. **Recommendation Engine**

   * Predefined skill-role mapping
   * Weighted scoring system:

     * Core skills (Python, ML) → higher weight
     * Supporting skills → lower weight

4. **Final Ranking**

   * Combines:

     * Skill match score
     * Average salary
   * Outputs top career options

---

## 📂 Dataset

* Data Science Jobs in India (CSV)

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Demo Preview

(Add screenshots here after deployment)

---

## 🌐 Future Improvements

* Resume upload → automatic skill extraction
* ML-based recommendation system
* Real-time job API integration
* Better UI/UX with advanced charts

---

## 👩‍💻 Author

**Manya Malik**

---

## ⭐ Why This Project Matters

This project demonstrates:

* Real-world data analysis workflow
* Business understanding of salary trends
* Practical implementation of recommendation logic

---

## 🔗 Live App

(Add your Streamlit link here after deployment)
