import uuid

from sqlalchemy.orm import Session

from backend.customers import repository as customer_repository
from backend.customers.schemas import CustomerCreate, CustomerUpdate


class CustomerNotFoundError(Exception):
    pass


def create_customer(db: Session, organization_id: uuid.UUID, data: CustomerCreate):
    customer = customer_repository.create(db, organization_id, data.model_dump())
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, organization_id: uuid.UUID, customer_id: uuid.UUID):
    customer = customer_repository.get_by_id(db, organization_id, customer_id)
    if not customer:
        raise CustomerNotFoundError("Customer not found")
    return customer


def list_customers(db: Session, organization_id: uuid.UUID, skip: int = 0, limit: int = 50):
    return customer_repository.list_all(db, organization_id, skip, limit)


def update_customer(db: Session, organization_id: uuid.UUID, customer_id: uuid.UUID, data: CustomerUpdate):
    customer = get_customer(db, organization_id, customer_id)
    customer_repository.update(db, customer, data.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, organization_id: uuid.UUID, customer_id: uuid.UUID):
    customer = get_customer(db, organization_id, customer_id)
    customer_repository.soft_delete(db, customer)
    db.commit()