from pygame.math import Vector2

from .base_system import System
from common.managers.event_manager import Event

from common.components import AnimationComponent
from common.components import DirectionMovingComponent
from common.components import DirectionFacingComponent
from common.components import EntityStatusComponent

class PlayerSystem(System):
    ACTION_QUEUE_MAX_SIZE = 5

    def __init__(self, game_state, entity_manager, event_manager, logger):
        super().__init__(game_state, entity_manager, event_manager, logger)

        self.logger = logger.loggers['player_system']

        self.player_ID = self.entity_manager.player_ID

        self.keys_down = {}
        self.action_queue = []

        self.event_manager.subscribe(self.event_manager.EVENT_TAB, self.open_main_menu)

        self.event_manager.subscribe(self.event_manager.KEYS_DOWN_UPDATE, self.update_direction_moving)

    def get_component(self, entity_id, component_type):
        return self.entity_manager.get_component(entity_id, component_type)    

    def post_event(self, event):
        self.logger.info(f"Posting Event: {event.type, event.data}")
        self.event_manager.post(event)

    def open_main_menu(self, event):
        self.logger.info("Opening Main Menu")
        self.post_event(self.event_manager.CHANGE_STATE, (self.event_manager.MAIN_MENU, True))

    def update_action_queue(self, event):
        self.logger.info(f"Key Down Event Received: {event.type, event.data}")
        if event.data[0] == self.event_manager.KEY_DOWN:
            self.action_queue.append((event.type, event.data[1]))

    def update_direction_moving(self, event):
        direction_moving = Vector2(0,0)
        direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction
        #self.logger.info(f"Keys Down: {event.data}")
        if self.event_manager.EVENT_UP in event.data:
            direction_moving += Vector2(0, -1)
        if self.event_manager.EVENT_DOWN in event.data:
            direction_moving += Vector2(0, 1)
        if self.event_manager.EVENT_LEFT in event.data:
            direction_moving += Vector2(-1, 0)
        if self.event_manager.EVENT_RIGHT in event.data:
            direction_moving += Vector2(1, 0)
        
        if self.event_manager.EVENT_RUN in event.data:
            self.get_component(self.player_ID, EntityStatusComponent).is_running = True
        else:
            self.get_component(self.player_ID, EntityStatusComponent).is_running = False
        
        if direction_moving == Vector2(0,0):
            self.get_component(self.player_ID, EntityStatusComponent).is_moving = False
            self.get_component(self.player_ID, EntityStatusComponent).is_idle = True
            self.get_component(self.player_ID, EntityStatusComponent).has_moved = False
        else:
            self.get_component(self.player_ID, EntityStatusComponent).is_moving = True
            self.get_component(self.player_ID, EntityStatusComponent).is_idle = False
            self.get_component(self.player_ID, EntityStatusComponent).has_moved = True
        
        # Set direction facing
        if direction_moving == Vector2(0, -1):
            direction_facing = "up"
        elif direction_moving == Vector2(0, 1):
            direction_facing = "down"
        elif direction_moving == Vector2(-1, 0):
            direction_facing = "left"
        elif direction_moving == Vector2(1, 0):
            direction_facing = "right"

        elif direction_moving == Vector2(1, 1):
            direction_facing = "right_down"
        elif direction_moving == Vector2(-1, 1):
            direction_facing = "left_down"
        elif direction_moving == Vector2(1, -1):
            direction_facing = "right_up"
        elif direction_moving == Vector2(-1, -1):
            direction_facing = "left_up"

        self.get_component(self.player_ID, DirectionFacingComponent).direction = direction_facing.split("_")[0]

        self.get_component(self.player_ID, DirectionMovingComponent).direction = direction_moving

        self.logger.info(f"Moving Direction: {self.get_component(self.player_ID, DirectionMovingComponent).direction}")
        self.logger.info(f"Facing Direction: {self.get_component(self.player_ID, DirectionFacingComponent).direction}")


    def update_animation(self, delta_time):
        direction_moving = self.get_component(self.player_ID, DirectionMovingComponent).direction
        direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction

        if self.get_component(self.player_ID, EntityStatusComponent).is_idle:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["idle_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_moving and not self.get_component(self.player_ID, EntityStatusComponent).is_running:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["walk_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_running:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["run_" + direction_facing]


    def update(self, delta_time):
        self.update_animation(delta_time)
        #self.logger.info(f"Keys that are down: {self.keys_down}")
        #self.logger.info(f"Action Queue: {self.action_queue}")
        #print(self.get_component(self.player_ID, NameComponent).name)