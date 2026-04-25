import pandas as pd

# Load dataset
df = pd.read_csv("data/Data_Science_Jobs_in_India.csv")

# STEP 1: Remove useless column
df = df.drop(columns=['Unnamed: 0'])

# STEP 2: Clean salary columns
df['avg_salary'] = df['avg_salary'].str.replace('L', '').astype(float)
df['min_salary'] = df['min_salary'].str.replace('L', '').astype(float)
df['max_salary'] = df['max_salary'].str.replace('L', '').astype(float)

# STEP 3: Basic insights (optional)
print("\nMost Common Job Roles:\n")
print(df['job_title'].value_counts())

print("\nAverage Salary by Role:\n")
print(df.groupby('job_title')['avg_salary'].mean().sort_values(ascending=False))

print("\nExperience vs Salary:\n")
print(df.groupby('min_experience')['avg_salary'].mean())

# STEP 4: Skill mapping
skill_map = {
    "Data Scientist": ["python", "machine learning", "statistics"],
    "Data Analyst": ["excel", "sql", "tableau"],
    "Data Engineer": ["python", "sql", "big data"],
    "Machine Learning Engineer": ["python", "machine learning", "deep learning"],
    "Business Analyst": ["excel", "communication", "sql"]
}

# STEP 5: User input
exp = int(input("\nEnter your years of experience: "))

skills_input = input("\nEnter your skills (comma separated): ").lower()
user_skills = [skill.strip() for skill in skills_input.split(',')]

# STEP 6: Filter based on experience (fixed edge case)
filtered = df[(df['min_experience'] <= exp) & 
              (df['min_experience'] >= max(0, exp - 1))]

# Remove unrealistic roles for low experience
if exp < 3:
    filtered = filtered[~filtered['job_title'].str.contains('Senior')]

# STEP 7: Skill matching
score = {}

for role, skills in skill_map.items():
    match = len(set(skills) & set(user_skills))
    score[role] = match

# STEP 8: Salary-based recommendation
recommendation = filtered.groupby('job_title')['avg_salary'].mean().sort_values(ascending=False)

# Convert score dict to DataFrame
score_df = pd.DataFrame(list(score.items()), columns=['job_title', 'skill_score'])

# Merge skill + salary
final = pd.merge(recommendation.reset_index(), score_df, on='job_title')

# Keep only relevant roles (skill match > 0)
final = final[final['skill_score'] > 0]

# Sort by skill match first, then salary
final = final.sort_values(by=['skill_score', 'avg_salary'], ascending=False)

# STEP 9: Final Output (safe)
if final.empty:
    print("\nNo matching roles found. Try adding more relevant skills.")
else:
    print("\nFinal AI-Based Recommendations:\n")
    for index, row in final.head(5).iterrows():
        print(f"{row['job_title']} → Skill Match: {row['skill_score']} | Avg Salary: {round(row['avg_salary'], 2)} LPA")

# STEP 10: Salary Insights
print("\nExpected Salary Range:\n")
print(filtered['avg_salary'].describe())
