#! usr/bin/python3
"""
CS161 Final Project using PyQt.

Using PyQt5 this code will create a game designed
for multiple players and will be played with a mouse.
The goal of the game is to make squares of arbitrary size,
When more than one square is made on a single turn the
multiplier is in the number of squares placed.
Multiplier resets if 0-1 square is formed.


Blake Phillips.
"""
import sys
from itertools import combinations
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QLine, QPoint, QRectF
from PyQt5.QtWidgets import QWidget, QApplication
windowSize = 600
yAxisSpace = 100
xAxisSpace = 20

class Score:

  def __init__(self, player_name):
    """Set the class variables."""
    self.__squaresize = 0
    self.__player_name = player_name
    self.__score = 0
    self.__multiplier = 1
    self.__turn = False
    self.__color = 0
    self.__owned = [] #Owned Spaces on Grid
    self.__lines = [] #Lines to be drawn

  def get_name(self):
      """Acquire name."""
    return self.__player_name

  def get_score(self):
      """Acquire score."""
    return self.__score

  def changeSquaresize(self,squaresize):
    """Square Resizer."""
    self.__squaresize = squaresize

  def add_points(self, amount):
      """Point multiplier."""
    self.__score += amount * self.__multiplier
    return self.__score

  def subtract_points(self, amount):
      """Point deduction."""
    self.__multiplier = 1
    self.__score -= amount
    if self.__score < 0:
      self.__score = 0
    return self.__score

  def get_color(self):
      """Acquire color."""
    return self.__color
  
  def change_color(self,color):
      """Change color."""
    self.__color = color
  
  def get_turn(self):
      """Acquire turn."""
    return self.__turn

  def end_turn(self):
      """Halt turn."""
    self.__turn = False

  def begin_turn(self):
      """Enable turn."""
    self.__turn = True

  def getOwned(self):
      """Pwn oneself."""
    return self.__owned

  def addOwned(self,qRect):
      """Owned addition."""
    self.__owned += [qRect]

  def getLines(self):
      """Acquire lines."""
    return self.__lines

  def addLines(self,qline):
      """Add lines."""
    self.__lines += [qline]


  def get_multiplier(self):
      """Fetch multiplier."""
    return self.__multiplier

  def increment_multiplier(self,number):
      """Incremental multiplier."""
    self.__multiplier += number
    return self.__multiplier

  def reset_multiplier(self):
      """Reset the multiplier."""
    self.__multiplier = 1 


  def __str__(self):
      """Add strings."""
    return "Player: " + self.__player_name + ", Score: " + str(self.__score) + ", Level: " + str(self.__level) + ",Multiplier: " + str(self.__multiplier) + ", Lives: " + str(self.__lives)


class SquareGame(QWidget):

  def __init__(self):
      """Graphics, innits."""
    super().__ini
    self.setGeometry(350,50, windowSize+xAxisSpace, windowSize + yAxisSpace )
    self.setWindowTitle('Square Finder')
   

    self.playerOne = Score("Player One")
    self.playerTwo = Score("Player Two")
    self.playerThree = Score("Player Three")
    self.playerFour = Score("Player Four")


    self.board = []
    self.playerList = []
    self.squareSize = 0
    self.lineset = [] #Lines that get added when a square exists
    
    #Screen mode flags
    self.overview = True
    self.chooseColor = False
    self.begin_game = False
    self.chooseSize = False
    self.GameSize = 0

    #controls player colors
    self.colorlist = ['0ea037','ff66cc','3399ff','ff9900']

    #Buttons for choices
    self.OptionOne = QRectF((windowSize -6*xAxisSpace)/2,((windowSize)-150)/4,150,100)
    self.OptionTwo = QRectF((windowSize -6*xAxisSpace)/2,(windowSize-150)/2,150,100)
    self.OptionThree = QRectF((windowSize -6*xAxisSpace)/2,(3*(windowSize-150)/4),150,100)
    self.OptionFour = QRectF((windowSize - 6*xAxisSpace)/2,windowSize-150,150,100)
    self.OptionOneT = QRectF((windowSize  )/2,(((windowSize)-150)/4)+45,150,100)
    self.OptionTwoT = QRectF((windowSize)/2,((windowSize-150)/2)+45,150,100)
    self.OptionThreeT = QRectF((windowSize)/2,((3*(windowSize-150)/4))+45,150,100)
    self.OptionFourT = QRectF((windowSize)/2,windowSize-105,150,100)
    self.Optionlist = [self.OptionOne,self.OptionTwo,self.OptionThree,self.OptionFour]
    self.show()

  def ChangeColor(self):
      """Player color set."""
    colorlistQ = [QColor("#"+color) for color in self.colorlist]
    i = 0
    for player in self.playerList:
      player.change_color(colorlistQ[i])
      i+=1

  def distance (self,point1,point2):
      """Fetch tuple, give distance."""
    #Takes two tuple points and outputs a distance
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    distance = ((x1-x2)**2 +(y1-y2)**2)**(1/2)
    return distance


  def pointsAreSquare(self,pointset,player):
      """Checklist if four point are square, in tuples."""
    size = 0
    a = pointset[0]
    b = pointset[1]
    c = pointset[2]
    d = pointset[3]
    ab = self.distance(a,b)
    ac = self.distance(a,c)
    ad = self.distance(a,d)
    bc = self.distance(b,c)
    bd = self.distance(b,d)
    cd = self.distance(c,d)
    #Checks to see if two and only two of the distances from point a are equal. Then if true, checks if the third distance is larger.
    #Then checks to make sure the corresponding other sides and diagonals are equal. If so adds the corresponding line segments and returns True and a value
    if ab == ac:
      if ab >= ad:
        return False, 0
      elif ad == bc and ab == cd and ab == bd:
        size = int((ab/self.squareSize)**2)
        player.addLines(QLine(a[0],a[1],b[0],b[1]))
        player.addLines(QLine(a[0],a[1],c[0],c[1]))
        player.addLines(QLine(c[0],c[1],d[0],d[1]))
        player.addLines(QLine(b[0],b[1],d[0],d[1]))
        return True, size
      else:
        return False, 0

    elif ab == ad:
      if ab >= ac:
        return False, 0
      elif ac == bd and ab ==cd and bc == ab:
        size = int((ab/self.squareSize)**2 )
        player.addLines(QLine(a[0],a[1],b[0],b[1]))
        player.addLines(QLine(a[0],a[1],d[0],d[1]))
        player.addLines(QLine(c[0],c[1],d[0],d[1]))
        player.addLines(QLine(b[0],b[1],c[0],c[1]))
        return True, size
      else:
        return False, 0
    elif ad == ac:
      if ad >= ab:
        return False, 0
      elif ab == cd and ad == bc and ad == bd:
        size = int((ac/self.squareSize)**2)
        player.addLines(QLine(a[0],a[1],d[0],d[1]))
        player.addLines(QLine(a[0],a[1],c[0],c[1]))
        player.addLines(QLine(b[0],b[1],c[0],c[1]))
        player.addLines(QLine(b[0],b[1],d[0],d[1]))
        return True, size
      else:
       return False, 0
    else:
      return False, 0



  def gainPoints(self,squ1,player):
    """Receive clicked square, then determines."""
    value = 0
    squaresformed = 0
    owned =(combinations(player.getOwned(),3)) #All the different combinations of owned points by a player
    pointsets = [[(squ1.center().x(),squ1.center().y()),(comb[0].center().x(),comb[0].center().y()),(comb[1].center().x(),comb[1].center().y()),(comb[2].center().x(),comb[2].center().y())] for comb in owned] #converted into a list of tuple integer points
    for pointset in pointsets:
      result = self.pointsAreSquare(pointset,player)
      if result[0]:
        squaresformed += 1
        value += result[1]
    if squaresformed >1:
      player.increment_multiplier(squaresformed)
    else:
      player.reset_multiplier()
    player.add_points(value)




  def setPlayerNumber(self,x):
    """Create the playercount list."""
    if x == 2:
      self.playerList = [self.playerOne,self.playerTwo]
    elif x == 3:
      self.playerList = [self.playerOne,self.playerTwo,self.playerThree]
    elif x == 4:
      self.playerList = [self.playerOne,self.playerTwo, self.playerThree,self.playerFour]
    else:
      self.playerList = [self.playerOne]


  def boardChange(self):
    """Create board and squares."""
    self.squareSize = windowSize/self.GameSize
    self.board = [[0 for row in range(self.GameSize)] for column in range(self.GameSize)]
    for row in range(0,self.GameSize):
      for column in range(0,self.GameSize):
        self.board[row][column] = [QRect(column * self.squareSize + xAxisSpace/2,row*self.squareSize + yAxisSpace/2,self.squareSize,self.squareSize), 0]
    for player in self.playerList:
      player.changeSquaresize(self.squareSize)

  def paintEvent(self, event):
      """Brush event."""
    qp = QPainter()
    blackPen = QPen(QBrush(Qt.black),1)
    qp.begin(self)
    qp.setPen(blackPen)
    
    if self.begin_game:
      # If player has control of a square, then draw that players color. Either way, draw the grid.
      for row in self.board:
        for column in row:
          if column[1]:
            qp.setBrush(column[1])
            qp.drawChord(column[0],0,5760)
            qp.setBrush(0)
          qp.drawRect(column[0])
      i=0
      #Write out the scores of each plaayers
      for player in self.playerList:
        if i <2:
          qp.drawText(200,(yAxisSpace/4) +20*i,player.get_name() +" "+str(player.get_score()))
          i+=1
        else:
          qp.drawText(500,(yAxisSpace/4)+20*(i-2),player.get_name() +" "+str(player.get_score()))
          i+=1
      #Write out who's turn it is, and their multiplier
      for player in self.playerList:
        if player.get_turn():
          qp.drawText(5,yAxisSpace/4,player.get_name()+ " Go:")
          qp.drawText(5,yAxisSpace/4 +15,"Multiplier is " + str(player.get_multiplier())+"x")
          break
      for player in self.playerList:
        for line in player.getLines():
          qp.setPen(QPen(player.get_color(),7))
          qp.drawLine(line)
    #Choosing the size of the board
    elif self.chooseSize:
      qp.drawText((windowSize/2)-55, 50, "Choose a Game Size")
      qp.drawRect(self.OptionOne)
      qp.drawRect(self.OptionTwo)
      qp.drawRect(self.OptionThree)
      qp.drawRect(self.OptionFour)
      qp.drawText(self.OptionOneT," 6x6")
      qp.drawText(self.OptionTwoT," 8x8")
      qp.drawText(self.OptionThreeT,"10x10")
      qp.drawText(self.OptionFourT,"12x12")
    
    #Overview of game
    elif self.overview:
      qp.drawText((windowSize/2)-200, 300, "- The goal of this game is to make squares of arbitrary size.")
      qp.drawText((windowSize/2)-200, 330, "- It may be played alone or competitively")
      qp.drawText((windowSize/2)-200, 360, "- When a square is made, points are recieved based on the area")
      qp.drawText((windowSize/2)-200, 390, "- When more than one square is made on a single turn, the multiplier is increased")
      qp.drawText((windowSize/2)-200, 405, "by the number of squares placed")
      qp.drawText((windowSize/2)-200, 435, "- The multiplier resets when 0 or 1 square is formed")


      qp.drawRect(self.OptionOne)
      qp.drawText(self.OptionOneT,"Options")


    #Choosing the number of players
    else:
      qp.drawText((windowSize/2)-65, 50, "Choose Number of Players")
      qp.drawRect(self.OptionOne)
      qp.drawRect(self.OptionTwo)
      qp.drawRect(self.OptionThree)
      qp.drawRect(self.OptionFour)
      qp.drawText(self.OptionOneT,"One")
      qp.drawText(self.OptionTwoT,"Two")
      qp.drawText(self.OptionThreeT,"Three")
      qp.drawText(self.OptionFourT,"Four")
    qp.end()



  def mousePressEvent(self, event):
    if self.begin_game:
      flag =False
      #Iterates through each row and column until it finds the clicked one. Then iterates through the players to see which player's turn it is.
      #When a player's turn is found, the corresponding square is set to that player's color. Then starts the next player in the list's turn. (sorry I used else, I'm sure there is another structure)
      for row in self.board:
        if flag:
          break
        for column in row:
          if column[0].contains(event.x(),event.y()) and column[1] == False:
            for player in self.playerList:
              if player.get_turn():
                column[1] = player.get_color()
                self.gainPoints(column[0],player)
                player.addOwned(column[0])
                player.end_turn()
                flag = True
                continue
              if flag:
                player.begin_turn()
                break
            else:
              self.playerList[0].begin_turn()
            break
      self.update()
    
    # overview screen
    elif self.overview:
      if self.OptionOne.contains(event.x(),event.y()):
        self.overview = False
      self.update()

    #Board Size buttons
    elif self.chooseSize:
      Optionlist = zip(self.Optionlist,(6,8,10,12))
      for option in Optionlist:
        if option[0].contains(event.x(),event.y()):
          self.GameSize = option[1]
          self.boardChange()
          self.begin_game = True
          self.update()
          break
    #Player number buttons
    else:
      Optionlist = zip(self.Optionlist, (1,2,3,4))
      for option in Optionlist:
        if option[0].contains(event.x(),event.y()):
          self.setPlayerNumber(option[1])
          self.chooseSize = True
          self.playerOne.begin_turn()
          self.ChangeColor()
          self.update()




if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = SquareGame()
  sys.exit(app.exec_())
