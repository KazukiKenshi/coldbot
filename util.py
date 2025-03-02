from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Detect flags -d for ERP demo, -i for interview, -p for payment followup, -o request for placing order, followed by customer index.")

    parser.add_argument("-d", type=int, help="Integer value for -d flag")
    parser.add_argument("-i", type=int, help="Integer value for -i flag")
    parser.add_argument("-p", type=int, help="Integer value for -p flag")
    parser.add_argument("-o", type=int, help="Integer value for -o flag")

    args = parser.parse_args()

    provided_flags = sum(arg is not None for arg in vars(args).values())

    if provided_flags > 1:
        parser.error("Only one flag (-d, -i, -p, -o) can be used at a time.")

    return args


def get_service_account_credentials(service_account_file,scopes):
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    return creds

def get_service(service_account_file,scopes):
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    return build("calendar", "v3", credentials=creds)

def schedule_demo(summary, start_time, end_time, email):
    service = get_service()
    
    company_calendar_id = email

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    event = service.events().insert(calendarId=company_calendar_id, body=event).execute()
    print(f"Event scheduled: {event.get('htmlLink')}")


def get_next_state(state, intent):
    if state == "DEMO_INTRO" and intent == "ASK_INFO":
        return "ASK_INFO"
    elif state == "DEMO_INTRO" and intent == "END_CONVERSATION":
        return "PERSUADE"
    elif state == "DEMO_INTRO" and intent == "SCHEDULE_DEMO":
        return "SCHEDULE_DEMO"
    elif state == "ASK_INFO" and intent == "END_CONVERSATION":
        return "PERSUADE"
    elif state == "ASK_INFO" and intent == "SCHEDULE_DEMO":
        return "SCHEDULE_DEMO"
    elif state == "PERSUADE" and intent == "END_CONVERSATION":
        return "END_DEMO"
    elif state == "PERSUADE" and intent == "SCHEDULE_DEMO":
        return "SCHEDULE_DEMO"
    elif state == "SCHEDULE_DEMO" and intent == "END_CONVERSATION":
        return "END_DEMO"
    elif state == "INTRODUCTION" and intent == "DISCUSS_SKILLS":
        return "DISCUSS_SKILLS"
    elif state == "INTRODUCTION" and intent == "DISCUSS_SKILLS":
        return "DISCUSS_SKILLS"
    elif state == "INTRODUCTION" and intent == "DISCUSS_EXPERIENCE":
        return "DISCUSS_EXPERIENCE"
    elif state == "DISCUSS_SKILLS" and intent == "END_CONVERSATION":
        return "END_INTERVIEW"
    elif state == "DISCUSS_EXPERIENCE" and intent == "END_CONVERSATION":
        return "END_INTERVIEW"
    

    elif state == "REMIND_PAYMENT" and intent == "REQUEST_EXTENSION":
        return "REQUEST_EXTENSION"
    elif state == "ORDER_INTRO":
        return "FOLLOW_ORDER"
    elif state == "PAYMENT_INTRO":
        return "REMIND_PAYMENT"
    elif state == "FOLLOW_ORDER" and intent == "END_CONVERSATION":
        return "END_PAYMENT"
    elif state == "REQUEST_EXTENSION" and intent == "END_CONVERSATION":
        return "END_PAYMENT"
    
    else:
        return state


def get_customer_product_info(json_filename, index):
    # Load JSON data from file
    with open(json_filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    people = data["people"]
    products = {p["name"]: p for p in data["products"]}  # Convert product list to dictionary for quick lookup

    # Check if the index is valid
    if index < 0 or index >= len(people):
        return "Invalid index. Please provide a valid customer index."

    # Get the specific customer's data
    person = people[index]
    customer_name = person["name"]
    interested_products = person["interested_in"]

    # Create product details
    product_details = "\n".join(
        f"   {p}, {products[p]['description']} at ₹{products[p]['price']} , discount of {products[p]['discount']} %"
        for p in interested_products if p in products
    )

    # Format the output
    output = f"Customer Name = {customer_name}\nProducts:\n{product_details}"
    
    return output

def get_payment_due_info(json_filename, index):
    # Load JSON data from file
    with open(json_filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    customers = data["customers"]

    # Check if the index is valid
    if index < 0 or index >= len(customers):
        return "Invalid index. Please provide a valid customer index."

    # Get the specific customer's data
    customer = customers[index]
    customer_name = customer["name"]
    service = customer["service"]
    amount = customer["due_amount"]
    due_date = customer["due_date"]

    # Format the output
    output = f"Customer Name : {customer_name}\nPayment Due : {service} - ₹{amount} (Due by {due_date})"
    
    return output

def load_name_from_file(filename, index):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if 0 <= index < len(lines):
                return lines[index].strip()
            else:
                return "Index out of range."
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"