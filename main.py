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
        print(f"User already exists: {email}")
        return

    try:
        session.add(User(name=name, email=email))
        session.commit()
        print(f"User {name} added!")
    except IntegrityError:
        session.rollback()
        print("ERROR: Could not add user.")

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

#Query
def query_users():
    for user in  session.query(User).all():
        print(f"ID: {User.id}, Name: {user.name}, Email: {user.email}")

def query_tasks():
    email = input("Enter the email of the user for tasks:")
    user  = get_user_by_email(email)
    if not user:
        print("There was no user with that email")
        return
    
    for task in user.tasks:
        print(f"Task ID: {task.id}, Title: {task.title}")


def update_user():
    email = input("Email of who you want to update:  ")
    user = get_user_by_email(email)
    if not user:
        print("There is no user with that email")
        return
    
    user.name = input("Enter a new name for the user (leave blank to stay the same):") or user.name
    user.email = input("Enter a new email (leave blank to stay the same)") or user.email
    session.commit()
    print("User has been updated!")

def delete_users():
    email = input("Email of who you want to delete: ")
    user  = get_user_by_email(email)
    if not user:
        print("There is no user with that email")
        return
    if confirm_action(f"Are you sure you want to delete: {user.name}?"):
        session.delete(user)
        session.commit()
        print("user has been deleted!")

def delete_task():
    task_id = input("Enter the ID of the task to delete: ")        
    task = session.query(Task).get(task_id)
    if not task:
        print("There is no task there!")
        return
    if confirm_action(f"Are you want to delete this task: {task.id}?"):
     session.delete(tas)
     session.commit()
    print("Task has been deleted!")

# Main Program Loopthis 
def main() -> None:
    actions = {
        "1": add_user,
        "2": add_tasks,
        "3": query_users,
        "4": query_tasks,
        "5": update_user,
        "6": delete_users,
        "7": delete_task
    }

    while True:
        print("\nOptions:\n1. Add User\n2. Add Task\n3. Query Users\n4. Query Tasks\n5. Update Users\n6. Delete\n7. Delete Task\n8. Exit")
        choice = input("Enter an option: ")
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



