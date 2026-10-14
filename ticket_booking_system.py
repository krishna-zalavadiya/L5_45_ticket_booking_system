"""Movie theater ticket booking and seating management module.

This module demonstrates seat reservation, cancellation, pricing, ticket hashes,
PIN generation, seating-chart export, and a sold-seat summary.
"""

import hashlib
from pathlib import Path
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}

booking_history = []


def reserve_seat(seat_id, customer, history=None):
    """Reserve a seat if it exists and is currently available."""
    if seat_id not in theater_seats or theater_seats[seat_id]["is_sold"]:
        return False

    theater_seats[seat_id]["is_sold"] = True

    # CORRECTED: Use None as the default, not a shared mutable list.
    if history is None:
        history = booking_history

    history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Mark an existing seat as available; return whether it existed."""
    # CORRECTED: Validate the seat rather than hiding errors with bare except.
    if seat_id not in theater_seats:
        return False

    theater_seats[seat_id]["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True if a seat exists and is available."""
    # CORRECTED: Removed the unused booking_fee variable.
    if seat_id not in theater_seats:
        return False

    return not theater_seats[seat_id]["is_sold"]


def compute_discounted_price(seat_id, discount_percent):
    """Return the seat price after a validated percentage discount."""
    if seat_id not in theater_seats:
        raise ValueError("Invalid seat ID")

    # CORRECTED: Accept a number rather than executing a string with eval().
    if (
        isinstance(discount_percent, bool)
        or not isinstance(discount_percent, (int, float))
        or not 0 <= discount_percent <= 100
    ):
        raise ValueError("Discount must be a number between 0 and 100")

    base_price = theater_seats[seat_id]["price"]
    # CORRECTED: Round the result to two decimal places for currency display.
    return round(base_price * (1 - discount_percent / 100), 2)


def generate_ticket_hash(ticket_code):
    """Return a SHA-256 fingerprint for a ticket code."""
    # CORRECTED: Replace MD5 with SHA-256.
    # Note: an unkeyed hash is a fingerprint, not proof of ticket authenticity.
    return hashlib.sha256(ticket_code.encode("utf-8")).hexdigest()


def generate_booking_pin():
    """Generate a cryptographically strong four-digit booking PIN."""
    # CORRECTED: Use secrets instead of random for security-sensitive values.
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the current seating dictionary to a text file."""
    # CORRECTED: Use Path.write_text instead of manual open/close.
    # CORRECTED: Avoid os.system; print the message without invoking a shell.
    Path(filename).write_text(str(theater_seats), encoding="utf-8")
    print(f"Seating chart exported to: {filename}")


def get_theater_summary(seats):
    """Return the number of seats currently marked as sold."""
    # CORRECTED: Use values() because the seat ID is not needed in this loop.
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a small demonstration of the ticket-booking functions."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")

    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())

    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))
    print("Order history:", booking_history)


if __name__ == "__main__":
    # CORRECTED: Run the demo only when this file is executed directly.
    main()
