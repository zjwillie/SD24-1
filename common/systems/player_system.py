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

        self.event_manager.subscribe(self.event_manager.MOVEMENT_KEY_EVENT, self.update_direction)

        self.event_manager.subscribe(self.event_manager.EVENT_LIGHT_ATTACK, self.update_action_queue)

        self.event_manager.subscribe(self.event_manager.PLAYER_ANIMATION_FINISHED, self.handle_animation_finished)

        self.event_manager.subscribe(self.event_manager.EVENT_RUN, self.update_dashing_flag)

    def update_dashing_flag(self, event):
        if event.data[0] == self.event_manager.KEY_DOWN:
            self.get_component(self.player_ID, EntityStatusComponent).is_dashing = True
        else:
            self.get_component(self.player_ID, EntityStatusComponent).is_dashing = False

    def handle_animation_finished(self, event):
        direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction
        self.logger.info(f"Player Animation Finished: {event.data}")
        self.get_component(self.player_ID, EntityStatusComponent).reset()

        self.get_component(self.player_ID, EntityStatusComponent).is_idle = True
        self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["idle_" + direction_facing]

    #TODO Keep in mind that the player may be any entity, this way can control others if needed
    def set_player_ID(self, player_ID):
        self.player_ID = player_ID

    def get_component(self, entity_id, component_type):
        return self.entity_manager.get_component(entity_id, component_type)    

    def post_event(self, event):
        self.logger.info(f"Posting Event: {event.type, event.data}")
        self.event_manager.post(event)

    def open_main_menu(self, event):
        self.logger.info("Opening Main Menu")
        self.post_event(Event(self.event_manager.CHANGE_STATE, (self.event_manager.MAIN_MENU, True)))

    def update_action_queue(self, event):
        self.logger.info(f"Key Event Received: {event.type, event.data}")
        if event.data[0] == self.event_manager.KEY_DOWN:
            self.action_queue.append((event.type, event.data[1]))
            if len(self.action_queue) > self.ACTION_QUEUE_MAX_SIZE:
                self.action_queue.pop(0)

    def update_direction(self, event):
        if self.get_component(self.player_ID, EntityStatusComponent).is_attacking == False:
            direction_moving = Vector2(0,0)
            direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction

            # Handle joystick events
            if event.data['joystick_axis'] and ('x' in event.data['joystick_axis'] or 'y' in event.data['joystick_axis']):
                if 'x' in event.data['joystick_axis']:
                    direction_moving.x = event.data['joystick_axis']['x']
                if 'y' in event.data['joystick_axis']:
                    direction_moving.y = event.data['joystick_axis']['y']

                # Normalize direction_moving for full 360 degree movement
                if direction_moving.length() > 0:
                    direction_moving = direction_moving.normalize()

                # Determine the direction facing based on the relative values of x and y
                if direction_moving.x > 0:
                    if direction_moving.y > 0:
                        direction_facing = "right_down"
                    elif direction_moving.y < 0:
                        direction_facing = "right_up"
                    else:
                        direction_facing = "right"
                elif direction_moving.x < 0:
                    if direction_moving.y > 0:
                        direction_facing = "left_down"
                    elif direction_moving.y < 0:
                        direction_facing = "left_up"
                    else:
                        direction_facing = "left"
                else:
                    if direction_moving.y > 0:
                        direction_facing = "down"
                    elif direction_moving.y < 0:
                        direction_facing = "up"

            # If no joystick events, handle keyboard events
            if self.event_manager.EVENT_UP in event.data['keys_down_time'] or self.event_manager.EVENT_DOWN in event.data['keys_down_time'] or self.event_manager.EVENT_LEFT in event.data['keys_down_time'] or self.event_manager.EVENT_RIGHT in event.data['keys_down_time']:
                if self.event_manager.EVENT_UP in event.data['keys_down_time']:
                    direction_moving.y = -1
                if self.event_manager.EVENT_DOWN in event.data['keys_down_time']:
                    direction_moving.y = 1
                if self.event_manager.EVENT_LEFT in event.data['keys_down_time']:
                    direction_moving.x = -1
                if self.event_manager.EVENT_RIGHT in event.data['keys_down_time']:
                    direction_moving.x = 1

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
    
            # Set entity status based on direction_moving
            if direction_moving == Vector2(0,0):
                self.get_component(self.player_ID, EntityStatusComponent).is_moving = False
                self.get_component(self.player_ID, EntityStatusComponent).is_idle = True
                self.get_component(self.player_ID, EntityStatusComponent).has_moved = False
                self.get_component(self.player_ID, EntityStatusComponent).is_dashing = False
            else:
                self.get_component(self.player_ID, EntityStatusComponent).is_moving = True
                self.get_component(self.player_ID, EntityStatusComponent).is_idle = False
                self.get_component(self.player_ID, EntityStatusComponent).has_moved = True
    
            self.get_component(self.player_ID, DirectionFacingComponent).direction = direction_facing.split("_")[0]
            self.get_component(self.player_ID, DirectionMovingComponent).direction = direction_moving


    def update_animation(self, delta_time):
        direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction

        if self.get_component(self.player_ID, EntityStatusComponent).is_idle:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["idle_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_moving and not self.get_component(self.player_ID, EntityStatusComponent).is_dashing:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["walk_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_dashing:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["dash_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_attacking:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["light_attack_" + direction_facing]

        self.logger.info(f"Status: {self.get_component(self.player_ID, EntityStatusComponent).is_idle, self.get_component(self.player_ID, EntityStatusComponent).is_moving, self.get_component(self.player_ID, EntityStatusComponent).is_dashing, self.get_component(self.player_ID, EntityStatusComponent).is_attacking}")

                                    
    def handle_actions(self, delta_time):
            if not self.get_component(self.player_ID, EntityStatusComponent).is_acting:
                action = self.action_queue.pop(0)
                if action[0] == self.event_manager.EVENT_LIGHT_ATTACK:
                    self.logger.info(f"Handle_Action: {self.event_manager.EVENT_LIGHT_ATTACK}")
                    entity_status_component = self.get_component(self.player_ID, EntityStatusComponent)
                    entity_status_component.reset()
                    entity_status_component.is_attacking = True
                    entity_status_component.is_acting = True

    def update(self, delta_time):
        if len(self.action_queue) > 0:
            self.handle_actions(delta_time)

        self.update_animation(delta_time)
