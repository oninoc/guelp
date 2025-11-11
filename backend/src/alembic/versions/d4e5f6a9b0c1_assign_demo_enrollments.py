"""ensure demo teachers, classrooms, and enrollments exist

Revision ID: d4e5f6a9b0c1
Revises: c3d4e5f6a8b9
Create Date: 2025-11-11 18:05:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d4e5f6a9b0c1"
down_revision: Union[str, Sequence[str], None] = "c3d4e5f6a8b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _assign_teacher_to_classroom_subject(connection, *, classroom_desc: str, subject_name: str, teacher_email: str) -> None:
    connection.execute(
        sa.text(
            """
            UPDATE classroom_subject
            SET teacher_id = sub.teacher_id
            FROM (
                SELECT cs.id AS classroom_subject_id, t.id AS teacher_id
                FROM classroom cs_room
                JOIN classroom_subject cs ON cs.classroom_id = cs_room.id
                JOIN subject subj ON subj.id = cs.subject_id
                JOIN teacher t ON t.user_id = (SELECT u.id FROM "user" u WHERE u.email = :teacher_email)
                WHERE cs_room.description = :classroom_desc
                  AND subj.name = :subject_name
                  AND cs.teacher_id IS DISTINCT FROM t.id
            ) sub
            WHERE classroom_subject.id = sub.classroom_subject_id
            """
        ),
        {
            "classroom_desc": classroom_desc,
            "subject_name": subject_name,
            "teacher_email": teacher_email,
        },
    )


def _enroll_student(connection, *, student_email: str, classroom_desc: str, subject_name: str) -> None:
    connection.execute(
        sa.text(
            """
            INSERT INTO classroom_subject_student (classroom_subject_id, student_id, status, is_active, created_at)
            SELECT cs.id, stu.id, 'enrolled', TRUE, NOW()
            FROM student stu
            JOIN classroom_subject cs ON cs.classroom_id = (
                SELECT id FROM classroom WHERE description = :classroom_desc LIMIT 1
            )
            JOIN subject subj ON subj.id = cs.subject_id
            WHERE stu.email = :student_email
              AND subj.name = :subject_name
              AND NOT EXISTS (
                  SELECT 1 FROM classroom_subject_student css
                  WHERE css.classroom_subject_id = cs.id AND css.student_id = stu.id
              )
            """
        ),
        {
            "student_email": student_email,
            "classroom_desc": classroom_desc,
            "subject_name": subject_name,
        },
    )


def _ensure_role(connection, *, code: str, name: str, description: str) -> None:
    connection.execute(
        sa.text(
            """
            INSERT INTO role (name, code, description, created_at)
            SELECT :name, :code, :description, NOW()
            WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = :code)
            """
        ),
        {"name": name, "code": code, "description": description},
    )


def _assign_role(connection, *, user_email: str, role_code: str) -> None:
    connection.execute(
        sa.text(
            """
            INSERT INTO user_role_relation (user_id, role_id, relation_type)
            SELECT u.id, r.id, 'direct'
            FROM "user" u
            JOIN role r ON r.code = :role_code
            WHERE u.email = :user_email
              AND NOT EXISTS (
                  SELECT 1 FROM user_role_relation urr
                  WHERE urr.user_id = u.id AND urr.role_id = r.id
              )
            """
        ),
        {"user_email": user_email, "role_code": role_code},
    )


def upgrade() -> None:
    connection = op.get_bind()

    # Ensure teacher & student roles exist
    _ensure_role(
        connection,
        code="teacher",
        name="Teacher",
        description="Teacher role with classroom access",
    )
    _ensure_role(
        connection,
        code="student",
        name="Student",
        description="Student role with academic access",
    )

    # Ensure teachers remain attached to classroom subjects
    _assign_teacher_to_classroom_subject(
        connection,
        classroom_desc="Primary 1A",
        subject_name="Mathematics",
        teacher_email="maria.gomez@school.demo",
    )
    _assign_teacher_to_classroom_subject(
        connection,
        classroom_desc="Primary 1A",
        subject_name="Science",
        teacher_email="juan.perez@school.demo",
    )
    _assign_teacher_to_classroom_subject(
        connection,
        classroom_desc="Primary 1B",
        subject_name="History",
        teacher_email="juan.perez@school.demo",
    )

    # Ensure students are enrolled in classroom subjects
    _enroll_student(
        connection,
        student_email="sofia.luna@student.demo",
        classroom_desc="Primary 1A",
        subject_name="Mathematics",
    )
    _enroll_student(
        connection,
        student_email="diego.matos@student.demo",
        classroom_desc="Primary 1A",
        subject_name="Mathematics",
    )
    _enroll_student(
        connection,
        student_email="diego.matos@student.demo",
        classroom_desc="Primary 1A",
        subject_name="Science",
    )
    _enroll_student(
        connection,
        student_email="valentina.costa@student.demo",
        classroom_desc="Primary 1B",
        subject_name="History",
    )

    # Assign roles to demo accounts
    for email in ("maria.gomez@school.demo", "juan.perez@school.demo"):
        _assign_role(connection, user_email=email, role_code="teacher")
    for email in (
        "sofia.luna@student.demo",
        "diego.matos@student.demo",
        "valentina.costa@student.demo",
    ):
        _assign_role(connection, user_email=email, role_code="student")


def downgrade() -> None:
    connection = op.get_bind()

    # Remove the specific enrollments introduced by this migration
    connection.execute(
        sa.text(
            """
            DELETE FROM classroom_subject_student
            WHERE student_id IN (
                SELECT id FROM student WHERE email = ANY(:student_emails)
            )
            AND classroom_subject_id IN (
                SELECT cs.id
                FROM classroom_subject cs
                JOIN classroom c ON c.id = cs.classroom_id
                JOIN subject subj ON subj.id = cs.subject_id
                WHERE (c.description = 'Primary 1A' AND subj.name IN ('Mathematics','Science'))
                   OR (c.description = 'Primary 1B' AND subj.name = 'History')
            )
            """
        ),
        {"student_emails": ["sofia.luna@student.demo", "diego.matos@student.demo", "valentina.costa@student.demo"]},
    )

    # Remove role assignments created by this migration
    connection.execute(
        sa.text(
            """
            DELETE FROM user_role_relation
            WHERE role_id IN (SELECT id FROM role WHERE code IN ('teacher','student'))
              AND user_id IN (
                SELECT id FROM "user"
                WHERE email = ANY(:emails)
              )
            """
        ),
        {
            "emails": [
                "maria.gomez@school.demo",
                "juan.perez@school.demo",
                "sofia.luna@student.demo",
                "diego.matos@student.demo",
                "valentina.costa@student.demo",
            ]
        },
    )

