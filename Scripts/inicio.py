import pygame
from pygame import *
import sys
import cv2
from tutorial import executar_tutorial
from transicoes import fade_in
from objetos import ObjetoColisao


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
        self.PRETO = (16, 23, 74)
        self.fonte = pygame.font.SysFont(None, 60)

        self.estado = "menu"
        self.rodando = True

        # --- Imagens principais ---
        self.imagem_menu = pygame.image.load("assets/imagens/menu03.11.2025.png")
        self.imagem_jogo = pygame.image.load("assets/imagens/relatorioProvisorio.png")
        self.imagem_inicio = pygame.image.load("assets/imagens/imagem3.png")
        self.imagem_limite_teste = pygame.image.load("assets/mapaQuadrantes/testemapa.png")
        self.imagemsonar = pygame.image.load("assets/equipamentos/sonar.png")

        # CAIXAS DE DIÁLOGO
        self.posicao_dialogo = 0
        self.caixadialogo1 = pygame.image.load("assets/elementos/caixadialogoteste.png")
        self.exibir_caixa_dialogo1 = False

        self.caixadialogo2 = pygame.image.load("assets/elementos/caixadialogo2.png")
        self.exibir_caixa_dialogo2 = False

        self.exibir_caixa_dialogo3 = False

        self.tutorial_exibido = False
        self.mostrar_texto_tutorial = True


        # TIMERS
        self.passou_sete_segundos = False
        self.inicio_timer = None 
        self.clock = pygame.time.Clock()

        # --- Texto ---
        self.texto_completo = (
            "Atualmente Cadete C-137 encontra-se na Via Láctea, "
            "em direção a um exoplaneta não identificado, estou em sua órbita "
            "coletando dados sobre, analisando a segurança do local e se há habitantes. "
            "Seguindo o planejamento da missão, tenho que coletar matéria prima em escassez "
            "no planeta Skebob. A priori esse sistema solar é muito semelhante ao nosso na questão de recursos. "
            "Ficarei rondando planeta por planeta desse sistema."
        )
        self.texto_mostrado = ""
        self.tempo_entre_caracteres = 30
        self.ultimo_tempo = pygame.time.get_ticks()

        self.texto_pressione_t_abrir_sonar = "Pressione T para abrir o equipamento Sonar"
        self.mostrar_texto_tutorial = True

        # --- Câmera ---
        self.camera_x = 1100
        self.camera_y = 1100
        self.velocidade_camera = 7
        self.largura_imagem = self.imagem_limite_teste.get_width()
        self.altura_imagem = self.imagem_limite_teste.get_height()
        self.virado_esquerda = True

        # --- PERSONAGEM ---
        self.frames_personagem = [
            pygame.image.load(f"assets/animacoes/frame{i}.png").convert_alpha() for i in range(1,6)
        ]
        self.frames_personagem_direita = [
            pygame.image.load(f"assets/animacoes/virado_direita/frame{i}_direita.png").convert_alpha() for i in range(1,6)
        ]
        self.frame_atual = 0
        self.tempo_animacao = 250  
        self.ultimo_frame_troca = pygame.time.get_ticks()
        self.pos_personagem = (self.largura // 2, self.altura // 2)

        # --- HITBOXES ---
        self.rect_personagem = pygame.Rect(self.pos_personagem[0], self.pos_personagem[1], 50, 80)

        # --- EQUIPAMENTOS ---
        self.sonarAberto = False

        # --- VINHETA ---
        self.vinheta_surface = self.criar_vinheta()

    def criar_vinheta(self):
        vinheta = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        centro_x, centro_y = self.largura // 2, self.altura // 2
        max_raio = max(self.largura, self.altura) // 2
        for y in range(self.altura):
            for x in range(self.largura):
                dx = x - centro_x
                dy = y - centro_y
                distancia = (dx**2 + dy**2)**0.5
                alpha = min(180, int(180 * (distancia / max_raio)))
                vinheta.set_at((x, y), (0, 0, 0, alpha))
        return vinheta

    def aplicar_vinheta(self):
        self.tela.blit(self.vinheta_surface, (0, 0))

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

                    if evento.key == pygame.K_RETURN and self.exibir_caixa_dialogo1:
                        self.exibir_caixa_dialogo1 = False
                        self.posicao_dialogo = 2
                        self.passou_sete_segundos = False  # Reset timer para próximo diálogo
                        self.inicio_timer = pygame.time.get_ticks()

                    if evento.key == pygame.K_RETURN and self.exibir_caixa_dialogo2:
                        self.exibir_caixa_dialogo2 = False

                    if evento.key == pygame.K_t:
                        self.sonarAberto = not self.sonarAberto
                        if not self.tutorial_exibido:
                            self.mostrar_texto_tutorial = True
                            self.tutorial_exibido = True
                        else:
                            self.mostrar_texto_tutorial = False

        teclas = pygame.key.get_pressed()
        if self.estado == "iniciar":
            camera_x_ant = self.camera_x
            camera_y_ant = self.camera_y

            if teclas[pygame.K_LEFT]:
                self.camera_x -= self.velocidade_camera
                self.virado_esquerda = True
            if teclas[pygame.K_RIGHT]:
                self.camera_x += self.velocidade_camera
                self.virado_esquerda = False
            if teclas[pygame.K_UP]:
                self.camera_y -= self.velocidade_camera
            if teclas[pygame.K_DOWN]:
                self.camera_y += self.velocidade_camera

            for obj in getattr(self, "objetos", []):
                rect_obj_camera = obj.rect.move(-self.camera_x, -self.camera_y)
                if self.rect_personagem.colliderect(rect_obj_camera):
                    self.camera_x = camera_x_ant
                    self.camera_y = camera_y_ant
                    break

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

            # --- Atualiza texto letra por letra ---
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_tempo > self.tempo_entre_caracteres and len(self.texto_mostrado) < len(self.texto_completo):
                self.texto_mostrado += self.texto_completo[len(self.texto_mostrado)]
                self.ultimo_tempo = tempo_atual

            # --- Caixa de diálogo 1 ---
            if self.inicio_timer is None:
                self.inicio_timer = pygame.time.get_ticks()

            if not self.passou_sete_segundos and self.posicao_dialogo == 0:
                if pygame.time.get_ticks() - self.inicio_timer >= 7000:
                    self.exibir_caixa_dialogo1 = True
                    self.passou_sete_segundos = True

            if self.exibir_caixa_dialogo1:
                pos_x = (self.largura - self.caixadialogo1.get_width()) // 2
                pos_y = self.altura - self.caixadialogo1.get_height() - 30
                self.tela.blit(self.caixadialogo1, (pos_x, pos_y))

            # --- Caixa de diálogo 2 ---
            if not self.passou_sete_segundos and self.posicao_dialogo == 2:
                if pygame.time.get_ticks() - self.inicio_timer >= 7000:
                    self.exibir_caixa_dialogo2 = True
                    self.passou_sete_segundos = True

            if self.exibir_caixa_dialogo2:
                pos_x = (self.largura - self.caixadialogo2.get_width()) // 2
                pos_y = self.altura - self.caixadialogo2.get_height() - 30
                self.tela.blit(self.caixadialogo2, (pos_x, pos_y))

            # --- Tutorial e sonar ---
            if self.mostrar_texto_tutorial:
                texto_surface = self.fonte.render(self.texto_pressione_t_abrir_sonar, True, self.BRANCO)
                texto_rect = texto_surface.get_rect()
                texto_rect.bottomleft = (20, self.altura - 5)
                self.tela.blit(texto_surface, texto_rect)

            if self.sonarAberto:
                pos_x = (self.largura - self.imagemsonar.get_width()) // 2
                pos_y = self.altura - self.imagemsonar.get_height() - 30
                self.tela.blit(self.imagemsonar, (pos_x, pos_y))

            # --- VINHETA ---
            self.aplicar_vinheta()


    def tela_menu(self):
        self.tela.blit(self.imagem_menu, (0, 0))

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
