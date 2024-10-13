# Bond parameters
face_value = 100  # Face value of the bond
coupon_rate = 0.02  # Annual coupon rate (2%)
semiannual_coupon = (coupon_rate / 2) * face_value  # Semiannual coupon payment
market_price = 98  # The bond is trading at 98%
years = 5  # 5-year bond
num_periods = years * 2  # Semiannual periods

# Function to calculate bond price given a yield
def bond_price(yield_semi):
    price = 0
    for t in range(1, num_periods + 1):
        price += semiannual_coupon / (1 + yield_semi)**t
    price += face_value / (1 + yield_semi)**num_periods
    return price

# Bisection method to find the yield
def bisection_method(low, high, tolerance=1e-4):
    while (high - low) > tolerance:
        mid = (low + high) / 2
        price_mid = bond_price(mid)
        
        if price_mid < market_price:
            high = mid
        else:
            low = mid
    return mid

# Running the bisection method
semiannual_yield = bisection_method(0.0, 0.10, 1e-4)
print(f"Semiannual Yield: {semiannual_yield:.6f}")
