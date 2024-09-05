from datetime import datetime
import re


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
                    print('Please set the due date in the future')
                    continue
                else:
                    return valid_date
            except ValueError as e:
                print(e)  # ValueError message for specific date time exceptions
        else:
            print('Not a valid date input, please ensure spaces are included')


def print_task(task: str) -> None:
    """Function to print task template to the console

    Parameters:
        task (str): comma separated values in a string
    """
    username, title, description, start_date, due_date, complete = task.split(', ')
    print('-' * 80)
    print(f'''Task:\t\t{title}
Assigned to:\t{username}
Date assigned:\t{start_date}
Due date:\t{due_date}
Task Complete?\t{complete}
Task Description:
 {description}''')
    print('-' * 80)


def print_statistics(tasks_amount: int, user_amount: int) -> None:
    """Function to print statistics to console

    Parameters:
        tasks_amount (int): number of tasks
        user_amount (int): number of users
    """
    print('-' * 80)
    print(f'''*** Task Manager Statistics ***
Total tasks:\t{tasks_amount}
Total users:\t{user_amount}''')
    print('-' * 80)


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
                print(f'Welcome {username_input}')
                return username_input
            else:
                print('You have entered the incorrect password')
        except KeyError:
            print('Your username does not exist, please contact your admin')


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
            print('User already in use, please try another...')
        else:
            new_username = username

    # Checks confirmation of password matches with password
    while not new_password:
        password = input(f'Please enter a password for {new_username}: ')
        confirm_password = input('Please confirm the password again: ')

        if password == confirm_password:
            new_password = password
        else:
            print('Your password\'s did not match, please try again')

    # format the new user to write to user.txt
    new_user = '{}, {}'.format(new_username, new_password)
    read_write('user.txt', new_user)

    print(f'{new_username} has successfully been registered')


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
            return print(f'{title} has been added to {existing_user}\'s tasks')
        else:
            print(f'{existing_user} does not exist, please try again')


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
            print("You currently have no tasks assigned to you")
    else:
        all_tasks = tasks_raw.values()
        for tasks in all_tasks:
            for task in tasks:
                print_task(task)


print('*** Welcome to Task Manager ***')

user = login()

while True:
    # Menu output dependent on user
    menu = input(f'''Select one of the following options:
{'r - register a user' if user == 'admin' else ''}
{'s - view statistics' if user == 'admin' else ''}
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').lower()

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
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")