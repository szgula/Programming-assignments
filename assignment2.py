# assignment 2

from robot_world import *

def script_0_demo(robot):
    # demo script to show the capabilities of the robot
    # read the assignment instructions for details

    # demo of scans
    direction = robot.scan_direction()
    print("current robot direction:", direction)
    obstacle = robot.scan_object_ahead()
    print("first obstacle ahead:", obstacle)
    steps = robot.scan_steps_ahead()
    print("steps to the first obstacle:", steps)
    energy = robot.scan_energy()
    print("remaining energy for steps:", energy)

    # demo of stepping and turning
    robot.step_forward()
    robot.step_forward()
    robot.turn_left()
    robot.turn_right()
    robot.turn_right()
    robot.turn_left()
    robot.step_back()
    robot.step_back()
    robot.turn_right()

    # demo of detections
    print()
    direction = robot.scan_direction()
    print("current robot direction:", direction)
    obstacle = robot.scan_object_ahead()
    print("first obstacle ahead:", obstacle)
    steps = robot.scan_steps_ahead()
    print("steps to the first obstacle:", steps)
    energy = robot.scan_energy()
    print("remaining energy for steps:", energy)

    # demo of grabbing, pushing forward, dragging backward and releasing of a block
    robot.step_forward() # when the robot faces and touches the block it can grab it
    robot.grab_release_block()
    robot.step_forward()
    robot.step_back()
    robot.grab_release_block()
    robot.step_back()
    robot.turn_right()
    robot.turn_right()
    robot.turn_right()
    return # end of demo

################################################
#   helper functions defined by you can go here
#   start of helper function part

def move_1(robot):   #walk to first obstacle and turn right
    steps = robot.scan_steps_ahead() #check how many steps to the first obstacle
    while steps > 0:
        robot.step_forward()
        steps -= 1
    robot.turn_right()

def move_2(robot):  #walk to first obstacle and stop
    steps = robot.scan_steps_ahead() #check how many steps to the first obstacle
    while steps > 0:
        robot.step_forward()
        steps -= 1
        
        
#   end of helper function part
################################################

################################################
#   start of assignment solution code

def script_1(robot):
    move_1(robot)         #helper function
    move_1(robot)         #robot in the corner
    measurement_1 = robot.scan_energy()     #remaining energy
    move_1(robot)
    move_1(robot)
    move-1(robot)
    move_1(robot)
    measurement_2 = robot.scan_energy() #remaining energy after steps
    circumference = measurement_1 - measurement_2
    print("It takes", circumference, "steps to walk around the world.")
    return


def script_2(robot):
    direction = robot.scan_direction() #current direction 
    if direction == 'RIGHT':
        robot.turn_right()
    elif direction == "LEFT":
        robot.turn_left()
    elif direction == "UP":
        robot.turn_right()
        robot.turn_right()
    else:
        pass            #now robot is heading 'DOWN'
    move_2(robot)       #go to the wall with helper function
    robot.turn_right()
    steps_1 = robot.scan_steps_ahead()
    robot.turn_right()
    length = robot.scan_steps_ahead()  #length of the room (not world)
    robot.turn_right()
    steps_2 = robot.scan_steps_ahead() 
    width = steps_1 + steps_2 #width of the room w(not world)          
    robot.turn_left()
    while length != 0:
        robot.step_forward()
        robot.turn_right()
        steps_r = robot.scan_steps_ahead()      #how many steps robot can do to the right 
        robot.turn_right()
        robot.turn_right()
        steps_l = robot.scan_steps_ahead()      #how many steps robot can do to the left 
        robot.turn_right()
        length -= 1
        current_width = steps_r + steps_l       #width of the room in current position 
        if current_width != width:
            if width - steps_r <= 0:
                robot.turn_right()
                move_2(robot)       #move helper function
                break               #stop 'while'
            else:
                robot.turn_left()
                move_2(robot)       #move helper function
                break               #stop 'while'
    return


def script_3(robot):
    direction = robot.scan_direction() #current direction 
    if direction == 'RIGHT':
        robot.turn_right()
    elif direction == "LEFT":
        robot.turn_left()
    elif direction == "UP":
        robot.turn_right()
        robot.turn_right()
    else:
        pass            #now robot is heading 'DOWN'
    move_2(robot)       #move with helper function
    robot.turn_right()
    steps_1 = robot.scan_steps_ahead()
    robot.turn_right()
    length = robot.scan_steps_ahead()  #length of the world
    robot.turn_right()
    steps_2 = robot.scan_steps_ahead() 
    width = steps_1 + steps_2 #width of the world        
    robot.turn_left()
    while length != 0:
        robot.step_forward()
        robot.turn_right()
        steps_r = robot.scan_steps_ahead()      #how many steps robot can do to the right 
        robot.turn_right()
        robot.turn_right()
        steps_l = robot.scan_steps_ahead()      #how many steps robot can do to the left 
        robot.turn_right()
        length -= 1
        current_width = steps_r + steps_l       #width of the room in current position 
        if current_width != width:
            robot.turn_right()
            obstacle = robot.scan_object_ahead()
            if obstacle == 'Tile':
                move_2(robot)           #move with helper function
                robot.step_forward()    #robot on top of the tile
                break              #stop 'while'
            else:
                robot.turn_right()
                robot.turn_right()
                move_2(robot)            #move with helper function
                robot.step_forward()    #robot on top of the tile
                break                   #stop 'while'
            
#if robot has not found the Thile it means that it is on his way
    robot.turn_right()  
    robot.turn_right()
    obstacle = robot.scan_object_ahead()
    if obstacle == 'Tile':
        move_2(robot)           #move with helper function
        robot.step_forward()    #robot on top of the tile
        robot.turn_()
        
    direction = robot.scan_direction() #check current direction and faced robot to 'LEFT'
    if direction == 'RIGHT':
        robot.turn_right()
        robot.turn_right()
    elif direction == 'DOWN':
        robot.turn_right()
    elif direction == 'UP':
        robot.turn_left()        
#find the position of "Title"
#robot is heading "LEFT"
    steps_left = robot.scan_steps_ahead()      #how many steps robot can do to the left 
    robot.turn_left() 
    steps_down = robot.scan_steps_ahead()       #how many steps robot can do down
    print('The tile is at', steps_left, 'steps RIGHT and', steps_down, 'steps UP from the bottom-left corner')
    return

def script_4(robot):
    # your solution of 4. Walk around the Block here
    return

def script_5(robot):
    # your solution of 5. Follow the Tile Path here
    return

def script_6(robot):
    # your solution of 6. Push the Block over the Tile here
    return

#   end of assignment solution code
################################################

def show_menu():
    print()
    print("options:")
    print("  (0) demo script")
    print("  (1) run around the room")
    print("  (2) switch rooms")
    print("  (3) where is the tile?")
    print("  (4) around the block")
    print("  (5) walk the tile path")
    print("  (6) push the block over the tile")
    print("  (s) change speed of the script")
    print("  (q) quit")

def main():
    pygame.init()
    robot = RobotWorld(cell_size = 40, step_time_in_ms = 50)

    print("0HV120 Assignment 2 (2017)")
    show_menu()
    option = input("your choice: ")
    while option != 'q':
        if option.isdigit():
            level = int(option)
            run_script = robot.start_level(level)
            if run_script:
                if level == 0:
                    script_0_demo(robot)
                elif level == 1:
                    script_1(robot)
                elif level == 2:
                    script_2(robot)
                elif level == 3:
                    script_3(robot)
                elif level == 4:
                    script_4(robot)
                elif level == 5:
                    script_5(robot)
                elif level == 6:
                    script_6(robot)
            robot.stop_level(run_script)
        elif option == 's':
            answer = input("Enter step time in ms between 50 and 1000: ")
            step_time = int(answer)
            robot.set_step_time(step_time)
        elif option == 'q':
            print("thank you for playing")
        else:
            print("i did not recognise option '" + option + "'.")
            show_menu()
        show_menu()
        option = input("option: ")

    # 'q' pressed: exit program
    pygame.quit()

main()
