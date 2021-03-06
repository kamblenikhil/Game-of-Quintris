# "Fancier" animated interactive version of quintris. v0.2
# Prof. David Crandall, Sept 2021

from QuintrisGame import *

class AnimatedQuintris(QuintrisGame):

  def __init__(self):
      QuintrisGame.__init__(self)

  # This thread just repeated displays the current game board to the screen.
  def display_thread(self):
    while 1:
      self.print_board(True)
      print("Controls: b moves left, n rotates, m moves right, h flips, spacebar drops\n")
      time.sleep(0.1)

  # This thread is in charge of making the piece fall over time.
  def gravity_thread(self):
    while True:
      while 1:
        time.sleep(0.5)
        self.row = self.row+1
        if(QuintrisGame.check_collision(*self.state, self.piece, self.row+1, self.col)): break

      # place new piece in final resting spot 
      self.finish()

  # This thread just starts things up
  def start_game(self, player):
    t2 = threading.Thread(target=self.gravity_thread)
    t2.setDaemon(True)
    t3 = threading.Thread(target=self.display_thread)
    t3.setDaemon(True)
    t2.start()
    t3.start()

    player.control_game(self)
