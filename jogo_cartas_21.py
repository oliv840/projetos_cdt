import pygame
import random

pygame.init()

# Cores e dimensões
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 128, 0)
CINZA = (200, 200, 200)
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Blackjack 21 (com animações)")

clock = pygame.time.Clock()

# ------------ Classes ------------
class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
    def __str__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = []
        self._criar_e_embaralhar()

    def _criar_e_embaralhar(self):
        self.cartas.clear()
        valores = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        naipes = ['Copas','Espadas','Ouros','Paus']
        for naipe in naipes:
            for valor in valores:
                self.cartas.append(Carta(valor, naipe))
        random.shuffle(self.cartas)

    def distribuir(self):
        if not self.cartas:
            self._criar_e_embaralhar()
        return self.cartas.pop()

class Mao:
    def __init__(self):
        self.cartas = []
        self.valor = 0
        self.ases = 0

    def adicionar(self, carta):
        self.cartas.append(carta)
        if carta.valor.isdigit():
            self.valor += int(carta.valor)
        elif carta.valor in ['J','Q','K']:
            self.valor += 10
        else:  # Ás
            self.valor += 11
            self.ases += 1
        while self.valor > 21 and self.ases:
            self.valor -= 10
            self.ases -= 1

    def __str__(self):
        return ", ".join(str(c) for c in self.cartas)

# ------------ Carregamento de Imagens ------------
def carregar_imagem_carta(carta):
    path = f"cartas/{carta.valor}_{carta.naipe}.png"
    return pygame.image.load(path).convert_alpha()

imagem_verso = pygame.image.load("cartas/verso.png").convert_alpha()

# ------------ Desenho na Tela ------------
def desenhar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)
    surface = fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(x, y))
    tela.blit(surface, rect)

def desenhar_cartas(mao, y, esconder_primeira=False):
    x = 150
    for i, carta in enumerate(mao.cartas):
        img = imagem_verso if i==0 and esconder_primeira else carregar_imagem_carta(carta)
        img = pygame.transform.scale(img, (100, 150))
        tela.blit(img, (x, y))
        x += 120

def desenhar_botao(ret, texto, ativo=True):
    mouse = pygame.mouse.get_pos()
    cor = (170,170,170) if ativo else (120,120,120)
    if ret.collidepoint(mouse) and ativo:
        cor = (210,210,210)
    pygame.draw.rect(tela, cor, ret, border_radius=10)
    desenhar_texto(texto, 30, PRETO, ret.centerx, ret.centery)

# ------------ Lógica e Estados ------------
def iniciar_jogo():
    global baralho, mao_jogador, mao_dealer, estado_jogo, mensagem
    baralho = Baralho()
    mao_jogador = Mao()
    mao_dealer = Mao()
    estado_jogo = "jogando"
    mensagem = ""
    for _ in range(2):
        mao_jogador.adicionar(baralho.distribuir())
        mao_dealer.adicionar(baralho.distribuir())
    if mao_jogador.valor == 21:
        estado_jogo = "manter"

# Função simples de animação (cartas deslizam)
def animar_carta(carta, x1, y1, x2, y2, duração=400):
    start = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()
        t = min((now - start) / duração, 1)
        x = x1 + (x2 - x1)*t
        y = y1 + (y2 - y1)*t
        tela.fill(VERDE)
        desenhar_cartas(mao_jogador, 320)
        desenhar_cartas(mao_dealer, 70, esconder_primeira=True)
        img = carregar_imagem_carta(carta)
        img = pygame.transform.scale(img, (100, 150))
        tela.blit(img, (x, y))
        pygame.display.flip()
        clock.tick(60)
        if t >= 1:
            break

# ------------ Estados da Tela ------------
estado_tela = "menu"
botao_iniciar = pygame.Rect(LARGURA/2-100, ALTURA/2, 200, 60)

rodando = True
while rodando:
    tela.fill(VERDE)

    if estado_tela == "menu":
        desenhar_texto("Blackjack 21", 60, BRANCO, LARGURA/2, ALTURA/2 - 100)
        desenhar_botao(botao_iniciar, "Iniciar Jogo")
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if botao_iniciar.collidepoint(e.pos):
                    iniciar_jogo()
                    estado_tela = "jogo"

    elif estado_tela == "jogo":
        # Evento e lógica simplificada
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and estado_jogo == "jogando":
                if botao_pedir.collidepoint(e.pos):
                    carta = baralho.distribuir()
                    animar_carta(carta, -100, ALTURA/2, 150 + len(mao_jogador.cartas)*120, 320)
                    mao_jogador.adicionar(carta)
                    if mao_jogador.valor > 21:
                        estado_jogo = "manter"
                if botao_manter.collidepoint(e.pos):
                    estado_jogo = "manter"

        if estado_jogo == "manter":
            while mao_dealer.valor < 17:
                pygame.time.delay(500)
                carta = baralho.distribuir()
                animar_carta(carta, LARGURA+100, ALTURA/2, 150 + len(mao_dealer.cartas)*120, 70)
                mao_dealer.adicionar(carta)
            if mao_jogador.valor > 21:
                mensagem = "Você estourou! Dealer vence."
            elif mao_dealer.valor > 21:
                mensagem = "Dealer estourou! Você vence!"
            elif mao_jogador.valor > mao_dealer.valor:
                mensagem = "Você vence!"
            elif mao_jogador.valor < mao_dealer.valor:
                mensagem = "Você perdeu!"
            else:
                mensagem = "Empate!"
            estado_jogo = "fim"

        # Desenho
        desenhar_texto("Dealer", 35, BRANCO, 100, 50)
        desenhar_cartas(mao_dealer, 70, esconder_primeira=(estado_jogo!="fim"))
        if estado_jogo == "fim":
            desenhar_texto(f"Valor Dealer: {mao_dealer.valor}", 30, BRANCO, LARGURA/2, 250)

        desenhar_texto("Jogador", 35, BRANCO, 100, 300)
        desenhar_cartas(mao_jogador, 320)
        desenhar_texto(f"Sua Pontuação: {mao_jogador.valor}", 30, BRANCO, LARGURA/2, 500)

        if estado_jogo == "jogando":
            botao_pedir = pygame.Rect(LARGURA/2 - 160, ALTURA - 100, 150, 50)
            botao_manter = pygame.Rect(LARGURA/2 + 10, ALTURA - 100, 150, 50)
            desenhar_botao(botao_pedir, "Pedir Carta")
            desenhar_botao(botao_manter, "Manter")

    elif estado_tela == "fim":
        desenhar_texto("Fim de Jogo", 60, BRANCO, LARGURA/2, 150)
        desenhar_texto(mensagem, 40, BRANCO, LARGURA/2, 250)
        desenhar_texto(f"Você: {mao_jogador.valor}", 30, BRANCO, LARGURA/2, 320)
        desenhar_texto(f"Dealer: {mao_dealer.valor}", 30, BRANCO, LARGURA/2, 360)
        desenhar_cartas(mao_dealer, 70, False)
        desenhar_cartas(mao_jogador, 320, False)
        botao_voltar = pygame.Rect(LARGURA/2 - 100, ALTURA - 100, 200, 50)
        desenhar_botao(botao_voltar, "Menu")
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                rodando = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if botao_voltar.collidepoint(e.pos):
                    estado_tela = "menu"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
