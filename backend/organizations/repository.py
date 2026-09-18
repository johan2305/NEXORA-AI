import uuid

from sqlalchemy.orm import Session

from backend.organizations.models import Membership, Organization


def create_organization(db: Session, name: str, slug: str) -> Organization:
    org = Organization(name=name, slug=slug)
    db.add(org)
    db.flush()
    return org


def create_membership(db: Session, user_id: uuid.UUID, organization_id: uuid.UUID, role: str) -> Membership:
    membership = Membership(user_id=user_id, organization_id=organization_id, role=role)
    db.add(membership)
    db.flush()
    return membership


def get_first_membership_for_user(db: Session, user_id: uuid.UUID) -> Membership | None:
    return db.query(Membership).filter(Membership.user_id == user_id).first()