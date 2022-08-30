# Visualiser for A search Algorithm 
import pygame 
import math 
from queue import PriorityQueue
from time import sleep

WIDTH =800
WIN=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


RED = (255, 0, 0)
GREEN = (21,71,52)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Nodes:
    # how to keep track of the nodes 
    def __init__(self, row, col, width, total_rows):
            self.row= row
            self.col= col
            self.x=row * width
            self.y=col * width
            self.color = WHITE
            self.adj_nodes = []
            self.width = width
            self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_explored(self):
        return self.color == YELLOW

    def is_open(self):
            return self.color == RED

    def is_block(self):
            return self.color == BLACK

    def is_start(self):
            return self.color == BLUE

    def is_end(self):
            return self.color == TURQUOISE

    def reset(self):
            self.color = WHITE

    def make_start(self):
            self.color = BLUE

    def make_closed(self):
            self.color = YELLOW

    def make_open(self):
            self.color = RED # for the edge 

    def make_block(self):
            self.color = BLACK

    def make_end(self):
            self.color = TURQUOISE

    def make_path(self):
            self.color = GREEN

    def draw(self, win):
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_adj_nodes(self,grid):
        self.adj_nodes=[]
            # check up = not the first row and up not block
        if self.row>0 and not grid[self.row-1][self.col].is_block():
            self.adj_nodes.append(grid[self.row-1][self.col])

        # check down = not the last row and down not block
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_block():
            self.adj_nodes.append(grid[self.row+1][self.col]) 

        # check left 
        if self.col>0 and not grid[self.row][self.col-1].is_block():
            self.adj_nodes.append(grid[self.row][self.col-1])

        # check right 
        if self.col<self.total_rows-1:
            if not grid[self.row][self.col+1].is_block():
                self.adj_nodes.append(grid[self.row][self.col+1])

    def lt(self,other):
            pass 

def h(p1,p2): # calculating the absolute distance 
    x1,y1=p1
    x2,y2=p2 
    return abs(x1-x2)+abs(y1-y2)


def make_grid(rows,width):
    grid =[]
    gap = width //rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            Node = Nodes(i,j,gap,rows)
            grid[i].append(Node) #grid is 2d array and grid[i] is one row which has all nodes in i-th row
    return grid 


def draw_grid(win,rows,width):
    box_size = width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*box_size),(width,i*box_size))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*box_size,0),(j*box_size,width))


def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_node(pos,rows,width):
    x,y= pos # x and y are co-ordinates 
    box_size = width//rows
    row=x//box_size
    col=y//box_size
    return row,col

def reconstruct_path(came_from,start, end, draw):
    before = end  
    while before!=start:
        path_node = before 
        path_node.make_path()
        before = came_from[path_node]
        draw()



def algorithm(draw,grid,start,end):
    count=0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from ={} #dictionary
    g_score ={node:float("inf") for row in grid for node in row} 
    # g_score is distance of this node from start node 
    g_score[start]=0 
    f_score ={node:float("inf") for row in grid for node in row} 
    # g_score is distance of this node from start node 
    f_score[start]= h(start.get_pos(),end.get_pos())
    open_set_hash={start} # a dictionary again 
    print("algorithm(): WORKING")
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, start, end, draw)
            end.make_end()
            return True


        for adj_nodes in current.adj_nodes:
            draw()
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[adj_nodes]:
                came_from[adj_nodes] = current #what is the origin of [adj_nodes] = current 
                g_score[adj_nodes] = temp_g_score
                f_score[adj_nodes] = temp_g_score + h(adj_nodes.get_pos(), end.get_pos())
                if adj_nodes not in open_set_hash:
                    count += 1
                    open_set.put((f_score[adj_nodes], count, adj_nodes))
                    open_set_hash.add(adj_nodes)
                    adj_nodes.make_open()

        if current != start:
                current.make_closed()


    return False          









def main(win,width):
    ROWS = int(input("Please enter a number for dimension of your maze. If you type 50, you will get 50x50 grid to create a maze.\n"))
    grid=make_grid(ROWS,WIDTH)
    draw(WIN,grid,ROWS,WIDTH)
    start= None 
    end = None 
    run = True 
    started = False 

    while run:
        
        
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run=False 
            if started:
                continue 

            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_node(pos,ROWS,WIDTH)
                node = grid[row][col]
                if not start:
                    start=node
                    start.make_start()
                    draw(WIN,grid,ROWS,WIDTH)
                elif not end and node!=start: 
                    end=node
                    end.make_end()
                    draw(WIN,grid,ROWS,WIDTH)
                elif node!=end and node!= start:
                    node.make_block()
                    draw(WIN,grid,ROWS,WIDTH)
            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_node(pos,ROWS,WIDTH)
                node = grid[row][col]
                node.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_adj_nodes(grid)
                    algorithm(lambda: draw(WIN,grid,ROWS,WIDTH),grid,start,end)


    
    
main(WIN,WIDTH)

