#!/usr/bin/env python
# coding: utf-8

# ## Part 1: Explore the Data
# 
# Import the data and use Pandas to learn more about the dataset.

# In[1]:


import pandas as pd
import numpy as np

df = pd.read_csv('Resources/client_dataset.csv')

df.head()


# In[2]:


# View the column names in the data

df.columns.tolist()


# In[3]:


# Use the describe function to gather some basic statistics

df.describe()


# In[4]:


# Use this space to do any additional research
# and familiarize yourself with the data.

max_unit_price = df["unit_price"].max()
print (f'The max unit price is {max_unit_price}.')
        


# In[5]:


df.info()

df_cat_subcat_item = df[["category", "subcategory", "item_id", "qty"]]

df_cat_subcat_item

df_sorted = df.sort_values(by='qty', ascending=False)

df_sorted

df_sorted_filtered = df_sorted[["category", "subcategory", "item_id", "qty"]]

df_sorted_filtered


# In[6]:


df.dtypes


# In[7]:


# What three item categories had the most entries?

top_three_categories = df['category'].value_counts().head(3)

print("Top three item categories with the most entries:")
print(top_three_categories)



# In[8]:


# Counting the occurrences of each category and converting it to a DataFrame
category_counts = df['category'].value_counts().reset_index()

# Renaming the columns for clarity
category_counts.columns = ['category', 'count']

# Sorting by count in descending order and getting the top 3 categories
top_three_categories = category_counts.head(3).set_index('category')

print("Top three item categories with the most entries:")
top_three_categories


# In[9]:


# For the category with the most entries,
# which subcategory had the most entries?

# Identify the category with the most entries
top_category = df['category'].value_counts().idxmax()

# Filter the dataset to only include entries from the top category
top_category_data = df[df['category'] == top_category]

# Find the subcategory with the most entries within the top category
top_subcategory = top_category_data['subcategory'].value_counts().idxmax()

print(f"In the '{top_category}' category, the subcategory with the most entries is '{top_subcategory}'.")


# In[10]:


# Which five clients had the most entries in the data?

top_five_clients = df['client_id'].value_counts().head(5)

print("The top five clients with the most entries are:")
print(top_five_clients)


# In[11]:


# Store the client ids of those top 5 clients in a list.

top_five_client_ids = top_five_clients.index.tolist()
print("The client ID's of the top five clients are:", top_five_client_ids)


# In[12]:


# How many total units (the qty column) did the
# client with the most entries order order?

# Identify the client with the most entries
top_client_id = df['client_id'].value_counts().idxmax()

# Filter the DataFrame for this client
top_client_data = df[df['client_id'] == top_client_id]

# Sum the 'qty' column for this client
total_units_ordered = top_client_data['qty'].sum()

print(f"The client with the most entries (Client ID: {top_client_id}) ordered a total of {total_units_ordered} units.")


# ## Part 2: Transform the Data
# Do we know that this client spent the more money than client 66037? If not, how would we find out? Transform the data using the steps below to prepare it for analysis.

# In[13]:


# Create a column that calculates the 
# subtotal for each line using the unit_price
# and the qty

# Create a new column 'subtotal' by multiplying 'unit_price' by 'qty'
# Replace 'unit_price' and 'qty' with the actual column names if they are different
df['subtotal'] = df['unit_price'] * df['qty']

# Display DataFrame and confirm 'subtotal' appears
df.head(10)


# In[14]:


# Create a column for shipping price.
# Assume a shipping price of $7 per pound
# for orders over 50 pounds and $10 per
# pound for items 50 pounds or under.

# Calculate total weight for each line
df['total_weight'] = df['unit_weight'] * df['qty']

# Define a function to calculate shipping price based on total weight
def calculate_shipping(total_weight):
    if total_weight > 50:
        return total_weight * 7  # $7 per pound for orders over 50 pounds
    else:
        return total_weight * 10  # $10 per pound for orders 50 pounds or under

# Apply the function to calculate shipping price for each line
df['shipping_price'] = df['total_weight'].apply(calculate_shipping)

# Display the DataFrame to confirm the new columns have been added
df.head()



# In[15]:


# Create a column for the total price
# using the subtotal and the shipping price
# along with a sales tax of 9.25%

# Assuming the sales tax rate is 9.25%
sales_tax_rate = 0.0925

# Calculate the total line price
df['total_price'] = (df['subtotal'] + df['shipping_price']) * (1 + sales_tax_rate)

# Display the DataFrame to confirm the new column has been added
df.head()



# In[16]:


# Create a column for the cost
# of each line using unit cost, qty, and
# shipping price (assume the shipping cost
# is exactly what is charged to the client).

# Calculate the cost of each line
df['line_cost'] = (df['unit_cost'] * df['qty']) + df['shipping_price']

# Display the DataFrame to confirm the new column has been added
df.head()


# In[17]:


# Create a column for the profit of
# each line using line cost and line price

# Calculate the profit for each line
df['line_profit'] = df['total_price'] - df['line_cost']

# Display the DataFrame to confirm the new column has been added
df.head()


# ## Part 3: Confirm your work
# You have email receipts showing that the total prices for 3 orders. Confirm that your calculations match the receipts. Remember, each order has multiple lines.
# 
# Order ID 2742071 had a total price of \$152,811.89
# 
# Order ID 2173913 had a total price of \$162,388.71
# 
# Order ID 6128929 had a total price of \$923,441.25
# 

# In[18]:


# Check your work using the totals above

# Group by 'order_id' and sum 'total_price'
order_totals = df.groupby('order_id')['total_price'].sum()

# Compare with provided totals
provided_totals = {
    2742071: 152811.89,
    2173913: 162388.71,
    6128929: 923441.25
}

for order_id, provided_total in provided_totals.items():
    calculated_total = order_totals.get(order_id, 0)
    print(f"Order ID {order_id}: Calculated Total = ${calculated_total:.2f}, Provided Total = ${provided_total:.2f}")


# ## Part 4: Summarize and Analyze
# Use the new columns with confirmed values to find the following information.

# In[19]:


# How much did each of the top 5 clients by quantity
# spend? Check your work from Part 1 for client ids.

# List of top 5 clients by quantity
top_clients = [33615, 66037, 46820, 38378, 24741]


# In[20]:


# Create a summary DataFrame showing the totals for the
# for the top 5 clients with the following information:
# total units purchased, total shipping price,
# total revenue, and total profit. Sort by total profit.

summary_df = df[df['client_id'].isin(top_clients)].groupby('client_id').agg(
    Units=('qty', 'sum'),
    Shipping=('shipping_price', 'sum'),  # Assuming shipping is based on the provided logic
    Total_Revenue=('total_price', 'sum'),
    Total_Profit=('line_profit', 'sum')
).sort_values(by='Total_Profit', ascending=False)



# In[21]:


# Format the data and rename the columns
# to names suitable for presentation.
# Currency should be in millions of dollars.

# Converting currency to millions for the columns that exist
summary_df['Shipping'] /= 1e6
summary_df['Total_Revenue'] /= 1e6
summary_df['Total_Profit'] /= 1e6

# Renaming columns
summary_df.rename(columns={
    'Shipping': 'Shipping (M$)',
    'Total_Revenue': 'Total Revenue (M$)',
    'Total_Profit': 'Total Profit (M$)'
}, inplace=True)

# Display the formatted DataFrame
summary_df


# In[22]:


# Sort the updated data by "Total Profit" form highest to lowest

sorted_summary_df = summary_df.sort_values(by='Total Profit (M$)', ascending=False)

# Resetting the index for presentation
sorted_summary_df.reset_index(drop=True, inplace=True)

# Display the sorted DataFrame
sorted_summary_df


# In[ ]:




