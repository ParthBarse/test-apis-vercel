import pygsheets
import pandas as pd

# Authorization
gc = pygsheets.authorize(service_file='creds.json')

# Define the data
data = [
    {
      "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
      "productName": "Masala Dosa",
      "productPrice": "120",
      "productTotalPrice": 240,
      "quantity": 2,
      "username": "testUser"
    },
    {
      "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
      "productName": "Soda",
      "productPrice": "40",
      "productTotalPrice": 80,
      "quantity": 2,
      "username": "testUser"
    },
    {
      "pic_url": "https://media.istockphoto.com/id/962353378/vector/fast-food-line-icon.jpg?s=612x612&w=0&k=20&c=xD9-KlVj_w4hqhlB6VnsnTqcaumATgDnywNdhrhOok4=",
      "productName": "Pizza",
      "productPrice": "200",
      "productTotalPrice": 600,
      "quantity": 3,
      "username": "testUser"
    }
]

# Convert data to DataFrame
df = pd.DataFrame(data)

# Open the Google spreadsheet (where 'Stall-management-data' is the name of my sheet)
sh = gc.open('Stall-management-data')

# Select the first sheet
wks = sh[0]

# Get existing data from the worksheet
existing_data = wks.get_all_records()

# Combine existing data with the new data
combined_data = existing_data + data

# Convert combined data to DataFrame
df_combined = pd.DataFrame(combined_data)

# Update the entire worksheet with the combined data
wks.set_dataframe(df_combined, start='A1')
