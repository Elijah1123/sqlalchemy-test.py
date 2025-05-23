# What this program does
# It’s a simple user-task manager using SQLAlchemy and SQLite database.

# You can add users (with name and email).

# You can add tasks linked to a user (by email).

# It stores everything in a database (Test.db).

# You interact with it using a text menu in the terminal.

# Code Breakdown
# 1. Setup database connection and ORM base
# python
# Copy
# Edit
# engine = create_engine("sqlite:///Test.db", echo=False)
# Base = declarative_base()
# Session = sessionmaker(bind=engine)
# session = Session()
# create_engine(...) sets up SQLite database.

# declarative_base() lets you define classes that map to tables.

# sessionmaker and session allow talking to the database (adding, querying, etc.).

# 2. Define models (tables)
# python
# Copy
# Edit
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')
# User class represents the users table.

# Each user has an ID, name, and unique email.

# tasks is a list of all tasks linked to this user.

# python
# Copy
# Edit
# class Task(Base):
#     __tablename__ = "tasks"
#     id = Column(Integer, primary_key=True)
#     title = Column(String(50), nullable=True)
#     description = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship('User', back_populates='tasks')
# Task class represents the tasks table.

# Each task has an ID, title, description, and a user_id linking to a user.

# The user attribute connects the task back to its owner user.

# 3. Create tables in database
# python
# Copy
# Edit
# Base.metadata.create_all(engine)
# This creates the tables users and tasks in the database if they don’t exist yet.

# 4. Helper function: get a user by email
# python
# Copy
# Edit
# def get_user_by_email(email):
#     return session.query(User).filter_by(email=email).first()
# Looks up a user by their email in the database.

# Returns the first matching user or None if not found.

# 5. Helper function: confirm user action
# python
# Copy
# Edit
# def confirm_action(prompt: str) -> bool:
#     return input(f"{prompt} (yes/no): ").strip().lower() == 'yes'
# Asks user a yes/no question and returns True if answer is 'yes'.

# 6. Add a new user
# python
# Copy
# Edit
# def add_user():
#     name = input("Enter user name: ")
#     email = input("Enter user email: ")
#     if get_user_by_email(email):
#         print(f'User already exists: {email}')
#         return
#     try:
#         session.add(User(name=name, email=email))
#         session.commit()
#         print(f'User {name} added!')
#     except IntegrityError:
#         session.rollback()
#         print('ERROR: Could not add user.')
# Gets user name and email.

# Checks if user exists; if yes, stops.

# Otherwise, adds user to database and commits.

# Handles database errors gracefully.

# 7. Add a task linked to a user
# python
# Copy
# Edit
# def add_tasks():
#     email = input("Enter the email of the user to add tasks: ")
#     user = get_user_by_email(email)
#     if not user:
#         print('No user found with that email!')
#         return
#     title = input("Enter the title: ")
#     description = input("Enter the description: ")
#     task = Task(title=title, description=description, user=user)
#     session.add(task)
#     session.commit()
#     print(f"Task '{title}' added for user {user.name}.")
# Gets email, finds user.

# If user not found, stops.

# Otherwise, collects task title and description.

# Creates a new task linked to that user.

# Saves it in the database.

# 8. Main program loop
# python
# Copy
# Edit
# def main() -> None:
#     actions = {
#         "1": add_user,
#         "2": add_tasks,
#     }
#     while True:
#         print("\nOptions:\n1. Add User\n2. Add Task\n8. Exit")
#         choice = input("Choose an option: ")
#         if choice == "8":
#             print("Adios!")
#             break
#         action = actions.get(choice)
#         if action:
#             action()
#         else:
#             print("That is not a valid option.")
# Shows a menu with options.

# Waits for user to enter choice.

# Calls the corresponding function (add_user or add_tasks).

# Exits if user chooses 8.

# Prints error if invalid option.

# 9. Run main only if script executed directly
# python
# Copy
# Edit
# if __name__ == "__main__":
#     main()
# Ensures the program runs the menu only when you run this script directly, not when imported as a module.

# Summary
# The code connects to a database.

# Defines users and tasks as tables.

# Lets you add users and tasks from the command line.

# Saves and relates tasks to users.

# Uses a simple menu loop for interaction.

