from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Avg, Count, Sum
from django.db.models.functions import TruncMonth
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
import uuid
import json

from .models import RoomType, Room, Booking, Payment, RoomReview
from .forms import RoomSearchForm, BookingForm, PaymentForm, RoomReviewForm


# ── HOME ──────────────────────────────────────────────────────────────────────
def home(request):
    room_types = RoomType.objects.filter(is_active=True)[:3]
    total_rooms = Room.objects.filter(is_active=True).count()
    # Count all non-cancelled bookings as "happy guests"
    happy_guests = Booking.objects.exclude(status="cancelled").count()
    return render(request, "hotel/home.html", {
        "room_types": room_types,
        "total_rooms": total_rooms,
        "happy_guests": happy_guests,
    })


# ── ROOM LIST ─────────────────────────────────────────────────────────────────
def room_list(request):
    rooms = Room.objects.filter(status="available", is_active=True).select_related("room_type")
    form = RoomSearchForm(request.GET or None)

    if request.GET and form.is_valid():
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")
        guests = form.cleaned_data.get("guests")

        if check_in and check_out:
            booked_rooms = Booking.objects.filter(
                Q(check_in_date__lt=check_out) & Q(check_out_date__gt=check_in),
                status__in=["confirmed", "pending"]
            ).values_list("room_id", flat=True)
            rooms = rooms.exclude(id__in=booked_rooms)

        if guests:
            rooms = rooms.filter(room_type__capacity__gte=guests)

    return render(request, "hotel/room_list.html", {"form": form, "rooms": rooms})


# ── ROOM DETAIL ───────────────────────────────────────────────────────────────
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    reviews = room.reviews.select_related("user").order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    has_reviewed = False
    can_review = False
    if request.user.is_authenticated:
        has_reviewed = reviews.filter(user=request.user).exists()
        can_review = Booking.objects.filter(
            guest=request.user, room=room, status="completed"
        ).exists()
    return render(request, "hotel/room_detail.html", {
        "room": room,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "has_reviewed": has_reviewed,
        "can_review": can_review,
    })


# ── AI ROOM RECOMMENDATION ────────────────────────────────────────────────────
def room_recommendations(request):
    """Simple rule-based recommendation engine."""
    guests = int(request.GET.get("guests", 1))
    budget = float(request.GET.get("budget", 99999))
    preference = request.GET.get("preference", "")

    rooms = Room.objects.filter(
        status="available",
        is_active=True,
        room_type__capacity__gte=guests,
        room_type__price_per_night__lte=budget,
    ).select_related("room_type")

    if preference:
        rooms = rooms.filter(
            Q(room_type__name__icontains=preference) |
            Q(room_type__amenities__icontains=preference)
        )

    # Score rooms: higher rating + lower price = better recommendation
    scored = []
    for room in rooms:
        avg_r = room.reviews.aggregate(Avg("rating"))["rating__avg"] or 3.0
        price_score = max(0, 1 - (float(room.room_type.price_per_night) / (budget + 1)))
        score = (avg_r / 5) * 0.6 + price_score * 0.4
        scored.append({"room": room, "score": score, "avg_rating": round(avg_r, 1)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return render(request, "hotel/recommendations.html", {
        "recommendations": scored[:6],
        "guests": guests,
        "budget": budget,
        "preference": preference,
    })


# ── MAKE BOOKING ──────────────────────────────────────────────────────────────
@login_required
def make_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.guest = request.user
            booking.room = room

            if booking.check_out_date <= booking.check_in_date:
                messages.error(request, "Check-out must be after check-in.")
                return render(request, "hotel/make_booking.html", {"form": form, "room": room})

            nights = (booking.check_out_date - booking.check_in_date).days
            booking.total_price = nights * room.room_type.price_per_night
            booking.status = "pending"
            booking.save()

            messages.success(request, "Booking created! Complete payment to confirm.")
            return redirect("payment", booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, "hotel/make_booking.html", {"form": form, "room": room})


# ── PAYMENT (Razorpay) ────────────────────────────────────────────────────────
@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)

    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id", "")
        razorpay_order_id = request.POST.get("razorpay_order_id", "")

        if razorpay_payment_id or request.POST.get("payment_method"):
            pay = Payment(
                booking=booking,
                amount=booking.total_price,
                transaction_id=str(uuid.uuid4())[:12].upper(),
                razorpay_payment_id=razorpay_payment_id or None,
                razorpay_order_id=razorpay_order_id or None,
                payment_method=request.POST.get("payment_method", "razorpay"),
                status="completed",
            )
            pay.save()

            booking.status = "confirmed"
            booking.save()
            booking.room.status = "occupied"
            booking.room.save()

            _send_booking_confirmation(booking, pay)

            messages.success(request, "🎉 Payment successful! Your booking is confirmed.")
            return redirect("booking_details", booking_id=booking.id)

    amount_paise = int(booking.total_price * 100)
    razorpay_key = settings.RAZORPAY_KEY_ID

    return render(request, "hotel/payment.html", {
        "booking": booking,
        "amount_paise": amount_paise,
        "razorpay_key": razorpay_key,
    })


def _send_booking_confirmation(booking, payment_obj):
    try:
        subject = f"✅ Booking Confirmed – #{booking.id} | Hotel Royal Stay"
        message = f"""
Dear {booking.guest.get_full_name() or booking.guest.username},

Your booking has been confirmed!

📋 Booking Details:
  Room: {booking.room.room_number} ({booking.room.room_type.name})
  Check-in:  {booking.check_in_date}
  Check-out: {booking.check_out_date}
  Guests:    {booking.number_of_guests}
  Nights:    {booking.nights}

💰 Payment:
  Amount: ₹{payment_obj.amount}
  Transaction ID: {payment_obj.transaction_id}
  Method: {payment_obj.get_payment_method_display()}

Thank you for choosing Hotel Royal Stay!
We look forward to welcoming you.

Hotel Royal Stay — Hitech City, Hyderabad
📞 +91 7777711111 | ✉ info@hotelroyalstay.com
        """.strip()

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.guest.email],
            fail_silently=True,
        )
    except Exception:
        pass


# ── MY BOOKINGS ───────────────────────────────────────────────────────────────
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(guest=request.user).select_related(
        "room", "room__room_type"
    ).prefetch_related("payment").order_by("-created_at")
    return render(request, "hotel/my_bookings.html", {"bookings": bookings})


# ── BOOKING DETAIL ────────────────────────────────────────────────────────────
@login_required
def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    payment_obj = Payment.objects.filter(booking=booking).first()
    return render(request, "hotel/booking_detail.html", {
        "booking": booking,
        "payment": payment_obj,
    })


# ── CANCEL BOOKING ────────────────────────────────────────────────────────────
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    if booking.status in ["pending", "confirmed"]:
        booking.status = "cancelled"
        booking.save()
        booking.room.status = "available"
        booking.room.save()
        messages.success(request, "Booking cancelled successfully.")
    return redirect("my_bookings")


# ── ADD REVIEW ────────────────────────────────────────────────────────────────
@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    has_stayed = Booking.objects.filter(
        guest=request.user, room=room, status="completed"
    ).exists()
    if not has_stayed:
        messages.error(request, "You can only review after completing your stay.")
        return redirect("room_detail", pk=room.id)

    if request.method == "POST":
        form = RoomReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()
            messages.success(request, "Thank you for your review! ⭐")
            return redirect("room_detail", pk=room.id)
    else:
        form = RoomReviewForm()
    return render(request, "hotel/add_review.html", {"form": form, "room": room})


# ── ADMIN DASHBOARD (Analytics) ───────────────────────────────────────────────
@staff_member_required
def admin_dashboard(request):
    today = date.today()
    this_month_start = today.replace(day=1)

    total_bookings = Booking.objects.count()
    confirmed = Booking.objects.filter(status="confirmed").count()
    cancelled = Booking.objects.filter(status="cancelled").count()
    pending = Booking.objects.filter(status="pending").count()
    completed = Booking.objects.filter(status="completed").count()

    total_revenue = Payment.objects.filter(status="completed").aggregate(
        total=Sum("amount")
    )["total"] or 0

    monthly_revenue = Payment.objects.filter(
        status="completed",
        payment_date__gte=this_month_start
    ).aggregate(total=Sum("amount"))["total"] or 0

    total_rooms = Room.objects.filter(is_active=True).count()
    occupied_rooms = Room.objects.filter(status="occupied").count()
    available_rooms = Room.objects.filter(status="available").count()
    maintenance_rooms = Room.objects.filter(status="maintenance").count()
    occupancy_rate = round((occupied_rooms / total_rooms * 100) if total_rooms else 0, 1)

    six_months_ago = today - timedelta(days=180)
    monthly_data = (
        Payment.objects.filter(status="completed", payment_date__gte=six_months_ago)
        .annotate(month=TruncMonth("payment_date"))
        .values("month")
        .annotate(revenue=Sum("amount"), count=Count("id"))
        .order_by("month")
    )

    chart_labels = [d["month"].strftime("%b %Y") for d in monthly_data]
    chart_revenue = [float(d["revenue"]) for d in monthly_data]

    recent_bookings = Booking.objects.select_related(
        "guest", "room", "room__room_type"
    ).order_by("-created_at")[:10]

    top_rooms = (
        RoomType.objects.annotate(booking_count=Count("room__booking"))
        .order_by("-booking_count")[:5]
    )

    todays_checkins = Booking.objects.filter(
        check_in_date=today, status="confirmed"
    ).count()
    todays_checkouts = Booking.objects.filter(
        check_out_date=today, status="confirmed"
    ).count()

    return render(request, "hotel/admin_dashboard.html", {
        "total_bookings": total_bookings,
        "confirmed": confirmed,
        "cancelled": cancelled,
        "pending": pending,
        "completed": completed,
        "total_revenue": total_revenue,
        "monthly_revenue": monthly_revenue,
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms,
        "maintenance_rooms": maintenance_rooms,
        "occupancy_rate": occupancy_rate,
        "chart_labels": json.dumps(chart_labels),
        "chart_revenue": json.dumps(chart_revenue),
        "recent_bookings": recent_bookings,
        "top_rooms": top_rooms,
        "todays_checkins": todays_checkins,
        "todays_checkouts": todays_checkouts,
    })