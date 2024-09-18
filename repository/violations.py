from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import Violations
from schema import ViolationsSchema


class ViolationRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_violations(self) -> list[ViolationsSchema]:
        with self.db_session as session:
            violations: list[ViolationsSchema] = session.execute(select(Violations)).scalars().all()
        return violations

    def get_violation(self, violation_id: int) -> ViolationsSchema | None:
        with self.db_session as session:
            violation: ViolationsSchema = session.execute(select(Violations).where(Violations.id == violation_id)
                                                     ).scalar_one_or_none()
        return violation

    def create_violation(self, violation: ViolationsSchema) -> int:
        violation_model = Violations(
            main_id=violation.main_id,
            photo=violation.photo,
            video=violation.video,
            category=violation.category,
            confidence=violation.confidence,
            date=violation.date,
            time=violation.time,
            camera=violation.camera,
            field=violation.field,
            well_pad=violation.well_pad,
            color=violation.color)
        with self.db_session as session:
            session.add(violation_model)
            session.commit()
            return violation.id


    def update_violation(self, violation_id: int, violation: ViolationsSchema) -> ViolationsSchema | None:
        query = (update(Violations).where(Violations.id == violation_id).values(
            main_id=violation.main_id,
            photo=violation.photo,
            video=violation.video,
            category=violation.category,
            confidence=violation.confidence,
            date=violation.date,
            time=violation.time,
            camera=violation.camera,
            field=violation.field,
            well_pad=violation.well_pad,
            color=violation.color
                ).returning(Violations.id))
        with self.db_session as session:
            violation_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_violation(violation_id)


    def delete_violation(self, violation_id: int) -> None:
        query = delete(Violations).where(Violations.id == violation_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()
