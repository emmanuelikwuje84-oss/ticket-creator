
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

FILE_NAME = "ticket.json"
tickets = []


def generate_ai_answer(title):
    print("\nFetching Possible solutions...")
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                 "role": "system",
                 "content": (
                        "You are a customer support assistant. "
                        "Give a short, practical answer in simple English. "
                        "Use this format:\n"
                        "Possible cause: one sentence.\n"
                        "Solution:\n"
                        "1. First step.\n"
                        "2. Second step.\n"
                        "3. Third step.\n"
                        "Use no more than 3 steps."
                )    
            },
            {
                "role": "user",
                "content": title
            }
        ]
    )

    return response.choices[0].message.content


def ticket_creation():
    print("====== CREATE TICKET ======")
    title = input("Enter title: ")
    category = input("Category(Hardware,software,Network,Others): ")

    while True:
        try:
            affected_user = int(input("Affected user (positive integer): "))

            if affected_user <= 0:
                print("Error: Enter a positive whole number.")
                continue

            break

        except ValueError:
            print("Error: Enter an integer only, such as 3 or 10.")

    urgency = input("Urgency(High,Medium,Low): ")

    ticket = {
        "id": len(tickets) + 1,
        "title": title,
        "category": category,
        "affected_user": affected_user,
        "urgency": urgency
    }

    ticket["ai_answer"] = generate_ai_answer(title)

    tickets.append(ticket)
    return ticket

try:
    new_ticket = ticket_creation()

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4,)

    print("\n--- Ticket Created Successfully ---")
    print(f"Ticket ID:      {new_ticket['id']}")
    print(f"Title:          {new_ticket['title']}")
    print(f"Category:       {new_ticket['category']}")
    print(f"Affected User:  ID {new_ticket['affected_user']}")
    print(f"Urgency Level:  {new_ticket['urgency'].upper()}")
    print(f"AI Answer:      {new_ticket['ai_answer']}")

except Exception as error:
    print(f"An error occurred: {error}")
