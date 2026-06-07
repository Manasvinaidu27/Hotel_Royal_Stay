import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from hotel.models import RoomType, Room

# Room Types
standard = RoomType.objects.get_or_create(
    name="Standard Room",
    defaults={"description": "Comfortable room with all basic amenities.", "price_per_night": 1999, "capacity": 2, "amenities": "WiFi, AC, TV, Hot Water"}
)[0]

deluxe = RoomType.objects.get_or_create(
    name="Deluxe Room",
    defaults={"description": "Spacious room with premium furnishings and city view.", "price_per_night": 3500, "capacity": 2, "amenities": "WiFi, AC, Smart TV, Mini Bar, Bathtub"}
)[0]

suite = RoomType.objects.get_or_create(
    name="Suite",
    defaults={"description": "Luxury suite with separate living area and premium amenities.", "price_per_night": 7999, "capacity": 4, "amenities": "WiFi, AC, Smart TV, Mini Bar, Jacuzzi, Living Room, Kitchen"}
)[0]

# Rooms
rooms_data = [
    ("101", standard, 1), ("102", standard, 1), ("103", standard, 1),
    ("201", deluxe, 2),   ("202", deluxe, 2),   ("203", deluxe, 2),
    ("301", suite, 3),    ("302", suite, 3),
]

for number, rtype, floor in rooms_data:
    Room.objects.get_or_create(
        room_number=number,
        defaults={"room_type": rtype, "floor_number": floor, "status": "available", "is_active": True}
    )

print(f"✅ Created {Room.objects.count()} rooms across {RoomType.objects.count()} room types!")