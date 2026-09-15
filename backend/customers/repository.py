import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.customers.models import Customer


def create(db: Session, organization_id: uuid.UUID, data: dict) -> Customer:
    customer = Customer(organization_id=organization_id, **data)
    db.add(customer)
    db.flush()
    return customer


def get_by_id(db: Session, organization_id: uuid.UUID, customer_id: uuid.UUID) -> Customer | None:
    return (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.organization_id == organization_id,
            Customer.deleted_at.is_(None),
        )
        .first()
    )


def list_all(db: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 50) -> list[Customer]:
    return (
        db.query(Customer)
        .filter(Customer.organization_id == organization_id, Customer.deleted_at.is_(None))
        .order_by(Customer.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update(db: Session, customer: Customer, data: dict) -> Customer:
    for key, value in data.items():
        if value is not None:
            setattr(customer, key, value)
    db.flush()
    return customer


def soft_delete(db: Session, customer: Customer) -> None:
    customer.deleted_at = datetime.now(timezone.utc)
    db.flush()