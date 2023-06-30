"""
Ferramenta de desenho para projeção interativa - versão com "edge detection" de webcam

Daniel Seda e Alexandre Villares para Menos 1 invisível
Espetáculo Sankofa - Sesc Av. Paulista - abril de 2023

TODO:
OK - Apagar transicionando
OK - Carregar SVG das adinkras
OK - Interface de teclado para selecionar adinkra
OK - Scroll wheel muda o tamanho

OK - Clique carimba adinkra corrente

- ligar e desligar o stroke
- Apagamento move material para uma layer mais abaixo e atua apenas na layer mais abaixo.
- Enquando desenho acontece em layer transparente por cima.

"""
simbolo = 1
simbolo_size = 150
cor = 255
cor_fundo = 0
fade = 0
drag_stroke = False

cores = (
    color(0),
    color(255),
    color(100),
    color(200),
    color(200, 0, 200),
    color(0, 200, 200),
    color(200, 200, 0),
    color(200, 0, 0),
    color(0, 0, 200),
    color(0, 200, 0),
)    

def setup():
    global layer0
    #size(800, 600)
    full_screen()
    no_cursor()
    shape_mode(CENTER)
    frame_rate(30)
    layer0 = create_graphics(width, height)
    layer0.begin_draw()
    layer0.clear()
    layer0.shape_mode(CENTER)
    layer0.end_draw()
    carrega_adinkras()
    
    
def draw():
    global fade
    background(255)
    image(layer0, 0, 0)
    
    
    fill(cor)
    if simbolo is not None:
        shape(adinkras[simbolo],
              mouse_x, mouse_y,
              simbolo_size, simbolo_size)
    else:
        circle(mouse_x, mouse_y, 20)

    if fade and frame_count % 15 == 0:
        layer0.begin_draw()
        layer0.fill(cor_fundo, 32)
        layer0.rect(0, 0, width, height)
        layer0.end_draw()
        fade -= 1
        print(fade)
   

def key_pressed():
    global cor, cor_fundo, fade, simbolo, drag_stroke
    k = str(key)
    if k in '0123456789':
        cor = cores[int(k)]
    if k == ' ':
        cor_fundo = cor
        fade = 25
    if k in 'abcdefghijklmnopqrstuvwxyz':
        simbolo = ord(k) - 97
        if simbolo >= len(adinkras):
            simbolo = None
    elif k == "/":
        drag_stroke = not drag_stroke


def carrega_adinkras():
    global adinkras
    adinkras  = []
    data_folder = sketch_path('adinkras')  # este é um objeto pathlib.Path
    caminhos_arquivos = []
    for caminho_arquivo in data_folder.iterdir():  
        if caminho_arquivo.is_file() and caminho_arquivo.name.lower().endswith('svg'):
            caminhos_arquivos.append(caminho_arquivo)
    # Agora efetivamente carrega na memória cada imagem a partir dos caminhos
    # listados no passo anterior. Se alista estiver vazia não faz nada.
    for caminho_arquivo in caminhos_arquivos:
        shp = load_shape(str(caminho_arquivo))
        shp.disable_style()
        adinkras.append(shp)
        
def mouse_clicked():
    if simbolo is not None:
        layer0.begin_draw()
        layer0.fill(cor)
        layer0.shape(adinkras[simbolo], int(mouse_x), int(mouse_y),
                     simbolo_size, simbolo_size)
        layer0.end_draw()


def mouse_dragged():
    if simbolo is not None:
        layer0.begin_draw()
        layer0.push_style()
        layer0.fill(cor)
        if not drag_stroke:
            layer0.no_stroke()
        layer0.shape(adinkras[simbolo], int(mouse_x), int(mouse_y),
                     simbolo_size, simbolo_size)
        layer0.pop_style()
        layer0.end_draw()

        
        
def mouse_wheel(e):
    global simbolo_size
    simbolo_size += e.get_count() * 5
    
