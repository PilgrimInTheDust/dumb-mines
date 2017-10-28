import numpy as np
from numpy.random import randint
from scipy.signal import convolve2d

class Board:
	def __init__(self,height=10,width=10,n_bombs=10):
		self.height = height
		self.width = width
		self.n_bombs = n_bombs
		self.shape = (height, width)

	def generate(self):
		self.bombs = np.zeros(shape = (self.height, self.width), dtype=np.int8)

		placed = 0
		while placed < self.n_bombs:
			x = randint(0, self.height)
			y = randint(0, self.width)

			if self.is_bomb(x,y):
				continue

			self.bombs[x,y] = 1
			placed += 1

		self.compute_counts()


	def compute_counts(self):
		ker = np.array([[1,1,1],[1,0,1],[1,1,1]])
		self.counts = convolve2d(self.bombs, ker, 'same')

	def is_bomb(self,x,y):
		return self.bombs[x,y] == 1

	def is_empty(self,x,y):
		return self.counts[x,y] == 0

	def load(self,file):
		pass

	def set_counts(self,x,y,val):
		self.counts[x,y] = val
	def get_counts(self,x,y):
		return self.counts[x,y]

	def neighboors(self, x, y):
		w = self.height-1
		h = self.width-1
		xlc = x-1 if x != 0 else x
		ylc = y-1 if y !=0 else y
		xuc = x+1 if x != h else x
		yuc = y+1 if y != w else y
		one = (x, ylc)
		two = (xlc,ylc)
		three = (xlc,y)
		four = (xlc,yuc)
		five = (x,yuc)
		six = (xuc,yuc)
		seven = (xuc,y)
		eight = (xuc, ylc)
		return [one, two, three, four, five, six , seven, eight]

	def zeros_around(self, x, y):
		zeros = []
		nb = [couple for couple in self.neighboors(x,y) if couple != (x,y)]
		for couple in nb:
			if not self.get_counts(*couple):
				zeros.append(couple)

		return zeros


class Game:
	def __init__(self):
		pass

	def start(self):
		print('#'*20)
		print("## Mines of doom v0.1\n")

		height = int(input("Height: "))
		width = int(input("Width: "))
		n_bombs = int(input("Bombs: "))

		self.board = Board(height,width,n_bombs)
		self.board.generate()

		self.alive = True
		self.revealed = np.zeros(shape = self.board.shape)

	def print_board(self):

		for x in range(self.board.height):
			for y in range(self.board.width):
				if self.revealed[x,y]:
					if self.board.bombs[x,y]:
						print('B', end = ' ')
					else:
						print(self.board.counts[x,y], end = ' ')
				else:
					print('X', end=' ')
			print()

	def run(self):

		print('#'*20)
		self.print_board()

		ok = True
		while ok:
			print("Your next move (format X Y): ",end='')
			try:
				x, y = [int(i) for i in input().split()]
			except:
				continue
			if (x<self.board.height and y<self.board.width):
				ok = False

		if self.board.is_bomb(x,y):
			self.revealed = np.ones(shape=self.board.shape)
			self.alive = False
			self.game_over()
		else:
			self.revealed[x,y] = 1
			#cluster 0
			if self.board.counts[x,y] == 0:
				self.clusterize_zeros(x,y)



		return self.alive

	def clusterize_zeros(self,x,y):
		zeros = []
		zeros.append((x,y))
		newzeros = zeros
		while len(newzeros) != 0:
			tmp = newzeros
			newzeros = []
			for couple in tmp:
				zeros_around = self.board.zeros_around(*couple)
				for ze in zeros_around:
					if ze in zeros:
						continue
					else:
						newzeros.append(ze)
						zeros.append(ze)
		#open all zeros
		for couple in zeros:
			self.round_rev(*couple)



	def round_rev(self,x,y):
		nb = [couple for couple in self.board.neighboors(x,y) if couple != (x,y)]
		for couple in nb:
			self.set_rev(*couple)

	def set_rev(self,x,y):
		self.revealed[x,y] = 1

	def game_over(self):
		print('#'*20)
		self.print_board()

		print('Enjoy getting blown :3')
if __name__ == "__main__":

	game = Game()
	game.start()

	while True:
		if not game.run():
			break
