# requirements.txt
# asyncio
# aiohttp
# python-dateutil

import asyncio
import aiohttp
import json
import random
from datetime import datetime, timedelta
from dateutil import rrule
from time import sleep

# --- Configuration ---
BASE_URL = "http://localhost:8000"  # Replace with your API base URL
API_KEY = "test "  # Replace with your actual API key for /bot-api/
HEADERS_BOT = {"Api-Key": API_KEY} if API_KEY else {}
HEADERS_JSON = {"Content-Type": "application/json"}
# ---------------------


# --- Data Generation Helpers ---
def generate_random_phone():
    return f"+7{random.randint(1000000000, 9999999999)}"


def generate_random_name():
    names = [
        "Иван",
        "Мария",
        "Пётр",
        "Анна",
        "Александр",
        "Елена",
        "Дмитрий",
        "Ольга",
        "Сергей",
        "Татьяна",
    ]
    return random.choice(names)


def generate_random_surname():
    surnames = [
        "Иванов",
        "Петрова",
        "Смирнов",
        "Кузнецова",
        "Попов",
        "Лебедева",
        "Козлов",
        "Новикова",
        "Морозов",
        "Волкова",
    ]
    return random.choice(surnames)


def generate_random_service_title():
    services = [
        "Стрижка",
        "Маникюр",
        "Педикюр",
        "Окрашивание",
        "Укладка",
        "Чистка лица",
        "Массаж",
        "Депиляция",
    ]
    return random.choice(services)


def generate_random_schedule():
    return f"{random.randint(1, 7)} через {random.randint(1, 3)}"


def generate_random_work_hours():
    start_hour = random.randint(7, 10)
    end_hour = random.randint(start_hour + 6, 22)  # Ensure end is after start
    return f"{start_hour:02d}:00", f"{end_hour:02d}:00"


def generate_random_price():
    return random.randint(500, 5000)


def generate_random_duration():
    # Durations in minutes
    return random.choice([30, 45, 60, 90, 120])


async def create_organization_type(session, type_title):
    """Creates an Organization Type via bot API."""
    url = f"{BASE_URL}/bot-api/service/"
    data = {"title": type_title}
    try:
        async with session.post(
            url, json=data, headers={**HEADERS_BOT, **HEADERS_JSON}
        ) as resp:
            if resp.status in (200, 201):
                response_data = await resp.json()
                if response_data.get("success"):
                    # Assuming the service ID is returned or can be extracted
                    # This API seems to be for Master Services, might need adjustment
                    # Let's assume it returns data with an 'id' field for the created item
                    org_type_id = response_data.get("data", {}).get(
                        "id"
                    ) or response_data.get("id")
                    print(
                        f"Created Organization Type '{type_title}' with (potential) ID: {org_type_id}"
                    )
                    return org_type_id
                else:
                    print(f"Error creating Organization Type: {response_data}")
                    return None
            else:
                print(
                    f"HTTP Error {resp.status} for Organization Type creation: {await resp.text()}"
                )
                return None
    except Exception as e:
        print(f"Exception during Organization Type creation: {e}")
        return None


async def create_organization(session, org_type_id):
    """Creates an Organization via bot API."""
    url = f"{BASE_URL}/bot-api/organization/create/"
    start_time, end_time = generate_random_work_hours()
    # Using a dummy telegram_id for creation
    data = aiohttp.FormData()
    data.add_field("title", "Тестовая Организация")
    data.add_field("telegram_id", "org_admin_123")
    # data.add_field('main_image', ...) # Omitted for simplicity
    data.add_field("main_image_url", "https://example.com/default_org.jpg")
    data.add_field("time_begin", start_time)
    data.add_field("time_end", end_time)
    data.add_field("address", "г. Москва, ул. Тестовая, д. 1")
    data.add_field("work_schedule", generate_random_schedule())
    data.add_field("organization_type_id", str(org_type_id))  # Pass ID as string
    data.add_field("contact_phone", generate_random_phone())
    data.add_field("gallery", ["https://example.com/image.png"])

    try:
        async with session.post(url, data=data, headers=HEADERS_BOT) as resp:
            if resp.status in (200, 201):
                response_data = await resp.json()
                if response_data.get("success"):
                    # Extract organization ID from response
                    org_data = response_data.get("data", {})
                    org_id = org_data.get("id") or org_data.get("organization_id")
                    print(
                        f"Created Organization 'Тестовая Организация' with ID: {org_id}"
                    )
                    return org_id
                else:
                    print(f"Error creating Organization: {response_data}")
                    return None
            else:
                resp_text = await resp.text()
                print(
                    f"HTTP Error {resp.status} for Organization creation: {resp_text[:4000]}"
                )
                return None
    except Exception as e:
        print(f"Exception during Organization creation: {e}")
        return None


async def create_masters(session, org_id, num_masters=3):
    """Creates Masters via bot API."""
    master_ids = []
    for i in range(num_masters):
        url = f"{BASE_URL}/bot-api/masters/"
        name = generate_random_name()
        surname = generate_random_surname()
        data = {
            "name": name,
            "surname": surname,
            "telegram_id": f"master_{random.randint(1000, 9999)}",
            "organization_id": org_id,
            "gender": random.choice(["MEN", "WOMEN"]),
            # "image": ... # Omitted
            "image_url": "https://imag.ru/image.png",
        }
        try:
            async with session.post(
                url, json=data, headers={**HEADERS_BOT, **HEADERS_JSON}
            ) as resp:
                if resp.status in (200, 201):
                    response_data = await resp.json()
                    if response_data.get("success"):
                        master_id = response_data.get("master_id", None)
                        print(f"Created Master '{name} {surname}' with ID: {master_id}")
                        master_ids.append(master_id)
                    else:
                        print(f"Error creating Master {i + 1}: {response_data}")
                else:
                    print(
                        f"HTTP Error {resp.status} for Master {i + 1} creation: {await resp.text()}"
                    )
        except Exception as e:
            print(f"Exception during Master {i + 1} creation: {e}")
    return master_ids


async def create_services(session, master_ids, services_per_master=3):
    """Creates Services for Masters via bot API."""
    service_map = {}  # {master_id: [service_id, ...]}
    for master_id in master_ids:
        service_ids = []
        for i in range(services_per_master):
            url = f"{BASE_URL}/bot-api/masters/{master_id}/services/"
            title = f"{generate_random_service_title()} {i + 1}"
            duration = generate_random_duration()
            data = {
                "title": title,
                "short_description": f"Описание услуги {title}",
                "price": generate_random_price(),
                "min_time": duration,  # Assuming min_time is in minutes
            }
            try:
                async with session.post(
                    url, json=data, headers={**HEADERS_BOT, **HEADERS_JSON}
                ) as resp:
                    if resp.status in (200, 201):
                        response_data = await resp.json()
                        if response_data.get("success"):
                            service_id = response_data.get("service_id")
                            print(
                                f"Created Service '{title}' for Master {master_id} with ID: {service_id}"
                            )
                            service_ids.append(service_id)
                        else:
                            print(
                                f"Error creating Service {i + 1} for Master {master_id}: {response_data}"
                            )
                    else:
                        print(
                            f"HTTP Error {resp.status} for Service {i + 1} (Master {master_id}) creation: {await resp.text()}"
                        )
            except Exception as e:
                print(
                    f"Exception during Service {i + 1} (Master {master_id}) creation: {e}"
                )
        service_map[master_id] = service_ids
    return service_map


async def create_random_bookings(session, master_ids, service_map, num_bookings=40):
    """Creates random bookings via the main API."""
    # First, get organization details to know working hours
    # This is a simplification. Ideally, you'd fetch org details once.
    # For now, let's assume a standard working day for simplicity in time selection.
    # A more robust way would be to fetch the org and parse its time_begin/end.
  
    for i in range(num_bookings):
        master_id = random.choice(master_ids)
        available_service_ids = service_map.get(master_id, [])
        if not available_service_ids:
            print(
                f"No services available for Master {master_id}, skipping booking {i + 1}"
            )
            continue

        # Select a service
        service_id = random.choice(available_service_ids)

        # --- Get Free Times (Simulation) ---
        # Instead of calling the real free times API (which is complex),
        # we'll simulate finding a free slot within the next few days.
        # This is a simplified version and might create conflicts in reality.
        # A real script would call /booking/get-free-times/ and parse the result.

        # Generate a date within the next 14 days
        days_ahead = random.randint(0, 13)
        booking_date = datetime.now().date() + timedelta(days=days_ahead)

        # --- Simulate getting a free time ---
        # Assume working hours are 9:00 to 18:00 for simplicity in this script
        start_hour = 9
        end_hour = 18
        # Try to find a time. Simple brute force for demo.
        success = False
        for _ in range(20):  # Try 20 times to find a "free" slot
            await asyncio.sleep(random.random())

            hour = random.randint(
                start_hour, end_hour - 1
            )  # Avoid booking at exactly end time
            minute = random.choice([0, 30])  # Simple time slots
            booking_time = f"{hour:02d}:{minute:02d}"

            # --- Create the booking/order ---
            # We'll use the OrderCreateView endpoint which seems to handle booking logic
            url = f"{BASE_URL}/api/order/create/"
            # Generate customer details
            customer_phone = generate_random_phone()
            customer_name = f"{generate_random_name()} {generate_random_surname()}"
            data = {
                "master_id": master_id,
                "service_ids": [service_id],  # API expects a list
                "begin_date": booking_date.isoformat(),  # YYYY-MM-DD
                "begin_time": booking_time,  # HH:MM
                "customer_phone": customer_phone,
                "customer_name": customer_name,
                "customer_notice": f"Тестовое бронирование {i + 1}",
            }
            try:
                # Use json payload for POST
                async with session.post(
                    url, json=data, headers=HEADERS_JSON
                ) as resp:
                    if resp.status in (200, 201):
                        response_data = await resp.json()
                        if response_data.get("success"):
                            print(
                                f"Successfully created Booking {i + 1} for Master {master_id} on {booking_date} at {booking_time}"
                            )
                            success = True
                            break  # Break the retry loop on success
                        else:
                            # Check if it's a time conflict or other error
                            message = response_data.get("message", "")
                            if (
                                "conflict" in message.lower()
                                or "busy" in message.lower()
                                or "not free" in message.lower()
                            ):
                                print(
                                    f"  Time conflict for Booking {i + 1} (Master {master_id}, {booking_date} {booking_time}), retrying..."
                                )
                                # Don't break, let the loop try another time
                            else:
                                print(
                                    f"  Error creating Booking {i + 1}: {response_data}"
                                )
                                break  # Break on other errors
                    else:
                        resp_text = await resp.text()
                        print(
                            f"HTTP Error {resp.status} for Booking {i + 1}: {resp_text[:5000]}"
                        )
                        break  # Break on HTTP errors
            except Exception as e:
                print(f"Exception during Booking {i + 1} creation: {e}")
                break  # Break on exceptions

        if not success:
            print(f"Failed to create Booking {i + 1} after retries.")



# --- Main Execution ---
async def main():
    timeout = aiohttp.ClientTimeout(total=60)  # 60 seconds timeout
    async with aiohttp.ClientSession(timeout=timeout) as session:

        print("--- Starting Data Population ---")
        print("\n1. Creating Organization Type...")
        print("\n2. Creating Organization...")

        org_id = await create_organization(session, 1)
        if not org_id:
            print("Failed to create Organization. Aborting.")
            return

        print("\n3. Creating Masters...")
        master_ids = await create_masters(session, org_id, num_masters=3)
        if not master_ids:
            print("Failed to create any Masters. Aborting.")
            return
        print(f"Created Masters with IDs: {master_ids}")

        print("\n4. Creating Services...")
        service_map = await create_services(session, master_ids, services_per_master=3)
        print(f"Service mapping created: {service_map}")

        # 5. Create Random Bookings
        print("\n5. Creating Random Bookings...")
        await create_random_bookings(session, master_ids, service_map, num_bookings=15)

        actions = [
            create_organization(session, 1),
            create_masters(session, org_id, num_masters=3),
            create_services(session, master_ids, services_per_master=3),
            create_services(session, master_ids, services_per_master=3),
            create_random_bookings(session, master_ids, service_map, num_bookings=15)
        ]

        while True:
            try:
                x = 5
                if x == 1:
                    await create_organization(session, 1)
                elif x == 2:
                    await create_masters(session, org_id, num_masters=3)
                elif x == 3:
                    await create_services(session, master_ids, services_per_master=3)
                elif x == 4:
                    await create_services(session, master_ids, services_per_master=3)
                elif x == 5:
                    await create_random_bookings(session, master_ids, service_map, num_bookings=15)
                await asyncio.sleep(4)
            except Exception as error:
                print(error)
if __name__ == "__main__":
    asyncio.run(main())
