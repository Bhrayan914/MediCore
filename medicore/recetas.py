
from .common import *
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QSizePolicy

class RecetasMixin:
    def crear_recetas(self):
        pestaña = QWidget()
        layout = QVBoxLayout(pestaña)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)

        formulario = QFormLayout()
        formulario.setContentsMargins(5, 5, 5, 10)
        formulario.setHorizontalSpacing(18)
        formulario.setVerticalSpacing(12)
        formulario.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        formulario.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        etiqueta_consulta = QLabel("Consulta:")
        etiqueta_consulta.setStyleSheet("""
            QLabel {
                color: #222222;
                background-color: transparent;
                font-size: 13px;
                font-weight: bold;
            }
        """)

        self.consulta_receta = QComboBox()
        self.consulta_receta.addItem("Seleccionar consulta")
        self.consulta_receta.setMinimumHeight(38)
        self.consulta_receta.setMinimumWidth(250)
        self.consulta_receta.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.consulta_receta.setStyleSheet("estilo_campo")

        formulario.addRow(etiqueta_consulta, self.consulta_receta)

        etiqueta_fecha = QLabel("Fecha de emisión:")
        etiqueta_fecha.setStyleSheet("""
            QLabel {
                color: #222222;
                background-color: transparent;
                font-size: 13px;
                font-weight: bold;
            }
        """)

        self.fecha_receta = QDateEdit()
        self.fecha_receta.setCalendarPopup(True)
        self.fecha_receta.setDate(QDate.currentDate())
        self.fecha_receta.setDisplayFormat("dd/MM/yyyy")
        self.fecha_receta.setMinimumHeight(38)
        self.fecha_receta.setMinimumWidth(200)
        self.fecha_receta.setStyleSheet("estilo_campo")

        formulario.addRow(etiqueta_fecha, self.fecha_receta)

        layout.addLayout(formulario)

        botones = QHBoxLayout()
        botones.setSpacing(8)

        btn_guardar = QPushButton("Guardar")
        btn_editar = QPushButton("Editar")
        btn_eliminar = QPushButton("Eliminar")
        btn_limpiar = QPushButton("Limpiar")

        btn_guardar.clicked.connect(self.guardar_receta)
        btn_editar.clicked.connect(self.editar_receta)
        btn_eliminar.clicked.connect(self.eliminar_receta)
        btn_limpiar.clicked.connect(self.limpiar_receta)

        for boton in (
            btn_guardar,
            btn_editar,
            btn_eliminar,
            btn_limpiar
        ):
            boton.setMinimumHeight(36)
            botones.addWidget(boton)

        layout.addLayout(botones)

        self.tabla_recetas = QTableWidget()
        self.tabla_recetas.setColumnCount(3)
        self.tabla_recetas.setHorizontalHeaderLabels([
            "ID Receta",
            "Consulta",
            "Fecha emisión"
        ])

        self.tabla_recetas.setAlternatingRowColors(True)
        self.tabla_recetas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabla_recetas.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tabla_recetas.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla_recetas.cellClicked.connect(
            self.seleccionar_receta
        )

        layout.addWidget(self.tabla_recetas)

        self.tabs.addTab(pestaña, "Recetas Médicas")

    def guardar_receta(self):
        consulta = self.consulta_receta.currentText()
        fecha = self.fecha_receta.date().toString("yyyy-MM-dd")

        if self.consulta_receta.currentIndex() == 0:
            QMessageBox.warning(
                self,
                "Consulta",
                "Selecciona una consulta."
            )
            return

        for fila in range(self.tabla_recetas.rowCount()):
            item = self.tabla_recetas.item(fila, 1)

            if item and item.text() == consulta:
                QMessageBox.warning(
                    self,
                    "Receta duplicada",
                    "Esta consulta ya tiene una receta."
                )
                return

        fila = self.tabla_recetas.rowCount()
        self.tabla_recetas.insertRow(fila)

        datos = [
            str(fila + 1),
            consulta,
            fecha
        ]

        for columna, dato in enumerate(datos):
            self.tabla_recetas.setItem(
                fila,
                columna,
                QTableWidgetItem(dato)
            )

        self.limpiar_receta()
        self.actualizar_detalle_receta()

    def editar_receta(self):
        fila = self.tabla_recetas.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccionar registro",
                "Selecciona una receta."
            )
            return

        if self.consulta_receta.currentIndex() == 0:
            QMessageBox.warning(
                self,
                "Consulta",
                "Selecciona una consulta."
            )
            return

        consulta_nueva = self.consulta_receta.currentText()

        for otra_fila in range(self.tabla_recetas.rowCount()):
            if otra_fila == fila:
                continue

            item = self.tabla_recetas.item(otra_fila, 1)

            if item and item.text() == consulta_nueva:
                QMessageBox.warning(
                    self,
                    "Receta duplicada",
                    "Esta consulta ya tiene una receta."
                )
                return

        datos = [
            consulta_nueva,
            self.fecha_receta.date().toString("yyyy-MM-dd")
        ]

        for columna, dato in enumerate(datos, start=1):
            self.tabla_recetas.setItem(
                fila,
                columna,
                QTableWidgetItem(dato)
            )

        self.limpiar_receta()
        self.actualizar_detalle_receta()

    def eliminar_receta(self):
        fila = self.tabla_recetas.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccionar registro",
                "Selecciona una receta."
            )
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Deseas eliminar esta receta?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self.tabla_recetas.removeRow(fila)

            for fila_actual in range(self.tabla_recetas.rowCount()):
                self.tabla_recetas.setItem(
                    fila_actual,
                    0,
                    QTableWidgetItem(str(fila_actual + 1))
                )

            self.actualizar_detalle_receta()

    def limpiar_receta(self):
        self.consulta_receta.setCurrentIndex(0)
        self.fecha_receta.setDate(QDate.currentDate())
        self.tabla_recetas.clearSelection()

    def seleccionar_receta(self, fila, columna):
        consulta = self.tabla_recetas.item(fila, 1)
        fecha = self.tabla_recetas.item(fila, 2)

        if consulta:
            indice = self.consulta_receta.findText(consulta.text())

            if indice >= 0:
                self.consulta_receta.setCurrentIndex(indice)

        if fecha:
            fecha_objeto = QDate.fromString(
                fecha.text(),
                "yyyy-MM-dd"
            )

            if fecha_objeto.isValid():
                self.fecha_receta.setDate(fecha_objeto)

    def actualizar_recetas(self):
        if not hasattr(self, "consulta_receta"):
            return

        self.consulta_receta.clear()
        self.consulta_receta.addItem("Seleccionar consulta")

        if not hasattr(self, "tabla_consultas"):
            return

        for fila in range(self.tabla_consultas.rowCount()):
            item = self.tabla_consultas.item(fila, 0)

            if item:
                self.consulta_receta.addItem(
                    "Consulta " + item.text()
                )
