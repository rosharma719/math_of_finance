import numpy as np
import pandas as pd
from scipy.optimize import newton

# Hardcoded discount factors we know at specific points (0.5, 2, 3, 5, 7, 10 years)
known_discount_factors = {
    0.5: 0.9962083,  # 6m T-Bill
    2: 0.9724397,    # 2y Treasury
    3: 0.9424406,    # 3y Treasury
    5: 0.8839327,    # 5y Treasury
    7: 0.8172758,    # 7y Treasury
    10: 0.7219367    # 10y Treasury
}

# Interpolate discount factors (log-linear)
def interpolate_discount_factors(known_factors, method='log-linear', max_years=10):
    times = np.array(list(known_factors.keys()))
    factors = np.array(list(known_factors.values()))
    semiannual_periods = np.arange(0.5, max_years + 0.5, 0.5)

    if method == 'linear':
        interpolated_factors = np.interp(semiannual_periods, times, factors)
    elif method == 'log-linear':
        log_factors = np.log(factors)
        interpolated_log_factors = np.interp(semiannual_periods, times, log_factors)
        interpolated_factors = np.exp(interpolated_log_factors)

    return pd.Series(interpolated_factors, index=semiannual_periods)

# Perform log-linear interpolation
log_linear_interpolated_factors = interpolate_discount_factors(known_discount_factors, method='log-linear')

# Print out interpolated discount factors for each semiannual period
print("Interpolated Discount Factors (Log-Linear):")
print(log_linear_interpolated_factors)

# Bond Pricing using the exact formula
def price_bond_with_discount_factors(coupon_rate, discount_factors, maturity=5, periods_per_year=2):
    """Calculate bond price based on coupon rate using interpolated discount factors."""
    periods = maturity * periods_per_year  # Total number of periods (semiannual)
    coupon_payment = coupon_rate / periods_per_year  # Semiannual coupon payment
    price = 0

    # Sum the discounted coupon payments using appropriate discount factors
    for i in range(1, periods + 1):
        discount_factor = discount_factors[i / periods_per_year]
        price += coupon_payment * discount_factor

    # Add the discounted principal repayment
    price += 100 * discount_factors[maturity]

    return price

# Function to calculate semiannual yield using Newton's method
def convert_price_to_yield(price, coupon_rate, maturity=5, periods_per_year=2):
    """Convert bond price to yield using the classical bond pricing formula and Newton's method."""
    periods = maturity * periods_per_year
    coupon_payment = coupon_rate / periods_per_year  # Semiannual coupon payment
    
    # Define the bond price equation to solve for yield
    def price_for_yield(y):
        bond_price = sum([coupon_payment / (1 + y / periods_per_year) ** i for i in range(1, periods + 1)])
        bond_price += 100 / (1 + y / periods_per_year) ** periods
        return bond_price - price  # Return the difference from the given price
    
    # Use Newton's method to solve for the yield
    initial_guess = 0.03  # Starting guess for the yield
    bond_yield = newton(price_for_yield, initial_guess)

    return bond_yield * periods_per_year  # Annualized yield

# Calculate bond prices using interpolated discount factors
price_1_percent = price_bond_with_discount_factors(1, log_linear_interpolated_factors)
price_8_percent = price_bond_with_discount_factors(8, log_linear_interpolated_factors)

# Print bond prices
print(f"\nPrice of 5-year bond with 1% coupon (log-linear): {price_1_percent:.5f}")
print(f"Price of 5-year bond with 8% coupon (log-linear): {price_8_percent:.5f}")

# Convert bond prices to yields using Newton's method
yield_1_percent = convert_price_to_yield(price_1_percent, 1)
yield_8_percent = convert_price_to_yield(price_8_percent, 8)

# Print the calculated semiannual yields
print(f"\nSemiannual yield for 1% bond: {yield_1_percent * 100:.5f}%")
print(f"Semiannual yield for 8% bond: {yield_8_percent * 100:.5f}%")

# Compute zero-coupon rates based on interpolated discount factors
def calculate_zero_coupon_yield(df):
    """Calculate the zero-coupon yield based on interpolated discount factors."""
    return (-2 * np.log(df)) / df.index

log_linear_zcb_yields = calculate_zero_coupon_yield(log_linear_interpolated_factors)

# Print out zero-coupon rates
print("\nCorresponding Zero-Coupon Yields (Log-Linear):")
print(log_linear_zcb_yields * 100)  # Multiply by 100 to display yields as percentages
