import pygame, time, math, random
from pygame.locals import *

pygame.init

# LEFT, FRONT, RIGHT

KEYS_LABELS = ['W', 'A', 'S', 'D']
SCREEN_X = 640
SCREEN_Y = 480
N_KEYS = len(KEYS_LABELS)
BUFFER_SEG = 10

CAR_WIDTH = 15
CAR_HEIGHT = 15

RADIUS_SMALL = 25

TRACK_LEFT = (SCREEN_X - CAR_WIDTH) / 2 - BUFFER_SEG
TRACK_RIGHT = (SCREEN_X + CAR_WIDTH) / 2 + BUFFER_SEG
TRACK_WIDTH = TRACK_RIGHT - TRACK_LEFT

CARPOS_X = (SCREEN_X - CAR_WIDTH) / 2
CARPOS_Y = SCREEN_Y - CAR_HEIGHT
RADIUS_LARGE = RADIUS_SMALL + TRACK_WIDTH

DIA_SMALL = 2 * RADIUS_SMALL
DIA_LARGE = 2 * RADIUS_LARGE
SPEED = 0.1
SPEED_GAME = 0.1

HEIGHT_DIFF = RADIUS_LARGE - RADIUS_SMALL

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

car = pygame.image.load('car.jpg')

keys = [False] * N_KEYS

def leftTurn(i):
	pygame.draw.arc(screen, 0, ((TRACK_LEFT - DIA_SMALL, HEIGHT_DIFF + i), (DIA_SMALL, DIA_SMALL)), 0, math.pi / 2, 1)
	pygame.draw.arc(screen, 0, ((TRACK_RIGHT - DIA_LARGE, i), (DIA_LARGE, DIA_LARGE)), 0, math.pi / 2, 1)
	pygame.draw.arc(screen, 0, ((TRACK_LEFT - DIA_SMALL, 2 * HEIGHT_DIFF + i - DIA_LARGE), (DIA_SMALL, DIA_SMALL)), math.pi, 1.5 * math.pi, 1)
	pygame.draw.arc(screen, 0, ((TRACK_RIGHT - DIA_LARGE, HEIGHT_DIFF + i - DIA_LARGE), (DIA_LARGE, DIA_LARGE)), math.pi, 1.5 * math.pi, 1)
	return HEIGHT_DIFF + i


def rightTurn(i):
	pygame.draw.arc(screen, 0, ((TRACK_RIGHT, HEIGHT_DIFF + i), (DIA_SMALL, DIA_SMALL)), math.pi / 2, math.pi, 1)
	pygame.draw.arc(screen, 0, ((TRACK_LEFT, i), (DIA_LARGE, DIA_LARGE)), math.pi / 2, math.pi, 1)
	pygame.draw.arc(screen, 0, ((TRACK_RIGHT, 2 * HEIGHT_DIFF + i - DIA_LARGE), (DIA_SMALL, DIA_SMALL)), 1.5 * math.pi, 2 * math.pi, 1)
	pygame.draw.arc(screen, 0, ((TRACK_LEFT, HEIGHT_DIFF + i - DIA_LARGE), (DIA_LARGE, DIA_LARGE)), 1.5 *  math.pi, 2 * math.pi, 1)
	return HEIGHT_DIFF + i



def goLeft():
	global TRACK_LEFT, TRACK_RIGHT, CARPOS_Y, CARPOS_X
	ORIGINAL_TRACK_LEFT = TRACK_LEFT
	ORIGINAL_TRACK_RIGHT = TRACK_RIGHT
	NEW_TRACK_LEFT = TRACK_LEFT - (RADIUS_SMALL + RADIUS_LARGE)
	NEW_TRACK_RIGHT = TRACK_RIGHT - (RADIUS_SMALL + RADIUS_LARGE)
	for i in range(int((SCREEN_Y + DIA_LARGE) / SPEED_GAME)):
		screen.fill([255, 255, 255])
		H_new = leftTurn((i * SPEED_GAME) - DIA_LARGE)
		pygame.draw.line(screen, 0,(ORIGINAL_TRACK_LEFT, H_new + RADIUS_SMALL), (ORIGINAL_TRACK_LEFT, SCREEN_Y), 1)
		pygame.draw.line(screen, 0, (ORIGINAL_TRACK_RIGHT, H_new + RADIUS_SMALL), (ORIGINAL_TRACK_RIGHT, SCREEN_Y), 1)
		screen.blit(car, (CARPOS_X, CARPOS_Y))
		pygame.draw.line(screen, 0,(NEW_TRACK_LEFT, 0), (NEW_TRACK_LEFT, H_new - RADIUS_LARGE), 1)
		pygame.draw.line(screen, 0, (NEW_TRACK_RIGHT, 0), (NEW_TRACK_RIGHT, H_new - RADIUS_LARGE), 1)
		pygame.display.flip()
		if CARPOS_Y + (CAR_HEIGHT / 2) > H_new + RADIUS_SMALL:
			LEFT_DIST = CARPOS_X - ORIGINAL_TRACK_LEFT + (CAR_WIDTH / 2)
			RIGHT_DIST = ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2)
			print([LEFT_DIST, 0, RIGHT_DIST])
		elif CARPOS_Y + (CAR_HEIGHT / 2) > H_new:
			LEFT_DIST = CARPOS_X - ORIGINAL_TRACK_LEFT + (CAR_WIDTH / 2) + RADIUS_SMALL - math.sqrt((RADIUS_SMALL ** 2) - ((CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL) ** 2))
			RIGHT_DIST = ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) - RADIUS_LARGE + math.sqrt((RADIUS_LARGE ** 2) - ((CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL) ** 2))
			TOP_DIST = CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL + math.sqrt((RADIUS_LARGE ** 2) - ((ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) - RADIUS_LARGE) ** 2))
			print([LEFT_DIST, TOP_DIST, RIGHT_DIST])
		elif CARPOS_Y + (CAR_HEIGHT / 2) > H_new + RADIUS_SMALL - RADIUS_LARGE:
			LEFT_DIST = CARPOS_X - NEW_TRACK_LEFT + (CAR_WIDTH / 2) - (RADIUS_LARGE - math.sqrt((RADIUS_LARGE ** 2) - ((H_new - CARPOS_Y - (CAR_HEIGHT / 2) - RADIUS_LARGE) ** 2)))
			RIGHT_DIST = ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) - RADIUS_LARGE + math.sqrt((RADIUS_LARGE ** 2) - ((CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL) ** 2))
			TOP_DIST = CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL + math.sqrt((RADIUS_LARGE ** 2) - ((ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) - RADIUS_LARGE) ** 2))
			print([LEFT_DIST, TOP_DIST, RIGHT_DIST])
			# exit()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_w:
					keys[0] = True
				elif event.key == K_a:
					keys[1] = True
				elif event.key == K_s:
					keys[2] = True
				elif event.key == K_d:
					keys[3] = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					keys[0] = False
				elif event.key == pygame.K_a:
					keys[1] = False
				elif event.key == pygame.K_s:
					keys[2] = False
				elif event.key == pygame.K_d:
					keys[3] = False

		if keys[0]:
			CARPOS_Y -= SPEED
		if keys[1]:
			CARPOS_X -= SPEED
		if keys[2]:
			CARPOS_Y += SPEED
		if keys[3]:
			CARPOS_X += SPEED

	TRACK_LEFT = NEW_TRACK_LEFT
	TRACK_RIGHT = NEW_TRACK_RIGHT


def goRight():
	global TRACK_LEFT, TRACK_RIGHT, CARPOS_Y, CARPOS_X
	ORIGINAL_TRACK_LEFT = TRACK_LEFT
	ORIGINAL_TRACK_RIGHT = TRACK_RIGHT
	NEW_TRACK_LEFT = TRACK_LEFT + (RADIUS_SMALL + RADIUS_LARGE)
	NEW_TRACK_RIGHT = TRACK_RIGHT + (RADIUS_SMALL + RADIUS_LARGE)
	for i in range(int((SCREEN_Y + DIA_LARGE) / SPEED_GAME)):
		screen.fill([255, 255, 255])
		H_new = rightTurn((i * SPEED_GAME) - DIA_LARGE)
		pygame.draw.line(screen, 0,(ORIGINAL_TRACK_LEFT, H_new + RADIUS_SMALL), (ORIGINAL_TRACK_LEFT, SCREEN_Y), 1)
		pygame.draw.line(screen, 0, (ORIGINAL_TRACK_RIGHT, H_new + RADIUS_SMALL), (ORIGINAL_TRACK_RIGHT, SCREEN_Y), 1)
		screen.blit(car, (CARPOS_X, CARPOS_Y))
		pygame.draw.line(screen, 0,(NEW_TRACK_LEFT, 0), (NEW_TRACK_LEFT, H_new - RADIUS_LARGE), 1)
		pygame.draw.line(screen, 0, (NEW_TRACK_RIGHT, 0), (NEW_TRACK_RIGHT, H_new - RADIUS_LARGE), 1)
		pygame.display.flip()
		if CARPOS_Y + (CAR_HEIGHT / 2) > H_new + RADIUS_SMALL:
			print([CARPOS_X - ORIGINAL_TRACK_LEFT + (CAR_WIDTH / 2), 0, ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2)])
		elif CARPOS_Y + (CAR_HEIGHT / 2) < H_new - RADIUS_LARGE:
			print([CARPOS_X - NEW_TRACK_LEFT + (CAR_WIDTH / 2), 0, NEW_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2)])
		elif CARPOS_Y + (CAR_HEIGHT / 2) > H_new:
			BASE_HEIGHT = H_new + RADIUS_SMALL - CARPOS_Y - (CAR_HEIGHT / 2)
			LEFT_DIST = CARPOS_X - ORIGINAL_TRACK_LEFT + (CAR_WIDTH / 2) - RADIUS_LARGE + math.sqrt((RADIUS_LARGE ** 2) - (BASE_HEIGHT ** 2))
			RIGHT_DIST = ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) + RADIUS_SMALL - math.sqrt((RADIUS_SMALL ** 2) - (BASE_HEIGHT ** 2))
			TOP_DIST = math.sqrt((RADIUS_LARGE ** 2) - ((CARPOS_X - ORIGINAL_TRACK_LEFT - RADIUS_LARGE) ** 2)) - BASE_HEIGHT
			print([LEFT_DIST, TOP_DIST, RIGHT_DIST])
		elif CARPOS_Y + (CAR_HEIGHT / 2) > H_new - RADIUS_LARGE + RADIUS_SMALL:
			BASE_HEIGHT = H_new + RADIUS_SMALL - CARPOS_Y - (CAR_HEIGHT / 2)
			LEFT_DIST = CARPOS_X - ORIGINAL_TRACK_LEFT + (CAR_WIDTH / 2) - RADIUS_LARGE + math.sqrt((RADIUS_LARGE ** 2) - (BASE_HEIGHT ** 2))
			RIGHT_DIST = ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) + RADIUS_SMALL + math.sqrt((RADIUS_LARGE ** 2) - ((H_new - CARPOS_Y - (CAR_HEIGHT / 2) - RADIUS_LARGE) ** 2))
			TOP_DIST = math.sqrt((RADIUS_LARGE ** 2) - ((CARPOS_X - ORIGINAL_TRACK_LEFT - RADIUS_LARGE) ** 2)) - BASE_HEIGHT
			if CARPOS_X > NEW_TRACK_LEFT - RADIUS_SMALL:
				TOP_DIST = CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL + RADIUS_LARGE + RADIUS_SMALL - (math.sqrt(RADIUS_SMALL ** 2) - ((RADIUS_SMALL - NEW_TRACK_LEFT + CARPOS_X) ** 2))
			print([LEFT_DIST, TOP_DIST, RIGHT_DIST])
		else:
			BASE_HEIGHT = H_new + RADIUS_SMALL - CARPOS_Y - (CAR_HEIGHT / 2)
			LEFT_DIST = CARPOS_X - NEW_TRACK_LEFT + (CAR_WIDTH / 2) + RADIUS_SMALL - math.sqrt((RADIUS_SMALL ** 2) - ((RADIUS_SMALL - H_new - RADIUS_SMALL + RADIUS_LARGE + CARPOS_Y) ** 2))
			RIGHT_DIST = ORIGINAL_TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2) + RADIUS_SMALL + math.sqrt((RADIUS_LARGE ** 2) - ((H_new - CARPOS_Y - RADIUS_LARGE) ** 2))
			TOP_DIST = CARPOS_Y + (CAR_HEIGHT / 2) - H_new - RADIUS_SMALL + RADIUS_LARGE + RADIUS_SMALL - (math.sqrt(RADIUS_SMALL ** 2) - ((RADIUS_SMALL - NEW_TRACK_LEFT + CARPOS_X) ** 2))
			if CARPOS_X > NEW_TRACK_LEFT:
				TOP_DIST = 0
			print([LEFT_DIST, TOP_DIST, RIGHT_DIST])

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == K_w:
					keys[0] = True
				elif event.key == K_a:
					keys[1] = True
				elif event.key == K_s:
					keys[2] = True
				elif event.key == K_d:
					keys[3] = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					keys[0] = False
				elif event.key == pygame.K_a:
					keys[1] = False
				elif event.key == pygame.K_s:
					keys[2] = False
				elif event.key == pygame.K_d:
					keys[3] = False

		if keys[0]:
			CARPOS_Y -= SPEED
		if keys[1]:
			CARPOS_X -= SPEED
		if keys[2]:
			CARPOS_Y += SPEED
		if keys[3]:
			CARPOS_X += SPEED

	TRACK_LEFT = NEW_TRACK_LEFT
	TRACK_RIGHT = NEW_TRACK_RIGHT



while True:
	screen.fill([255, 255, 255])
	x = random.randint(0, 2)
	if x == 1 and TRACK_LEFT - (RADIUS_SMALL + RADIUS_LARGE) > 0:
		goLeft()
	elif x == 2 and TRACK_RIGHT + (RADIUS_SMALL + RADIUS_LARGE) < SCREEN_X:
		goLeft()
	pygame.draw.line(screen, 0,(TRACK_LEFT, 0), (TRACK_LEFT, SCREEN_Y), 1)
	pygame.draw.line(screen, 0, (TRACK_RIGHT, 0), (TRACK_RIGHT, SCREEN_Y), 1)
	screen.blit(car, (CARPOS_X, CARPOS_Y))
	pygame.draw.line(screen, 0,(TRACK_LEFT, 0), (TRACK_LEFT, SCREEN_Y), 1)
	pygame.draw.line(screen, 0, (TRACK_RIGHT, 0), (TRACK_RIGHT, SCREEN_Y), 1)
	pygame.display.flip()
	print([CARPOS_X - TRACK_LEFT + (CAR_WIDTH / 2), 0, TRACK_RIGHT - CARPOS_X - (CAR_WIDTH / 2)])
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit(0)
		if event.type == pygame.KEYDOWN:
			if event.key == K_w:
				keys[0] = True
			elif event.key == K_a:
				keys[1] = True
			elif event.key == K_s:
				keys[2] = True
			elif event.key == K_d:
				keys[3] = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				keys[0] = False
			elif event.key == pygame.K_a:
				keys[1] = False
			elif event.key == pygame.K_s:
				keys[2] = False
			elif event.key == pygame.K_d:
				keys[3] = False

	if keys[0]:
		CARPOS_Y -= SPEED
	if keys[1]:
		CARPOS_X -= SPEED
	if keys[2]:
		CARPOS_Y += SPEED
	if keys[3]:
		CARPOS_X += SPEED