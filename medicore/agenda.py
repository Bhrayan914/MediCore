from .common import *
from PySide6.QtWidgets import QCheckBox


class AgendaMixin:
        def crear_agenda(self):
            pestaña = QWidget()
            layout = QVBoxLayout()
            formulario = FormularioCompacto()
            formulario.setContentsMargins(0, 0, 0, 8)
            formulario.setHorizontalSpacing(18)
            formulario.setVerticalSpacing(12)
            formulario.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            formulario.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

            self.medico_agenda = QComboBox()
            self.medico_agenda.addItem("Seleccionar médico")

            formulario.addRow("Médico:", self.medico_agenda)

            self.dia_agenda = QComboBox()
            self.dia_agenda.addItems([
                "Lunes",
                "Martes",
                "Miercoles",
                "Jueves",
                "Viernes",
                "Sabado",
                "Domingo"
            ])

            formulario.addRow("Día:", self.dia_agenda)

            self.hora_inicio_agenda = QTimeEdit()
            self.hora_inicio_agenda.setTime(QTime(8, 0))

            formulario.addRow(
                "Hora de inicio:",
                self.hora_inicio_agenda
            )

            self.hora_fin_agenda = QTimeEdit()
            self.hora_fin_agenda.setTime(QTime(16, 0))

            formulario.addRow(
                "Hora de fin:",
                self.hora_fin_agenda
            )

            self.horario_especial = QCheckBox(
                "Horario especial (fuera del turno del médico)"
            )
            self.horario_especial.setToolTip(
                "Matutino: 7:00 a 12:00  |  Vespertino: 12:00 a 20:00  |  "
                "Nocturno: 20:00 a 7:00.\n"
                "Marca esta casilla solo si el médico trabajará fuera de su turno."
            )

            formulario.addRow("Tipo de horario:", self.horario_especial)

            estilizar_formulario(formulario, layout)
            layout.addLayout(formulario)

            botones = QHBoxLayout()

            btn_guardar = QPushButton("Guardar")
            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")
            btn_limpiar = QPushButton("Limpiar")

            btn_guardar.clicked.connect(self.guardar_agenda)
            btn_editar.clicked.connect(self.editar_agenda)
            btn_eliminar.clicked.connect(self.eliminar_agenda)
            btn_limpiar.clicked.connect(self.limpiar_agenda)

            botones.addWidget(btn_guardar)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)
            botones.addWidget(btn_limpiar)

            layout.addLayout(botones)

            self.tabla_agenda = QTableWidget()
            self.tabla_agenda.setColumnCount(6)
            self.tabla_agenda.setHorizontalHeaderLabels([
                "ID",
                "Médico",
                "Día",
                "Hora inicio",
                "Hora fin",
                "Tipo"
            ])

            self.tabla_agenda.cellClicked.connect(
                self.seleccionar_agenda
            )

            layout.addWidget(self.tabla_agenda)

            pestaña.setLayout(layout)
            self.tabs.addTab(pestaña, "Agenda Horarios")

        def guardar_agenda(self):
            medico = self.medico_agenda.currentText()
            dia = self.dia_agenda.currentText()
            inicio = self.hora_inicio_agenda.time()
            fin = self.hora_fin_agenda.time()

            if self.medico_agenda.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Médico",
                    "Selecciona un médico."
                )
                return

            if inicio >= fin:
                QMessageBox.warning(
                    self,
                    "Horario inválido",
                    "La hora de inicio debe ser menor que la hora de fin."
                )
                return

            fila = self.tabla_agenda.rowCount()
            self.tabla_agenda.insertRow(fila)

            datos = [
                str(fila + 1),
                medico,
                dia,
                inicio.toString("HH:mm"),
                fin.toString("HH:mm")
            ]

            for columna, dato in enumerate(datos):
                self.tabla_agenda.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_agenda()

        def editar_agenda(self):
            fila = self.tabla_agenda.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un horario."
                )
                return

            if self.medico_agenda.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Médico",
                    "Selecciona un médico."
                )
                return

            inicio = self.hora_inicio_agenda.time()
            fin = self.hora_fin_agenda.time()

            if inicio >= fin:
                QMessageBox.warning(
                    self,
                    "Horario inválido",
                    "La hora de inicio debe ser menor que la hora de fin."
                )
                return

            datos = [
                self.medico_agenda.currentText(),
                self.dia_agenda.currentText(),
                inicio.toString("HH:mm"),
                fin.toString("HH:mm")
            ]

            for columna, dato in enumerate(datos, start=1):
                self.tabla_agenda.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_agenda()

        def eliminar_agenda(self):
            fila = self.tabla_agenda.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un horario."
                )
                return

            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Deseas eliminar este horario?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.tabla_agenda.removeRow(fila)

        def limpiar_agenda(self):
            self.medico_agenda.setCurrentIndex(0)
            self.dia_agenda.setCurrentIndex(0)
            self.hora_inicio_agenda.setTime(QTime(8, 0))
            self.hora_fin_agenda.setTime(QTime(16, 0))
            self.horario_especial.setChecked(False)

        def seleccionar_agenda(self, fila, columna):
            medico = self.tabla_agenda.item(fila, 1)
            dia = self.tabla_agenda.item(fila, 2)
            inicio = self.tabla_agenda.item(fila, 3)
            fin = self.tabla_agenda.item(fila, 4)
            tipo = self.tabla_agenda.item(fila, 5)

            self.horario_especial.setChecked(
                bool(tipo) and tipo.text() == "Especial"
            )

            if medico:
                indice = self.medico_agenda.findText(medico.text())
                if indice >= 0:
                    self.medico_agenda.setCurrentIndex(indice)

            if dia:
                indice = self.dia_agenda.findText(dia.text())
                if indice >= 0:
                    self.dia_agenda.setCurrentIndex(indice)

            if inicio:
                self.hora_inicio_agenda.setTime(
                    QTime.fromString(inicio.text(), "HH:mm")
                )

            if fin:
                self.hora_fin_agenda.setTime(
                    QTime.fromString(fin.text(), "HH:mm")
                )

        def actualizar_agenda(self):
            if not hasattr(self, "medico_agenda"):
                return

            self.medico_agenda.clear()
            self.medico_agenda.addItem("Seleccionar médico")

            for fila in range(self.tabla_medicos.rowCount()):
                item = self.tabla_medicos.item(fila, 2)
                if item:
                    self.medico_agenda.addItem(item.text())