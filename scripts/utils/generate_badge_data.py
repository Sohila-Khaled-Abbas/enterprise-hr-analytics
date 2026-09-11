# scripts/utils/generate_badge_data.py
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_badge_payload(output_path: str, target_month: str):
    """Generates a JSON array representing API badge logs for 7000 employees."""
    start_date = datetime.strptime(f"{target_month}-01", "%Y-%m-%d")
    days_in_month = 31 # May has 31 days
    
    # Same IDs from the HR flat file
    emp_ids = [f"EMP-{10000 + i}" for i in range(1, 7001)]
    buildings = ["HQ-CAIRO", "TECH-GIZA", "OPS-ALEX", "REMOTE-VPN"]
    
    logs = []
    log_counter = 1
    
    for emp in emp_ids:
        # Ghost worker simulation: 2% of active employees have no logs
        if random.random() < 0.02:
            continue
            
        for day_offset in range(days_in_month):
            current_date = start_date + timedelta(days=day_offset)
            is_weekend = current_date.weekday() >= 4 # Friday (4) and Saturday (5) in Egypt
            
            # Skip most weekends
            if is_weekend and random.random() < 0.95:
                continue
                
            # Random arrival between 7:30 AM and 10:30 AM
            arrival_hour = random.randint(7, 10)
            arrival_minute = random.randint(0, 59)
            check_in = current_date.replace(hour=arrival_hour, minute=arrival_minute)
            
            # 5% chance of forgetting to check out
            forgot_checkout = random.random() < 0.05
            if forgot_checkout:
                check_out_str = None
            else:
                work_duration = random.randint(6, 10)
                check_out = check_in + timedelta(hours=work_duration, minutes=random.randint(0, 59))
                check_out_str = check_out.strftime("%Y-%m-%dT%H:%M:%SZ")

            building = random.choice(buildings)
            
            # Create nested JSON structure typical of APIs
            logs.append({
                "meta": {
                    "log_id": f"LOG-{log_counter}",
                    "source": "TURNSTILE" if building != "REMOTE-VPN" else "GATEWAY"
                },
                "event": {
                    "employee_id": emp,
                    "access_date": current_date.strftime("%Y-%m-%d"),
                    "facility_code": building,
                    "timestamps": {
                        "first_in": check_in.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "last_out": check_out_str
                    }
                }
            })
            log_counter += 1

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"data": logs}, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(logs)} badge events for {target_month}.")

if __name__ == "__main__":
    generate_badge_payload("data/raw/api_badge_logs_202605.json", "2026-05")
