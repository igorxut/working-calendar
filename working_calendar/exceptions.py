class NotDateException(Exception):
    def __init__(self, class_name):
        super().__init__('Argument \'date\' is \'{}\'. It should be \'datetime.date\'.'.format(class_name))


class NotDayOfWeekException(Exception):
    def __init__(self, class_name):
        super().__init__('Argument \'day\' is \'{}\'. It should be \'DayOfWeek\'.'.format(class_name))


class StartGreaterEndException(Exception):
    def __init__(self):
        super().__init__('Argument \'end_date\' should be greater or equal than argument \'start_date\'')
