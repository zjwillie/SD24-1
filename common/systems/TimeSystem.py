class TimeSystem(System):
    TIME_FACTOR = 100000
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_PER_DAY = 24
    DAYS_PER_WEEK = 7
    WEEKS_PER_MONTH = 4
    MONTHS_PER_YEAR = 12
    DAYS_PER_MONTH = DAYS_PER_WEEK * WEEKS_PER_MONTH
    DAYS_PER_YEAR = DAYS_PER_WEEK * WEEKS_PER_MONTH * MONTHS_PER_YEAR

    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.event_manager.subscribe("move_time_forward", self.move_time_forward)

    def get_seconds_since_created(self, entity):
        age_component = self.entity_manager.get_component(entity, AgeComponent)
        time_since_creation = time.time() - age_component.time_created
        return time_since_creation

    def update(self, delta_time):
        # Scale delta_time by TIME_FACTOR
        scaled_delta = delta_time * self.TIME_FACTOR
        world_time_component.second += scaled_delta

        # Update minutes and reset seconds if over 60
        if world_time_component.second >= self.SECONDS_PER_MINUTE:
            world_time_component.minute += int(world_time_component.second / self.SECONDS_PER_MINUTE)
            world_time_component.second %= self.SECONDS_PER_MINUTE

        # Update hours and reset minutes if over 60
        if world_time_component.minute >= self.MINUTES_PER_HOUR:
            world_time_component.hour += int(world_time_component.minute / self.MINUTES_PER_HOUR)
            world_time_component.minute %= self.MINUTES_PER_HOUR

        # Update days and reset hours if over 24
        if world_time_component.hour >= self.HOURS_PER_DAY:
            world_time_component.day += int(world_time_component.hour / self.HOURS_PER_DAY)
            world_time_component.hour %= self.HOURS_PER_DAY

        # Update weeks based on days, but not used for month progression
        world_time_component.week = int((world_time_component.day - 1) / self.DAYS_PER_WEEK) + 1

        # Update months and reset days if over DAYS_PER_MONTH
        if world_time_component.day > self.DAYS_PER_MONTH:
            world_time_component.month += int((world_time_component.day - 1) / self.DAYS_PER_MONTH)
            world_time_component.day = ((world_time_component.day - 1) % self.DAYS_PER_MONTH) + 1

        # Update years and reset months if over MONTHS_PER_YEAR
        if world_time_component.month > self.MONTHS_PER_YEAR:
            world_time_component.year += int((world_time_component.month - 1) / self.MONTHS_PER_YEAR)
            world_time_component.month = ((world_time_component.month - 1) % self.MONTHS_PER_YEAR) + 1

        print(f"Time: {world_time_component.year}Y {world_time_component.month}M {world_time_component.week}W {world_time_component.day}D {world_time_component.hour}H {world_time_component.minute}M {world_time_component.second}S")

    
    def set_time(self, world_time_component, time):
        world_time_component.time += time

    def move_time_forward(self, world_time_component, hour=0, minute=0, second=0):
        current_hour = int((world_time_component.time / 3600) % self.NUMBER_OF_HOURS_IN_A_DAY)
        current_minute = int((world_time_component.time % 3600) / 60)
        current_second = int(world_time_component.time % 60)
        
        remaining_time_today = self.NUMBER_OF_SECONDS_IN_A_DAY - (current_hour * 3600 + current_minute * 60 + current_second)
        time_until_specified_time_next_day = hour * 3600 + minute * 60 + second
        
        total_time_to_move_forward = remaining_time_today + time_until_specified_time_next_day
        
        self.set(world_time_component, total_time_to_move_forward)

    def move_to_time(self, world_time_component, year=1344, month=1, week=1, day=1, hour=0, minute=0, second=0):
        total_time_to_move_forward = 0

        total_time_to_move_forward += (year - world_time_component.year) * self.NUMBER_OF_DAYS_IN_A_YEAR * self.NUMBER_OF_SECONDS_IN_A_DAY
        total_time_to_move_forward += (month - world_time_component.month) * self.NUMBER_OF_DAYS_IN_A_MONTH * self.NUMBER_OF_SECONDS_IN_A_DAY
        total_time_to_move_forward += (week - world_time_component.week) * self.NUMBER_OF_DAYS_IN_A_WEEK * self.NUMBER_OF_SECONDS_IN_A_DAY
        total_time_to_move_forward += (day - world_time_component.day) * self.NUMBER_OF_SECONDS_IN_A_DAY
        total_time_to_move_forward += (hour - world_time_component.hour) * 3600
        total_time_to_move_forward += (minute - world_time_component.minute) * 60
        total_time_to_move_forward += (second - world_time_component.second)

        self.set(world_time_component, total_time_to_move_forward)
