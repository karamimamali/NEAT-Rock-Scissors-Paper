import pygame
import random
import neat
import os
pygame.init()

wn_width = 1440
wn_height = 768
FPS = 60
BG_color = (10, 52, 59)
gen = 0
STAT_FONT = pygame.font.SysFont('calibri', 20)
HUNT_FONT = pygame.font.SysFont('calibri', 20)

pygame.display.set_caption('Platformer')

WN =  pygame.display.set_mode((wn_width, wn_height))

from classes import Unit

def collide_with_wall(rocks,scissors,papers,wn_height,wn_width):
    for unit in [*papers,*rocks,*scissors]:
        if unit.rect.y > wn_height - unit.rect.height:
            unit.rect.y = wn_height - unit.rect.height
        elif unit.rect.y < 0:
            unit.rect.y = 0
        
        if unit.rect.x < 0:
            unit.rect.x = 0
        elif unit.rect.x > wn_width - unit.rect.width:
            unit.rect.x = wn_width - unit.rect.width
    
        

def eval_genomes(genomes, config):
    global gen, WN
    WN = WN
    gen += 1

    rocks = []
    nets_r = []
    ge_r = []

    scissors = []
    nets_s = []
    ge_s = []

    papers = []
    nets_p = []
    ge_p = []

    time = 0
    i = 1
    for id, genome in genomes:
        if i <= 10:
            genome.fitness = 0 
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets_r.append(net)
            rocks.append(Unit('rock',random.randint(680,760),random.randint(1,200),32,32))
            ge_r.append(genome)
        elif i > 10 and i <= 20:
            genome.fitness = 0 
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets_s.append(net)
            scissors.append(Unit('scissors',random.randint(1100,1300),random.randint(400,700),32,32))
            ge_s.append(genome)
        elif i > 20 and i <= 30:
            genome.fitness = 0 
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets_p.append(net)
            papers.append(Unit('paper',random.randint(100,300),random.randint(400,700),32,32))
            ge_p.append(genome)
        i +=1

# You can simply comment the clock in order to train yout genomes faster.

    clock = pygame.time.Clock()
    Run = True
    while Run:
        clock.tick(FPS)
        time += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
                pygame.quit()
                quit()
                


        for x, unit in enumerate(papers):
            if len(rocks) != 0 or len(scissors) != 0:
                ge_p[x].fitness += 0.1
                near_unit, distance = unit.near_unit([*rocks,*scissors])
                if near_unit.type == 'rock':
                    type_par = 1
                else:
                    type_par = -1
                output = nets_p[papers.index(unit)].activate((distance,near_unit.rect.x,near_unit.rect.y,type_par))

                decision = output.index(max(output))
                

                if decision == 0:  
                    ge_p[x].fitness -= 1
                elif decision == 1:
                    
                    unit.up()
                elif decision == 2:
                   
                    unit.down()
                elif decision == 3:
                    
                    unit.left()
                elif decision == 4:
                    
                    unit.right()

                
                if pygame.sprite.spritecollideany(unit,rocks):
                    unit.hunted += 1
                    ge_p[x].fitness += 5
                if pygame.sprite.spritecollideany(unit,scissors):
                    ge_p[x].fitness -= 5
                    nets_p.pop(x)
                    ge_p.pop(x)
                    papers.pop(x)

        for x, unit in enumerate(scissors):
            if len(rocks) != 0 or len(papers) != 0:
                ge_s[x].fitness += 0.1
            
                near_unit, distance = unit.near_unit([*rocks,*papers])
                if near_unit.type == 'rock':
                    type_par = -1
                else:
                    type_par = 1
                    
                output = nets_s[scissors.index(unit)].activate((distance,near_unit.rect.x,near_unit.rect.y,type_par))


                decision = output.index(max(output))
            
                if decision == 0:  
                    ge_s[x].fitness -= 1
                elif decision == 1:
             
                    unit.up()
                elif decision == 2:
     
                    unit.down()
                elif decision == 3:
        
                    unit.left()
                elif decision == 4:
          
                    unit.right()

                if pygame.sprite.spritecollideany(unit,papers):
                    unit.hunted += 1
                    ge_s[x].fitness += 5
                if pygame.sprite.spritecollideany(unit,rocks):
                    ge_s[x].fitness -= 5
                    nets_s.pop(x)
                    ge_s.pop(x)
                    scissors.pop(x)


        for x, unit in enumerate(rocks):
            if len(papers) != 0 or len(scissors) != 0:
                ge_r[x].fitness += 0.1
                near_unit, distance = unit.near_unit([*scissors,*papers])
                if near_unit.type == 'paper':
                    type_par = -1
                else:
                    type_par = 1
                
                output = nets_r[rocks.index(unit)].activate((distance,near_unit.rect.x,near_unit.rect.y,type_par))

                decision = output.index(max(output))
                

                if decision == 0:  
                    ge_r[x].fitness -= 1
                elif decision == 1:
           
                    unit.up()
                elif decision == 2:
                  
                    unit.down()
                elif decision == 3:
             
                    unit.left()
                elif decision == 4:
            
                    unit.right()

                
                if pygame.sprite.spritecollideany(unit,scissors):
                    unit.hunted += 1
                    ge_r[x].fitness += 5
                if pygame.sprite.spritecollideany(unit,papers):
                    ge_r[x].fitness -= 5
                    nets_r.pop(x)
                    ge_r.pop(x)
                    rocks.pop(x)


        collide_with_wall(rocks,scissors,papers,wn_height,wn_width)

        WN.fill(BG_color)
        
        score_label = STAT_FONT.render("Rocks: " + str(len(rocks)),1,(255,255,255))
        WN.blit(score_label, (10, 10))

        score_label = STAT_FONT.render("Papers: " + str(len(papers)),1,(255,255,255))
        WN.blit(score_label, (10, 30))

        score_label = STAT_FONT.render("Scissors: " + str(len(scissors)),1,(255,255,255))
        WN.blit(score_label, (10, 50))

        score_label = STAT_FONT.render(f"Gen: {gen}",1,(255,255,255))
        WN.blit(score_label, (wn_width-score_label.get_width()-10, 10))

        
        for unit in [*papers,*rocks,*scissors]:
            score_label = HUNT_FONT.render(f"{unit.hunted}",1,(255,255,255))
            unit.draw(WN, score_label)         

        if len([*papers,*rocks,*scissors]) == 0 or 10 < time/FPS:
            break
        


        pygame.display.update()
        
        

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    #p = neat.Checkpointer.restore_checkpoint('gen-99')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100,filename_prefix="gen-"))

    winner = p.run(eval_genomes, 1000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)


