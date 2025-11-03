import pygame

class ObjetoColisao:
    def __init__(self, imagem, x, y):
        self.imagem = pygame.image.load(imagem).convert_alpha()
        self.rect = self.imagem.get_rect(topleft=(x, y))

    def desenhar(self, tela, camera_x, camera_y):
        tela.blit(self.imagem, (self.rect.x - camera_x, self.rect.y - camera_y))
