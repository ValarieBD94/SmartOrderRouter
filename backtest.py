import pandas as pd
import json
import os

def preprocess_data(file_path):
    # Load and sort
    df = pd.read_csv(file_path)

    df = df.sort_values(by=['ts_event', 'publisher_id'])

    # Drop duplicates to keep first message per publisher_id per timestamp
    df = df.drop_duplicates(subset=['ts_event', 'publisher_id'], keep='first')

    # Group into snapshots (one per ts_event)
    snapshots = []
    for ts, group in df.groupby('ts_event'):
        snapshot = {
            row['publisher_id']: {
                'ask_px': row['ask_px_00'],
                'ask_sz': row['ask_sz_00']
            }
            for _, row in group.iterrows()
        }
        snapshots.append(snapshot)

    return snapshots

def allocate(snap, total_order, lambda_over, lambda_under, theta_queue):
    allocations = {}
    n = len(snap)
    base_alloc = total_order / n  # naive equal split

    for venue, data in snap.items():
        ask = data['ask_px']
        depth = data['ask_sz']

        cost = ask + lambda_over * max(0, base_alloc - depth) - lambda_under * min(base_alloc, depth)

        allocations[venue] = min(base_alloc, depth)

    return allocations

def backtest_main():
    # Use a relative path or configurable path to the file
    file_path = os.path.join(os.getcwd(), "l1_day.csv")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
    
    snapshots = preprocess_data(file_path)
    
    lambda_over = 0.1
    lambda_under = 0.1
    theta_queue = 0.1  # Not used in simple version

    total_order = 5000
    filled = 0
    cash_spent = 0

    for snap in snapshots:
        if filled >= total_order:
            break

        to_fill = total_order - filled
        alloc = allocate(snap, to_fill, lambda_over, lambda_under, theta_queue)

        for venue, shares in alloc.items():
            if filled >= total_order:
                break
            px = snap[venue]['ask_px']
            sz = snap[venue]['ask_sz']

            fill_qty = min(shares, sz, total_order - filled)
            if fill_qty > 0:
                filled += fill_qty
                cash_spent += fill_qty * px

    avg_price = cash_spent / filled if filled > 0 else None

    output = {
        'best_params': {
            'lambda_over': lambda_over,
            'lambda_under': lambda_under,
            'theta_queue': theta_queue
        },
        'total_cash_spent': round(cash_spent, 2),
        'avg_fill_price': round(avg_price, 4) if avg_price else None
    }

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    backtest_main()
