# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:42:14 2020

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
        self.neighbors = []
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
        
    def get_neightbors(self):
        return self.neighbors
    
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

    
start_node = (25,26)
end_node = (44,39)
maze_dim = 50


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
        point_objects.append(Points(maze_dim,i))    
        adj_neighbors = neighbor_table[i]
        point_objects[i].set_neighbors(adj_neighbors) 
        point_coordinate = point_list[i]
        point_objects[i].set_point_coordinate(point_coordinate)
    
    for i in range(len(point_objects)):
        if point_objects[i].get_point_coordinates() == start_node:
            point_objects[i].set_step(0)
            start_point = point_objects[i]
        if point_objects[i].get_point_coordinates() == end_node:
            end_point = point_objects[i]

def run():
    global step_list, current_point
    global neighbor_table, point_list, point_index, point_objects
    # setup_lists()
    # setup_neighbors()
    # # setup_points()
    del neighbor_table
    del point_list
    del point_index
    current_point = start_point    
    found_point = False
    number_of_steps = 0
    point_check = []
    while( found_point is not True):
        yield current_point
        current_point.set_visited()
        # set steps for neighbor points
        # get the neighbors from the current point
        neighbors_temp = current_point.get_neightbors()
        # compare the steps generated from current point with existing steps
        current_step = current_point.get_step()+1
        for neighbor in neighbors_temp:
            if point_objects[neighbor].get_block_status() == False:
                if point_objects[neighbor].check_visited() == False:
                        if neighbor not in point_check:
                            point_check.append(neighbor)
                        # continue to compare steps
                        neighbor_step_temp = point_objects[neighbor].get_step()
                        if current_step < neighbor_step_temp:
                            point_objects[neighbor].set_step(current_step)
                            point_objects[neighbor].set_pre_vertex(current_point.get_index())
                        else:
                            pass
                        # check if it is the end node
                        if point_objects[neighbor] == end_point:
                            current_point_temp = current_point
                            current_point = end_point
                            number_of_steps += 1
                            found_point = True
                            yield current_point
                            break
                
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
            # After findind next point -> confirm previous point
            current_point = next_point_temp
            number_of_steps += 1
            del next_point_temp
        # Found the point
        else:
            step_list = [current_point.get_index()]
            pre_point = current_point.get_pre_vertex()
            while(pre_point != -1):
                step_list.append(pre_point)
                current_point = point_objects[pre_point]
                pre_point = current_point.get_pre_vertex()
            step_list = list(reversed(step_list))



if __name__ == '__main__':
    
    # pygame init
    pygame.init()
    # Window Init
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
##########################################    SETUP  ###################################################
    # setup the list of points
    setup_lists()
    setup_neighbors()
    setup_points()
    
    width = 10
    height = 10
    num_of_box = SCREEN_HEIGHT//height
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
    
    # Draw the rectangles          
    def draw_rect(rect):
        pygame.draw.rect(win,pygame.Color(200,0,0),rect)
    
    def draw_boxes(rect_coordinates):
        for rect_coor in rect_coordinates:
            rect = pygame.Rect(rect_coor[0],rect_coor[1],width,height)
            rect.centerx = rect_coor[0]
            rect.centery = rect_coor[1]
            pygame.draw.rect(win,pygame.Color('blue'),rect)
            
    def draw_initial_points():
        global rect_start, rect_end
        rect_start = pygame.Rect(0,0,width,height)
        rect_end = pygame.Rect(0,0,width,height)
        rect_start.centerx = width/2 + start_node[0]*width
        rect_start.centery = height/2 + start_node[1]*height
        rect_end.centerx = width/2 + end_node[0]*width
        rect_end.centery = height/2 + end_node[1]*height            
        pygame.draw.rect(win, pygame.Color('purple'),rect_start)
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
            pygame.draw.rect(win,pygame.Color('green'),rect)
            
    def add_obstacles(coordinates):
        global point_objects
        for coor_pair in coordinates:
            coor_pair_x = int((coor_pair[0]-(width/2))//width)
            coor_pair_y = int((coor_pair[1]-(height/2))//height)
            for i in range(len(point_objects)):
                if (coor_pair_x,coor_pair_y) == point_objects[i].get_point_coordinates():
                    point_objects[i].set_block()
                    break
                
        
        
################################# RUNNING THE PYGAME MODULE #################################
            
    running = True    
    try:
        while running:
            win.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    for coor_x in x_valid:
                        for coor_y in y_valid:
                            if abs(y-coor_y) <= height//2:
                                y = coor_y
                                break
                        if abs(x-coor_x) <= width//2:
                            x = coor_x
                            break
                    pygame.mouse.set_pos(x,y)
                    rect = pygame.Rect(0,0,width,height)
                    rect.centerx = x
                    rect.centery = y
                    rect_coor_list.append([x,y])
                    # pygame.draw.rect(win,pygame.Color('blue'),rect)
                    # pygame.display.update()
                    # time.sleep(1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        rect_coor_list.pop()
                    if event.key == pygame.K_SPACE:
                        finish_obstacle = True
                        
            
            # update obstacles for the points
            if finish_obstacle is True and run_obstacle == 1:
                add_obstacles(rect_coor_list)
                run_obstacle = 0
            # draw start node and destination node
            draw_initial_points()
            # draw boxes created by mouse
            draw_boxes(rect_coor_list)
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
                            time.sleep(0.05)
                            draw_boxes(rect_coor_list)
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
                        draw_boxes(rect_coor_list)
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
                            pygame.draw.rect(win,pygame.Color(0,200,0),rect)
                            draw_boxes(rect_coor_list)
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
                        pygame.draw.rect(win,pygame.Color(0,200,0),rect) 
                        draw_boxes(rect_coor_list)
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
            draw_final_path(final_path)
            draw_initial_points()
            draw_boxes(rect_coor_list)
            pygame.display.update()
            # pygame.draw.rect(win, pygame.Color('blue'),rect_start)
            # pygame.draw.rect(win, pygame.Color('gold'),rect_end)
    except:
        # catch the error
        print(traceback.format_exc())        
        pygame.display.quit()
        pygame.quit()
        sys.exit()
            