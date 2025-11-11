from collections import defaultdict
from datetime import datetime
from statistics import mean
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException

from ....models.classroom_subject import ClassroomSubject
from ...shared.base_auth_handler import BaseAuthHandler
from .get_teacher_classroom_students_request import (
    GetTeacherClassroomStudentsRequest,
)
from .get_teacher_classroom_students_response import (
    GetTeacherClassroomStudentsResponse,
    TeacherClassroomStudentSubject,
    TeacherClassroomStudentSummary,
    TeacherQualificationRecord,
)


def _parse_numeric(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


GRADE_TO_SCORE = {
    "AD": 20,
    "A": 17,
    "B": 14,
    "C": 10,
    "D": 5,
}
GRADE_ORDER = ["AD", "A", "B", "C", "D"]


def grade_to_score(letter: Optional[str]) -> Optional[float]:
    if not letter:
        return None
    return GRADE_TO_SCORE.get(letter.strip().upper())


def score_to_grade(score: Optional[float]) -> Optional[str]:
    if score is None:
        return None
    for index, grade in enumerate(GRADE_ORDER):
        value = GRADE_TO_SCORE[grade]
        if index == len(GRADE_ORDER) - 1:
            return grade
        next_value = GRADE_TO_SCORE[GRADE_ORDER[index + 1]]
        midpoint = (value + next_value) / 2
        if score >= midpoint:
            return grade
    return GRADE_ORDER[-1]


class GetTeacherClassroomStudentsHandler(
    BaseAuthHandler[
        GetTeacherClassroomStudentsRequest, GetTeacherClassroomStudentsResponse
    ]
):
    async def execute(
        self, request: GetTeacherClassroomStudentsRequest
    ) -> GetTeacherClassroomStudentsResponse:
        teacher_id = UUID(request.teacher_id)
        classroom_id = UUID(request.classroom_id)
        requesting_user_id = UUID(request.requesting_user_id)

        teacher = await self.unit_of_work.teacher_repository.get_by_id(teacher_id)
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")

        if not request.can_manage_any and teacher.user_id != requesting_user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        classroom = await self.unit_of_work.classroom_repository.get_by_id(
            classroom_id
        )
        if classroom is None:
            raise HTTPException(status_code=404, detail="Classroom not found")

        is_tutor = classroom.tutor_id == teacher_id

        teacher_classroom_subjects = await self.unit_of_work.classroom_subject_repository.get_for_teacher(
            teacher_id,
            include_substitute=True,
            with_relations=True,
            only_active=not request.include_inactive,
        )
        assigned_subject_ids = {
            cs.id
            for cs in teacher_classroom_subjects
            if cs.classroom_id == classroom_id
        }

        if not is_tutor and not assigned_subject_ids:
            raise HTTPException(status_code=403, detail="Forbidden")

        classroom_subjects: List[ClassroomSubject] = (
            await self.unit_of_work.classroom_subject_repository.get_for_classroom(
                classroom_id,
                with_relations=True,
                only_active=not request.include_inactive,
            )
        )

        students_map: Dict[UUID, Dict[str, object]] = defaultdict(
            lambda: {
                "student": None,
                "subjects": [],
            }
        )

        for classroom_subject in classroom_subjects:
            primary_teacher_id = classroom_subject.teacher_id or classroom_subject.substitute_teacher_id
            primary_teacher = (
                classroom_subject.teacher
                if classroom_subject.teacher and classroom_subject.teacher.names
                else classroom_subject.substitute_teacher
            )
            subjects_teacher_name = None
            if primary_teacher and primary_teacher.names:
                subjects_teacher_name = (
                    f"{primary_teacher.names} {primary_teacher.father_last_name or ''}".strip()
                )
            for enrollment in classroom_subject.students:
                if not request.include_inactive and not enrollment.is_active:
                    continue
                student = enrollment.student
                if student is None:
                    continue
                students_map[student.id]["student"] = student
                can_manage = request.can_manage_any or teacher_id in {
                    classroom_subject.teacher_id,
                    classroom_subject.substitute_teacher_id,
                }

                history_records: List[TeacherQualificationRecord] = []
                grade_scores: List[float] = []

                sorted_records = sorted(
                    enrollment.qualifications,
                    key=lambda record: record.created_at or datetime.min,
                )
                for record in sorted_records:
                    grade_letter = (
                        record.grade.strip().upper()
                        if record.grade
                        else None
                    )
                    score = grade_to_score(grade_letter)
                    if score is not None:
                        grade_scores.append(score)
                    history_records.append(
                        TeacherQualificationRecord(
                            id=record.id,
                            grade=grade_letter,
                            description=record.description,
                            teacher_id=str(record.teacher_id)
                            if record.teacher_id
                            else None,
                            teacher_full_name=(
                                f"{record.teacher.names} {record.teacher.father_last_name or ''}".strip()
                                if record.teacher and record.teacher.names
                                else None
                            ),
                            created_at=record.created_at.isoformat()
                            if isinstance(record.created_at, datetime)
                            else None,
                        )
                    )

                current_grade = (
                    enrollment.qualification.strip().upper()
                    if enrollment.qualification
                    else None
                )
                current_score = grade_to_score(current_grade)
                if not grade_scores and current_score is not None:
                    grade_scores.append(current_score)

                average_score = mean(grade_scores) if grade_scores else None
                average_grade = score_to_grade(average_score) or current_grade

                subject_entry = TeacherClassroomStudentSubject(
                    classroom_subject_student_id=enrollment.id,
                    classroom_subject_id=classroom_subject.id,
                    subject_id=classroom_subject.subject_id,
                    subject_name=classroom_subject.subject.name
                    if classroom_subject.subject
                    else "Subject",
                    teacher_id=str(primary_teacher_id)
                    if primary_teacher_id
                    else None,
                    teacher_name=subjects_teacher_name,
                    qualification=enrollment.qualification,
                    status=enrollment.status,
                    is_active=enrollment.is_active,
                    can_manage=can_manage,
                    average_grade=average_grade,
                    average_score=average_score,
                    history=history_records,
                )
                students_map[student.id]["subjects"].append(subject_entry)

        summaries: List[TeacherClassroomStudentSummary] = []
        for student_id, payload in students_map.items():
            student = payload["student"]
            if student is None:
                continue
            subjects: List[TeacherClassroomStudentSubject] = payload["subjects"]
            numeric_qualifications = [
                value
                for value in (
                    _parse_numeric(subject.qualification) for subject in subjects
                )
                if value is not None
            ]
            average = (
                round(mean(numeric_qualifications), 2)
                if numeric_qualifications
                else None
            )
            summaries.append(
                TeacherClassroomStudentSummary(
                    student_id=str(student.id),
                    student_code=student.code,
                    full_name=student.full_name,
                    email=student.email or (student.user.email if student.user else None),
                    average_qualification=average,
                    subjects=subjects,
                )
            )

        summaries.sort(key=lambda item: item.full_name)

        return GetTeacherClassroomStudentsResponse(students=summaries)

