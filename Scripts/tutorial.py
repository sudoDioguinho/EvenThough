import pygame
import math #usei pra oscilar o efeito de boiar
from objetos import ObjetoColisao

class ObjetoColisao:
    def __init__(self, imagem, x, y):
        self.imagem = pygame.image.load(imagem).convert_alpha()
        self.rect = self.imagem.get_rect(topleft=(x, y))

    def desenhar(self, tela, camera_x, camera_y):
        tela.blit(self.imagem, (self.rect.x - camera_x, self.rect.y - camera_y))

def executar_tutorial(jogo):
    """Tela de tutorial / início, chamada a partir do jogo principal."""
    jogo.tela.fill((0, 0, 0))
    
    # --- Desenha o mapa ---
    area_visivel = pygame.Rect(jogo.camera_x, jogo.camera_y, jogo.largura, jogo.altura)
    jogo.tela.blit(jogo.imagem_limite_teste, (0, 0), area_visivel)

    if not hasattr(jogo, "objetos"):
        jogo.objetos = [
            ObjetoColisao("assets/imagens/rocha.png", 600, 600),
            #ObjetoColisao("assets/mapaQuadrantes/borda2.png", 500, 0),
           # ObjetoColisao("assets/mapaQuadrantes/borda.png", 0, 500),
            #ObjetoColisao("assets/mapaQuadrantes/borda2.png", 1460, 0),
            #ObjetoColisao("assets/mapaQuadrantes/borda.png", 0, 7000),
            ObjetoColisao("assets/mapa_hitboxes/testechaocaverna.png", 0,650),
            ObjetoColisao("assets/mapa_hitboxes/testechaocaverna.png", 0,2750),
            ObjetoColisao("assets/mapa_hitboxes/testeparedeesquerdacaverna.png", -600,800),
            ObjetoColisao("assets/mapa_hitboxes/testeparedeesquerdacaverna.png", 6000,800),
        ]

    for obj in jogo.objetos:
        obj.desenhar(jogo.tela, jogo.camera_x, jogo.camera_y)

    # --- Atualiza animação do personagem ---
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - jogo.ultimo_frame_troca > jogo.tempo_animacao:
        jogo.frame_atual = (jogo.frame_atual + 1) % len(jogo.frames_personagem)
        jogo.ultimo_frame_troca = tempo_atual
    amplitude = 14  
    frequencia = 0.0035  
    deslocamento_y = amplitude * math.sin(tempo_atual * frequencia)
    
    pos_x, pos_y = jogo.pos_personagem
    pos_y_animado = pos_y + deslocamento_y

    if jogo.virado_esquerda:
        frame = jogo.frames_personagem[jogo.frame_atual]
    else:
        frame = jogo.frames_personagem_direita[jogo.frame_atual]

    rect = frame.get_rect(center=(pos_x, pos_y_animado))
    jogo.rect_personagem.topleft = rect.topleft  # atualiza hitbox

    # --- Por fim, desenha o personagem por cima de tudo ---
    jogo.tela.blit(frame, rect)

    jogo.tutorial = "durante"
