import pandas as pd

df = pd.read_csv("data.csv")

print("\n📊 Data Preview")
print(df.head())

print("\n❌ Mistake Types")
print(df[df["Status"] == "Wrong"]["ErrorType"].value_counts())

print("\n📚 Topic Accuracy")
print(df.groupby("Topic")["Status"].apply(lambda x: (x=="Correct").mean()*100))

print("\n⏱️ Average Time on Wrong Answers")
print(df[df["Status"]=="Wrong"]["TimeSpent"].mean())