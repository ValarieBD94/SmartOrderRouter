# Smart Order Router – Backtesting Project

This project implements a simplified Smart Order Router (SOR) backtesting engine based on the static cost model described in *Cont & Kukanov (2013), "Optimal Order Placement in Limit Order Markets"*. It simulates how a large buy order can be optimally allocated across multiple trading venues using historical Level 1 (L1) market data.

---

## 📁 Project Structure


---

## ⚙️ What It Does

The backtesting engine performs the following steps:

1. **Data Preprocessing**  
   Loads the CSV file (`l1_day.csv`), sorts it by timestamp and venue, removes duplicate venue quotes per timestamp, and creates a list of market "snapshots."

2. **Static Cost Model Allocation**  
   Based on a simplified version of the Cont-Kukanov model, the system decides how to allocate portions of the total order to each venue. It penalizes overfilling shallow venues and rewards efficient use of liquidity.

3. **Simulated Execution**  
   The router simulates placing the order, calculates the shares filled at each venue, and tracks the total cash spent.

4. **Performance Reporting**  
   At the end, it prints:
   - The model parameters used (`lambda_over`, `lambda_under`, `theta_queue`)
   - Total cash spent
   - Average price per share filled

---

## 🧪 How to Run the Project

### Requirements

- Python 3.8+
- `pandas`

You can install dependencies via pip:

```bash
pip install pandas
