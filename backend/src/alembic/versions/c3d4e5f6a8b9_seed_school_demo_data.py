"""seed demo school data for teachers, students, classrooms, subjects

Revision ID: c3d4e5f6a8b9
Revises: b2c3d4e5f6a7
Create Date: 2025-11-11 17:40:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union, Optional
from datetime import datetime
from uuid import uuid4, UUID

from alembic import op
import sqlalchemy as sa

try:
    from passlib.context import CryptContext
except Exception:  # pragma: no cover - migrations should still run even if passlib is missing
    CryptContext = None  # type: ignore


# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a8b9"
down_revision: Union[str, Sequence[str], None] = "4ca8d306b124"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PASSWORD = "123456"


def _pwd_hash(password: str) -> str:
    if CryptContext is None:
        return password
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return context.hash(password)


def _ensure_user(connection, *, email: str, name: str, last_name: str, phone: str, address: str) -> UUID:
    row = connection.execute(sa.text('SELECT id FROM "user" WHERE email = :email'), {"email": email}).fetchone()
    if row:
        return row[0]

    user_id = uuid4()
    now = datetime.utcnow()
    hashed_password = _pwd_hash(PASSWORD)
    token = uuid4().hex
    refresh_token = uuid4().hex

    connection.execute(
        sa.text(
            'INSERT INTO "user" (id, created_at, name, last_name, phone, address, email, password, token, refresh_token) '
            'VALUES (:id, :created_at, :name, :last_name, :phone, :address, :email, :password, :token, :refresh_token)'
        ),
        {
            "id": user_id,
            "created_at": now,
            "name": name,
            "last_name": last_name,
            "phone": phone,
            "address": address,
            "email": email,
            "password": hashed_password,
            "token": token,
            "refresh_token": refresh_token,
        },
    )
    return user_id


def _assign_role(connection, *, user_id: UUID, role_code: str) -> None:
    role_row = connection.execute(sa.text("SELECT id FROM role WHERE code = :code"), {"code": role_code}).fetchone()
    if role_row is None:
        return
    role_id = role_row[0]
    connection.execute(
        sa.text(
            "INSERT INTO user_role_relation (user_id, role_id, relation_type) "
            "SELECT :user_id, :role_id, 'direct' "
            "WHERE NOT EXISTS (SELECT 1 FROM user_role_relation WHERE user_id = :user_id AND role_id = :role_id)"
        ),
        {"user_id": user_id, "role_id": role_id},
    )


def _ensure_teacher(connection, *, user_id: UUID, names: str, father_last_name: str, mother_last_name: str,
                    doc_type: str, doc_number: str, birth_date: str, gender: str, nationality: str) -> UUID:
    row = connection.execute(
        sa.text("SELECT id FROM teacher WHERE user_id = :user_id"), {"user_id": user_id}
    ).fetchone()
    if row:
        return row[0]

    teacher_id = uuid4()
    connection.execute(
        sa.text(
            "INSERT INTO teacher (id, created_at, names, father_last_name, mother_last_name, document_type, "
            "document_number, birth_date, gender, nationality, user_id) "
            "VALUES (:id, :created_at, :names, :father_last_name, :mother_last_name, :document_type, "
            ":document_number, :birth_date, :gender, :nationality, :user_id)"
        ),
        {
            "id": teacher_id,
            "created_at": datetime.utcnow(),
            "names": names,
            "father_last_name": father_last_name,
            "mother_last_name": mother_last_name,
            "document_type": doc_type,
            "document_number": doc_number,
            "birth_date": birth_date,
            "gender": gender,
            "nationality": nationality,
            "user_id": user_id,
        },
    )
    return teacher_id


def _ensure_student(connection, *, user_id: UUID, code: str, names: str, father_last_name: str, mother_last_name: str,
                    phone: str, address: str, email: str, birth_date: str, gender: str, nationality: str) -> UUID:
    row = connection.execute(
        sa.text("SELECT id FROM student WHERE user_id = :user_id"), {"user_id": user_id}
    ).fetchone()
    if row:
        return row[0]

    student_id = uuid4()
    connection.execute(
        sa.text(
            "INSERT INTO student (id, created_at, code, names, father_last_name, mother_last_name, phone, address, "
            "email, birth_date, gender, nationality, user_id) "
            "VALUES (:id, :created_at, :code, :names, :father_last_name, :mother_last_name, :phone, :address, "
            ":email, :birth_date, :gender, :nationality, :user_id)"
        ),
        {
            "id": student_id,
            "created_at": datetime.utcnow(),
            "code": code,
            "names": names,
            "father_last_name": father_last_name,
            "mother_last_name": mother_last_name,
            "phone": phone,
            "address": address,
            "email": email,
            "birth_date": birth_date,
            "gender": gender,
            "nationality": nationality,
            "user_id": user_id,
        },
    )
    return student_id


def _ensure_subject(connection, *, name: str, description: str) -> int:
    row = connection.execute(sa.text("SELECT id FROM subject WHERE name = :name"), {"name": name}).fetchone()
    if row:
        return row[0]
    connection.execute(
        sa.text(
            "INSERT INTO subject (name, description, created_at) VALUES (:name, :description, NOW())"
        ),
        {"name": name, "description": description},
    )
    row = connection.execute(sa.text("SELECT id FROM subject WHERE name = :name"), {"name": name}).fetchone()
    return row[0]


def _ensure_classroom(connection, *, description: str, level: str, degree: str,
                      start_time: Optional[str], end_time: Optional[str], tutor_id: Optional[UUID]) -> UUID:
    row = connection.execute(
        sa.text("SELECT id FROM classroom WHERE description = :description AND level = :level AND degree = :degree"),
        {"description": description, "level": level, "degree": degree},
    ).fetchone()
    if row:
        class_id = row[0]
        if tutor_id:
            connection.execute(
                sa.text("UPDATE classroom SET tutor_id = :tutor_id WHERE id = :id"),
                {"tutor_id": tutor_id, "id": class_id},
            )
        return class_id

    classroom_id = uuid4()
    connection.execute(
        sa.text(
            "INSERT INTO classroom (id, created_at, description, level, degree, start_time, end_time, tutor_id) "
            "VALUES (:id, :created_at, :description, :level, :degree, :start_time, :end_time, :tutor_id)"
        ),
        {
            "id": classroom_id,
            "created_at": datetime.utcnow(),
            "description": description,
            "level": level,
            "degree": degree,
            "start_time": start_time,
            "end_time": end_time,
            "tutor_id": tutor_id,
        },
    )
    return classroom_id


def _ensure_classroom_subject(connection, *, classroom_id: UUID, subject_id: int, teacher_id: Optional[UUID]) -> int:
    row = connection.execute(
        sa.text(
            "SELECT id FROM classroom_subject WHERE classroom_id = :classroom_id AND subject_id = :subject_id"
        ),
        {"classroom_id": classroom_id, "subject_id": subject_id},
    ).fetchone()
    if row:
        classroom_subject_id = row[0]
        connection.execute(
            sa.text("UPDATE classroom_subject SET teacher_id = :teacher_id WHERE id = :id"),
            {"teacher_id": teacher_id, "id": classroom_subject_id},
        )
        return classroom_subject_id

    result = connection.execute(
        sa.text(
            "INSERT INTO classroom_subject (classroom_id, subject_id, teacher_id, is_active, created_at) "
            "VALUES (:classroom_id, :subject_id, :teacher_id, TRUE, NOW()) RETURNING id"
        ),
        {"classroom_id": classroom_id, "subject_id": subject_id, "teacher_id": teacher_id},
    )
    return result.scalar_one()


def _ensure_classroom_subject_student(connection, *, classroom_subject_id: int, student_id: UUID, status: str) -> None:
    connection.execute(
        sa.text(
            "INSERT INTO classroom_subject_student (classroom_subject_id, student_id, status, is_active, created_at) "
            "SELECT :classroom_subject_id, :student_id, :status, TRUE, NOW() "
            "WHERE NOT EXISTS (SELECT 1 FROM classroom_subject_student WHERE classroom_subject_id = :classroom_subject_id AND student_id = :student_id)"
        ),
        {"classroom_subject_id": classroom_subject_id, "student_id": student_id, "status": status},
    )


def upgrade() -> None:
    connection = op.get_bind()

    # Create demo teachers
    teacher_definitions = [
        {
            "email": "maria.gomez@school.demo",
            "name": "Maria",
            "last_name": "Gomez",
            "phone": "555-1001",
            "address": "123 Main St",
            "teacher": {
                "names": "Maria",
                "father_last_name": "Gomez",
                "mother_last_name": "Lopez",
                "document_type": "DNI",
                "document_number": "TCH-1001",
                "birth_date": "1985-04-12",
                "gender": "Female",
                "nationality": "Peruvian",
            },
        },
        {
            "email": "juan.perez@school.demo",
            "name": "Juan",
            "last_name": "Perez",
            "phone": "555-1002",
            "address": "456 Central Ave",
            "teacher": {
                "names": "Juan",
                "father_last_name": "Perez",
                "mother_last_name": "Ramirez",
                "document_type": "DNI",
                "document_number": "TCH-1002",
                "birth_date": "1982-09-03",
                "gender": "Male",
                "nationality": "Peruvian",
            },
        },
    ]

    teacher_ids: dict[str, UUID] = {}
    for teacher in teacher_definitions:
        user_id = _ensure_user(
            connection,
            email=teacher["email"],
            name=teacher["name"],
            last_name=teacher["last_name"],
            phone=teacher["phone"],
            address=teacher["address"],
        )
        _assign_role(connection, user_id=user_id, role_code="user")
        t = teacher["teacher"]
        teacher_id = _ensure_teacher(
            connection,
            user_id=user_id,
            names=t["names"],
            father_last_name=t["father_last_name"],
            mother_last_name=t["mother_last_name"],
            doc_type=t["document_type"],
            doc_number=t["document_number"],
            birth_date=t["birth_date"],
            gender=t["gender"],
            nationality=t["nationality"],
        )
        teacher_ids[teacher["email"]] = teacher_id

    # Create demo students
    student_definitions = [
        {
            "email": "sofia.luna@student.demo",
            "name": "Sofia",
            "last_name": "Luna",
            "phone": "555-2001",
            "address": "Sunset Blvd 100",
            "student": {
                "code": "STU-001",
                "names": "Sofia",
                "father_last_name": "Luna",
                "mother_last_name": "Campos",
                "birth_date": "2014-06-20",
                "gender": "Female",
                "nationality": "Peruvian",
            },
        },
        {
            "email": "diego.matos@student.demo",
            "name": "Diego",
            "last_name": "Matos",
            "phone": "555-2002",
            "address": "Ocean Ave 55",
            "student": {
                "code": "STU-002",
                "names": "Diego",
                "father_last_name": "Matos",
                "mother_last_name": "Quispe",
                "birth_date": "2013-11-02",
                "gender": "Male",
                "nationality": "Peruvian",
            },
        },
        {
            "email": "valentina.costa@student.demo",
            "name": "Valentina",
            "last_name": "Costa",
            "phone": "555-2003",
            "address": "River St 201",
            "student": {
                "code": "STU-003",
                "names": "Valentina",
                "father_last_name": "Costa",
                "mother_last_name": "Rojas",
                "birth_date": "2014-01-15",
                "gender": "Female",
                "nationality": "Peruvian",
            },
        },
    ]

    student_ids: dict[str, UUID] = {}
    for student in student_definitions:
        user_id = _ensure_user(
            connection,
            email=student["email"],
            name=student["name"],
            last_name=student["last_name"],
            phone=student["phone"],
            address=student["address"],
        )
        _assign_role(connection, user_id=user_id, role_code="user")
        s = student["student"]
        student_id = _ensure_student(
            connection,
            user_id=user_id,
            code=s["code"],
            names=s["names"],
            father_last_name=s["father_last_name"],
            mother_last_name=s["mother_last_name"],
            phone=student["phone"],
            address=student["address"],
            email=student["email"],
            birth_date=s["birth_date"],
            gender=s["gender"],
            nationality=s["nationality"],
        )
        student_ids[student["email"]] = student_id

    # Subjects
    subject_ids = {
        "Matematica": _ensure_subject(connection, name="Mathematics", description="Numbers, algebra and geometry"),
        "Ciencia": _ensure_subject(connection, name="Science", description="Natural sciences"),
        "Historia": _ensure_subject(connection, name="History", description="World history basics"),
    }

    # Classrooms
    classroom_a_id = _ensure_classroom(
        connection,
        description="Primary 1A",
        level="Primary",
        degree="1A",
        start_time="08:00",
        end_time="13:00",
        tutor_id=teacher_ids.get("maria.gomez@school.demo"),
    )
    classroom_b_id = _ensure_classroom(
        connection,
        description="Primary 1B",
        level="Primary",
        degree="1B",
        start_time="08:30",
        end_time="13:30",
        tutor_id=teacher_ids.get("juan.perez@school.demo"),
    )

    # Classroom subjects
    math_a_id = _ensure_classroom_subject(
        connection,
        classroom_id=classroom_a_id,
        subject_id=subject_ids["Mathematics"],
        teacher_id=teacher_ids.get("maria.gomez@school.demo"),
    )
    science_a_id = _ensure_classroom_subject(
        connection,
        classroom_id=classroom_a_id,
        subject_id=subject_ids["Science"],
        teacher_id=teacher_ids.get("juan.perez@school.demo"),
    )
    history_b_id = _ensure_classroom_subject(
        connection,
        classroom_id=classroom_b_id,
        subject_id=subject_ids["History"],
        teacher_id=teacher_ids.get("juan.perez@school.demo"),
    )

    # Enroll students
    def enroll(student_email: str, classroom_subject_id: int):
        student_id = student_ids.get(student_email)
        if student_id:
            _ensure_classroom_subject_student(
                connection,
                classroom_subject_id=classroom_subject_id,
                student_id=student_id,
                status="enrolled",
            )

    enroll("sofia.luna@student.demo", math_a_id)
    enroll("diego.matos@student.demo", math_a_id)
    enroll("diego.matos@student.demo", science_a_id)
    enroll("valentina.costa@student.demo", history_b_id)


def downgrade() -> None:
    connection = op.get_bind()

    student_emails = [
        "sofia.luna@student.demo",
        "diego.matos@student.demo",
        "valentina.costa@student.demo",
    ]
    teacher_emails = [
        "maria.gomez@school.demo",
        "juan.perez@school.demo",
    ]

    # Remove classroom subject student entries
    connection.execute(
        sa.text(
            "DELETE FROM classroom_subject_student WHERE student_id IN (SELECT id FROM student WHERE email = ANY(:emails))"
        ),
        {"emails": student_emails},
    )

    # Remove classroom subjects that were created (only if they reference demo classrooms or subjects)
    connection.execute(
        sa.text(
            "DELETE FROM classroom_subject WHERE classroom_id IN (SELECT id FROM classroom WHERE description IN ('Primary 1A','Primary 1B'))"
        )
    )

    # Remove classrooms
    connection.execute(
        sa.text("DELETE FROM classroom WHERE description IN ('Primary 1A','Primary 1B')")
    )

    # Remove subjects if no other classroom uses them
    connection.execute(
        sa.text(
            "DELETE FROM subject WHERE name IN ('Mathematics','Science','History') "
            "AND NOT EXISTS (SELECT 1 FROM classroom_subject WHERE subject_id = subject.id)"
        )
    )

    # Remove students and their users
    connection.execute(
        sa.text("DELETE FROM student WHERE email = ANY(:emails)"),
        {"emails": student_emails},
    )
    connection.execute(
        sa.text('DELETE FROM "user" WHERE email = ANY(:emails)'),
        {"emails": student_emails},
    )

    # Remove teachers and their users
    connection.execute(
        sa.text("DELETE FROM teacher WHERE user_id IN (SELECT id FROM \"user\" WHERE email = ANY(:emails))"),
        {"emails": teacher_emails},
    )
    connection.execute(
        sa.text('DELETE FROM "user" WHERE email = ANY(:emails)'),
        {"emails": teacher_emails},
    )

