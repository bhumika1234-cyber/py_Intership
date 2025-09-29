import pandas as pd
import matplotlib.pyplot as plt

data = {
    "Product": ["Laptop", "Mobile", "Tablet", "Laptop", "Mobile", "Tablet", "Laptop", "Mobile"],
    "Region": ["North", "South", "East", "West", "North", "South", "East", "West"],
    "Sales": [1200, 800, 400, 1000, 1500, 700, 1300, 900]
}

df = pd.DataFrame(data)

# Save as CSV (optional) so you can reload
df.to_csv("sales.csv", index=False)

print("Sample Data:")
print(df)

sales_by_product = df.groupby("Product")["Sales"].sum()
print("\nSales by Product:")
print(sales_by_product)

# Plot: Bar Chart for Product Sales
sales_by_product.plot(kind='bar', color='skyblue', figsize=(7,5))
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.show()

sales_by_region = df.groupby("Region")["Sales"].sum()
print("\nSales by Region:")
print(sales_by_region)

sales_by_region.plot(kind='pie', autopct='%1.1f%%', figsize=(6,6))
plt.title("Sales Distribution by Region")
plt.ylabel("")
plt.show()






