import pygame

def fade_in(jogo, duracao_ms):
    """Transição suave do preto até o jogo visível."""
    fade_surface = pygame.Surface((jogo.largura, jogo.altura))
    fade_surface.fill((0, 0, 0))
    fade_surface.set_alpha(255)

    clock = pygame.time.Clock()
    tempo_inicio = pygame.time.get_ticks()

    from tutorial import executar_tutorial  

    rodando = True
    while rodando:
        agora = pygame.time.get_ticks()
        decorrido = agora - tempo_inicio
        alpha = max(255 - int((decorrido / duracao_ms) * 255), 0)
        fade_surface.set_alpha(alpha)

        jogo.processar_eventos()

        executar_tutorial(jogo)

        jogo.tela.blit(fade_surface, (0, 0))
        pygame.display.flip()

        if alpha == 0:
            rodando = False

        clock.tick(60)
