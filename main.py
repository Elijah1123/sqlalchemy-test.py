from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

# Setup
engine = create_engine("sqlite:///Test.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='tasks')

# Create tables
Base.metadata.create_all(engine)

# Helper functions
def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() == 'yes'

# CRUD Functions
def add_user():
    name = input("Enter user name: ")
    email = input("Enter user email: ")

    if get_user_by_email(email):
        print(f'User already exists: {email}')
        return

    try:
        session.add(User(name=name, email=email))
        session.commit()
        print(f'User {name} added!')
    except IntegrityError:
        session.rollback()
        print('ERROR: Could not add user.')

def add_tasks():
    email = input("Enter the email of the user to add tasks: ")
    user = get_user_by_email(email)

    if not user:
        print('No user found with that email!')
        return

    title = input("Enter the title: ")
    description = input("Enter the description: ")

    task = Task(title=title, description=description, user=user)
    session.add(task)
    session.commit()
    print(f"Task '{title}' added for user {user.name}.")

# Main Program Loop
def main() -> None:
    actions = {
        "1": add_user,
        "2": add_tasks,
    }

    while True:
        print("\nOptions:\n1. Add User\n2. Add Task\n8. Exit")
        choice = input("Choose an option: ")

        if choice == "8":
            print("Adios!")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("That is not a valid option.")

# Correct entry point
if __name__ == "__main__":
    main()



