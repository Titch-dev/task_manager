from datetime import datetime
import re
### Templates ###
from templates import templates as t


def display_formatter(template: str, *dynamic_vars: str | int):
    """Function to dynamically enter variables to display strings

    Parameters:
        template: string to format with variables
        *dynamic_vars: strings and integers to format template

    Returns:
        Concatenated string
    """
    return template.format(*dynamic_vars)


def return_to_menu() -> str:
    """Function to request user input before returning to menu options

    Returns:
        Input request string
    """
    return input('Press enter to return to menu: ')


def read_write(document: str, expression: str = None) -> str | None:
    """Simple function to either read or write to document

    Parameters:
        document (str): Pathname of document to read or write
        expression (str): Expression to write to document if provided

    Returns:
        If used to read document, function will return document as a str,
        else will return None
    """
    with open(f'{document}', 'a+') as f:
        if expression:
            f.write('\n' + expression)  # Writes 'expression' string to 'document'
        else:
            f.seek(0)  # To point to the beginning of the document
            return f.read()


def user_dictionary() -> dict:
    """Function reads user.txt file, and returns data as a dictionary

    Returns:
        A dictionary of usernames (keys) and passwords (values)
    """
    users_raw = read_write('user.txt')
    user_list = users_raw.split('\n')
    user_dict = dict()

    for user in user_list:
        username, password = user.split(', ')
        user_dict[username] = password

    return user_dict


def task_dictionary() -> dict:
    """Function reads tasks.txt file, and returns data as a dictionary

    Returns:
        A dictionary of users (keys) and respective tasks (values)
    """
    raw_tasks = read_write('tasks.txt')
    list_tasks = raw_tasks.split('\n')
    task_dict = dict()
    # Deconstruct each task to retrieve username for Keys in dictionary
    for task in list_tasks:
        username, title, description, start_date, due_date, complete = task.split(', ')
        if username in task_dict:
            task_dict[username].append(task)
        else:
            task_dict[username] = [task]

    return task_dict


def date_validator(start_date):
    """ Function to validate user input and return formated date time string

    Parameters:
       start_date (str): today's date

    Returns:
        User generated date string
    """
    regex = r'[0-9]{1,2}\s[0-9]{1,2}\s[0-9]{4}'

    while True:
        user_input = input('Please enter the due date of the task "dd mm yyyy": ')
        if re.match(regex, user_input):
            day, month, year = user_input.split(' ')
            try:
                valid_date = datetime(int(year), int(month), int(day)).strftime('%d %b %Y')
                if start_date > valid_date:
                    print(display_formatter(t.ERROR_MESSAGE, 'Please set the due date in the future'))
                    continue
                else:
                    return valid_date
            except ValueError as e:
                print(e)  # ValueError message for specific date time exceptions
        else:
            print(display_formatter(t.ERROR_MESSAGE, 'Not a valid date input, please ensure spaces are included'))


def print_task(task: str) -> None:
    """Function to print task template to the console

    Parameters:
        task (str): comma separated values in a string
    """
    username, title, description, start_date, due_date, complete = task.split(', ')
    print(display_formatter(t.TASK, title, username, start_date, due_date, complete, description))


def print_statistics(tasks_amount: int, user_amount: int) -> None:
    """Function to print statistics to console

    Parameters:
        tasks_amount (int): number of tasks
        user_amount (int): number of users
    """
    print(display_formatter(t.STATS, tasks_amount, user_amount))


def login():
    """Function to validate user and respective password exists

    Returns:
        String of username for task_manager session
    """
    while True:
        username_input = input('Please enter your username: ')
        password_input = input('Please enter your password: ')
        users = user_dictionary()

        try:
            if users[username_input] == password_input:
                print(display_formatter(t.CONFIRM_MESSAGE, f'Welcome {username_input}'))
                return username_input
            else:
                print(display_formatter(t.ERROR_MESSAGE, 'You have entered the incorrect password'))
        except KeyError:
            print(display_formatter(t.ERROR_MESSAGE, 'Username does not exist, please contact your admin'))


def register_user(user: str) -> None:
    """Function to allow 'admin' user to create a new user

    Parameters:
        user (str): username of the user currently logged in
    """
    new_username = None
    new_password = None
    existing_users = user_dictionary()
    # Checks whether username already exists
    while not new_username:
        username = input('Please enter the username you wish to register: ')

        if username in existing_users:
            print(display_formatter(t.ERROR_MESSAGE, 'User already in use, please try another...'))
        else:
            new_username = username

    # Checks confirmation of password matches with password
    while not new_password:
        password = input(f'Please enter a password for {new_username}: ')
        confirm_password = input('Please confirm the password again: ')

        if password == confirm_password:
            new_password = password
        else:
            print(display_formatter(t.ERROR_MESSAGE, 'Your password\'s did not match, please try again'))

    # format the new user to write to user.txt
    new_user = '{}, {}'.format(new_username, new_password)
    read_write('user.txt', new_user)

    print(display_formatter(t.CONFIRM_MESSAGE, f'{new_username} has successfully been registered'))


def view_statistics() -> None:
    """ Function to count the number of tasks and users"""
    tasks = task_dictionary()
    users = user_dictionary()
    all_tasks = tasks.values()  # cast all tasks into iterable list
    task_amount = 0

    # Iterate over the tasks and add to the task_amount
    for task in all_tasks:
        task_amount += len(task)

    user_amount = len(users.keys())

    print_statistics(task_amount, user_amount)


def add_task() -> None:
    """Function to validate user inputs and write a task to tasks.txt"""
    users = user_dictionary()

    while True:
        existing_user = input('Please enter the username to add a task to: ')
        # Check user exists and validate user inputs for task
        if existing_user in users:
            title = input('Please enter the title of the task: ')
            description = input('Please enter the description of the task: ')
            start_date = datetime.now().strftime('%d %b %Y')
            due_date = date_validator(start_date)
            # format the new task to write to tasks.txt
            task = '{}, {}, {}, {}, {}, No'.format(existing_user,
                                                   title,
                                                   description,
                                                   start_date,
                                                   due_date)
            read_write('tasks.txt', task)
            return print(display_formatter(t.CONFIRM_MESSAGE, f'{title} has been added to {existing_user}\'s tasks'))
        else:
            print(display_formatter(t.ERROR_MESSAGE, f'{existing_user} does not exist, please try again'))


def view_tasks(user: str = None):
    """Function to parse task data dependent on user provided

    Parameters:
        user (str): Username if provided
    """
    tasks_raw = task_dictionary()

    if user:
        try:
            user_tasks = tasks_raw[user]
            for task in user_tasks:
                print_task(task)
        except KeyError:
            print(display_formatter(t.ERROR_MESSAGE, "You currently have no tasks assigned to you"))
    else:
        all_tasks = tasks_raw.values()
        for tasks in all_tasks:
            for task in tasks:
                print_task(task)


print('*** Welcome to Task Manager ***')

user = login()

while True:
    # Menu output dependent on user
    if user == 'admin':
        menu = input(display_formatter(t.MENU_ADMIN)).lower()
    else:
        menu = input(display_formatter(t.MENU_USER)).lower()

    if menu == 'r' and user == 'admin':
        register_user(user)

    elif menu == 's' and user == 'admin':
        view_statistics()
        return_to_menu()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_tasks()
        return_to_menu()

    elif menu == 'vm':
        view_tasks(user)
        return_to_menu()

    elif menu == 'e':
        print(display_formatter(t.CONFIRM_MESSAGE, 'Goodbye!!!'))
        exit()

    else:
        print(display_formatter(t.ERROR_MESSAGE, "You have entered an invalid input. Please try again"))
