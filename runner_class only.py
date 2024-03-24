import pygame
from sys import exit
from random import randint, choice
from copy import deepcopy


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 5))  # Define the size of the projectile
        self.image.fill((0, 0, 255))  # Color the projectile blue
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        self.rect.x += 10  # Speed of the projectile
        if self.rect.x > 800:  # Remove the projectile if it goes beyond the screen
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.image = self.player_walk[0]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.max_mana = 5  # Maximum mana the player can have.
        self.mana = self.max_mana  # Current mana starts full.



		#self.gravity = 0

		#self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		#self.jump_sound.set_volume(0.5)


		#self.player_index = 0
		#self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.rect.y -= 8
        if (keys[pygame.K_s] or keys[pygame.K_DOWN])and self.rect.bottom < 400:
            self.rect.y += 8
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
            self.rect.x -= 5  # Adjust speed as needed
            if self.rect.left < 0:  # Prevent moving out of bounds
                self.rect.left = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
            self.rect.x += 5  # Adjust speed as needed
            if self.rect.right > 800:  # Assuming screen width is 800
                self.rect.right = 800

    # Method for shooting projectiles
    def shoot(self):
        if self.mana == self.max_mana:
           projectile = Projectile(self.rect.midtop)
           projectile_group.add(projectile)
           self.mana -= self.max_mana  # Decrease mana by 1 for each projectile shot
	

    def regenerate_mana(self, regen_rate):
        if self.mana < self.max_mana:
            self.mana += regen_rate
            self.mana = min(self.mana, self.max_mana)  # Ensure mana doesn't exceed max.



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = randint(50, 350)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
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

def draw_mana_bar(surface, x, y, pct):
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (pct / 5) * BAR_LENGTH  # Calculate fill based on mana percentage.
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, (0, 0, 255), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Harry Potter\'s Dementor Dash')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
magic_font_30 = pygame.font.Font('font/witches-magic.ttf', 30)
magic_font_10 = pygame.font.Font('font/witches-magic.ttf', 10)
magic_font_20 = pygame.font.Font('font/witches-magic.ttf', 18)
magic_font_40 = pygame.font.Font('font/witches-magic.ttf', 40)

intro_font_15 = pygame.font.Font('font/introfont.ttf', 15)


#screen state variables
freeze_screen = False
game_active = False
trivia_screen = False
introduction_screen = True
demented_screen = False
controls_screen = False


#this is to facilitate the animation onto the screen of the introduction story
last_update = pygame.time.get_ticks()
interval = 150

index1 = 0
index2 = 0
index3 = 0
index4 = 0

intro_line1 = "The rumblings have been true.. the Dementors of Azkaban have lost control again!"
intro_line2 = "These creatures of sadness and despair are preying on all who come in their way.."
intro_line3 = "As all hope seems lost, and darkness seems destined to envelop all we know and love"
intro_line4 = "The Boy Who Lived, Lightning, The Chosen One, comes soaring in fearlessly once more..."

# Demented screen animation variables
demented_index1 = 0
demented_index2 = 0
demented_index3 = 0
demented_last_update = 0
demented_interval = 150  # Adjust the speed of the text animation

# Demented messages
demented_line1 = "You have surrendered to the dementor's kiss..."
demented_line2 = "You will now perish with your soul being snatched..."
demented_line3 = "All of Hogwarts and the Wizarding World is at doom!"

instructions_screen = False

controls_text_lines = [
    ("Flight Mechanics", ""),
    ("", ""),
    ("Soar Upwards:", "W or Up Arrow"),
    ("Descend Downwards:", "S or Down Arrow"),
    ("Pivot Left:", "A or Left Arrow"),
    ("Pivot Right:", "D or Right Arrow"),
    ("Expecto Patronus:", "Spacebar"),
    ("", ""),
    ("", ""),
    ("Press Enter to continue", "")
]



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
projectile_group = pygame.sprite.Group()  # Group for projectiles

sky_surface = pygame.image.load('graphics/hogwarts.png').convert()
trivia_surface = pygame.image.load('graphics/trivia.png').convert()
introduction_surface = pygame.image.load('graphics/introduction.png')

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




#load in trivia questions here

#NOTE: WHEN ADDING TRIVIA QUESTIONS MAKE SURE THEY'RE ALL AROUND THE SAME LENGTH TO ENSURE THEY ALL FIT. ALSO, WE SPLIT INTO 2 LINES BY '.' SO MAKE SURE THERE'S A PERIOD IN EACH QUESTION
TRIVIA_QUESTIONS_POOL = {
	"Harry Potter is remembered as a legendary seeker at Hogwarts. Select the number of snitches Harry caught while playing.": ["a) 5 snitches", "b) 2 snitches", "c) 7 snitches", "d) 1 snitch",
	pygame.K_c],
	"Harry Potter has used his broom in masterful ways to get out of tight situations. Select Harry's first broom.": ["a) The Bongo 45", "b) The Nimbus 2000", "c) The Demented Horror", "d) The Firebolt",
	pygame.K_b],
	"Harry famously ventured off to find Voldemort's Horcruxes. Select the object that is not a Horcrux." : ["a) Tom Riddle's Diary", "b) The Elder Wand", "c) The Diadem of Ravenclaw", "d) Marvolo Gaunt's Ring",
																															  pygame.K_b],

}  #we keep this as a constant, since every time we use a question we remove it from the dict in order to prevent repeating questions. When we run out of questions we reload all questions to prevent crash

trivia_questions = deepcopy(TRIVIA_QUESTIONS_POOL)
 
curr_trivia_question, curr_trivia_ans = choice(list(trivia_questions.items())) #refresh this after every trivia question is answered to get a new one
trivia_questions.pop(curr_trivia_question)


#this is probably good for blitting text (automates the font, getrect, then blip task)
def blit_text(text, font,r,g,b,center):
	text_message = font.render(text,True,(r,g,b))
	text_message_rect = text_message.get_rect(center = center)
	screen.blit(text_message,text_message_rect)



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly'])))
				obstacle_count += 1
				obstacle_lock = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					player.sprite.shoot()
		
		elif introduction_screen:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				introduction_screen = False
				controls_screen = True  # Transition to the controls screen

		elif freeze_screen:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				trivia_screen = True
				freeze_screen = False
				obstacle_group.empty()
		
		elif controls_screen:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				controls_screen = False
		
		elif demented_screen:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				demented_screen = False
				demented_index1 = 0
				demented_index2 = 0
				demented_index3 = 0
				


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
				demented_screen = True

				# Reset player's position and mana
				player.sprite.rect.midbottom = (80, 300)  # Reset position
				player.sprite.mana = player.sprite.max_mana  # Refill mana

				# Reset the game timer
				start_time = int(pygame.time.get_ticks() / 1000)
				total_pause = 0  # Reset total pause time if you're using it

				# Clear obstacles and projectiles
				obstacle_group.empty()
				projectile_group.empty()

				# Additional resets as needed (e.g., score, obstacle timer, etc.)
				score = 0
				pygame.time.set_timer(obstacle_timer, 1200)  # Reset obstacle spawning timer, adjust as needed
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)
				total_pause = 0

				obstacle_interval = 1200
				obstacle_count = 0
				obstacle_lock = False
				pygame.time.set_timer(obstacle_timer,obstacle_interval)


	if game_active:
		screen.blit(sky_surface,(0,0))
		score = display_score()
		
		player.draw(screen)
		player.update()

		draw_mana_bar(screen, 10, 10, player.sprite.mana)  # Draw the mana bar based 
		player.sprite.regenerate_mana(0.02)  # Regenerate mana over time; adjust rate as needed.on current mana.


		print(obstacle_count, obstacle_interval)

		#update our timer with the score (maybe after every 10, it reduces by 100?)
		if obstacle_count % 10 == 0 and obstacle_interval > 500 and obstacle_lock:
			obstacle_interval -= 100
			pygame.time.set_timer(obstacle_timer,obstacle_interval)
			obstacle_lock = False

		obstacle_group.draw(screen)
		obstacle_group.update()

		projectile_group.draw(screen)
		projectile_group.update()

		# Handle collisions between projectiles and obstacles
		pygame.sprite.groupcollide(projectile_group, obstacle_group, True, True)

		pygame.display.update()

		game_active = collision_sprite()
		if not game_active:

			freeze_screen = True
			pause_start = pygame.time.get_ticks()  #start the pause timer
	
	elif freeze_screen:
		screen.blit(sky_surface,(0,0))
		
		player.draw(screen)
		obstacle_group.draw(screen)

		#game over text

		dead_message = magic_font_30.render("PRESS ENTER TO SAME HIM FROM THE KISS!",True,(255,255,255))
		dead_message_rect = dead_message.get_rect(center = (400,40))
		screen.blit(dead_message, dead_message_rect)

		you_died = magic_font_40.render("HARRY GOT CAUGHT!",True,(255,255,255))
		you_died_rect = you_died.get_rect(center = (400,200))
		screen.blit(you_died,you_died_rect)
		


		

	
	elif trivia_screen:
		screen.blit(trivia_surface, (0,0))
		trivia_message = magic_font_30.render("Answer Correctly to Save Harry!",True,(255,255,255))
		trivia_message_rect = trivia_message.get_rect(center = (400,50))

		#For readability, split the question into 2 (deliminator is '.') and have them on separate lines (trivia_question_1 and 2)
		trivia_question_1 = magic_font_20.render(curr_trivia_question.split('.')[0]+'.',True,(255,255,255))
		trivia_question_rect_1 = trivia_question_1.get_rect(center = (400, 100))

		trivia_question_2 = magic_font_20.render(curr_trivia_question.split('.')[1]+'?',True,(255,255,255))
		trivia_question_rect_2 = trivia_question_2.get_rect(center = (400,150))

		
		screen.blit(trivia_message, trivia_message_rect)
		screen.blit(trivia_question_1, trivia_question_rect_1)
		screen.blit(trivia_question_2, trivia_question_rect_2)

		trivia_answer_a = magic_font_10.render(curr_trivia_ans[0],True,(255,255,255))
		trivia_answer_b = magic_font_10.render(curr_trivia_ans[1],True,(255,255,255))
		trivia_answer_c = magic_font_10.render(curr_trivia_ans[2],True,(255,255,255))
		trivia_answer_d = magic_font_10.render(curr_trivia_ans[3],True,(255,255,255))

		trivia_answer_a_rect = trivia_answer_a.get_rect(center = (400, 200))
		trivia_answer_b_rect = trivia_answer_b.get_rect(center = (400, 250))
		trivia_answer_c_rect = trivia_answer_c.get_rect(center = (400, 300))
		trivia_answer_d_rect = trivia_answer_d.get_rect(center = (400, 350))

		screen.blit(trivia_answer_a, trivia_answer_a_rect)
		screen.blit(trivia_answer_b, trivia_answer_b_rect)
		screen.blit(trivia_answer_c, trivia_answer_c_rect)
		screen.blit(trivia_answer_d, trivia_answer_d_rect)

		possible_keys = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]
		correct_key = curr_trivia_ans[-1] #by convention I'm storing the correct key that the user should press as the last element of the list
		incorrect_keys = [key for key in possible_keys if key != correct_key]
	
	elif controls_screen:
		screen.blit(introduction_surface,(0,0))

		left_column_x = 800 // 3 - 100  # Adjust as needed for the control names
		right_column_x = 800 // 3 + 150  # Adjust as needed for the control descriptions
		y_start = 100
		line_height = 30

		for i, (control, description) in enumerate(controls_text_lines):
			# Control names in the left column
			control_message = intro_font_15.render(control, True, (255, 255, 255))
			control_message_rect = control_message.get_rect(left=left_column_x, top=y_start + i*line_height)
			screen.blit(control_message, control_message_rect)
			
			# Control descriptions in the right column
			description_message = intro_font_15.render(description, True, (255, 255, 255))
			description_message_rect = description_message.get_rect(left=right_column_x, top=y_start + i*line_height)
			screen.blit(description_message, description_message_rect)


		# Display the player sprite on the right, but more towards the edge of the screen
		player_sprite_image = player.sprite.image
		# Adjust the position more to the right than before
		player_sprite_rect = player_sprite_image.get_rect(center=(800 - 130, 200))  # 100 pixels from the right edge
		screen.blit(player_sprite_image, player_sprite_rect)


		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				controls_screen = False

	
	elif introduction_screen:
		screen.blit(introduction_surface,(0,0))

		now = pygame.time.get_ticks()
		if (now - last_update > interval):
			if index1 < len(intro_line1.split()):
				index1 += 1
			elif index2 < len(intro_line2.split()):
				index2 += 1
			elif index3 < len(intro_line3.split()):
				index3 += 1
			elif index4 < len(intro_line4.split()):
				index4 += 1
			last_update = now

				
		blit_text(" ".join(intro_line1.split()[:index1]),intro_font_15,255,255,255,(400,150))
		blit_text(" ".join(intro_line2.split()[:index2]),intro_font_15,255,255,255,(400,190))
		blit_text(" ".join(intro_line3.split()[:index3]),intro_font_15,255,255,255,(400,230))
		blit_text(" ".join(intro_line4.split()[:index4]),intro_font_15,255,255,255,(400,270))
		blit_text("ENTER to continue",intro_font_15,255,255,255,(700,350))

	elif demented_screen:
		screen.blit(introduction_surface,(0,0))

		now = pygame.time.get_ticks()
		if (now - demented_last_update > demented_interval):
			if demented_index1 < len(demented_line1.split()):
				demented_index1 += 1
			elif demented_index2 < len(demented_line2.split()):
				demented_index2 += 1
			elif demented_index3 < len(demented_line3.split()):
				demented_index3 += 1
			demented_last_update = now

		blit_text(" ".join(demented_line1.split()[:demented_index1]), intro_font_15, 255, 255, 255, (400, 150))
		blit_text(" ".join(demented_line2.split()[:demented_index2]), intro_font_15, 255, 255, 255, (400, 190))
		blit_text(" ".join(demented_line3.split()[:demented_index3]), intro_font_15, 255, 255, 255, (400, 230))
		blit_text("Press Enter to Play Again", intro_font_15, 255, 255, 255, (650, 350))

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				# Reset player's position and mana
				player.sprite.rect.midbottom = (80, 300)  # Reset position
				player.sprite.mana = player.sprite.max_mana  # Refill mana

				# Clear obstacles and projectiles
				obstacle_group.empty()
				projectile_group.empty()

				# Reset score and timers
				score = 0
				start_time = int(pygame.time.get_ticks() / 1000)  # Reset game start time
				total_pause = 0  # Reset total pause time

				# Reset obstacle spawn timing and counters
				obstacle_interval = 1200  # Reset to initial obstacle spawn interval
				obstacle_count = 0
				pygame.time.set_timer(obstacle_timer, obstacle_interval)

				# Reset any additional game state variables
				game_active = False  # Or True, depending on your game's flow
				introduction_screen = True  # Or another appropriate state
				trivia_screen = False
				demented_screen = False

				# Reset the animation indexes for the demented screen
				demented_index1 = 0
				demented_index2 = 0
				demented_index3 = 0
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

	