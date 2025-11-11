"""refresh demo assignments and roles

Revision ID: e5f6a9b0c2d3
Revises: d4e5f6a9b0c1
Create Date: 2025-11-11 18:40:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5f6a9b0c2d3"
down_revision: Union[str, Sequence[str], None] = "d4e5f6a9b0c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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


def _fetch_scalar(connection, query: str, **params):
    row = connection.execute(sa.text(query), params).fetchone()
    return row[0] if row else None


def _upsert_classroom_subject(connection, *, classroom_desc: str, subject_name: str, teacher_email: str) -> None:
    classroom_id = _fetch_scalar(
        connection,
        "SELECT id FROM classroom WHERE description = :description LIMIT 1",
        description=classroom_desc,
    )
    subject_id = _fetch_scalar(
        connection,
        "SELECT id FROM subject WHERE name = :name LIMIT 1",
        name=subject_name,
    )
    teacher_id = _fetch_scalar(
        connection,
        "SELECT t.id FROM teacher t JOIN \"user\" u ON u.id = t.user_id WHERE u.email = :email LIMIT 1",
        email=teacher_email,
    )

    if classroom_id is None or subject_id is None:
        return

    exists = _fetch_scalar(
        connection,
        "SELECT id FROM classroom_subject WHERE classroom_id = :classroom_id AND subject_id = :subject_id",
        classroom_id=classroom_id,
        subject_id=subject_id,
    )

    if exists is None:
        connection.execute(
            sa.text(
                "INSERT INTO classroom_subject (classroom_id, subject_id, teacher_id, is_active, created_at) "
                "VALUES (:classroom_id, :subject_id, :teacher_id, TRUE, NOW())"
            ),
            {
                "classroom_id": classroom_id,
                "subject_id": subject_id,
                "teacher_id": teacher_id,
            },
        )
    elif teacher_id is not None:
        connection.execute(
            sa.text(
                "UPDATE classroom_subject SET teacher_id = :teacher_id "
                "WHERE classroom_id = :classroom_id AND subject_id = :subject_id"
            ),
            {
                "teacher_id": teacher_id,
                "classroom_id": classroom_id,
                "subject_id": subject_id,
            },
        )


def _enroll_student(connection, *, student_email: str, classroom_desc: str, subject_name: str) -> None:
    connection.execute(
        sa.text(
            """
            INSERT INTO classroom_subject_student (classroom_subject_id, student_id, status, is_active, created_at)
            SELECT cs.id, stu.id, 'enrolled', TRUE, NOW()
            FROM student stu
            JOIN "user" u ON u.id = stu.user_id
            JOIN classroom_subject cs ON cs.classroom_id = (
                SELECT id FROM classroom WHERE description = :classroom_desc LIMIT 1
            )
            JOIN subject subj ON subj.id = cs.subject_id
            WHERE u.email = :student_email
              AND subj.name = :subject_name
              AND NOT EXISTS (
                  SELECT 1 FROM classroom_subject_student css
                  WHERE css.classroom_subject_id = cs.id
                    AND css.student_id = stu.id
              );
            """
        ),
        {
            "student_email": student_email,
            "classroom_desc": classroom_desc,
            "subject_name": subject_name,
        },
    )


def upgrade() -> None:
    connection = op.get_bind()

    # Ensure roles
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

    # Assign roles to demo accounts
    for email in ("maria.gomez@school.demo", "juan.perez@school.demo"):
        _assign_role(connection, user_email=email, role_code="teacher")
    for email in (
        "sofia.luna@student.demo",
        "diego.matos@student.demo",
        "valentina.costa@student.demo",
    ):
        _assign_role(connection, user_email=email, role_code="student")

    # Classroom assignments
    _upsert_classroom_subject(
        connection,
        classroom_desc="Primary 1A",
        subject_name="Mathematics",
        teacher_email="maria.gomez@school.demo",
    )
    _upsert_classroom_subject(
        connection,
        classroom_desc="Primary 1A",
        subject_name="Science",
        teacher_email="juan.perez@school.demo",
    )
    _upsert_classroom_subject(
        connection,
        classroom_desc="Primary 1B",
        subject_name="History",
        teacher_email="juan.perez@school.demo",
    )

    # Enrollments
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


def downgrade() -> None:
    connection = op.get_bind()

    # Remove enrollments introduced here
    connection.execute(
        sa.text(
            """
            DELETE FROM classroom_subject_student
            WHERE student_id IN (
                SELECT stu.id
                FROM student stu
                JOIN "user" u ON u.id = stu.user_id
                WHERE u.email = ANY(:emails)
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
        {"emails": ["sofia.luna@student.demo", "diego.matos@student.demo", "valentina.costa@student.demo"]},
    )

    # Optionally remove role assignments (roles themselves remain)
    connection.execute(
        sa.text(
            """
            DELETE FROM user_role_relation
            WHERE role_id IN (SELECT id FROM role WHERE code IN ('teacher','student'))
              AND user_id IN (
                SELECT id FROM "user"
                WHERE email = ANY(:all_emails)
              )
            """
        ),
        {
            "all_emails": [
                "maria.gomez@school.demo",
                "juan.perez@school.demo",
                "sofia.luna@student.demo",
                "diego.matos@student.demo",
                "valentina.costa@student.demo",
            ]
        },
    )

