from datetime import datetime
from sqlalchemy import select, delete, update, func, case
from sqlalchemy.orm import Session
from database import Violations
from schema import ViolationsSchema
from typing import Dict


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

    def get_violations_from_time(self, start_date: datetime, end_date: datetime, sn: int) -> list[ViolationsSchema]:
        with self.db_session as session:
            violations: list[ViolationsSchema] = session.execute(select(Violations)
                                                                 .where(Violations.datetime >= start_date,
                                                                        Violations.datetime <= end_date,
                                                                        Violations.sn == sn)).scalars().all()
        return violations

    def get_amount_violations_from_time(self, start_date: datetime, end_date: datetime) -> int:
        with self.db_session as session:
            results = session.execute(
                select(
                    func.sum(case((Violations.category == 'danger_zone', 1), else_=0)).label("danger_zone"),
                    func.sum(case((Violations.category == 'glasses', 1), else_=0)).label("glasses"),
                    func.sum(case((Violations.category == 'gloves', 1), else_=0)).label("gloves"),
                    func.sum(case((Violations.category == 'helm', 1), else_=0)).label("helm"),
                    func.sum(case((Violations.category == 'safety_rope', 1), else_=0)).label("safety_rope")
                )
                .where(Violations.datetime >= start_date, Violations.datetime <= end_date)
            ).one()
            danger_zone = results.danger_zone or 0
            glasses = results.glasses or 0
            gloves = results.gloves or 0
            helm = results.helm or 0
            safety_rope = results.safety_rope or 0
            return {
                "danger_zone:": danger_zone,
                "glasses:": glasses,
                "gloves": gloves,
                "helm": helm,
                "safety_rope": safety_rope,
                "total": danger_zone +
                         glasses +
                         gloves +
                         helm +
                         safety_rope
            }

    def create_violation(self, violation: ViolationsSchema) -> int:
        violation_model = Violations(
            main_id=violation.main_id,
            photo=violation.photo,
            video=violation.video,
            category=violation.category,
            confidence=violation.confidence,
            datetime=violation.datetime,
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
            datetime=violation.datetime,
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
