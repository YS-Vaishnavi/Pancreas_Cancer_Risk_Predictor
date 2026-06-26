import pandas as pd
import numpy as np

# Set random seed for reproducible results
np.random.seed(42)

num_patients = 50

# 1. Synthesize balanced random demographics
ages = np.random.randint(23, 79, size=num_patients)
genders = np.random.choice([0, 1], size=num_patients) # 0 = Male, 1 = Female

# 2. Pre-assign clinical profiles to ensure a mix of Low, Medium, and High risks
# 0 = Normal/Healthy, 1 = Borderline/Inflamed, 2 = Severe Spike
profiles = np.random.choice([0, 1, 2], size=num_patients, p=[0.5, 0.3, 0.2])

# Initialize lab arrays
ca19 = np.zeros(num_patients)
lipase = np.zeros(num_patients)
amylase = np.zeros(num_patients)
glucose = np.zeros(num_patients)
bilirubin = np.zeros(num_patients)
alt = np.zeros(num_patients)
ast = np.zeros(num_patients)
wbc = np.zeros(num_patients)

# 3. Simulate variable medical distributions based on patient risk categories
for i in range(num_patients):
    if profiles[i] == 0:  # Healthy / Low Risk parameters
        ca19[i] = np.random.randint(5, 35)
        lipase[i] = np.random.randint(20, 140)
        amylase[i] = np.random.randint(30, 120)
        glucose[i] = np.random.randint(70, 99)
        bilirubin[i] = round(np.random.uniform(0.2, 1.1), 2)
        alt[i] = np.random.randint(10, 42)
        ast[i] = np.random.randint(10, 38)
        wbc[i] = np.random.randint(4500, 10500)
    
    elif profiles[i] == 1:  # Borderline / Medium Risk parameters
        ca19[i] = np.random.randint(30, 85)
        lipase[i] = np.random.randint(130, 220)
        amylase[i] = np.random.randint(110, 180)
        glucose[i] = np.random.randint(95, 145)
        bilirubin[i] = round(np.random.uniform(1.0, 1.9), 2)
        alt[i] = np.random.randint(35, 85)
        ast[i] = np.random.randint(35, 95)
        wbc[i] = np.random.randint(9500, 13500)
        
    else:  # Severe Complications / High Risk parameters
        ca19[i] = np.random.randint(80, 480)
        lipase[i] = np.random.randint(200, 495)
        amylase[i] = np.random.randint(160, 295)
        glucose[i] = np.random.randint(130, 280)
        bilirubin[i] = round(np.random.uniform(1.8, 4.8), 2)
        alt[i] = np.random.randint(70, 190)
        ast[i] = np.random.randint(85, 195)
        wbc[i] = np.random.randint(12000, 19500)

# 4. Construct structural dataframe matching the exact pipeline schema
df_cohort = pd.DataFrame({
    "Age": ages,
    "Gender": genders,
    "CA19-9": ca19.astype(int),
    "Lipase": lipase.astype(int),
    "Amylase": amylase.astype(int),
    "Glucose": glucose.astype(int),
    "Bilirubin": bilirubin,
    "ALT": alt.astype(int),
    "AST": ast.astype(int),
    "WBC": wbc.astype(int)
})

# Save to file
output_filename = "pancreasafe_cohort_50_patients.csv"
df_cohort.to_csv(output_filename, index=False)
print(f"🎉 Success! Generated '{output_filename}' containing 50 diverse patient profiles.")