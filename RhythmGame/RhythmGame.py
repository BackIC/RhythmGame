import pygame, time, timeit, threading, copy, os

#Game Setting
FPS = 70
BGA_FPS = 23.98
WINDOW_WIDTH = 854
WINDOW_HEIGHT = 480
S_HEIGHT = WINDOW_HEIGHT - 50

SHOWN_TIME = 1500
SPEED_RATE = 1.5
EFFECT_TIME = 1000

SCORE_STRING = ["GREAT", " GOOD", " ALSO", " MISS", "COMBO", "SCORE"]
WHITE = [255, 255, 255]

#Game Variable
score_status = [0, 0, 0, 0]
score = 0
combo = 0
display_score = 0
effect_opacity = [0, 0, 0, 0, 0]

#Game Init
sounds = pygame.mixer
sounds.pre_init(44100, -16, 2, 512)
sounds.init()

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Rhythm Game')

#Load Images
noteImage = pygame.image.load("note.jpg")
noteImage = pygame.transform.scale(noteImage, (70, 5))
note_effect = pygame.image.load("note-effect.png").convert_alpha()
note_effect.set_alpha(125)
note_effect = pygame.transform.scale(note_effect, (70, 200))
all_note_list = pygame.sprite.Group()

#Load Chabo
dArray = []
display_chabo = []
readTurn = 0
f = open("note.txt", "r")
for line in f.readlines():
    if line[0] == '#':
        if (readTurn > 0):
            display_chabo.append(dArray)
            dArray = []
        readTurn = int(line[1])
        continue

    line = line.replace("\n", "")
    dArray.append(int(float(line) * 1000))
f.close()
display_chabo.append(dArray)
checking_chabo = copy.deepcopy(display_chabo)


#LoadBGA
bga_files = []
for file in os.listdir("bga"):
    bga_files.append(file)


def getRuntime(): 
    end = timeit.default_timer()
    runtime = int((end - start) * 1000)
    return runtime

class Note(pygame.sprite.Sprite):
    def __init__(self, time):
        super().__init__()
        self.s_Time = time
        self.image = noteImage
        self.width = 50
        self.rect = self.image.get_rect()

    def update(self):
        if(self.rect.y > WINDOW_HEIGHT):
            all_note_list.remove(self)
            return

            
        end = timeit.default_timer()
        runtime = int((end - start) * 1000)
        self.rect.y = WINDOW_HEIGHT - ((self.s_Time - getRuntime()) / (SHOWN_TIME / SPEED_RATE)) * S_HEIGHT - (WINDOW_HEIGHT - S_HEIGHT)

keys_status = [0, 0, 0, 0, 0]
class KeyReader(threading.Thread):
    def run(self):
        while running:
            end = timeit.default_timer()
            runtime = getRuntime()
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_f]:
                effect_opacity[0] = 255
                if(keys_status[0] == 0):
                    sounds.Sound("hihat.wav").play()
                    checkNote(runtime, 0)
                keys_status[0] = 1
            else:
                keys_status[0] = 0
            if keys[pygame.K_g]:
                effect_opacity[1] = 255
                if(keys_status[1] == 0):
                    sounds.Sound("hihat.wav").play()
                    checkNote(runtime, 1)
                keys_status[1] = 1
            else:
                keys_status[1] = 0
            if keys[pygame.K_h]:
                effect_opacity[2] = 255
                if(keys_status[2] == 0):
                    sounds.Sound("hihat.wav").play()
                    checkNote(runtime, 2)
                keys_status[2] = 1
            else:
                keys_status[2] = 0
            if keys[pygame.K_j]:
                effect_opacity[3] = 255
                if(keys_status[3] == 0):
                    sounds.Sound("hihat.wav").play()
                    checkNote(runtime, 3)
                keys_status[3] = 1
            else:
                keys_status[3] = 0
            if keys[pygame.K_k]:
                effect_opacity[4] = 255
                if(keys_status[4] == 0):
                    sounds.Sound("hihat.wav").play()
                    checkNote(runtime, 4)
                keys_status[4] = 1
            else:
                keys_status[4] = 0
            time.sleep(0.001)

def checkNote(time, key):
    global combo, score, score_status

    abs_min = 999999
    index_min = 0
    if len(checking_chabo[key]) > 0:
        try:
            for i in range(0, len(checking_chabo[key])):
                if abs(checking_chabo[key][i] - time) < abs_min:
                    abs_min = abs(checking_chabo[key][i] - time)
                    index_min = i
            if(abs_min < 80):
                if abs_min < 30:
                    score_status[0] = score_status[0] + 1
                    score = score + (combo * 0.01 + 1) * 300
                    combo = combo + 1
                elif abs_min < 50:
                    score_status[1] = score_status[1] + 1
               
                    score = score + (combo * 0.01 + 1) * 300
                    combo = combo + 1
                else:
                    score_status[2] = score_status[2] + 1
                    score = score + (combo * 0.01 + 1) * 300
                    combo = combo + 1

                checking_chabo[key].pop(index_min)
        except:
            pass
        
class ChaboReader(threading.Thread):
    def run(self):
        while running:
            for i in range(0, len(display_chabo)):
                if not len(display_chabo[i]) is 0:
                    end = timeit.default_timer()
                    runtime = int((end - start) * 1000)
                    temp = SHOWN_TIME / SPEED_RATE
                    if display_chabo[i][0] - temp <= runtime:
                        createNote(i, display_chabo[i][0])
                        display_chabo[i].pop(0)
            checkMiss()
            time.sleep(0.001)

def checkMiss():
    global combo, score_status

    for i in range(0, len(checking_chabo)):
        if(len(checking_chabo[i]) > 0):
            if checking_chabo[i][0] - getRuntime() <= -80:
                checking_chabo[i].pop(0)
                score_status[3] = score_status[3] + 1
                combo = 0

def createNote(line, time):
    note = Note(time)
    note.rect.x = 100 + noteImage.get_rect().width * line
    note.rect.y = 0
    all_note_list.add(note)

def blit_alpha(target, source, location, opacity):
    # build_alpha By http://www.nerdparadise.com/programming/pygameblitopacity
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

bgmImage = 0
prevNum = 0

def draw():
    global display_score, score_status, bgmImage, prevNum

    try: 
        #Clear Sreen
        screen.fill((0, 0, 0))

        bgaNum = int((getRuntime() / 1000) * BGA_FPS)
        if (str(bgaNum) + ".jpg") in bga_files:
            if prevNum == bgaNum:
                screen.blit(bgmImage, bgmImage.get_rect())
            else:
                bgmImage = pygame.image.load("bga\\" + str(bgaNum) + ".jpg")
                bgmImage = pygame.transform.scale(bgmImage, (WINDOW_WIDTH, WINDOW_HEIGHT))
                screen.blit(bgmImage, bgmImage.get_rect())
                prevNum = bgaNum

        all_note_list.update()
        all_note_list.draw(screen)

        #Draw Lines And Key Boxes
        pygame.draw.line(screen, WHITE, [100 + noteImage.get_rect().width * 0, 0], [100 + noteImage.get_rect().width * 0, WINDOW_HEIGHT], 4)
        for i in range(1, 5):
            pygame.draw.line(screen, WHITE, [100 + noteImage.get_rect().width * i, 0], [100 + noteImage.get_rect().width * i,WINDOW_HEIGHT], 2)
        pygame.draw.line(screen, WHITE, [100 + noteImage.get_rect().width * 5, 0], [100 + noteImage.get_rect().width * 5,WINDOW_HEIGHT], 4)
        
        pygame.draw.line(screen, WHITE, [100, S_HEIGHT], [100 + noteImage.get_rect().width * 5, S_HEIGHT], 2)
        for i in range(0, 5):
            keyBox = pygame.Rect(100 + noteImage.get_rect().width * i + 2, S_HEIGHT + 2, noteImage.get_rect().width - 2, WINDOW_HEIGHT - S_HEIGHT - 2)
            if i % 2 == 0:
                pygame.draw.rect(screen, [255,107,108], keyBox)
            else:
                pygame.draw.rect(screen, [51,134,238], keyBox)

        #NoteEffect Drawer
        for i in range(0, len(effect_opacity)):
            if not effect_opacity[i] == 1:
                if effect_opacity[i] -30 >= 0:
                    effect_opacity[i] = effect_opacity[i] - 30
                    blit_alpha(screen, note_effect, (100 + note_effect.get_rect().width * i, 155 + 75), effect_opacity[i])
                else:
                    effect_opacity[i] = 0
                    blit_alpha(screen, note_effect, (100 + note_effect.get_rect().width * i, 155 + 75), effect_opacity[i])

        #Label Drawer
        myfont = pygame.font.SysFont("Dotum", 25)

        if display_score < int(score):
            display_score = display_score + 20

        totalHit = score_status[0] + score_status[1] + score_status[2] + score_status[3] + 0.0001
        for i in range(0, 4):
            label = myfont.render(SCORE_STRING[i] , 1, WHITE)
            screen.blit(label, (500, 100 + i * 50))
            label = myfont.render(str(score_status[i]) + "    ( " + str(int(score_status[i] / totalHit * 100)) + "% )", 1, WHITE)
            screen.blit(label, (600, 100 + i * 50))

        label = myfont.render(SCORE_STRING[4], 1, WHITE)
        screen.blit(label, (500, 300))
        label = myfont.render(str(combo), 1, WHITE)
        screen.blit(label, (600, 300))
        label = myfont.render(SCORE_STRING[5], 1, WHITE)
        screen.blit(label, (500, 350))
        label = myfont.render(str(int(display_score)), 1, WHITE)
        screen.blit(label, (600, 350))

        pygame.display.flip()
    except:
        pass


running = True
sounds.Sound("bgm.wav").play()
clock = pygame.time.Clock()
start = timeit.default_timer()
KeyReader().start()
ChaboReader().start()

while running:
    clock.tick(FPS)

    eventList = pygame.event.get()
    for event in eventList:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit() 
            break
    draw()
exit()