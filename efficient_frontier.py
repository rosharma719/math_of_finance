import numpy as np
import matplotlib.pyplot as plt

# Given data for Asset 1 and Asset 2
mu1 = 0.04  # Expected return of Asset 1 (4%)
sigma1 = 0.10  # Standard deviation of Asset 1 (10%)
mu2 = 0.06  # Expected return of Asset 2 (6%)
sigma2 = 0.06  # Standard deviation of Asset 2 (6%)
rho = 0.25  # Correlation between Asset 1 and Asset 2

# Covariance between Asset 1 and Asset 2
cov12 = rho * sigma1 * sigma2

# Create a range of portfolio weights for Asset 1 (w1), from -0.5 to 1.5 to show shorting and over-investing
w1 = np.linspace(-0.5, 1.5, 300)
w2 = 1 - w1  # Weight for Asset 2

# Portfolio returns and standard deviations
portfolio_return = w1 * mu1 + w2 * mu2
portfolio_variance = (w1**2 * sigma1**2) + (w2**2 * sigma2**2) + (2 * w1 * w2 * cov12)
portfolio_std = np.sqrt(portfolio_variance)

# Calculate the weights of the Minimum Variance Portfolio (MVP)
w1_mvp = (sigma2**2 - cov12) / (sigma1**2 + sigma2**2 - 2 * cov12)
w2_mvp = 1 - w1_mvp

# Return and standard deviation of the MVP
mu_mvp = w1_mvp * mu1 + w2_mvp * mu2
sigma_mvp = np.sqrt(w1_mvp**2 * sigma1**2 + w2_mvp**2 * sigma2**2 + 2 * w1_mvp * w2_mvp * cov12)

# Plot the efficient frontier (feasible set)
plt.figure(figsize=(10, 6))
plt.plot(portfolio_std, portfolio_return, label="Feasible Set (Efficient Frontier)", color='blue')

# Highlight the upper part (efficient frontier) by filtering where returns are above MVP
plt.plot(portfolio_std[portfolio_return >= mu_mvp], portfolio_return[portfolio_return >= mu_mvp], color='green', label="Efficient Frontier", linewidth=2)

# Plot the Minimum Variance Portfolio (MVP)
plt.scatter(sigma_mvp, mu_mvp, color='red', label="MVP", zorder=5)
plt.text(sigma_mvp, mu_mvp, '  MVP', fontsize=12, verticalalignment='bottom')

# Set plot labels and title
plt.title("Feasible Set and Minimum Variance Portfolio (MVP)")
plt.xlabel("Portfolio Risk (Standard Deviation)")
plt.ylabel("Portfolio Return")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Output the MVP weights, return, and risk
print(f"Minimum Variance Portfolio Weights: w1* = {w1_mvp:.4f}, w2* = {w2_mvp:.4f}")
print(f"Minimum Variance Portfolio Return: {mu_mvp:.4%}")
print(f"Minimum Variance Portfolio Standard Deviation: {sigma_mvp:.4%}")
