from BaseAI import BaseAI;
from random import randint;
from Grid import Grid;
from decimal import *;
import time;
from Displayer import Displayer;
time_limit = 0.12
time_extension = 0.03
displayer = Displayer();

class PlayerAI(BaseAI):
    states=0;
    start_time=0;
    def compactness(self,grid):
           down=0;
           up=0;
           d1=0;
           d2=0;
           u1=0;
           u2=0;
           for x in xrange(grid.size):
            for y in xrange(grid.size):
                if(grid.map[x][y] !=0) :
                      if(x>=y):
                          d1=d1+1;
                      else:
                          d2=d2+1;
                      if(x+y>=3):
                          u1=u1+1;
                      else:
                          u2=u2+1;
           down=abs(d1-d2);
           up=abs(u1-u2);
           if(down>=up):
               return down;
           else:
                return up
    def edgeBonus(self,grid):
        r1=0;
        r2=0;
        d1=0;
        d2=0;
        max=0;
        list=[];
        for x in xrange(grid.size):
            r1=r1+grid.map[x][0];
            r2=r2+grid.map[x][grid.size-1];
        if(r1<r2):
            r1=r2;
        for y in xrange(grid.size):
            d1=d1+grid.map[0][y];
            d2=d2+grid.map[grid.size-1][y]
        if(d1<d2):
            d1=d2;
        if(r1<d1):
            r1=d1;
        return r1;
    def monotonic(self,grid):
        penalty=0;
        inc=0;
        dec=0;
        vertical=0; # vertical penalty incresases going downwards
        for x in xrange(grid.size):
            for y in xrange(grid.size-1):
                a= grid.map[x][y];
                b= grid.map[x][y+1];
                
                if((a==0) or (b==0) ):
                    pass;
                else:
                    if(a < b): # should decrease going left->right
                        inc=inc+1; # does not decrease so penalty
                        
        for y in xrange(grid.size):
            for x in xrange(grid.size-1):
                a= grid.map[x][y];
                c= grid.map[x+1][y];
                if((a==0) or (c==0)):
                    pass;
                else:
                    if(a>c):
                        
                        vertical=vertical+1;
        
        return inc+vertical;

    # heuristic function to get static value of grid at any stage
    # not just terminal node
    def eval(self,grid):
        f1= grid.getMaxTile()*2;
        f2= len(grid.getAvailableCells())*400

        f4= self.compactness(grid)*300;
        f5= self.edgeBonus(grid)*7;
        f6= 0#self.monotonic(grid)*(-300); #penalty
       # print "heuristic",f1,f2,f4,f5,f6;
        sv=f1+f2+f4+f5 # static value
        return sv;

    #returns sv,time_exceeded
    def min_value(self,grid,alpha,beta,depth):
        time_exceeded=False
        self.states=self.states+1;
        if(time.clock()-self.start_time >= time_limit):
            time_exceeded = True;
            return  beta,time_exceeded;

        moves=grid.getAvailableMoves();
        cells=grid.getAvailableCells();
        if(depth <= 0):
           # print "depth limit reached";
            return self.eval(grid),time_exceeded;
        if(len(moves)==0):
            return self.eval(grid),time_exceeded;

        v = Decimal('Infinity');
        min_value_move = 0;
        #cell = cells[randint(0, len(cells) - 1)]
        sg=None;
        list=[];
        for i in cells:
            gridClone = grid.clone();
            gridClone.setCellValue(i,2);
            sv,move,time_exceeded = self.max_value(gridClone,alpha,beta,depth-1);
           # list.append(gridClone)
            if(time_exceeded == True):
                return beta,time_exceeded;
            if(sv<v):
                v = sv;
                min_value_move=i;
                sg=gridClone;
            if(v <beta):
                beta=v;
            if(alpha>=beta):
               break;
        #print "selected min position,sv",depth,v;

        return v,time_exceeded;

    def max_value(self,grid,alpha,beta,depth):

        self.states=self.states+1;
        time_exceeded=False
        if(time.clock() -self.start_time >= time_limit):
            time_exceeded=True;
            return alpha,0,time_exceeded;

        move  = None;
        moves = grid.getAvailableMoves();
        cells = grid.getAvailableCells();
        max_value_move = 0;
        # this is terminal state
        if(depth<=0):
           return self.eval(grid),None,time_exceeded;
        if(len(moves) == 0  ):
          return self.eval(grid),None,time_exceeded;
        v = Decimal('-Infinity')
        sg=None;
        list=[];
        for i in moves:
            gridClone = grid.clone();
            gridClone.move(i);
            sv,time_exceeded=self.min_value(gridClone,alpha,beta,depth-1);
            list.append(gridClone)
            if(time_exceeded == True):
                return alpha,max_value_move,time_exceeded;
            if(sv > v):
                v = sv;
                max_value_move = i;
                sg=gridClone;

            if(v > alpha):
                alpha = v ;
            if(alpha >= beta): #cutoff
                break;
        #print "selected max position:",depth,v;
        #displayer.display(sg);
        return v,max_value_move,time_exceeded ;

    def getMove(self,grid):
      displayer = Displayer();
      time_exceeded = False;
      start_depth = 3; # depth for dfs starting
      moves = grid.getAvailableMoves()
      cells = grid.getAvailableCells();
      alpha = Decimal('-Infinity') ; # -infinity
      beta  =  Decimal('Infinity')  # +infinity
      self.start_time=time.clock();
      prev_sv=0;# move and sv for previous level
      prev_move=0;
      while(time_exceeded == False):
         # print "---------starting position for this move----------";
         # displayer.display(grid);
          sv,move,time_exceeded = self.max_value(grid,alpha,beta,start_depth);
         # print time_exceeded;
          if(time_exceeded == False):
              start_depth=start_depth+1;
              prev_sv=sv;
              prev_move=move;

          else:
              pass;


      return prev_move;
     # moves=grid.getAvailableMoves()

  #    return moves[randint(0,len(moves)-1)];
