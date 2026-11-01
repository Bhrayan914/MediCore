from .common import *


class MedicamentosMixin:
        def crear_medicamentos(self):
            pestaña = QWidget()
            layout = QVBoxLayout()
            formulario = FormularioCompacto()
            formulario.setContentsMargins(0, 0, 0, 8)
            formulario.setHorizontalSpacing(18)
            formulario.setVerticalSpacing(12)
            formulario.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            formulario.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

            self.nombre_medicamento = QLineEdit()
            formulario.addRow(
                "Nombre del medicamento:",
                self.nombre_medicamento
            )

            self.presentacion_medicamento = QLineEdit()
            formulario.addRow(
                "Presentación:",
                self.presentacion_medicamento
            )

            self.existencia_medicamento = QSpinBox()
            self.existencia_medicamento.setRange(0, 100000)

            formulario.addRow(
                "Existencia:",
                self.existencia_medicamento
            )

            estilizar_formulario(formulario, layout)
            layout.addLayout(formulario)

            botones = QHBoxLayout()

            btn_guardar = QPushButton("Guardar")
            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")
            btn_limpiar = QPushButton("Limpiar")

            btn_guardar.clicked.connect(self.guardar_medicamento)
            btn_editar.clicked.connect(self.editar_medicamento)
            btn_eliminar.clicked.connect(self.eliminar_medicamento)
            btn_limpiar.clicked.connect(self.limpiar_medicamento)

            botones.addWidget(btn_guardar)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)
            botones.addWidget(btn_limpiar)

            layout.addLayout(botones)

            self.tabla_medicamentos = QTableWidget()
            self.tabla_medicamentos.setColumnCount(4)
            self.tabla_medicamentos.setHorizontalHeaderLabels([
                "ID",
                "Nombre",
                "Presentación",
                "Existencia"
            ])

            self.tabla_medicamentos.cellClicked.connect(
                self.seleccionar_medicamento
            )

            layout.addWidget(self.tabla_medicamentos)

            pestaña.setLayout(layout)
            self.tabs.addTab(pestaña, "Medicamentos")

        def guardar_medicamento(self):
            nombre = self.nombre_medicamento.text().strip()
            presentacion = self.presentacion_medicamento.text().strip()
            existencia = self.existencia_medicamento.value()

            if not nombre or not presentacion:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa el nombre y la presentación."
                )
                return

            for fila in range(self.tabla_medicamentos.rowCount()):
                item = self.tabla_medicamentos.item(fila, 1)
                if item and item.text().lower() == nombre.lower():
                    QMessageBox.warning(
                        self,
                        "Medicamento duplicado",
                        "El medicamento ya existe."
                    )
                    return

            fila = self.tabla_medicamentos.rowCount()
            self.tabla_medicamentos.insertRow(fila)

            datos = [
                str(fila + 1),
                nombre,
                presentacion,
                str(existencia)
            ]

            for columna, dato in enumerate(datos):
                self.tabla_medicamentos.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_medicamento()
            self.actualizar_detalle_receta()

        def editar_medicamento(self):
            fila = self.tabla_medicamentos.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un medicamento."
                )
                return

            nombre = self.nombre_medicamento.text().strip()
            presentacion = self.presentacion_medicamento.text().strip()

            if not nombre or not presentacion:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa todos los campos."
                )
                return

            datos = [
                nombre,
                presentacion,
                str(self.existencia_medicamento.value())
            ]

            for columna, dato in enumerate(datos, start=1):
                self.tabla_medicamentos.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_medicamento()

        def eliminar_medicamento(self):
            fila = self.tabla_medicamentos.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un medicamento."
                )
                return

            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Deseas eliminar este medicamento?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.tabla_medicamentos.removeRow(fila)
                self.actualizar_detalle_receta()

        def limpiar_medicamento(self):
            self.nombre_medicamento.clear()
            self.presentacion_medicamento.clear()
            self.existencia_medicamento.setValue(0)

        def seleccionar_medicamento(self, fila, columna):
            nombre = self.tabla_medicamentos.item(fila, 1)
            presentacion = self.tabla_medicamentos.item(fila, 2)
            existencia = self.tabla_medicamentos.item(fila, 3)

            if nombre:
                self.nombre_medicamento.setText(nombre.text())

            if presentacion:
                self.presentacion_medicamento.setText(presentacion.text())

            if existencia:
                self.existencia_medicamento.setValue(
                    int(existencia.text())
                )
