# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:30:44 2020

@author: Lawrence
"""


# -*- coding: utf-8 -*-

"""
Created on Sun May 10 11:51:24 2020

@author: Lawrence
"""

import pygame, sys, time, traceback
# Dijisktra Algorithm

class Points:
    def __init__(self,maze_dim,index):
        self.pre_vertex = -1
        self.steps = maze_dim*maze_dim
        self._index = index
        self.neighbors = []  # including neighbor indexes and cost
        self.coordinates = ()
        self.visited = False
        self.blocked = False
    def get_index(self):
        return self._index
    
    def set_step(self,step_num):
        self.steps = step_num
        
    def get_step(self):
        return self.steps
    
    def set_pre_vertex(self,vertex):
        self.pre_vertex = vertex  
        
    def get_pre_vertex(self):
        return self.pre_vertex
    
    def set_neighbors(self,list_neighbors):
        self.neighbors = list_neighbors
        
    def get_neighbors(self):
        neighbor_name_list = []
        for i in range(len(self.neighbors)):
            neighbor_name_list.append(self.neighbors[i][0])
        return neighbor_name_list
    
    def set_cost(self,neighbor_name,cost_value,loop):
        if loop >=1:
            for i in range(len(self.neighbors)):
                if self.neighbors[i][0] == neighbor_name:
                    self.neighbors[i][1] = cost_value
                    loop -= 1
                    point_objects[neighbor_name].set_cost(self._index,cost_value,loop) 
    
    def get_cost(self,neighbor_name):
        for i in range(len(self.neighbors)):
            if self.neighbors[i][0] == neighbor_name:
                return self.neighbors[i][1]
    
    def set_point_coordinate(self,coordinates):
        self.coordinates = coordinates

    def get_point_coordinates(self):
        return self.coordinates
    
    def set_visited(self):
        self.visited = True
        
    def check_visited(self):
        return self.visited
    
    def set_block(self):
        self.blocked = True
        
    def get_block_status(self):
        return self.blocked

    
start_node = (20,21)
end_node = (36,24)
maze_dim = 90


def setup_lists():
    global max_index
    global point_list,point_index,visited_node
    point_list = ()
    # create the point list
    list_x = [i for i in range(maze_dim)]
    list_x = list_x*maze_dim
    list_y = []
    for i in range(maze_dim):
            list_y.append(i)
            for _ in range(maze_dim-1):
                list_y.append(i)
                
    point_list = tuple(zip(list_y,list_x))
    point_index = [i for i in range(len(point_list))]
    max_index = max(point_index)
    visited_node = []
    
# node_number = {}
# # create the point number for each point
# for i in range(len(point_list)):
#     node_number.update({point_list[i] : point_index[i]})

# connect the neighbr nodes together
def setup_neighbors():
    global neighbor_table
    neighbor_table = {i : [] for i in point_index }
    for point in point_index:
        if point + maze_dim > max_index:
            pass
        else:
            neighbor_table[point].append(point+maze_dim)
            neighbor_table[point+maze_dim].append(point)
            
        if (point + 1) % maze_dim == 0 or point + 1 > max_index:
            pass
        else:
            neighbor_table[point].append(point+1)
            neighbor_table[point+1].append(point)

# Create the list of point objects
def setup_points():
    global start_point,end_point
    global point_objects   
    point_objects = []
    for i in range(len(point_index)):
        adj_neighbors_values = []
        adj_neighbors_values.clear()
        point_objects.append(Points(maze_dim,i))    
        adj_neighbors = neighbor_table[i]
        for j in range(len(neighbor_table[i])):
            adj_neighbors_values.append([neighbor_table[i][j],1])
        point_objects[i].set_neighbors(adj_neighbors_values) 
        point_coordinate = point_list[i]
        point_objects[i].set_point_coordinate(point_coordinate)
    
    for i in range(len(point_objects)):
        if point_objects[i].get_point_coordinates() == start_node:
            point_objects[i].set_step(0)
            start_point = point_objects[i]
        if point_objects[i].get_point_coordinates() == end_node:
            end_point = point_objects[i]

def run():
    global step_list, current_point, next_point_temp,min_step_list, point_check
    global neighbor_table, point_list, point_index, point_objects
    # setup_lists()
    # setup_neighbors()
    # # setup_points()
    # del neighbor_table
    # del point_list
    # del point_index
    current_point = start_point  
    current_point.set_step(0)
    found_point = False
    number_of_steps = 0
    point_check = []
    while( found_point is not True):
        yield current_point
        current_point.set_visited()
        # set steps for neighbor points
        # get the neighbors from the current point
        neighbors_temp = current_point.get_neighbors()
        # compare the steps generated from current point with existing steps
        # current_step = current_point.get_step()+1
        for neighbor in neighbors_temp:
            if point_objects[neighbor].get_block_status() == False:
                if point_objects[neighbor].check_visited() == False:
                        if neighbor not in point_check:
                            point_check.append(neighbor)
                        # continue to compare steps
                        # find the cost between 2 points
                        cost_between_points = current_point.get_cost(neighbor)
                        current_step = current_point.get_step() + cost_between_points
                        neighbor_step_temp = point_objects[neighbor].get_step()
                        if current_step < neighbor_step_temp:
                            point_objects[neighbor].set_step(current_step)
                            point_objects[neighbor].set_pre_vertex(current_point.get_index())
                        else:
                            pass
                
        if found_point is not True:   
        # compare all steps available to pick the node
            min_step_list = []
            min_step_list.clear()
            min_point_list = []
            min_point_list.clear()
            for i in point_check:
                if point_objects[i].check_visited() == False:
                    min_step_list.append(point_objects[i].get_step())
                    min_point_list.append(point_objects[i].get_index())
            for i in range(len(min_step_list)):
                min_step = min(min_step_list)
                min_index = min_step_list.index(min_step)
                min_point_index = min_point_list[min_index]
                next_point_temp = point_objects[min_point_index]
                if i == len(min_step_list) - 1:
                    point_check.remove(min_point_index)
                    pass
            # After findind next point -> confirm previous point
            current_point = next_point_temp
            number_of_steps += 1
            # del next_point_temp
            # Found the point
            if current_point == end_point:
                found_point = True
                yield current_point
        # Found the point
        if found_point is True:
            step_list = [current_point.get_index()]
            pre_point = current_point.get_pre_vertex()
            while(pre_point != -1):
                step_list.append(pre_point)
                current_point = point_objects[pre_point]
                pre_point = current_point.get_pre_vertex()
            step_list = list(reversed(step_list))
            break



if __name__ == '__main__':
    
    # pygame init
    pygame.init()
    # Window Init
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 1000
    win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
##########################################    SETUP  ###################################################
    # setup the list of points
    setup_lists()
    setup_neighbors()
    setup_points()
    
    width = 24
    height = 24
    num_of_box = SCREEN_WIDTH//width
    # valid values for boxes coordinates
    x_valid = [width//2 + i*width for i in range(num_of_box)]
    y_valid = [height//2 + i*height for i in range(num_of_box)]
    # list of boxes drawn by mouse
    rect_coor_list = []    
    # list of points in the diji algo
    current_point_list = []
    # original coor of the diji algo
    original_coor = []
    # number of running times for algo
    run_for_once = 1
    # list of points in the final path
    final_path = []
    # number of drawing the final path
    run_path = 1
    j=0
    # finish obstacle?
    finish_obstacle = False
    # set obstacles
    set_obstacles = False
    run_obstacle = 1
    press = False
    # variables for drawing path weight
    path_weight_style = ['dirt','jungle','river','wall']
    chosen_style = path_weight_style[-1]
    # jungle line list
    jungle_list = []
    jungle_check = 0
    # river line list
    river_list = []
    river_check = 0
    # dirt_line list
    dirt_list = []
    dirt_check = 0
    
    # Draw the rectangles          
    def draw_rect(rect):
        pygame.draw.rect(win,pygame.Color('salmon'),rect)
    
    def draw_boxes(rect_coordinates):
        for rect_coor in rect_coordinates:
            rect = pygame.Rect(rect_coor[0],rect_coor[1],width,height)
            rect.centerx = rect_coor[0]
            rect.centery = rect_coor[1]
            pygame.draw.rect(win,pygame.Color('darkmagenta'),rect)
            
    def draw_initial_points():
        global rect_start, rect_end
        rect_start = pygame.Rect(0,0,width,height)
        rect_end = pygame.Rect(0,0,width,height)
        rect_start.centerx = width/2 + start_node[0]*width
        rect_start.centery = height/2 + start_node[1]*height
        rect_end.centerx = width/2 + end_node[0]*width
        rect_end.centery = height/2 + end_node[1]*height            
        pygame.draw.rect(win, pygame.Color('white'),rect_start)
        pygame.draw.rect(win, pygame.Color('white'),rect_end)
    
    
    def draw_finished_algo(coordinates):
        for coor_pair in coordinates:
            rect = pygame.Rect(0,0,width,height)
            rect.centerx = coor_pair[0]
            rect.centery = coor_pair[1]
            draw_rect(rect)
        
    def draw_final_path(coordinates):
        for coor_pair in coordinates:
            rect = pygame.Rect(0,0,width,height)
            rect.centerx = coor_pair[0]
            rect.centery = coor_pair[1]
            pygame.draw.rect(win,pygame.Color('black'),rect)
            
    def add_obstacles(coordinates):
        global point_objects
        for coor_pair in coordinates:
            coor_pair_x = int((coor_pair[0]-(width/2))//width)
            coor_pair_y = int((coor_pair[1]-(height/2))//height)
            for i in range(len(point_objects)):
                if (coor_pair_x,coor_pair_y) == point_objects[i].get_point_coordinates():
                    point_objects[i].set_block()
                    break
                
    def add_jungle_path(coordinates):
        global point_objects
        for i in range(len(coordinates)-1):
            if coordinates[i] != coordinates[i+1] and coordinates[i] != [1000,1000]\
                and coordinates[i+1] != [1000,1000]:
                coor_pair_x = int((coordinates[i][0]-(width/2))//width)
                coor_pair_y = int((coordinates[i][1]-(height/2))//height)
                coor_pair_next_x = int((coordinates[i+1][0]-(width/2))//width)
                coor_pair_next_y = int((coordinates[i+1][1]-(height/2))//height)
                point_1 = point_list.index((coor_pair_x,coor_pair_y))
                point_2 = point_list.index((coor_pair_next_x,coor_pair_next_y))
                point_objects[point_1].set_cost(point_2,2,2)
                # print(str(point_1)+' '+str(point_2))
                
    def add_river_path(coordinates):
        global point_objects
        for i in range(len(coordinates)-1):
            if coordinates[i] != coordinates[i+1] and coordinates[i] != [1000,1000]\
                and coordinates[i+1] != [1000,1000]:
                coor_pair_x = int((coordinates[i][0]-(width/2))//width)
                coor_pair_y = int((coordinates[i][1]-(height/2))//height)
                coor_pair_next_x = int((coordinates[i+1][0]-(width/2))//width)
                coor_pair_next_y = int((coordinates[i+1][1]-(height/2))//height)
                point_1 = point_list.index((coor_pair_x,coor_pair_y))
                point_2 = point_list.index((coor_pair_next_x,coor_pair_next_y))
                point_objects[point_1].set_cost(point_2,3,2)
                # print(str(point_1)+' '+str(point_2)) 
    
    def add_dirt_path(coordinates):
        global point_objects
        for i in range(len(coordinates)-1):
            if coordinates[i] != coordinates[i+1] and coordinates[i] != [1000,1000]\
                and coordinates[i+1] != [1000,1000]:
                coor_pair_x = int((coordinates[i][0]-(width/2))//width)
                coor_pair_y = int((coordinates[i][1]-(height/2))//height)
                coor_pair_next_x = int((coordinates[i+1][0]-(width/2))//width)
                coor_pair_next_y = int((coordinates[i+1][1]-(height/2))//height)
                point_1 = point_list.index((coor_pair_x,coor_pair_y))
                point_2 = point_list.index((coor_pair_next_x,coor_pair_next_y))
                point_objects[point_1].set_cost(point_2,0.5,2)
    
                     
        
                
    def draw_jungle_line(coordinates):
        global jungle_check
        for i in range(len(coordinates)-1):
            coor_pair_x = int((coordinates[i][0]-(width/2))//width)
            coor_pair_y = int((coordinates[i][1]-(height/2))//height)
            coor_pair_next_x = int((coordinates[i+1][0]-(width/2))//width)
            coor_pair_next_y = int((coordinates[i+1][1]-(height/2))//height)
            if (abs(coor_pair_next_x - coor_pair_x) == 1\
                and abs(coor_pair_next_y - coor_pair_y) == 0)\
                or (abs(coor_pair_next_x - coor_pair_x) == 0\
                and abs(coor_pair_next_y - coor_pair_y) == 1):
                    pygame.draw.line(win,pygame.Color('green'),(coordinates[i][0],coordinates[i][1]),\
                                     (coordinates[i+1][0],coordinates[i+1][1]),6)
            else:
                if press == False and jungle_check == 1:
                    jungle_list.append([1000,1000])
                    jungle_check = 0
                    
    def draw_river_line(coordinates):
        global river_check
        for i in range(len(coordinates)-1):
            coor_pair_x = int((coordinates[i][0]-(width/2))//width)
            coor_pair_y = int((coordinates[i][1]-(height/2))//height)
            coor_pair_next_x = int((coordinates[i+1][0]-(width/2))//width)
            coor_pair_next_y = int((coordinates[i+1][1]-(height/2))//height)
            if (abs(coor_pair_next_x - coor_pair_x) == 1\
                and abs(coor_pair_next_y - coor_pair_y) == 0)\
                or (abs(coor_pair_next_x - coor_pair_x) == 0\
                and abs(coor_pair_next_y - coor_pair_y) == 1):
                    pygame.draw.line(win,pygame.Color('dodgerblue'),(coordinates[i][0],coordinates[i][1]),\
                                     (coordinates[i+1][0],coordinates[i+1][1]),6)
            else:
                if press == False and river_check == 1:
                    river_list.append([1000,1000])
                    river_check = 0
    
    def draw_dirt_line(coordinates):
        global dirt_check
        for i in range(len(coordinates)-1):
            coor_pair_x = int((coordinates[i][0]-(width/2))//width)
            coor_pair_y = int((coordinates[i][1]-(height/2))//height)
            coor_pair_next_x = int((coordinates[i+1][0]-(width/2))//width)
            coor_pair_next_y = int((coordinates[i+1][1]-(height/2))//height)
            if (abs(coor_pair_next_x - coor_pair_x) == 1\
                and abs(coor_pair_next_y - coor_pair_y) == 0)\
                or (abs(coor_pair_next_x - coor_pair_x) == 0\
                and abs(coor_pair_next_y - coor_pair_y) == 1):
                    pygame.draw.line(win,pygame.Color('brown'),(coordinates[i][0],coordinates[i][1]),\
                                     (coordinates[i+1][0],coordinates[i+1][1]),6)
            else:
                if press == False and dirt_check == 1:
                    dirt_list.append([1000,1000])
                    dirt_check = 0
    
                    
    def draw_grid():
        for row in range(0,SCREEN_WIDTH,width):
            pygame.draw.line(win,pygame.Color('maroon'),(row,0),(row,SCREEN_HEIGHT),4)
        for col in range(0,SCREEN_HEIGHT,height):
            pygame.draw.line(win,pygame.Color('maroon'),(0,col),(SCREEN_WIDTH,col),4)
        
    def draw_everything():
        draw_initial_points()
        draw_dirt_line(dirt_list)
        draw_jungle_line(jungle_list)
        draw_river_line(river_list)
        draw_boxes(rect_coor_list)
        draw_grid()
        
        
    
        
################################# RUNNING THE PYGAME MODULE #################################
            
    running = True    
    try:
        while running:
            win.fill((195,50,19))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    press = True
                    if jungle_check == 0:
                        jungle_check = 1
                    if river_check == 0:
                        river_check = 1
                    if dirt_check == 0:
                        dirt_check = 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    press = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        rect_coor_list.pop()
                    if event.key == pygame.K_RIGHT:
                        path_weight_style = path_weight_style[1:] + path_weight_style[:1]
                        chosen_style = path_weight_style[-1]
                    if event.key == pygame.K_SPACE:
                        finish_obstacle = True
                        
            # if holding the mouse
            if press == True and chosen_style == 'wall':            
                    x,y = pygame.mouse.get_pos()
                    for coor_x in x_valid:
                        for coor_y in y_valid:
                            if abs(y-coor_y) <= height//2:
                                y = coor_y
                                break
                        if abs(x-coor_x) <= width//2:
                            x = coor_x
                            break
                    # pygame.mouse.set_pos(x,y)
                    rect = pygame.Rect(0,0,width,height)
                    rect.centerx = coor_x
                    rect.centery = coor_y
                    if [coor_x,coor_y] not in rect_coor_list\
                        and ((coor_x-width/2)/width,(coor_y-height/2)/height) != start_node\
                        and ((coor_x-width/2)/width,(coor_y-height/2)/height) != end_node:
                        rect_coor_list.append([coor_x,coor_y])
            
            elif press == True and chosen_style == 'jungle':
                    allowed_jungle_cross = 1
                    x,y = pygame.mouse.get_pos()
                    for coor_x in x_valid:
                        for coor_y in y_valid:
                            if abs(y-coor_y) <= height//2:
                                y = coor_y
                                break
                        if abs(x-coor_x) <= width//2:
                            x = coor_x
                            break
                    # pygame.mouse.set_pos(x,y)
                    if [coor_x,coor_y] not in jungle_list\
                        or [coor_x,coor_y] in jungle_list:
                            jungle_list.append([coor_x,coor_y])

                        
            elif press == True and chosen_style == 'river':
                    x,y = pygame.mouse.get_pos()
                    for coor_x in x_valid:
                        for coor_y in y_valid:
                            if abs(y-coor_y) <= height//2:
                                y = coor_y
                                break
                        if abs(x-coor_x) <= width//2:
                            x = coor_x
                            break
                    # pygame.mouse.set_pos(x,y)
                    if [coor_x,coor_y] not in river_list\
                        or [coor_x,coor_y] in river_list:
                            river_list.append([coor_x,coor_y])
                            
            elif press == True and chosen_style == 'dirt':
                    x,y = pygame.mouse.get_pos()
                    for coor_x in x_valid:
                        for coor_y in y_valid:
                            if abs(y-coor_y) <= height//2:
                                y = coor_y
                                break
                        if abs(x-coor_x) <= width//2:
                            x = coor_x
                            break
                    # pygame.mouse.set_pos(x,y)
                    if [coor_x,coor_y] not in dirt_list\
                        or [coor_x,coor_y] in dirt_list:
                            dirt_list.append([coor_x,coor_y])
                            
            # update obstacles for the points
            if finish_obstacle is True and run_obstacle == 1:
                add_obstacles(rect_coor_list)
                add_dirt_path(dirt_list)
                add_jungle_path(jungle_list)
                add_river_path(river_list)
                # point_objects[1].set_cost(6,2,2)
                run_obstacle = 0
            # draw start node and destination node
            draw_everything()
            # pygame.display.update()
            i = 0
            # finding the destination point
            if run_obstacle == 0:
                if run_for_once != 0:
                    for point in run():
                        # make sure u can click exterminate the application in the middle of the app
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                pygame.display.quit()
                                pygame.quit()
                                sys.exit()
                        draw_initial_points()
                        if i == 0:
                            original_coor.append(start_point.get_point_coordinates()[0])
                            original_coor.append(start_point.get_point_coordinates()[1])
                            pre_x = original_coor[0]
                            pre_y = original_coor[1]
                            x_coor = width/2 + original_coor[0]*width
                            y_coor = height/2 + original_coor[1]*height
                            current_point_list.append((x_coor,y_coor))
                            rect = pygame.Rect(0,0,width,height)
                            rect.centerx = x_coor
                            rect.centery = y_coor
                            draw_rect(rect)
                            # time.sleep(0.05)
                            draw_everything()
                            pygame.display.update()
                            i = 1
                            continue
                        x_coor += (point.get_point_coordinates()[0] - pre_x)*width
                        y_coor += (point.get_point_coordinates()[1] - pre_y)*height
                        pre_x,pre_y = point.get_point_coordinates()[0],point.get_point_coordinates()[1]
                        rect.centerx = x_coor
                        rect.centery = y_coor
                        draw_rect(rect)
                        # time.sleep(0.001)
                        draw_everything()
                        pygame.display.update()
                        current_point_list.append((x_coor,y_coor))
                        if point.get_point_coordinates() == end_node:
                            run_for_once = 0
                
                if run_path != 0 and run_for_once == 0:
                    i = 0
                    for point in step_list:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                pygame.display.quit()
                                pygame.quit()
                                sys.exit()
                                
                        draw_initial_points()
                        point_coor = point_objects[point].get_point_coordinates()
                        if i == 0:
                            pre_x = point_coor[0]
                            pre_y = point_coor[1]
                            x_coor = width/2 + point_coor[0]*width
                            y_coor = height/2 + point_coor[1]*height
                            rect = pygame.Rect(0,0,width,height)
                            rect.centerx = x_coor
                            rect.centery = y_coor
                            final_path.append((x_coor,y_coor))
                            pygame.draw.rect(win,pygame.Color('black'),rect)
                            draw_everything()
                            pygame.display.update()
                            i = 1
                            continue
                        x_coor += (point_coor[0] - pre_x)*width
                        y_coor += (point_coor[1] - pre_y)*height
                        final_path.append((x_coor,y_coor))
                        pre_x,pre_y = point_coor[0],point_coor[1]
                        rect = pygame.Rect(0,0,width,height)
                        rect.centerx = x_coor
                        rect.centery = y_coor
                        time.sleep(0.05)
                        pygame.draw.rect(win,pygame.Color('black'),rect) 
                        draw_everything()
                        pygame.display.update()
                        if point_coor == end_node:
                            run_path = 0
                        
                        
                        
            draw_finished_algo(current_point_list)
            # # avoid overlapping between two paths
            # if j==0:
            #     for point in current_point_list:
            #         if point in final_path:
            #             current_point_list.remove(point)
            # j=1
            draw_everything()
            draw_final_path(final_path)

            pygame.display.update()
            
    except:
        # catch the error
        print(traceback.format_exc())        
        pygame.display.quit()
        pygame.quit()
        sys.exit()
            