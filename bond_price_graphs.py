import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Set the start and end dates
start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 12, 31)

# Generate all dates between start and end
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Manually set coupon payment dates
coupon_dates = [datetime(2020, 1, 1), datetime(2020, 7, 1), datetime(2021, 1, 1), datetime(2021, 7, 1), datetime(2022, 1, 1)]

# Bond parameters
face_value = 1000  # Par value ($1000)
coupon_rate = 0.04  # 4% annual coupon rate
coupon_frequency = 2  # Semi-annual coupon payments
ytm = 0.04  # Yield to maturity (e.g., 5% for discount, 3% for premium)

# Initialize lists for bond prices
clean_prices = []
dirty_prices = []
accrued_interest_list = []

# Function to calculate clean price based on YTM
def calculate_clean_price(face_value, coupon_rate, coupon_frequency, ytm, remaining_periods):
    coupon_payment = (coupon_rate / coupon_frequency) * face_value
    clean_price = (coupon_payment * (1 - (1 + ytm / coupon_frequency) ** (-remaining_periods))) / (ytm / coupon_frequency)
    clean_price += face_value / (1 + ytm / coupon_frequency) ** remaining_periods
    return clean_price

# Iterate through all dates and calculate prices
for date in dates:
    last_coupon_date = max([d for d in coupon_dates if d <= date])
    next_coupon_date = min([d for d in coupon_dates if d > last_coupon_date])
    days_since_last_coupon = (date - last_coupon_date).days
    days_in_period = (next_coupon_date - last_coupon_date).days
    remaining_periods = coupon_frequency * ((end_date - date).days / 365)

    # Calculate accrued interest
    coupon_payment = (coupon_rate / coupon_frequency) * face_value  # Semi-annual coupon payment
    accrued_interest = (days_since_last_coupon / days_in_period) * coupon_payment

    # If it's a coupon date, reset accrued interest to zero
    if date in coupon_dates:
        accrued_interest = 0

    # Calculate clean price based on YTM
    clean_price = calculate_clean_price(face_value, coupon_rate, coupon_frequency, ytm, remaining_periods)
    
    # Calculate dirty price (clean price + accrued interest)
    dirty_price = clean_price + accrued_interest

    # Append results to lists
    clean_prices.append(clean_price)
    dirty_prices.append(dirty_price)
    accrued_interest_list.append(accrued_interest)

# Create a DataFrame with the results
df_bond_prices = pd.DataFrame({
    'Date': dates,
    'Days Since Last Coupon': [(date - max([d for d in coupon_dates if d <= date])).days for date in dates],
    'Clean Price': clean_prices,
    'Accrued Interest': accrued_interest_list,
    'Dirty Price': dirty_prices
})

# Print the DataFrame as a full table (optional)
print(df_bond_prices.to_string(index=False))

# Plot the clean and dirty prices
plt.figure(figsize=(10, 6))
plt.plot(df_bond_prices['Date'], df_bond_prices['Clean Price'], label='Clean Price', linestyle='-', color='blue')
plt.plot(df_bond_prices['Date'], df_bond_prices['Dirty Price'], label='Dirty Price', linestyle='--', color='orange')

# Set plot title and labels dynamically based on the parameters
plt.title(f'Daily Bond Prices from {start_date.strftime("%m/%d/%Y")} to {end_date.strftime("%m/%d/%Y")} \n'
          f'(Coupon Rate: {coupon_rate*100:.2f}%, YTM: {ytm*100:.2f}%, Face Value: ${face_value})')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.axhline(y=face_value, color='red', linestyle=':')  # Horizontal line at par value for reference

# Add grid and legend
plt.grid(True)
plt.legend()

# Adjust the layout to prevent overlap of elements
plt.tight_layout()

# Show the plot
plt.show()
