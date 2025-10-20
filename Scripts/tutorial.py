import pygame
import math #usei pra oscilar o efeito de boiar

def executar_tutorial(jogo):
    """Tela de tutorial / início, chamada a partir do jogo principal."""
    jogo.tela.fill((0, 0, 0))
    
    area_visivel = pygame.Rect(jogo.camera_x, jogo.camera_y, jogo.largura, jogo.altura)
    jogo.tela.blit(jogo.imagem_limite_teste, (0, 0), area_visivel)

    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - jogo.ultimo_frame_troca > jogo.tempo_animacao:
        jogo.frame_atual = (jogo.frame_atual + 1) % len(jogo.frames_personagem)
        jogo.ultimo_frame_troca = tempo_atual
    amplitude = 8  
    frequencia = 0.0017  
    
    deslocamento_y = amplitude * math.sin(tempo_atual * frequencia)
    
    pos_x, pos_y = jogo.pos_personagem
    pos_y_animado = pos_y + deslocamento_y

    frame = jogo.frames_personagem[jogo.frame_atual]
    rect = frame.get_rect(center=(pos_x, pos_y_animado))
    jogo.tela.blit(frame, rect)

    jogo.tutorial = "durante"