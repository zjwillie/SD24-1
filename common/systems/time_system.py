from .base_system import System

class WorldTime():
    def __init__(self):
        self.time = 0

        self.hour = 23
        self.minute = 0
        self.second = 0
        self.day = 0
        self.week = 1
        self.month = 1
        self.year = 1344

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

        self.world_time = WorldTime()

        self.log = False

    def update(self, delta_time):
        # Scale delta_time by TIME_FACTOR
        scaled_delta = delta_time * self.TIME_FACTOR
        self.world_time.second += scaled_delta

        # Update minutes and reset seconds if over 60
        if self.world_time.second >= self.SECONDS_PER_MINUTE:
            self.world_time.minute += int(self.world_time.second / self.SECONDS_PER_MINUTE)
            self.world_time.second %= self.SECONDS_PER_MINUTE

        # Update hours and reset minutes if over 60
        if self.world_time.minute >= self.MINUTES_PER_HOUR:
            self.world_time.hour += int(self.world_time.minute / self.MINUTES_PER_HOUR)
            self.world_time.minute %= self.MINUTES_PER_HOUR

        # Update days and reset hours if over 24
        if self.world_time.hour >= self.HOURS_PER_DAY:
            self.world_time.day += int(self.world_time.hour / self.HOURS_PER_DAY)
            self.world_time.hour %= self.HOURS_PER_DAY

        # Update weeks based on days, but not used for month progression
        self.world_time.week = int((self.world_time.day - 1) / self.DAYS_PER_WEEK) + 1

        # Update months and reset days if over DAYS_PER_MONTH
        if self.world_time.day > self.DAYS_PER_MONTH:
            self.world_time.month += int((self.world_time.day - 1) / self.DAYS_PER_MONTH)
            self.world_time.day = 1

        # Update years and reset months if over MONTHS_PER_YEAR
        if self.world_time.month > self.MONTHS_PER_YEAR:
            self.world_time.year += int((self.world_time.month - 1) / self.MONTHS_PER_YEAR)
            self.world_time.month = 1


        self.logger.loggers['system'].info(f"Time: {self.world_time.hour}:{self.world_time.minute}:{self.world_time.second:.2f} - {self.world_time.day}/{self.world_time.month}/{self.world_time.year} - Week {self.world_time.week}") if self.log else None

