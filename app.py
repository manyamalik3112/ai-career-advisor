import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Career Advisor", layout="wide")

st.markdown("""
# 📊 AI Career Advisor  
### 🚀 Analyze job trends & get personalized career recommendations  

This dashboard helps you:
- 📈 Understand salary trends  
- 🎯 Discover best-fit roles  
- 📚 Identify skill gaps  
""")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/Data_Science_Jobs_in_India.csv")

# Clean data
df = df.drop(columns=['Unnamed: 0'], errors='ignore')

for col in ['avg_salary', 'min_salary', 'max_salary']:
    df[col] = df[col].str.replace('L', '').astype(float)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

exp = st.sidebar.slider("Select Experience (Years)", 0, 20, 2)

selected_roles = st.sidebar.multiselect(
    "Select Job Roles",
    df['job_title'].unique(),
    default=df['job_title'].unique()
)

salary_range = st.sidebar.slider(
    "Select Salary Range (LPA)",
    int(df['avg_salary'].min()),
    int(df['avg_salary'].max()),
    (5, 20)
)

# Apply filters
filtered_df = df[
    (df['job_title'].isin(selected_roles)) &
    (df['avg_salary'] >= salary_range[0]) &
    (df['avg_salary'] <= salary_range[1])
]

# -----------------------------
# KPI METRICS
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Salary", f"{round(filtered_df['avg_salary'].mean(),2)} LPA")

top_role = filtered_df.groupby('job_title')['avg_salary'].mean().idxmax()
col2.metric("Top Paying Role", top_role)

col3.metric("Total Jobs", len(filtered_df))

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📊 Salary Distribution")

fig1, ax1 = plt.subplots()
ax1.hist(filtered_df['avg_salary'], bins=15)
ax1.set_title("Salary Distribution Across Roles")
ax1.set_xlabel("Salary (LPA)")
ax1.set_ylabel("Frequency")
st.pyplot(fig1)

# -----------------------------
# AVG SALARY BY ROLE
# -----------------------------
st.subheader("💰 Average Salary by Role")

role_salary = filtered_df.groupby('job_title')['avg_salary'].mean().sort_values()

fig2, ax2 = plt.subplots()
role_salary.plot(kind='barh', ax=ax2)
ax2.set_title("Average Salary by Job Role")
ax2.set_xlabel("Avg Salary (LPA)")
st.pyplot(fig2)

# -----------------------------
# EXPERIENCE VS SALARY
# -----------------------------
st.subheader("📈 Experience vs Salary")

exp_salary = df.groupby('min_experience')['avg_salary'].mean()

fig3, ax3 = plt.subplots()
exp_salary.plot(ax=ax3)
ax3.set_title("Experience vs Salary Growth")
ax3.set_xlabel("Experience (Years)")
ax3.set_ylabel("Salary (LPA)")
st.pyplot(fig3)

# -----------------------------
# DATA-DRIVEN INSIGHTS
# -----------------------------
st.subheader("📌 Data-Driven Insights")

avg_salary = df['avg_salary'].mean()
max_role = df.groupby('job_title')['avg_salary'].mean().idxmax()
growth = df.groupby('min_experience')['avg_salary'].mean().pct_change().mean()

st.write(f"• Average salary across roles is **{round(avg_salary,2)} LPA**")
st.write(f"• Highest paying role is **{max_role}**")
st.write(f"• Salary grows ~**{round(growth*100,1)}% per experience level**")

# -----------------------------
# AI CAREER ADVISOR
# -----------------------------
st.subheader("🤖 AI Career Advisor")

skills_input = st.text_input("Enter your skills (comma separated)", "python, sql")

user_skills = [s.strip().lower() for s in skills_input.split(",")]

# -----------------------------
# SKILL MAP
# -----------------------------
skill_map = {
    "Data Scientist": ["python", "machine learning", "statistics"],
    "Data Analyst": ["excel", "sql", "tableau"],
    "Data Engineer": ["python", "sql", "big data"],
    "Machine Learning Engineer": ["python", "machine learning", "deep learning"],
    "Business Analyst": ["excel", "communication", "sql"]
}

# -----------------------------
# SKILL WEIGHTS
# -----------------------------
skill_weights = {
    "python": 3,
    "sql": 3,
    "excel": 2,
    "tableau": 2,
    "power bi": 2,
    "machine learning": 4,
    "deep learning": 4,
    "statistics": 3,
    "communication": 2,
    "big data": 3
}

# -----------------------------
# SCORING SYSTEM
# -----------------------------
scores = []

for role, skills in skill_map.items():
    matched = set(skills) & set(user_skills)
    score = sum(skill_weights.get(skill, 1) for skill in matched)
    scores.append((role, score, matched))

score_df = pd.DataFrame(scores, columns=["job_title", "score", "matched_skills"])

# -----------------------------
# EXPERIENCE FILTERING
# -----------------------------
rec_df = df[(df['min_experience'] <= exp)]

if exp < 3:
    rec_df = rec_df[~rec_df['job_title'].str.contains("Senior")]

salary_df = rec_df.groupby('job_title')['avg_salary'].mean().reset_index()

# Merge
final = pd.merge(score_df, salary_df, on='job_title')

final = final[final['score'] > 0]

final = final.sort_values(by=['score', 'avg_salary'], ascending=False)

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
st.subheader("🎯 Top Career Recommendations")

for _, row in final.head(5).iterrows():
    st.write(f"**{row['job_title']}**")
    st.write(f"✔ Skill Match Score: {row['score']}")
    st.write(f"💰 Avg Salary: {round(row['avg_salary'],2)} LPA")

    required_skills = set(skill_map[row['job_title']])
    missing = required_skills - set(user_skills)

    if missing:
        st.write(f"📚 To improve, learn: {', '.join(missing)}")

    st.write("---")

# -----------------------------
# SKILL MATCH VISUALIZATION
# -----------------------------
st.subheader("📊 Skill Match Comparison")

fig4, ax4 = plt.subplots()
ax4.barh(score_df['job_title'], score_df['score'])
ax4.set_xlabel("Skill Match Score")
st.pyplot(fig4)

# -----------------------------
# PROFILE STRENGTH
# -----------------------------
st.subheader("📈 Your Profile Strength")

total_possible = sum(skill_weights.values())
user_score = sum(skill_weights.get(skill, 1) for skill in user_skills)

percent = (user_score / total_possible) * 100

st.metric("Profile Strength", f"{round(percent,1)}%")

if percent < 40:
    st.warning("You need significant upskilling")
elif percent < 70:
    st.info("You're on the right track")
else:
    st.success("Strong profile for data roles")

# -----------------------------
# DOWNLOAD FEATURE
# -----------------------------
st.subheader("📥 Download Recommendations")

csv = final.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download as CSV",
    data=csv,
    file_name='career_recommendations.csv',
    mime='text/csv',
)

# -----------------------------
# SALARY SUMMARY
# -----------------------------
st.subheader("📊 Salary Summary")

st.dataframe(df['avg_salary'].describe())
