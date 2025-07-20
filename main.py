# imports
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv                         
import os 

load_dotenv()
database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

# creating database
engine = create_engine(database_url, echo = False) 

Base = declarative_base()     
Session = sessionmaker(bind = engine)  
session = Session()                    

# defining models 
class User(Base): 
    __tablename__="users"

    id = Column(Integer, primary_key=True)   
    name = Column(String, nullable=False)   
    email  = Column(String, nullable=False, unique = True)
    tasks = relationship("Task", back_populates = 'user', cascade="all, delete-orphan")  


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable = True )     
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))   
    user = relationship("User", back_populates= "tasks")

Base.metadata.create_all(engine)

# utility functions
def get_user_by_email(email_value): 
    return session.query(User).filter_by(email=email_value).first()


def confirm_action(prompt:str)->bool:
    check = input(f'{prompt} (yes/no):').strip().lower() =="yes"
    return check

# CRUD Operations

## C
def add_user():
    name_value, email_value = input("Enter the name: "), input("Enter the email: ")
    if get_user_by_email(email_value):
        print(f"User already exists: {email_value}")
        return     
    
    try:
        session.add(User(name = name_value, email = email_value))    
        session.commit()
        print(f"User {name_value} added.")
    except IntegrityError:    
        session.rollback()    
        print("ERROR.")

def add_task():
    email_value = input("Enter the email of the user to add tasks: ")
    user = get_user_by_email(email_value)
    if not user:
        print(f"No user found with the email : {email_value}")
        return 
    
    title_value, description_value = input ("Enter the title:"), input("Enter the description:")
    session.add(Task(title = title_value, description = description_value, user = user))
    session.commit()
    print(f"Added task to the database. {title_value}:{description_value}")

## R
def query_user():   
    for i in session.query(User).all():                 
        print(f"ID: {i.id}, Name: {i.name}, Email: {i.email}")

def query_task():
    email_value = input("Enter the email of the user for tasks: ")
    user = get_user_by_email(email_value)
    if not user:
        print("User not found.")
        return 
    if not user.tasks:
        print("This user has no tasks.")
        return
    
    for i in user.tasks:
        print(f"Task ID: {i.id}, Title: {i.title}, Description: {i.description}")


## U
def update_user():
    email_value = input("Enter the email of who you want to update: ")
    user = get_user_by_email(email_value)
    if not user:
        print("User not found.")
        return 
    
    user.name = input("Enter the to_update name of this user (leave blank to stay same): ") or user.name  # type: ignore
    user.email = input("Enter the to_update email of this user (leave blank to stay same): ") or user.email  # type: ignore
    session.commit()
    print("User has been updated.")


## D
def delete_user():
    email_value = input("Enter the email of who you want to delete: ")
    user = get_user_by_email(email_value)
    if not user:
        print("User not found.")
        return 
    
    if confirm_action(f"Are you sure you want to delete {user.name}?"):
        session.delete(user)
        session.commit()
        print("User has been deleted.")


def delete_task():
    email_value = input("Enter the email of who you want to delete the task of: ")
    user = get_user_by_email(email_value)
    if not user:
        print("User not found.")
        return 
    
    for i in user.tasks:
        print(f"Task ID: {i.id}, Title: {i.title}, Description: {i.description}")
    
    task_id_to_delete = input("Now, enter the task id to delete: ")
    task = next((j for j in user.tasks if str(j.id)==task_id_to_delete),None) 

    if not task:
        print("No task found with that ID for this user.")
        return 
    
    if confirm_action(f"Are you sure you want to delete this task: {task.id}?"):
        session.delete(task)
        session.commit()
        print("Task has been deleted.")
    

# Main ops
def main() -> None:  
    
    actions = {
        '1':add_user,
        '2':add_task,
        '3':query_user,
        '4':query_task,
        '5':update_user,
        '6':delete_user,
        '7':delete_task
    }
    while True:
        print("\nOptions:\n1. Add User\n2. Add Task\n3. Query Users\n4. Query Tasks\n5. Update User\n6. Delete User\n7. Delete Task\n8. Exit")

        choice = input("Enter an option:")

        if choice == '8':
            print("Exited")
            break
        else:
            action_value = actions.get(choice)   

            if action_value:                 
                action_value()
            else:
                print("That's not an option.")
        
if __name__ =="__main__":
    main()