from .common import *


class DetalleRecetaMixin:
        def crear_detalle_receta(self):
            pestaña = QWidget()
            layout = QVBoxLayout()
            formulario = FormularioCompacto()
            formulario.setContentsMargins(0, 0, 0, 8)
            formulario.setHorizontalSpacing(18)
            formulario.setVerticalSpacing(12)
            formulario.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            formulario.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

            self.receta_detalle = QComboBox()
            self.receta_detalle.addItem("Seleccionar receta")

            formulario.addRow(
                "Receta:",
                self.receta_detalle
            )

            self.medicamento_detalle = QComboBox()
            self.medicamento_detalle.addItem("Seleccionar medicamento")

            formulario.addRow(
                "Medicamento:",
                self.medicamento_detalle
            )

            self.dosis_detalle = QLineEdit()
            formulario.addRow(
                "Dosis indicada:",
                self.dosis_detalle
            )

            self.frecuencia_detalle = QLineEdit()
            formulario.addRow(
                "Frecuencia:",
                self.frecuencia_detalle
            )

            self.duracion_detalle = QLineEdit()
            formulario.addRow(
                "Duración:",
                self.duracion_detalle
            )

            self.cantidad_detalle = QSpinBox()
            self.cantidad_detalle.setRange(1, 10000)
            self.cantidad_detalle.setSuffix(" unidades")
            self.cantidad_detalle.setToolTip(
                "Unidades que se descuentan de la existencia del medicamento"
            )
            formulario.addRow(
                "Cantidad a entregar:",
                self.cantidad_detalle
            )

            estilizar_formulario(formulario, layout)
            layout.addLayout(formulario)

            botones = QHBoxLayout()

            btn_guardar = QPushButton("Guardar")
            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")
            btn_limpiar = QPushButton("Limpiar")
            btn_pdf = QPushButton("Exportar PDF")
            btn_pdf.setToolTip(
                "Genera la receta lista para imprimir (tamaño media carta) "
                "con el logo, los medicamentos y espacio para firma y sello"
            )

            btn_guardar.clicked.connect(self.guardar_detalle_receta)
            btn_editar.clicked.connect(self.editar_detalle_receta)
            btn_eliminar.clicked.connect(self.eliminar_detalle_receta)
            btn_limpiar.clicked.connect(self.limpiar_detalle_receta)
            btn_pdf.clicked.connect(self.exportar_receta_pdf)

            botones.addWidget(btn_guardar)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)
            botones.addWidget(btn_limpiar)
            botones.addWidget(btn_pdf)

            layout.addLayout(botones)

            self.tabla_detalle_receta = QTableWidget()
            self.tabla_detalle_receta.setColumnCount(6)
            self.tabla_detalle_receta.setHorizontalHeaderLabels([
                "Receta",
                "Medicamento",
                "Dosis",
                "Frecuencia",
                "Duración",
                "Cantidad"
            ])

            self.tabla_detalle_receta.cellClicked.connect(
                self.seleccionar_detalle_receta
            )

            layout.addWidget(self.tabla_detalle_receta)

            pestaña.setLayout(layout)
            self.tabs.addTab(pestaña, "Detalle Receta")

        def guardar_detalle_receta(self):
            receta = self.receta_detalle.currentText()
            medicamento = self.medicamento_detalle.currentText()
            dosis = self.dosis_detalle.text().strip()
            frecuencia = self.frecuencia_detalle.text().strip()
            duracion = self.duracion_detalle.text().strip()

            if self.receta_detalle.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Receta",
                    "Selecciona una receta."
                )
                return

            if self.medicamento_detalle.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Medicamento",
                    "Selecciona un medicamento."
                )
                return

            if not dosis or not frecuencia or not duracion:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa dosis, frecuencia y duración."
                )
                return

            for fila in range(self.tabla_detalle_receta.rowCount()):
                receta_item = self.tabla_detalle_receta.item(fila, 0)
                medicamento_item = self.tabla_detalle_receta.item(fila, 1)

                if (
                    receta_item
                    and medicamento_item
                    and receta_item.text() == receta
                    and medicamento_item.text() == medicamento
                ):
                    QMessageBox.warning(
                        self,
                        "Detalle duplicado",
                        "Ese medicamento ya está agregado a la receta."
                    )
                    return

            fila = self.tabla_detalle_receta.rowCount()
            self.tabla_detalle_receta.insertRow(fila)

            datos = [
                receta,
                medicamento,
                dosis,
                frecuencia,
                duracion
            ]

            for columna, dato in enumerate(datos):
                self.tabla_detalle_receta.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_detalle_receta()

        def editar_detalle_receta(self):
            fila = self.tabla_detalle_receta.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un detalle de receta."
                )
                return

            if self.receta_detalle.currentIndex() == 0:
                return

            if self.medicamento_detalle.currentIndex() == 0:
                return

            dosis = self.dosis_detalle.text().strip()
            frecuencia = self.frecuencia_detalle.text().strip()
            duracion = self.duracion_detalle.text().strip()

            if not dosis or not frecuencia or not duracion:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa todos los campos."
                )
                return

            datos = [
                self.receta_detalle.currentText(),
                self.medicamento_detalle.currentText(),
                dosis,
                frecuencia,
                duracion
            ]

            for columna, dato in enumerate(datos):
                self.tabla_detalle_receta.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_detalle_receta()

        def eliminar_detalle_receta(self):
            fila = self.tabla_detalle_receta.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un detalle."
                )
                return

            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Deseas eliminar este detalle?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.tabla_detalle_receta.removeRow(fila)

        def limpiar_detalle_receta(self):
            self.receta_detalle.setCurrentIndex(0)
            self.medicamento_detalle.setCurrentIndex(0)
            self.dosis_detalle.clear()
            self.frecuencia_detalle.clear()
            self.duracion_detalle.clear()
            self.cantidad_detalle.setValue(1)

        def seleccionar_detalle_receta(self, fila, columna):
            receta = self.tabla_detalle_receta.item(fila, 0)
            medicamento = self.tabla_detalle_receta.item(fila, 1)
            dosis = self.tabla_detalle_receta.item(fila, 2)
            frecuencia = self.tabla_detalle_receta.item(fila, 3)
            duracion = self.tabla_detalle_receta.item(fila, 4)

            if receta:
                indice = self.receta_detalle.findText(receta.text())
                if indice >= 0:
                    self.receta_detalle.setCurrentIndex(indice)

            if medicamento:
                indice = self.medicamento_detalle.findText(
                    medicamento.text()
                )
                if indice >= 0:
                    self.medicamento_detalle.setCurrentIndex(indice)

            if dosis:
                self.dosis_detalle.setText(dosis.text())

            if frecuencia:
                self.frecuencia_detalle.setText(frecuencia.text())

            if duracion:
                self.duracion_detalle.setText(duracion.text())

        def actualizar_detalle_receta(self):
            if hasattr(self, "receta_detalle"):
                self.receta_detalle.clear()
                self.receta_detalle.addItem("Seleccionar receta")

                for fila in range(self.tabla_recetas.rowCount()):
                    item = self.tabla_recetas.item(fila, 0)
                    if item:
                        self.receta_detalle.addItem(
                            "Receta " + item.text()
                        )

            if hasattr(self, "medicamento_detalle"):
                self.medicamento_detalle.clear()
                self.medicamento_detalle.addItem(
                    "Seleccionar medicamento"
                )

                for fila in range(self.tabla_medicamentos.rowCount()):
                    item = self.tabla_medicamentos.item(fila, 1)
                    if item:
                        self.medicamento_detalle.addItem(item.text())