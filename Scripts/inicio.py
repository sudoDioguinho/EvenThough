import pygame
import sys
import cv2

class Jogo:
    def __init__(self):
        pygame.init()
        self.largura, self.altura = 1920, 1080
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Inicio")

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.fonte = pygame.font.SysFont(None, 60)

        self.estado = "menu"
        self.rodando = True
        self.tutorial = False

        self.imagem_menu = pygame.image.load("assets/imagens/vermeiopng.png")
        self.imagem_jogo = pygame.image.load("assets/imagens/imagem2.png")
        self.imagem_inicio = pygame.image.load("assets/imagens/naveteste.png")

        self.clock = pygame.time.Clock()

    def executar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar_tela()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            elif evento.type == pygame.KEYDOWN:
                if self.estado == "menu":
                    if evento.key == pygame.K_RETURN:
                        self.estado = "jogo"
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado = "saiu"

                elif self.estado == "jogo":
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"
                    elif evento.key == pygame.K_RETURN:
                        self.estado = "cutscene"

    def atualizar_tela(self):
        if self.estado == "menu":
            self.tela_menu()
        elif self.estado == "saiu":
            self.rodando = False
        elif self.estado == "jogo":
            self.tela_jogo()
        elif self.estado == "cutscene":
            self.roda_cutscene()
        elif self.estado == "iniciar":
            self.inicio1()

    def tela_menu(self):
        self.tela.blit(self.imagem_menu, (0, 0))
        texto = self.fonte.render("MENU - Pressione ENTER", True, self.PRETO)
        self.tela.blit(texto, (100, 250))

    def tela_jogo(self):
        self.tela.blit(self.imagem_jogo, (0, 0))
        texto = self.fonte.render("TELA DE JOGO - ENTER para jogar, ESC para sair", True, self.BRANCO)
        self.tela.blit(texto, (50, 250))

    def roda_cutscene(self):
        cap = cv2.VideoCapture("assets/vídeos/video_1920x19080.mp4")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            self.tela.blit(frame, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        cap.release()
        self.estado = "iniciar"

    def inicio1(self):
        self.tutorial = True
        self.tela.blit(self.imagem_inicio, (0, 0))


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
