import pandas as pd

# Load CSV with no headers (columns will be numbered 0, 1, 2, ..., etc.)
df = pd.read_csv("data.dat", header=None, delim_whitespace=True)

# Divide column 8 (index 7) by column 34 (index 33)
# Use `.astype(float)` if needed to ensure numeric division
age_col = 66
disk_col = 7
env_col = 33

df[age_col] = df[age_col].astype(float)

# Filter Class 0: age < 1e5
class_0 = df[df[age_col] < 1e5][[disk_col, env_col, age_col]].copy()
class_0['ratio'] = class_0[disk_col] / class_0[env_col]
class_0 = class_0[[env_col, disk_col, 'ratio', age_col]]
class_0.columns = ['M_env', 'M_disk', 'M_disk/M_env', 'Age(yrs)']


# Filter Class I: 1e5 ≤ age < 2e5
class_1 = df[(df[age_col] >= 1e5) & (df[age_col] < 3e5)][[disk_col, env_col, age_col]].copy()
class_1['ratio'] = class_1[disk_col] / class_1[env_col]
class_1 = class_1[[env_col, disk_col, 'ratio', age_col]]
class_1.columns = ['M_env', 'M_disk', 'M_disk/M_env', 'Age(yrs)']

# result_0 = class_0[0] / class_0[1]

print(class_0.shape)
print(class_1.shape)

# header = "M_env, M_disk, ratio, Age(yrs)"
class_0.to_csv("class_0_stage.csv", index=False)
class_1.to_csv("class_1_stage.csv", index=False)
