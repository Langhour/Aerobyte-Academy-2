#!/usr/bin/env python3
"""
AeroByte Academy Database CLI & Management Tool
================================================
View, manage, inspect, and export data stored in the AeroByte database.

Usage examples:
    python backend/manage_database.py --stats
    python backend/manage_database.py --users
    python backend/manage_database.py --orders
    python backend/manage_database.py --enrollments
    python backend/manage_database.py --export
    python backend/manage_database.py --create-user "student@aerobyte.edu" "Password123" "Dara Sok"
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Setup sys.path and UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.content_store import (
    initialize_content_store,
    get_database_stats,
    list_users,
    list_all_store_orders,
    list_enrollments,
    create_user,
    find_user_by_email,
    _connect,
    DATABASE_PATH,
)
from app.user_security import hash_user_password


def show_stats():
    initialize_content_store()
    stats = get_database_stats()
    print("=" * 60)
    print("         AEROBYTE ACADEMY DATABASE OVERVIEW")
    print("=" * 60)
    print(f" Engine:         {stats['engine']}")
    print(f" Database File:  {stats['file_path']}")
    print(f" Storage Size:   {stats['size_formatted']} ({stats['size_bytes']:,} bytes)")
    print("-" * 60)
    print(" TABLES & ROW COUNTS:")
    for table_name, count in sorted(stats["tables"].items()):
        print(f"   • {table_name:<28} : {count:>5} records")
    print("=" * 60)


def show_users():
    users = list_users()
    print("=" * 70)
    print(f" REGISTERED USERS ({len(users)} total)")
    print("=" * 70)
    if not users:
        print("  (No users registered yet)")
        return
    for idx, u in enumerate(users, 1):
        print(f" [{idx}] ID:    {u['id']}")
        print(f"     Name:  {u['full_name']}")
        print(f"     Email: {u['email']} {'(Verified ✓)' if u.get('is_verified') else '(Pending Verification)'}")
        print(f"     Role:  {u.get('role', 'user')}")
        if u.get('phone'):
            print(f"     Phone: {u['phone']}")
        if u.get('telegram'):
            print(f"     TG:    @{u['telegram']}")
        if u.get('location'):
            print(f"     Loc:   {u['location']}")
        print(f"     Created: {u.get('created_at', 'N/A')}")
        print("-" * 70)


def show_orders():
    orders = list_all_store_orders(limit=50)
    print("=" * 70)
    print(f" AERO STORE ORDERS ({len(orders)} total)")
    print("=" * 70)
    if not orders:
        print("  (No store orders placed yet)")
        return
    for idx, o in enumerate(orders, 1):
        print(f" [{idx}] ORDER #{o['id']}  [{o.get('status', 'confirmed').upper()}]")
        print(f"     Customer: {o.get('customer_name')} ({o.get('user_email') or 'Guest'})")
        print(f"     Phone:    {o.get('phone')} | TG: {o.get('telegram') or 'N/A'}")
        print(f"     Method:   {o.get('fulfillment')}")
        print(f"     Total:    ${float(o.get('total', 0)):.2f} (KHR: {round(float(o.get('total', 0)) * 4100):,} ៛)")
        print(f"     Items:    {len(o.get('items', []))} item(s)")
        for item in o.get('items', []):
            print(f"        - {item.get('name')} x{item.get('quantity')} (${float(item.get('priceUsd', 0)):.2f})")
        print(f"     Date:     {o.get('created_at')}")
        print("-" * 70)


def show_enrollments():
    enrollments = list_enrollments()
    print("=" * 70)
    print(f" COURSE ENROLLMENTS ({len(enrollments)} total)")
    print("=" * 70)
    if not enrollments:
        print("  (No enrollments yet)")
        return
    for idx, e in enumerate(enrollments, 1):
        print(f" [{idx}] ID: {e.enrollment_id} | TX: {e.transaction_id}")
        print(f"     Student: {e.full_name} ({e.email})")
        print(f"     Course:  {e.course_id}")
        print(f"     Status:  {e.status} | Total: ${e.final_price_usd:.2f}")
        print("-" * 70)


def export_backup():
    initialize_content_store()
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = backend_dir / "data" / "backups"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"aerobyte_backup_{now_str}.json"

    export_data = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "stats": get_database_stats(),
        "users": list_users(),
        "store_orders": list_all_store_orders(limit=1000),
        "enrollments": [e.model_dump() for e in list_enrollments()],
    }

    out_file.write_text(json.dumps(export_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Database backup exported to: {out_file.resolve()}")
    print(f"  Total Users:       {len(export_data['users'])}")
    print(f"  Total Orders:      {len(export_data['store_orders'])}")
    print(f"  Total Enrollments: {len(export_data['enrollments'])}")


def create_user_cmd(email: str, password: str, full_name: str, role: str = "user"):
    existing = find_user_by_email(email)
    if existing:
        print(f"Error: User with email '{email}' already exists in database (ID: {existing['id']}).")
        return
    user_id = str(uuid4())
    pw_hash = hash_user_password(password)
    now = datetime.now(timezone.utc).isoformat()
    create_user(
        user_id=user_id,
        email=email,
        full_name=full_name,
        password_hash=pw_hash,
        created_at=now,
        is_verified=1,
    )
    print(f"✓ User created successfully!")
    print(f"  ID:        {user_id}")
    print(f"  Email:     {email}")
    print(f"  Name:      {full_name}")
    print(f"  Status:    Verified")


def main():
    parser = argparse.ArgumentParser(description="AeroByte Academy Database CLI")
    parser.add_argument("--stats", action="store_true", help="Show database overview and row counts")
    parser.add_argument("--users", action="store_true", help="List registered users")
    parser.add_argument("--orders", action="store_true", help="List Aero Store orders")
    parser.add_argument("--enrollments", action="store_true", help="List course enrollments")
    parser.add_argument("--export", action="store_true", help="Export full database JSON backup")
    parser.add_argument("--create-user", nargs=3, metavar=("EMAIL", "PASSWORD", "NAME"), help="Register a new user directly")

    args = parser.parse_args()

    if args.stats or len(sys.argv) == 1:
        show_stats()
    if args.users:
        show_users()
    if args.orders:
        show_orders()
    if args.enrollments:
        show_enrollments()
    if args.export:
        export_backup()
    if args.create_user:
        create_user_cmd(args.create_user[0], args.create_user[1], args.create_user[2])


if __name__ == "__main__":
    main()
