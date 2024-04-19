from pygame.math import Vector2

from .base_system import System
from common.managers.event_manager import Event

from common.components import AnimationComponent
from common.components import ControlComponent
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

        self.event_manager.subscribe(self.event_manager.MOVEMENT_KEY_EVENT, self.update_directions)

        self.event_manager.subscribe(self.event_manager.EVENT_LIGHT_ATTACK, self.update_action_queue)
        self.event_manager.subscribe(self.event_manager.EVENT_DODGE, self.update_action_queue)
        self.event_manager.subscribe(self.event_manager.EVENT_INTERACT, self.update_action_queue)

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

    #TODO this should be in a different system, but for now WEEEEEEEE
    def open_main_menu(self, event):
        self.logger.info("Opening Main Menu")
        self.post_event(Event(self.event_manager.CHANGE_STATE, (self.event_manager.MAIN_MENU, True)))

    def update_action_queue(self, event):
        self.logger.info(f"Key Event Received: {event.type, event.data}")
        if event.data[0] == self.event_manager.KEY_DOWN:
            if event.type == self.event_manager.EVENT_DODGE:
                self.action_queue.clear()
            self.action_queue.append((event.type, event.data[1]))          
            if len(self.action_queue) > self.ACTION_QUEUE_MAX_SIZE:
                self.action_queue.pop(0)

    def update_directions(self, event):
        if self.get_component(self.player_ID, EntityStatusComponent).is_acting == False:
            direction_moving = Vector2(0,0)
            direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction
            
            # Check joystick for movement
            if self.game_state.joystick_active:
                if 'x' in event.data['joystick_axis']:
                    if event.data['joystick_axis']['x'] > 0.5:
                        direction_moving.x = 1
                    elif event.data['joystick_axis']['x'] < -0.5:
                        direction_moving.x = -1
            
                if 'y' in event.data['joystick_axis']:
                    if event.data['joystick_axis']['y'] > 0.5:
                        direction_moving.y = 1
                    elif event.data['joystick_axis']['y'] < -0.5:
                        direction_moving.y = -1
            
            # Check moving keys
            if self.event_manager.EVENT_MOVE_DOWN in event.data['keys_down_time'] or self.event_manager.EVENT_MOVE_UP in event.data['keys_down_time'] or self.event_manager.EVENT_MOVE_LEFT in event.data['keys_down_time'] or self.event_manager.EVENT_MOVE_RIGHT in event.data['keys_down_time']:
                if self.event_manager.EVENT_MOVE_UP in event.data['keys_down_time']:
                    direction_moving.y = -1
                if self.event_manager.EVENT_MOVE_DOWN in event.data['keys_down_time']:
                    direction_moving.y = 1
                if self.event_manager.EVENT_MOVE_LEFT in event.data['keys_down_time']:
                    direction_moving.x = -1
                if self.event_manager.EVENT_MOVE_RIGHT in event.data['keys_down_time']:
                    direction_moving.x = 1
                    
            # Check joystick for facing
            if self.game_state.joystick_active:
                x = event.data['joystick_axis']['facing_x']
                y = event.data['joystick_axis']['facing_y']

                # Calculate the magnitude of the joystick input
                magnitude = (x**2 + y**2)**0.5

                # Normalize the joystick input
                if magnitude > 0:  # Avoid division by zero
                    x /= magnitude
                    y /= magnitude

                # Map the normalized joystick input to one of the four directions
                if y < -0.5:
                    direction_facing = "up"
                elif x > 0.5:
                    direction_facing = "right"
                elif y > 0.5:
                    direction_facing = "down"
                elif x < -0.5:
                    direction_facing = "left"
                elif magnitude < 0.1:  # No facing direction is actively being pressed on the joystick
                    # Set the facing direction to the moving direction
                    if direction_moving.x == 1:
                        direction_facing = "right"
                    elif direction_moving.x == -1:
                        direction_facing = "left"
                    elif direction_moving.y == 1:
                        direction_facing = "down"
                    elif direction_moving.y == -1:
                        direction_facing = "up"
            
            # Check facing keys
            if self.event_manager.EVENT_FACE_UP in event.data['keys_down_time'] or self.event_manager.EVENT_FACE_DOWN in event.data['keys_down_time'] or self.event_manager.EVENT_FACE_LEFT in event.data['keys_down_time'] or self.event_manager.EVENT_FACE_RIGHT in event.data['keys_down_time']:
                if self.event_manager.EVENT_FACE_UP in event.data['keys_down_time']:
                    direction_facing = "up"
                if self.event_manager.EVENT_FACE_DOWN in event.data['keys_down_time']:
                    direction_facing = "down"
                if self.event_manager.EVENT_FACE_LEFT in event.data['keys_down_time']:
                    direction_facing = "left"
                if self.event_manager.EVENT_FACE_RIGHT in event.data['keys_down_time']:
                    direction_facing = "right"
            
            # If no facing direction is actively being pressed, set the facing direction to the moving direction
            if not (self.event_manager.EVENT_FACE_UP in event.data['keys_down_time'] or self.event_manager.EVENT_FACE_DOWN in event.data['keys_down_time'] or self.event_manager.EVENT_FACE_LEFT in event.data['keys_down_time'] or self.event_manager.EVENT_FACE_RIGHT in event.data['keys_down_time'] or 'facing_x' in event.data['joystick_axis'] or 'facing_y' in event.data['joystick_axis']):
                if direction_moving.x == 1:
                    direction_facing = "right"
                elif direction_moving.x == -1:
                    direction_facing = "left"
                elif direction_moving.y == 1:
                    direction_facing = "down"
                elif direction_moving.y == -1:
                    direction_facing = "up"
    
            # Set entity status based on direction_moving
            if direction_moving == Vector2(0,0):
                self.get_component(self.player_ID, EntityStatusComponent).is_moving = False
                self.get_component(self.player_ID, EntityStatusComponent).is_idle = True
                self.get_component(self.player_ID, EntityStatusComponent).has_moved = False
            else:
                self.get_component(self.player_ID, EntityStatusComponent).is_moving = True
                self.get_component(self.player_ID, EntityStatusComponent).is_idle = False
                self.get_component(self.player_ID, EntityStatusComponent).has_moved = True
    
            self.get_component(self.player_ID, DirectionFacingComponent).direction = direction_facing.split("_")[0]
            self.get_component(self.player_ID, DirectionMovingComponent).direction = direction_moving

    def update_player_animation(self, delta_time):
        direction_facing = self.get_component(self.player_ID, DirectionFacingComponent).direction

        if self.get_component(self.player_ID, EntityStatusComponent).is_idle:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["idle_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_moving and not self.get_component(self.player_ID, EntityStatusComponent).is_dashing:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["walk_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_dashing:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["dash_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_attacking:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["light_attack_" + direction_facing]
        elif self.get_component(self.player_ID, EntityStatusComponent).is_dodging:
            self.get_component(self.player_ID, AnimationComponent).current_animation = self.get_component(self.player_ID, AnimationComponent).animations["dodge_" + direction_facing]

        #self.logger.info(f"Status: {self.get_component(self.player_ID, EntityStatusComponent).is_idle, self.get_component(self.player_ID, EntityStatusComponent).is_moving, self.get_component(self.player_ID, EntityStatusComponent).is_dashing, self.get_component(self.player_ID, EntityStatusComponent).is_attacking}")
                               
    def handle_actions(self, delta_time):
        if not self.get_component(self.player_ID, EntityStatusComponent).is_acting:
            action = self.action_queue.pop(0)
            if action[0] == self.event_manager.EVENT_LIGHT_ATTACK:
                self.logger.info(f"Handle_Action: {self.event_manager.EVENT_LIGHT_ATTACK}")
                entity_status_component = self.get_component(self.player_ID, EntityStatusComponent)
                entity_status_component.reset()
                entity_status_component.is_attacking = True
                entity_status_component.is_acting = True
            elif action[0] == self.event_manager.EVENT_DODGE:
                self.logger.info(f"Handle_Action: {self.event_manager.EVENT_DODGE}")
                entity_status_component = self.get_component(self.player_ID, EntityStatusComponent)
                entity_status_component.reset()
                entity_status_component.is_dodging = True
                entity_status_component.is_acting = True
            elif action[0] == self.event_manager.EVENT_INTERACT:
                self.logger.info(f"Handle_Action: {self.event_manager.EVENT_INTERACT}")
                #TODO Implement Interact

    def update(self, delta_time):
        control_component = self.get_component(self.player_ID, ControlComponent)

        if control_component.enabled == True:
            if len(self.action_queue) > 0:
                self.handle_actions(delta_time)

            self.update_player_animation(delta_time)
