from .common import *


class ConsultasMixin:
        def crear_consultas(self):
            pestaña = QWidget()
            layout = QVBoxLayout()
            formulario = FormularioCompacto()
            formulario.setContentsMargins(0, 0, 0, 8)
            formulario.setHorizontalSpacing(18)
            formulario.setVerticalSpacing(12)
            formulario.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            formulario.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

            self.expediente_consulta = QComboBox()
            self.expediente_consulta.addItem("Seleccionar expediente")

            formulario.addRow(
                "Expediente:",
                self.expediente_consulta
            )

            self.medico_consulta = QComboBox()
            self.medico_consulta.addItem("Seleccionar médico")

            formulario.addRow(
                "Médico:",
                self.medico_consulta
            )

            self.cita_consulta = QComboBox()
            self.cita_consulta.addItem("Seleccionar cita")

            formulario.addRow(
                "Cita:",
                self.cita_consulta
            )

            self.fecha_consulta = QDateEdit()
            self.fecha_consulta.setCalendarPopup(True)
            self.fecha_consulta.setDate(QDate.currentDate())

            formulario.addRow(
                "Fecha de consulta:",
                self.fecha_consulta
            )

            self.presion_consulta = QLineEdit()
            formulario.addRow(
                "Presión arterial:",
                self.presion_consulta
            )

            self.peso_consulta = QDoubleSpinBox()
            self.peso_consulta.setRange(0.50, 500.00)
            self.peso_consulta.setDecimals(2)
            self.peso_consulta.setSuffix(" kg")

            formulario.addRow(
                "Peso:",
                self.peso_consulta
            )

            self.sintomas_consulta = QTextEdit()
            formulario.addRow(
                "Síntomas:",
                self.sintomas_consulta
            )

            self.diagnostico_consulta = QTextEdit()
            formulario.addRow(
                "Diagnóstico:",
                self.diagnostico_consulta
            )

            estilizar_formulario(formulario, layout)
            layout.addLayout(formulario)

            botones = QHBoxLayout()

            btn_guardar = QPushButton("Guardar")
            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")
            btn_limpiar = QPushButton("Limpiar")

            btn_guardar.clicked.connect(self.guardar_consulta)
            btn_editar.clicked.connect(self.editar_consulta)
            btn_eliminar.clicked.connect(self.eliminar_consulta)
            btn_limpiar.clicked.connect(self.limpiar_consulta)

            botones.addWidget(btn_guardar)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)
            botones.addWidget(btn_limpiar)

            layout.addLayout(botones)

            self.tabla_consultas = QTableWidget()
            self.tabla_consultas.setColumnCount(9)
            self.tabla_consultas.setHorizontalHeaderLabels([
                "ID",
                "Expediente",
                "Médico",
                "Cita",
                "Fecha",
                "Presión",
                "Peso",
                "Síntomas",
                "Diagnóstico"
            ])

            self.tabla_consultas.cellClicked.connect(
                self.seleccionar_consulta
            )

            layout.addWidget(self.tabla_consultas)

            pestaña.setLayout(layout)
            self.tabs.addTab(pestaña, "Consultas Historial")

        def guardar_consulta(self):
            expediente = self.expediente_consulta.currentText()
            medico = self.medico_consulta.currentText()
            cita = self.cita_consulta.currentText()
            fecha = self.fecha_consulta.date().toString("yyyy-MM-dd")
            presion = self.presion_consulta.text().strip()
            peso = self.peso_consulta.value()
            sintomas = self.sintomas_consulta.toPlainText().strip()
            diagnostico = self.diagnostico_consulta.toPlainText().strip()

            if self.expediente_consulta.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Expediente",
                    "Selecciona un expediente."
                )
                return

            if self.medico_consulta.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Médico",
                    "Selecciona un médico."
                )
                return

            if self.cita_consulta.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Cita",
                    "Selecciona una cita."
                )
                return

            if not presion or not sintomas or not diagnostico:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa presión, síntomas y diagnóstico."
                )
                return

            if peso <= 0:
                QMessageBox.warning(
                    self,
                    "Peso",
                    "El peso debe ser mayor que cero."
                )
                return

            for fila in range(self.tabla_consultas.rowCount()):
                item = self.tabla_consultas.item(fila, 3)
                if item and item.text() == cita:
                    QMessageBox.warning(
                        self,
                        "Cita duplicada",
                        "Esta cita ya tiene una consulta registrada."
                    )
                    return

            fila = self.tabla_consultas.rowCount()
            self.tabla_consultas.insertRow(fila)

            datos = [
                str(fila + 1),
                expediente,
                medico,
                cita,
                fecha,
                presion,
                f"{peso:.2f}",
                sintomas,
                diagnostico
            ]

            for columna, dato in enumerate(datos):
                self.tabla_consultas.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_consulta()
            self.actualizar_recetas()

        def editar_consulta(self):
            fila = self.tabla_consultas.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona una consulta."
                )
                return

            if self.expediente_consulta.currentIndex() == 0:
                return

            if self.medico_consulta.currentIndex() == 0:
                return

            if self.cita_consulta.currentIndex() == 0:
                return

            presion = self.presion_consulta.text().strip()
            sintomas = self.sintomas_consulta.toPlainText().strip()
            diagnostico = self.diagnostico_consulta.toPlainText().strip()

            if not presion or not sintomas or not diagnostico:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa todos los campos obligatorios."
                )
                return

            datos = [
                self.expediente_consulta.currentText(),
                self.medico_consulta.currentText(),
                self.cita_consulta.currentText(),
                self.fecha_consulta.date().toString("yyyy-MM-dd"),
                presion,
                f"{self.peso_consulta.value():.2f}",
                sintomas,
                diagnostico
            ]

            for columna, dato in enumerate(datos, start=1):
                self.tabla_consultas.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_consulta()

        def eliminar_consulta(self):
            fila = self.tabla_consultas.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona una consulta."
                )
                return

            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Deseas eliminar esta consulta?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.tabla_consultas.removeRow(fila)

        def limpiar_consulta(self):
            self.expediente_consulta.setCurrentIndex(0)
            self.medico_consulta.setCurrentIndex(0)
            self.cita_consulta.setCurrentIndex(0)
            self.fecha_consulta.setDate(QDate.currentDate())
            self.presion_consulta.clear()
            self.peso_consulta.setValue(0)
            self.sintomas_consulta.clear()
            self.diagnostico_consulta.clear()

        def seleccionar_consulta(self, fila, columna):
            expediente = self.tabla_consultas.item(fila, 1)
            medico = self.tabla_consultas.item(fila, 2)
            cita = self.tabla_consultas.item(fila, 3)
            fecha = self.tabla_consultas.item(fila, 4)
            presion = self.tabla_consultas.item(fila, 5)
            peso = self.tabla_consultas.item(fila, 6)
            sintomas = self.tabla_consultas.item(fila, 7)
            diagnostico = self.tabla_consultas.item(fila, 8)

            if expediente:
                indice = self.expediente_consulta.findText(expediente.text())
                if indice >= 0:
                    self.expediente_consulta.setCurrentIndex(indice)

            if medico:
                indice = self.medico_consulta.findText(medico.text())
                if indice >= 0:
                    self.medico_consulta.setCurrentIndex(indice)

            if cita:
                indice = self.cita_consulta.findText(cita.text())
                if indice >= 0:
                    self.cita_consulta.setCurrentIndex(indice)

            if fecha:
                self.fecha_consulta.setDate(
                    QDate.fromString(fecha.text(), "yyyy-MM-dd")
                )

            if presion:
                self.presion_consulta.setText(presion.text())

            if peso:
                self.peso_consulta.setValue(float(peso.text()))

            if sintomas:
                self.sintomas_consulta.setPlainText(sintomas.text())

            if diagnostico:
                self.diagnostico_consulta.setPlainText(diagnostico.text())

        def actualizar_consultas(self):
            if hasattr(self, "expediente_consulta"):
                self.expediente_consulta.clear()
                self.expediente_consulta.addItem("Seleccionar expediente")

                for fila in range(self.tabla_expedientes.rowCount()):
                    item = self.tabla_expedientes.item(fila, 0)
                    if item:
                        self.expediente_consulta.addItem(
                            "Expediente " + item.text()
                        )

            if hasattr(self, "medico_consulta"):
                self.medico_consulta.clear()
                self.medico_consulta.addItem("Seleccionar médico")

                for fila in range(self.tabla_medicos.rowCount()):
                    item = self.tabla_medicos.item(fila, 2)
                    if item:
                        self.medico_consulta.addItem(item.text())

            if hasattr(self, "cita_consulta"):
                self.cita_consulta.clear()
                self.cita_consulta.addItem("Seleccionar cita")

                for fila in range(self.tabla_citas.rowCount()):
                    item = self.tabla_citas.item(fila, 0)
                    if item:
                        self.cita_consulta.addItem(
                            "Cita " + item.text()
                        )