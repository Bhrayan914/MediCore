from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap

from .autenticacion import autenticar_usuario


ESTILOS_LOGIN = """
    * {
        font-family: "Segoe UI", Arial, sans-serif;
    }

    QDialog {
        background: #FFFFFF;
    }

    /* ---------- Panel de marca (izquierda) ---------- */
    QFrame#panelMarca {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #142D45, stop: 1 #1B5368
        );
    }

    QFrame#tarjetaLogo {
        background: #FFFFFF;
        border-radius: 18px;
    }

    QLabel#marcaTitulo {
        color: #FFFFFF;
        font-size: 19px;
        font-weight: 700;
    }

    QLabel#marcaTexto {
        color: #B4CADA;
        font-size: 12px;
    }

    QLabel#marcaItem {
        color: #D5E2EC;
        font-size: 12px;
    }

    QLabel#marcaPie {
        color: #7F9CB3;
        font-size: 10px;
    }

    /* ---------- Panel del formulario (derecha) ---------- */
    QFrame#panelFormulario {
        background: #FFFFFF;
    }

    QLabel#sobretitulo {
        color: #168575;
        font-size: 11px;
        font-weight: 700;
    }

    QLabel#tituloLogin {
        color: #183A53;
        font-size: 28px;
        font-weight: 800;
    }

    QLabel#subtituloLogin {
        color: #62748A;
        font-size: 13px;
    }

    QLabel#etiquetaCampo {
        color: #25364A;
        font-size: 12px;
        font-weight: 600;
    }

    QLineEdit {
        background: #F7FAFC;
        border: 1px solid #D5DFE8;
        border-radius: 9px;
        padding: 11px 12px;
        font-size: 14px;
        color: #1E293B;
    }

    QLineEdit:focus {
        background: #FFFFFF;
        border: 2px solid #1EAA9B;
        padding: 10px 11px;
    }

    QCheckBox {
        color: #4A5C70;
        font-size: 12px;
        spacing: 8px;
    }

    QLabel#errorLogin {
        color: #B42318;
        background: #FEF3F2;
        border: 1px solid #FECDCA;
        border-radius: 8px;
        padding: 9px 12px;
        font-size: 12px;
    }

    QPushButton#botonIngresar {
        background: #1EAA9B;
        color: #FFFFFF;
        border: none;
        border-radius: 9px;
        padding: 13px;
        font-size: 14px;
        font-weight: 700;
    }

    QPushButton#botonIngresar:hover {
        background: #17958A;
    }

    QPushButton#botonIngresar:pressed {
        background: #127D73;
    }

    QPushButton#botonIngresar:disabled {
        background: #9FD6CF;
    }

    QLabel#pieLogin {
        color: #8896A6;
        font-size: 11px;
    }
"""


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.usuario_autenticado = None

        self.setWindowTitle("MediCore - Inicio de sesión")
        self.setFixedSize(900, 560)
        self.setStyleSheet(ESTILOS_LOGIN)

        self.crear_interfaz()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def crear_interfaz(self):
        raiz = QHBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        raiz.addWidget(self._crear_panel_marca())
        raiz.addWidget(self._crear_panel_formulario(), 1)

        self.campo_usuario.setFocus()

    def _ruta_logo(self):
        return Path(__file__).resolve().parent /"logo_medicore.png"

    def _crear_panel_marca(self):
        panel = QFrame()
        panel.setObjectName("panelMarca")
        panel.setFixedWidth(400)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(34, 36, 34, 26)
        layout.setSpacing(0)

        # Tarjeta blanca con el logo (el logo tiene texto azul oscuro,
        # por eso necesita un fondo claro).
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaLogo")

        sombra = QGraphicsDropShadowEffect(tarjeta)
        sombra.setBlurRadius(34)
        sombra.setOffset(0, 8)
        sombra.setColor(QColor(0, 0, 0, 80))
        tarjeta.setGraphicsEffect(sombra)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(20, 22, 20, 22)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap(str(self._ruta_logo()))

        if pixmap.isNull():
            logo.setText("MediCore")
            logo.setStyleSheet(
                "color: #183A53; font-size: 30px; font-weight: 800;"
            )
        else:
            escala = self.devicePixelRatioF()
            pixmap = pixmap.scaledToWidth(
                int(300 * escala),
                Qt.TransformationMode.SmoothTransformation
            )
            pixmap.setDevicePixelRatio(escala)
            logo.setPixmap(pixmap)

        layout_tarjeta.addWidget(logo)

        titulo = QLabel("Gestión clínica en un solo lugar")
        titulo.setObjectName("marcaTitulo")
        titulo.setWordWrap(True)

        texto = QLabel(
            "Pacientes, citas, expedientes, consultas y recetas "
            "organizados de forma segura y centralizada."
        )
        texto.setObjectName("marcaTexto")
        texto.setWordWrap(True)

        layout.addStretch(1)
        layout.addWidget(tarjeta)
        layout.addSpacing(30)
        layout.addWidget(titulo)
        layout.addSpacing(8)
        layout.addWidget(texto)
        layout.addSpacing(18)

        for beneficio in (
            "✓   Acceso según el rol de cada usuario",
            "✓   Información médica centralizada",
            "✓   Seguimiento clínico ordenado",
        ):
            item = QLabel(beneficio)
            item.setObjectName("marcaItem")
            layout.addWidget(item)
            layout.addSpacing(5)

        layout.addStretch(2)

        pie = QLabel("© 2026 MediCore · Proyecto académico")
        pie.setObjectName("marcaPie")
        layout.addWidget(pie)

        return panel

    def _crear_panel_formulario(self):
        panel = QFrame()
        panel.setObjectName("panelFormulario")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(60, 40, 60, 30)
        layout.setSpacing(0)

        sobretitulo = QLabel("ACCESO AL SISTEMA")
        sobretitulo.setObjectName("sobretitulo")

        titulo = QLabel("Iniciar sesión")
        titulo.setObjectName("tituloLogin")

        subtitulo = QLabel("Ingresa tus credenciales para continuar.")
        subtitulo.setObjectName("subtituloLogin")

        etiqueta_usuario = QLabel("Nombre de usuario")
        etiqueta_usuario.setObjectName("etiquetaCampo")

        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Introduce tu usuario")

        etiqueta_contrasena = QLabel("Contraseña")
        etiqueta_contrasena.setObjectName("etiquetaCampo")

        self.campo_contrasena = QLineEdit()
        self.campo_contrasena.setPlaceholderText("Introduce tu contraseña")
        self.campo_contrasena.setEchoMode(QLineEdit.EchoMode.Password)

        self.mostrar_contrasena = QCheckBox("Mostrar contraseña")
        self.mostrar_contrasena.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mostrar_contrasena.toggled.connect(self._alternar_contrasena)

        self.etiqueta_error = QLabel("")
        self.etiqueta_error.setObjectName("errorLogin")
        self.etiqueta_error.setWordWrap(True)
        self.etiqueta_error.hide()

        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.setObjectName("botonIngresar")
        self.boton_ingresar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_ingresar.setDefault(True)
        self.boton_ingresar.clicked.connect(self.iniciar_sesion)

        self.campo_usuario.returnPressed.connect(
            self.campo_contrasena.setFocus
        )
        self.campo_contrasena.returnPressed.connect(self.iniciar_sesion)

        # Al volver a escribir se limpia el mensaje de error.
        self.campo_usuario.textChanged.connect(self._ocultar_error)
        self.campo_contrasena.textChanged.connect(self._ocultar_error)

        pie = QLabel("Acceso autorizado al sistema")
        pie.setObjectName("pieLogin")
        pie.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch(1)
        layout.addWidget(sobretitulo)
        layout.addSpacing(4)
        layout.addWidget(titulo)
        layout.addSpacing(6)
        layout.addWidget(subtitulo)
        layout.addSpacing(28)
        layout.addWidget(etiqueta_usuario)
        layout.addSpacing(6)
        layout.addWidget(self.campo_usuario)
        layout.addSpacing(16)
        layout.addWidget(etiqueta_contrasena)
        layout.addSpacing(6)
        layout.addWidget(self.campo_contrasena)
        layout.addSpacing(10)
        layout.addWidget(self.mostrar_contrasena)
        layout.addSpacing(12)
        layout.addWidget(self.etiqueta_error)
        layout.addSpacing(12)
        layout.addWidget(self.boton_ingresar)
        layout.addStretch(2)
        layout.addWidget(pie)

        return panel

    # ------------------------------------------------------------------
    # Comportamiento
    # ------------------------------------------------------------------
    def _alternar_contrasena(self, visible):
        self.campo_contrasena.setEchoMode(
            QLineEdit.EchoMode.Normal
            if visible
            else QLineEdit.EchoMode.Password
        )

    def _mostrar_error(self, mensaje):
        self.etiqueta_error.setText(mensaje)
        self.etiqueta_error.show()

    def _ocultar_error(self, *_):
        if self.etiqueta_error.isVisible():
            self.etiqueta_error.hide()

    def iniciar_sesion(self):
        nombre_usuario = self.campo_usuario.text().strip()
        contrasena = self.campo_contrasena.text()

        if not nombre_usuario or not contrasena:
            self._mostrar_error("Introduce tu usuario y contraseña.")

            if not nombre_usuario:
                self.campo_usuario.setFocus()
            else:
                self.campo_contrasena.setFocus()

            return

        self._ocultar_error()
        self.boton_ingresar.setEnabled(False)
        self.boton_ingresar.setText("Verificando...")
        QApplication.processEvents()

        try:
            usuario = autenticar_usuario(
                nombre_usuario,
                contrasena
            )

            if usuario is None:
                self._mostrar_error(
                    "Usuario o contraseña incorrectos, "
                    "o la cuenta está inactiva."
                )
                self.campo_contrasena.clear()
                self.campo_contrasena.setFocus()
                return

            self.usuario_autenticado = usuario
            self.accept()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo iniciar sesión:\n{error}"
            )

        finally:
            self.boton_ingresar.setEnabled(True)
            self.boton_ingresar.setText("Ingresar")