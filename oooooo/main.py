import sys
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QPen, QColor, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QTextBrowser,
)

# CONCEITOS COM SUPORTE A IMAGENS DE EXEMPLO
# Dica: Você pode colocar o caminho de uma imagem local (ex: "imagens/classe.png") 
# ou uma URL na tag <img>.
CONCEITOS = {
    "Classe": r"""
        <h2>Classe</h2>
        <p>Uma classe representa um conjunto de objetos com características e comportamentos em comum.</p>
        <h3>Exemplo Visual</h3>
        <p><i>(Substitua o caminho abaixo pela sua imagem de exemplo)</i></p>
        <img src="C:\Users\Mathe\OneDrive\Documentos\oooooo\imagens_exemplo\imagem exemplo classe.png" width="220" style="border-radius: 4px;">
        <h3>Quando utilizar?</h3>
        <p>Quando precisar representar uma entidade do sistema com dados e comportamentos.</p>
    """,

    "Associação": r"""
        <h2>Associação</h2>
        <p>Representa um relacionamento estrutural entre classes.</p>
        <h3>Exemplo Visual</h3>
        <img src="C:/caminho/para/sua/imagem_associacao.png" width="220" style="border-radius: 4px;">
        <h3>Quando utilizar?</h3>
        <p>Quando objetos de classes diferentes precisam se relacionar.</p>
    """,

    "Herança": r"""
        <h2>Herança (Generalização)</h2>
        <p>Representa uma generalização: uma classe específica herda características de uma classe mais geral.</p>
        <h3>Exemplo Visual</h3>
        <img src="C:/caminho/para/sua/imagem_heranca.png" width="220" style="border-radius: 4px;">
    """,

    "Agregação": r"""
        <h2>Agregação</h2>
        <p>É uma relação todo-parte em que a parte pode continuar existindo independentemente do todo.</p>
        <h3>Exemplo Visual</h3>
        <img src="C:/caminho/para/sua/imagem_agregacao.png" width="220" style="border-radius: 4px;">
        <h3>Notação UML</h3>
        <p>Losango vazio no lado do todo.</p>
    """,

    "Composição": r"""
        <h2>Composição</h2>
        <p>É uma relação todo-parte forte, na qual o todo controla o ciclo de vida das partes.</p>
        <h3>Exemplo Visual</h3>
        <img src="C:/caminho/para/sua/imagem_composicao.png" width="220" style="border-radius: 4px;">
        <h3>Notação UML</h3>
        <p>Losango preenchido no lado do todo.</p>
    """,

    "Interface": r"""
        <h2>Interface</h2>
        <p>Define um contrato com operações que uma classe pode implementar.</p>
        <h3>Exemplo Visual</h3>
        <img src="C:/caminho/para/sua/imagem_interface.png" width="220" style="border-radius: 4px;">
    """,

    "Classe abstrata": r"""
        <h2>Classe Abstrata</h2>
        <p>É uma classe que não pode ser instanciada diretamente e serve como modelo base.</p>
        <h3>Exemplo Visual</h3>
        <img src="C:/caminho/para/sua/imagem_abstrata.png" width="220" style="border-radius: 4px;">
    """
}


class TelaCaptura(QWidget):
    """Janela translúcida para selecionar uma área da tela arrastando o mouse."""
    def __init__(self, callback_concluido):
        super().__init__()
        self.callback_concluido = callback_concluido
        self.inicio = QPoint()
        self.fim = QPoint()
        self.selecionando = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.showFullScreen()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

        if self.selecionando:
            rect = QRect(self.inicio, self.fim).normalized()
            painter.setPen(QPen(QColor(53, 105, 184), 2, Qt.PenStyle.SolidLine))
            painter.setBrush(QColor(255, 255, 255, 30))
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.inicio = event.position().toPoint()
            self.fim = self.inicio
            self.selecionando = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.selecionando:
            self.fim = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selecionando = False
            rect = QRect(self.inicio, self.fim).normalized()
            self.close()
            
            if rect.width() > 10 and rect.height() > 10:
                tela = QGuiApplication.primaryScreen()
                screenshot = tela.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
                self.callback_concluido(screenshot)
            else:
                self.callback_concluido(None)


class TutorUML(QWidget):
    def __init__(self):
        super().__init__()

        self.expandido = False
        self.posicao_mouse = None

        self.setWindowTitle("Tutor UML - Inspetor & Recorte")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.resize(64, 64)
        self.setMinimumSize(64, 64)

        self.setStyleSheet("""
            QWidget {
                background-color: #202633;
                color: #ffffff;
                font-family: Arial;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3569b8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #4b83d8;
            }
            QTextBrowser {
                background-color: #f5f7fa;
                color: #202633;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        self.criar_interface()
        self.mostrar_icone()

    def criar_interface(self):
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(6, 6, 6, 6)
        self.layout_principal.setSpacing(8)

        # Cabeçalho para arrastar
        self.cabecalho = QFrame()
        layout_cabecalho = QHBoxLayout(self.cabecalho)
        layout_cabecalho.setContentsMargins(0, 0, 0, 0)

        self.titulo = QLabel("Tutor UML")
        self.titulo.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.botao_recolher = QPushButton("—")
        self.botao_recolher.setFixedSize(32, 30)
        self.botao_recolher.clicked.connect(self.mostrar_icone)

        self.botao_fechar = QPushButton("X")
        self.botao_fechar.setFixedSize(32, 30)
        self.botao_fechar.clicked.connect(self.close)

        layout_cabecalho.addWidget(self.titulo)
        layout_cabecalho.addStretch()
        layout_cabecalho.addWidget(self.botao_recolher)
        layout_cabecalho.addWidget(self.botao_fechar)

        # Botão de Recorte de Tela
        self.botao_capturar = QPushButton("🔍 Recortar Símbolo da Tela")
        self.botao_capturar.clicked.connect(self.iniciar_recorte)

        # Grade de Botões Manuais (para escolher direto se preferir)
        self.painel_botoes = QWidget()
        self.grid_botoes = QGridLayout(self.painel_botoes)
        self.grid_botoes.setContentsMargins(0, 0, 0, 0)
        self.grid_botoes.setSpacing(4)

        coluna = 0
        linha = 0
        for conceito in CONCEITOS.keys():
            btn = QPushButton(conceito)
            btn.clicked.connect(lambda checked=False, c=conceito: self.atualizar_explicacao(c))
            self.grid_botoes.addWidget(btn, linha, coluna)
            coluna += 1
            if coluna > 1:  # 2 colunas
                coluna = 0
                linha += 1

        # Caixa de texto de explicações (Suporta HTML + Imagens)
        self.explicacao = QTextBrowser()
        self.explicacao.setOpenExternalLinks(True)

        self.layout_principal.addWidget(self.cabecalho)
        self.layout_principal.addWidget(self.botao_capturar)
        self.layout_principal.addWidget(self.painel_botoes)
        self.layout_principal.addWidget(self.explicacao)

        self.atualizar_explicacao("Classe")

    def iniciar_recorte(self):
        self.hide()
        self.tela_captura = TelaCaptura(self.processar_recorte)

    def processar_recorte(self, pixmap):
        self.show()
        self.raise_()

        if not pixmap:
            return

        # Aqui você seleciona qual conceito exibir após o recorte ou faz a lógica de reconhecimento
        # Exemplo simulando que ao recortar, exibe a "Classe" e avisa que o print foi feito:
        self.atualizar_explicacao("Classe")
        self.explicacao.append("<br><hr><p style='color: #3569b8; font-size: 11px;'><i>[Área recortada e carregada com sucesso!]</i></p>")

    def mostrar_icone(self):
        self.expandido = False

        self.botao_capturar.hide()
        self.painel_botoes.hide()
        self.explicacao.hide()
        self.botao_recolher.hide()
        self.titulo.setText("")

        self.resize(64, 64)
        self.setMinimumSize(64, 64)
        self.setMaximumSize(64, 64)

        self.setStyleSheet("""
            QWidget {
                background-color: #3569b8;
                color: white;
                border-radius: 12px;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
        """)

        self.botao_fechar.setText("×")
        self.botao_fechar.setFixedSize(24, 24)

        self.titulo.setText("✂️")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("font-size: 24px;")

        self.layout_principal.setContentsMargins(4, 4, 4, 4)
        self.layout_principal.setSpacing(0)

        self.botao_fechar.show()
        self.titulo.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.posicao_mouse = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if (
            self.posicao_mouse is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self.posicao_mouse
            )

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.posicao_mouse = None
            if not self.expandido:
                self.mostrar_painel()

    def mostrar_painel(self):
        self.expandido = True

        self.setStyleSheet("""
            QWidget {
                background-color: #202633;
                color: white;
                font-family: Arial;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3569b8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #4b83,d8;
                background-color: #4b83d8;
            }
            QTextBrowser {
                background-color: #f5f7fa;
                color: #202633;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        self.setMaximumSize(16777215, 16777215)
        self.setMinimumSize(340, 480)
        self.resize(380, 520)

        self.layout_principal.setContentsMargins(10, 10, 10, 10)
        self.layout_principal.setSpacing(8)

        self.titulo.setText("Tutor UML")
        self.titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.botao_fechar.setText("X")
        self.botao_fechar.setFixedSize(32, 30)

        self.botao_recolher.show()
        self.botao_capturar.show()
        self.painel_botoes.show()
        self.explicacao.show()

        self.raise_()

    def atualizar_explicacao(self, conceito):
        self.explicacao.setHtml(
            CONCEITOS.get(
                conceito,
                "<h2>Conceito não encontrado</h2>"
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    janela = TutorUML()
    janela.show()

    sys.exit(app.exec())