import pygame
from sys import exit
from random import randint, choice
from copy import deepcopy

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		#self.player_index = 0
		#self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[0]
		self.rect = self.image.get_rect(midbottom = (80,300))
		#self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)


	def update(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] and self.rect.top > 0:
			self.rect.y -= 8
		if keys[pygame.K_s] and self.rect.bottom < 400:
			self.rect.y += 8

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = randint(50, 350)

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time - total_pause
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		#obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Harry Potter\'s Dementor Dash')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
magic_font_30 = pygame.font.Font('font/witches-magic.ttf', 30)
magic_font_10 = pygame.font.Font('font/witches-magic.ttf', 10)

freeze_screen = False
game_active = False
trivia_screen = False
start_time = 0
pause_start = 0
pause_end = 0
total_pause = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
#bg_music.play(loops = -1)




#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/hogwarts.png').convert()
trivia_surface = pygame.image.load('graphics/trivia.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Harry Potter\'s Dementor Dash',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to fly!',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

start_screen = pygame.image.load('graphics/start_screen.png').convert()

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


#load in trivia questions here
TRIVIA_QUESTIONS_POOL = {
	"Harry Potter is remembered as a legendary seeker at Hogwarts. How many snitches did Harry catch during his playing years?": ["a) 5 snitches", "b) 2 snitches", "c) 7 snitches", "d) 1 snitch",
	pygame.K_c],
	"Harry Potter has used his broom in masterful ways to get out of tight situations, which was Harry's first ever broom?": ["a) The Bongo 45", "b) The Nimbus 2000", "c) The Demented Horror", "d) The Firebolt",
	pygame.K_b],
	"In his 7th year at Hogwarts, Harry famously ventured off to find Voldemort's Horcruxes, which object was not a Horcrux?" : ["a) Tom Riddle's Diary", "b) The Elder Wand", "c) The Diadem of Ravenclaw", "d) Marvolo Gaunt's Ring",
																															  pygame.K_b],

}  #we keep this as a constant, since every time we use a question we remove it from the dict in order to prevent repeating questions. When we run out of questions we reload all questions to prevent crash

trivia_questions = deepcopy(TRIVIA_QUESTIONS_POOL)
 
curr_trivia_question, curr_trivia_ans = choice(list(trivia_questions.items())) #refresh this after every trivia question is answered to get a new one
trivia_questions.pop(curr_trivia_question)



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly'])))

		elif freeze_screen:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				trivia_screen = True
				freeze_screen = False
				obstacle_group.empty()

		elif trivia_screen:
			if event.type == pygame.KEYDOWN and event.key == correct_key:
				game_active = True
				trivia_screen = False
				if len(trivia_questions) == 0:
					trivia_questions = deepcopy(TRIVIA_QUESTIONS_POOL)
				else:
					curr_trivia_question, curr_trivia_ans = choice(list(trivia_questions.items()))
					trivia_questions.pop(curr_trivia_question)



				#calculate the amount of time we spent waiting so the score is not crazy as shit
				pause_end = pygame.time.get_ticks()
				total_pause += int((pause_end - pause_start) / 1000)
				pause_end = 0 #reset our timer variables
				pause_start = 0

			elif event.type == pygame.KEYDOWN and event.key in incorrect_keys:
				game_active = False
				trivia_screen = False
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)
				total_pause = 0


	if game_active:
		screen.blit(sky_surface,(0,0))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		if not game_active:

			freeze_screen = True
			pause_start = pygame.time.get_ticks()  #start the pause timer
	
	elif freeze_screen:
		screen.blit(sky_surface,(0,0))
		
		player.draw(screen)
		obstacle_group.draw(screen)

		#game over text

		dead_message = magic_font_30.render("PRESS ENTER TO TRY TO REVIVE!",True,(255,255,255))
		dead_message_rect = dead_message.get_rect(center = (400,40))
		screen.blit(dead_message, dead_message_rect)


		

	
	elif trivia_screen:
		screen.blit(trivia_surface, (0,0))
		trivia_message = magic_font_30.render("Answer Correctly to Save Harry!",True,(255,255,255))
		trivia_message_rect = trivia_message.get_rect(center = (400,50))

		trivia_question = magic_font_10.render(curr_trivia_question,True,(255,255,255))
		trivia_question_rect = trivia_question.get_rect(center = (400, 100))

		
		screen.blit(trivia_message, trivia_message_rect)
		screen.blit(trivia_question, trivia_question_rect)

		trivia_answer_a = magic_font_10.render(curr_trivia_ans[0],True,(0,0,0))
		trivia_answer_b = magic_font_10.render(curr_trivia_ans[1],True,(0,0,0))
		trivia_answer_c = magic_font_10.render(curr_trivia_ans[2],True,(0,0,0))
		trivia_answer_d = magic_font_10.render(curr_trivia_ans[3],True,(0,0,0))

		trivia_answer_a_rect = trivia_answer_a.get_rect(center = (400, 150))
		trivia_answer_b_rect = trivia_answer_b.get_rect(center = (400, 200))
		trivia_answer_c_rect = trivia_answer_c.get_rect(center = (400, 250))
		trivia_answer_d_rect = trivia_answer_d.get_rect(center = (400, 300))

		screen.blit(trivia_answer_a, trivia_answer_a_rect)
		screen.blit(trivia_answer_b, trivia_answer_b_rect)
		screen.blit(trivia_answer_c, trivia_answer_c_rect)
		screen.blit(trivia_answer_d, trivia_answer_d_rect)

		possible_keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]
		correct_key = curr_trivia_ans[-1] #by convention I'm storing the correct key that the user should press as the last element of the list
		incorrect_keys = [key for key in possible_keys if key != correct_key]
	
	
		
	else:
		screen.blit(start_screen, (0,0))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)


		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)

	