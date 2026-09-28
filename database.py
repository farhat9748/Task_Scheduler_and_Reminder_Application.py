from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime


# -------------------------------------------------
# DATABASE CONFIGURATION
# -------------------------------------------------

DB_USER = "root"
DB_PASSWORD =  "your_mysql_password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "task_scheduler"


DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# -------------------------------------------------
# CREATE ENGINE
# -------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)


# -------------------------------------------------
# BASE
# -------------------------------------------------

Base = declarative_base()


# -------------------------------------------------
# USER TABLE
# -------------------------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    tasks = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# -------------------------------------------------
# TASK TABLE
# -------------------------------------------------

class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(20),
        default="pending"
    )

    priority = Column(
        String(10),
        default="medium"
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    is_recurring = Column(
        Boolean,
        default=False
    )

    recurrence_interval = Column(
        String(20),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="tasks"
    )

    reminders = relationship(
        "Reminder",
        back_populates="task",
        cascade="all, delete-orphan"
    )


# -------------------------------------------------
# REMINDER TABLE
# -------------------------------------------------

class Reminder(Base):

    __tablename__ = "reminders"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    remind_at = Column(
        DateTime,
        nullable=False
    )

    notification_type = Column(
        String(20),
        default="email"
    )

    is_sent = Column(
        Boolean,
        default=False
    )

    task = relationship(
        "Task",
        back_populates="reminders"
    )


# -------------------------------------------------
# CREATE TABLES
# -------------------------------------------------

Base.metadata.create_all(engine)


# -------------------------------------------------
# SESSION
# -------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)