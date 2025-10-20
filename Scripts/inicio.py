import pygame
import sys
import cv2
from tutorial import executar_tutorial
from transicoes import fade_in

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.largura, self.altura = 1920, 1080
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Inicio")

        self.musica_menu = pygame.mixer.Sound("assets/audios/musica_menu.mp3")
        self.musica_menu.play()

        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.fonte = pygame.font.SysFont(None, 60)

        self.estado = "menu"
        self.rodando = True

        # --- Imagens principais ---
        self.imagem_menu = pygame.image.load("assets/imagens/telaMenu.png")
        self.imagem_jogo = pygame.image.load("assets/imagens/relatorioProvisorio.png")
        self.imagem_inicio = pygame.image.load("assets/imagens/imagem3.png")
        self.imagem_limite_teste = pygame.image.load("assets/imagens/mapa5.png")

        self.clock = pygame.time.Clock()

        # --- Texto ---
        self.texto_completo = "Atualmente Cadete C-137 encontra-se na Via Láctea, em direção a um exoplaneta não identificado..."
        self.texto_mostrado = ""
        self.tempo_entre_caracteres = 60
        self.ultimo_tempo = pygame.time.get_ticks()

        # --- Câmera ---
        self.camera_x = 0
        self.camera_y = 0
        self.velocidade_camera = 2
        self.largura_imagem = self.imagem_limite_teste.get_width()
        self.altura_imagem = self.imagem_limite_teste.get_height()

        # --- PERSONAGEM ---
        self.frames_personagem = [
            pygame.image.load("assets/animacoes/frame1.png").convert_alpha(),
            pygame.image.load("assets/animacoes/frame2.png").convert_alpha(),
            pygame.image.load("assets/animacoes/frame3.png").convert_alpha(),
            pygame.image.load("assets/animacoes/frame4.png").convert_alpha(),
            pygame.image.load("assets/animacoes/frame5.png").convert_alpha()
            
        ]
        self.frame_atual = 0
        self.tempo_animacao = 250  
        self.ultimo_frame_troca = pygame.time.get_ticks()
        self.pos_personagem = (self.largura // 2, self.altura // 2)

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

                elif self.estado == "iniciar":
                    if evento.key == pygame.K_ESCAPE:
                        self.estado = "menu"

        # --- Movimentação da câmera no tutorial ---
        teclas = pygame.key.get_pressed()
        if self.estado == "iniciar":
            if teclas[pygame.K_LEFT]:
                self.camera_x -= self.velocidade_camera
            if teclas[pygame.K_RIGHT]:
                self.camera_x += self.velocidade_camera
            if teclas[pygame.K_UP]:
                self.camera_y -= self.velocidade_camera
            if teclas[pygame.K_DOWN]:
                self.camera_y += self.velocidade_camera

            self.camera_x = max(0, min(self.camera_x, self.largura_imagem - self.largura))
            self.camera_y = max(0, min(self.camera_y, self.altura_imagem - self.altura))

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
            executar_tutorial(self)  

    def tela_menu(self):
        self.tela.blit(self.imagem_menu, (0, 0))
        textoJogar = self.fonte.render("Jogar - Enter", True, self.BRANCO)
        self.tela.blit(textoJogar, (800, 350))
        textoSair = self.fonte.render("Sair - Esc", True, self.BRANCO)
        self.tela.blit(textoSair, (820, 600))

    def tela_jogo(self):
        self.tela.blit(self.imagem_jogo, (0, 0))

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_tempo > self.tempo_entre_caracteres and len(self.texto_mostrado) < len(self.texto_completo):
            self.texto_mostrado += self.texto_completo[len(self.texto_mostrado)]
            self.ultimo_tempo = tempo_atual

        palavras = self.texto_mostrado.split(" ")
        linhas = []
        linha_atual = ""
        limite_largura = self.largura - 100

        for palavra in palavras:
            teste_linha = linha_atual + palavra + " "
            largura_teste, _ = self.fonte.size(teste_linha)
            if largura_teste < limite_largura:
                linha_atual = teste_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual)

        y = 250
        for linha in linhas:
            texto = self.fonte.render(linha.strip(), True, self.BRANCO)
            self.tela.blit(texto, (50, y))
            y += self.fonte.get_height() + 10

    def roda_cutscene(self):
        cap = cv2.VideoCapture("assets/vídeos/cutscene.mp4")
        print("passou pelo video")
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
        fade_in(self, duracao_ms=3000)
        self.estado = "iniciar"


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
