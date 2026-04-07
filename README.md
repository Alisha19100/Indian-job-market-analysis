# Indian-job-market-analysis
End-to-end data analysis project on India's job market with an interactive Streamlit dashboard and ML-based salary prediction model.
# India Job Market Dashboard

An interactive Streamlit dashboard for analyzing **97,000+ Indian job postings**, featuring skill-based job recommendations, salary prediction, resume gap analysis, role comparisons, and company intelligence — all in a sleek dark theme.

---

##  Features Overview

| Feature | Description |
|---|---|
|  Market Overview | Top skills, job distribution by city, company analysis |
|  Salary Analysis | Salary by city, experience level, and company rating |
|  Job Recommender | Enter your skills → get matching job postings |
|  Resume Skill Gap Analyzer | Paste a JD → see what skills you're missing |
|  Salary Predictor | Predict salary by role, city, and years of experience |
|  Role Comparator | Side-by-side comparison of any two job roles |
|  Company Deep Dive | Complete hiring intelligence for any company |

---

##  Project Structure

```
project/
│
├── app.py                  # Main Streamlit application
│
├── data/
│   ├── df_tech_clean.csv   # Cleaned tech job postings (~97k rows)
│   ├── df_salary.csv       # Jobs with salary data
│   ├── df_tech_salary.csv  # Tech jobs with salary info
│   ├── df_rated.csv        # Jobs from rated companies
│   ├── job_titles.csv      # List of job titles (for salary predictor)
│   └── cities.csv          # List of cities (for salary predictor)
│
└── model/
    ├── salary_model.pkl    # Trained ML salary prediction model
    ├── le_title.pkl        # LabelEncoder for job titles
    └── le_city.pkl         # LabelEncoder for cities
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/india-job-market-dashboard.git
cd india-job-market-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**Required libraries:**

```
streamlit
pandas
plotly
scikit-learn
```

### 3. Prepare the data

Place the following CSV files inside a `data/` folder:

- `df_tech_clean.csv`
- `df_salary.csv`
- `df_tech_salary.csv`
- `df_rated.csv`
- `job_titles.csv`
- `cities.csv`

> **Data Source:** Kaggle — Indian Job Market dataset (~97,000 job postings)

### 4. Train the salary model (if not already done)

Run your model training notebook to generate and save the following files inside a `model/` folder:

- `salary_model.pkl`
- `le_title.pkl`
- `le_city.pkl`

> If the model files are missing, the Salary Predictor section will show a warning but the rest of the dashboard will still work.

### 5. Run the app

```bash
streamlit run app.py
```

---

##  Feature Details

### Market Overview
Displays 4 top-level KPI metrics (total postings, unique companies, cities, avg salary), followed by:
- Top 20 in-demand skills across all industries
- Top skills filtered by city/experience (sidebar filters)
- Job openings by city (map-style bar chart)
- Salary by city and experience level

###  Job Recommender
Enter your skills (comma-separated) and set a minimum match threshold. The recommender:
- Scores every job posting based on skill overlap
- Shows top matching roles, companies, and cities
- Displays expected salary range
- Lists related skills to learn next

###  Resume Skill Gap Analyzer
Paste any job description + enter your current skills. The analyzer:
- Extracts skills from the JD using a master skill list (80+ tech skills)
- Shows your match score (0–100%) with a progress bar
- Lists matched skills , missing skills , and bonus skills 
- Provides a visual skill gap bar chart
- Suggests learning resources for missing skills
- Finds similar jobs in the dataset matching your profile

### Salary Predictor
Select a job role, city, and years of experience. The predictor:
- Uses a trained ML model to predict salary in LPA
- Shows minimum / predicted / maximum expected salary
- Plots a salary growth projection curve from 0–20 years
- Compares the same role's salary across all cities

###  Role Comparator
Select two job roles side by side:
- Total openings, average salary, and average experience comparison
- Experience distribution (box plot) and top cities (grouped bar chart)
- Common skills, role-exclusive skills
- A "Which role should you choose?" recommendation section

###  Company Deep Dive
Select any company from the top 100 hiring companies:
- Total openings, cities, unique roles, avg salary, company rating
- Top roles and top skills required at that company
- City-wise hiring map, experience distribution pie chart
- Salary distribution and salary by experience level
- "How to get hired" guide with must-have skills and best roles to target

---

##  Sidebar Filters

The sidebar lets you filter the entire dashboard by:
- **City** — top 15 cities by job count
- **Experience Level** — Fresher / Junior / Mid / Senior / Expert

---

##  Data Preprocessing (in `load_data()`)

- City normalization: aliases like `Bengaluru → Bangalore`, `Gurugram → Gurgaon`, hybrid/remote variants mapped to clean city names
- Region mapping: cities grouped into South / North / West / East / Remote
- Experience categorization: `avgExperience` bucketed into 5 labeled bands
- Salary conversion: `avgSalary` (in ₹) → `avgSalary_LPA` (in lakhs)

---

##  Key Insights (from the data)

- **Bengaluru** leads in both job count and average salary
- **Python & SQL** are the most in-demand tech skills
- **Junior & Mid-level** roles make up ~65% of all openings
- **Accenture & Wipro** dominate tech hiring volume
- Higher-rated companies tend to offer better salaries
- **Data Engineer** is the top pure-data role in demand

---
