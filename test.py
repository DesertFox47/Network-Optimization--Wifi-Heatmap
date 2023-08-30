import pygame
from pygame.locals import *
from heat import map_heat
import numpy as np
from convert_csv import con
from collections import defaultdict
pygame.init()
screen = pygame.display.set_mode((1080, 720))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None,32)
color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
width = screen.get_width()
height = screen.get_height()
room_list = []
all_room_dict = {}
all_room_attach_det = {}
edges=[]
router_point=[0,0]
main_wifi_room=0
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def is_inside(x,y,w,h,p) :
   if (p[0] > x and p[0] < w+x and p[1] > y and p[1] < h+y) :
      return True
   else :
      return False
def get_room(numb):
    elem=all_room_dict[numb]
    return elem[0],elem[1],elem[2],elem[3]
def display_moving_rooms(rm_num):
    elem=all_room_dict[rm_num]
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        elem=all_room_dict[rm_num]
                        if event.key == pygame.K_LEFT:
                            elem[0]-=5
                            all_room_dict[rm_num]=elem
                        if event.key == pygame.K_RIGHT:
                            elem[0]+=5
                            all_room_dict[rm_num]=elem
                            print("right")
                        if event.key == pygame.K_UP:
                            elem[1]-=5
                            all_room_dict[rm_num]=elem
                            print("up")
                        if event.key == pygame.K_DOWN:
                            elem[1]+=5
                            all_room_dict[rm_num]=elem
                            print("down")
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if width-140 <= mouse[0] <= width and 0 <= mouse[1] <= 40:
                            display_rooms()
        mouse = pygame.mouse.get_pos()
        if width-140 <= mouse[0] <= width and 0 <= mouse[1] <= 40:
            pygame.draw.rect(screen,color_light,[width-140,0,140,40])
        else:
            pygame.draw.rect(screen,color_dark,[width-140,0,140,40])

        screen.blit(FONT.render('SAVE' , True , color) , (width-140+45,10))
        room_list = list(all_room_dict.values())
        for ele in room_list:
            pygame.draw.rect(screen, ele[5], pygame.Rect(ele[0],ele[1],ele[2], ele[3]),  2)
        pygame.display.update()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        clock.tick(30)

def move_room():
    clock = pygame.time.Clock()
    input_box1 = InputBox(width/2-70, 100, 140, 32)
    input_boxes = [input_box1]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                    display_moving_rooms(int(input_box1.text))
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)
        mouse = pygame.mouse.get_pos()
        if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
            pygame.draw.rect(screen,color_light,[width/2,height/2,140,40])
        else:
            pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40])
        screen.blit(FONT.render('Room No.' , True , color) , (width/3.5, 100))
        screen.blit(FONT.render('OK' , True , color) , (width/2+40,height/2+10))
        pygame.display.update()
        pygame.display.flip()
        screen.fill((0, 0, 0))
        clock.tick(30)
        
def room_pass_material(room_attach):
    room_pass_mat=[0,0,0,0,0,0]
    for each_room_attach in room_attach:
        room_mat=all_room_dict[each_room_attach][5]
        if room_mat==(220,220,220):
            room_pass_mat[0]+=1
        elif room_mat==(0,0,255):
            room_pass_mat[1]+=1
        elif room_mat==(255,0,0):
            room_pass_mat[2]+=1
        elif room_mat==(165,42,42):
            room_pass_mat[3]+=1
        elif room_mat==(255,255,255):
            room_pass_mat[4]+=1
        elif room_mat==(255,20,147):
            room_pass_mat[5]+=1
    return room_pass_mat

def BFS_SP(graph, start, goal):
	explored = []
	queue = [[start]]
	if start == goal:
		print("Same Node")
		return []
	while queue:
		path = queue.pop(0)
		node = path[-1]
		if node not in explored:
			neighbours = graph[node]
			for neighbour in neighbours:
				new_path = list(path)
				new_path.append(neighbour)
				queue.append(new_path)
				if neighbour == goal:
					print("Shortest path = ", *new_path)
					return new_path
			explored.append(node)
	print("So sorry, but a connecting"\
				"path doesn't exist :(")
	return []
def build_graph(edges):
    graph = defaultdict(list)
    for edge in edges:
        a, b = edge[0], edge[1]
        graph[a].append(b)
        graph[b].append(a)
    print(graph)
    return graph
def predict_signal():
    print("done")
    output=[]
    output.append(["X","Y","SHORTESTDIST","CONCRETE","HBLOCK","BRICK","WOOD","GLASS","RCCROOF","OUTPUT"])
    all_room_attach_det={}
    edges=[]
    for key, value in all_room_dict.items():
        if(key!=value[4]):
            edges.append([key,value[4]])
    all_room_attach_det=build_graph(edges)
    for key, value in all_room_dict.items():
        print(main_wifi_room)
        path=BFS_SP(all_room_attach_det,key,main_wifi_room)
        room_pass_mat=room_pass_material(path)
        if(room_pass_mat!=[]):
            out=con(int(value[0]),int(value[1]),value[2], value[3],router_point,room_pass_mat)
            output=output+out
    output=np.array(output)
    np.savetxt("./data/data.csv", output, delimiter = ",",fmt='%s')
    map_heat()

def find_cntr_pos(x,y):
    return sum(x)/len(x), sum(y)/len(y)

def display_rooms():
    clock = pygame.time.Clock()
    chk=False
    est_x=[]
    est_y=[]
    while True:
        room_list = list(all_room_dict.values())
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if width-140 <= mouse[0] <= width and 0 <= mouse[1] <= 40:
                            add_room()
                        if width-340 <= mouse[0] <= width-200 and 0 <= mouse[1] <= 40:
                            move_room()
                        if width-145 <= mouse[0] <= width-5 and height-45 <= mouse[1] <= height:
                            pygame.image.save(screen, "./data/floor_plan.png")
                            predict_signal()
                        if width-540 <= mouse[0] <= width-380 and 0 <= mouse[1] <= 40:
                            chk=False
                            while True:
                                mouse = pygame.mouse.get_pos()
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        global router_point
                                        global main_wifi_room
                                        router_point=[mouse[0],mouse[1]]
                                        print(router_point)
                                        for ele in all_room_dict:
                                            if(is_inside(all_room_dict[ele][0],all_room_dict[ele][1],all_room_dict[ele][2], all_room_dict[ele][3],router_point)==True):
                                                main_wifi_room=ele
                                                print(main_wifi_room)
                                                chk=True
                                                break
                                        if(chk==False):
                                            print("Router Point Not Inside Room")
                                            continue
                                        else:
                                            break
                                if(chk==True):
                                    break
                                            

        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos()
        if width-140 <= mouse[0] <= width and 0 <= mouse[1] <= 40:
            pygame.draw.rect(screen,color_light,[width-140,0,140,40])
        else:
            pygame.draw.rect(screen,color_dark,[width-140,0,140,40])

        if width-340 <= mouse[0] <= width-200 and 0 <= mouse[1] <= 40:
            pygame.draw.rect(screen,color_light,[width-340,0,140,40])
        else:
            pygame.draw.rect(screen,color_dark,[width-340,0,140,40])

        if width-145 <= mouse[0] <= width-5 and height-45 <= mouse[1] <= height:
            pygame.draw.rect(screen,color_light,[width-145,height-45,140,40])
        else:
            pygame.draw.rect(screen,color_dark,[width-145,height-45,140,40])

        if width-540 <= mouse[0] <= width-380 and 0 <= mouse[1] <= 40:
            pygame.draw.rect(screen,color_light,[width-540,0,160,40])
        else:
            pygame.draw.rect(screen,color_dark,[width-540,0,160,40])
        
        screen.blit(FONT.render('ADD' , True , color) , (width-140+45,10))
        screen.blit(FONT.render('EDIT' , True , color) , (width-340+45,10))
        screen.blit(FONT.render('ADD ROUTER' , True , color) , (width-540+5,10))
        screen.blit(FONT.render('PREDICT' , True , color) , (width-155+35,height-35))
        for ele in room_list:
            pygame.draw.rect(screen, ele[5], pygame.Rect(ele[0],ele[1],ele[2], ele[3]),  2)

            est_x.append((ele[0]+(ele[2]/2)))
            est_y.append((ele[1]+(ele[3]/2)))
        
        est_point=find_cntr_pos(est_x,est_y)
        print(est_point)
        pygame.draw.circle(screen,(0,255,0),est_point,100,width>0)
        if(chk==True):
            pygame.draw.circle(screen,(255,0,0),router_point,5,width=0)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(30)


def add_room():
    clock = pygame.time.Clock()
    input_box1 = InputBox(width/2-70, 100, 140, 32)
    input_box2 = InputBox(width/2-70, 150, 140, 32)
    input_box3 = InputBox(width/2-70, 200, 140, 32)
    input_box4 = InputBox(width/2-70, 250, 140, 32)
    input_box5 = InputBox(width/2-70, 300, 140, 32)
    input_box6 = InputBox(width/2-70, 350, 140, 32)
    input_boxes = [input_box1, input_box2,input_box3,input_box4,input_box5,input_box6]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2 <= mouse[0] <= width/2+140 and 400 <= mouse[1] <= 400+40:
                    input_len=int(input_box1.text)*12
                    input_wid=int(input_box2.text)*12
                    if input_box6.text=="CONCRETE":
                        matcol=(220,220,220)
                    elif input_box6.text=="HBLOCK":
                        matcol=(0,0,255)
                    elif input_box6.text=="BRICK":
                        matcol=(255,0,0)
                    elif input_box6.text=="WOOD":
                        matcol=	(165,42,42)
                    elif input_box6.text=="GLASS":
                        matcol=(255,255,255)
                    elif input_box6.text=="RCCROOF":
                        matcol=(255,20,147)
                    if input_box4.text=="C":
                        f=[width/2-input_len/2 , height/2-input_wid/2 , input_len,input_wid , 1 , matcol]
                    elif input_box4.text=="L":
                        print("left")
                        ret_x,ret_y,ret_w,ret_h=get_room(int(input_box3.text))
                        f=[ret_x-input_len,ret_y,input_len,input_wid,int(input_box3.text),matcol]
                    elif input_box4.text=="R":
                        print("right")
                        ret_x,ret_y,ret_w,ret_h=get_room(int(input_box3.text))
                        f=[ret_x+ret_w,ret_y,input_len,input_wid,int(input_box3.text),matcol]
                    elif input_box4.text=="T":
                        print("top")
                        ret_x,ret_y,ret_w,ret_h=get_room(int(input_box3.text))
                        f=[ret_x,ret_y-input_wid,input_len,input_wid,int(input_box3.text),matcol]
                    elif input_box4.text=="B":
                        print("bottom")
                        ret_x,ret_y,ret_w,ret_h=get_room(int(input_box3.text))
                        f=[ret_x,ret_y+ret_h,input_len,input_wid,int(input_box3.text),matcol]
                    all_room_dict[int(input_box5.text)]=f
                    print(all_room_dict)
                    display_rooms()

            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        screen.fill((0, 0, 0))
        for box in input_boxes:
            box.draw(screen)
        #button
        mouse = pygame.mouse.get_pos()
        if width/2 <= mouse[0] <= width/2+140 and 400 <= mouse[1] <= 400+40:
            pygame.draw.rect(screen,color_light,[width/2,400,140,40])
        else:
            pygame.draw.rect(screen,color_dark,[width/2,400,140,40])

        
        screen.blit(FONT.render('Length' , True , color) , (width/3.5, 100))
        screen.blit(FONT.render('Width' , True , color) , (width/3.5,150))
        screen.blit(FONT.render('Attached to' , True , color) , (width/3.5,200))
        screen.blit(FONT.render('Attach side' , True , color) , (width/3.5,250))
        screen.blit(FONT.render('Room No' , True , color) , (width/3.5,300))
        screen.blit(FONT.render('Material' , True , color) , (width/3.5,350))
        screen.blit(FONT.render('SAVE' , True , color) , (width/2+40,410))
        
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    add_room()
    pygame.quit()