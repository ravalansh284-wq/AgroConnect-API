import time

def send_order_confirmation(email: str,order_id: int):
    
    print(f"--- [Background Task Started] Generating Invoice for Order #{order_id} ---")

    time.sleep(5)

    print(f"--- [Background Task Finished] Email sent to {email} for Order #{order_id} ---")
    return True