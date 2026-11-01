from .common import *


class MedicosMixin:
        def crear_medicos(self):
            pestaña = QWidget()
            layout = QVBoxLayout()
            formulario = FormularioCompacto()
            formulario.setContentsMargins(0, 0, 0, 8)
            formulario.setHorizontalSpacing(18)
            formulario.setVerticalSpacing(12)
            formulario.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            formulario.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

            self.codigo_minsa = QLineEdit()
            self.nombre_medico = QLineEdit()

            formulario.addRow("Código MINSA:", self.codigo_minsa)
            formulario.addRow("Nombre:", self.nombre_medico)

            self.especialidad_medico = QComboBox()
            self.especialidad_medico.addItem("Seleccionar especialidad")

            formulario.addRow(
                "Especialidad:",
                self.especialidad_medico
            )

            self.turno_medico = QComboBox()
            self.turno_medico.addItems([
                "Matutino",
                "Vespertino",
                "Nocturno"
            ])

            formulario.addRow("Turno:", self.turno_medico)

            estilizar_formulario(formulario, layout)
            layout.addLayout(formulario)

            botones = QHBoxLayout()

            btn_guardar = QPushButton("Guardar")
            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")
            btn_limpiar = QPushButton("Limpiar")

            btn_guardar.clicked.connect(self.guardar_medico)
            btn_editar.clicked.connect(self.editar_medico)
            btn_eliminar.clicked.connect(self.eliminar_medico)
            btn_limpiar.clicked.connect(self.limpiar_medico)

            botones.addWidget(btn_guardar)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)
            botones.addWidget(btn_limpiar)

            layout.addLayout(botones)

            self.tabla_medicos = QTableWidget()
            self.tabla_medicos.setColumnCount(5)
            self.tabla_medicos.setHorizontalHeaderLabels([
                "ID",
                "Código MINSA",
                "Nombre",
                "Especialidad",
                "Turno"
            ])

            self.tabla_medicos.cellClicked.connect(
                self.seleccionar_medico
            )

            layout.addWidget(self.tabla_medicos)

            pestaña.setLayout(layout)
            self.tabs.addTab(pestaña, "Médicos")

        def guardar_medico(self):
            codigo = self.codigo_minsa.text().strip()
            nombre = self.nombre_medico.text().strip()
            especialidad = self.especialidad_medico.currentText()
            turno = self.turno_medico.currentText()

            if not codigo or not nombre:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa todos los campos."
                )
                return

            if self.especialidad_medico.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Especialidad",
                    "Selecciona una especialidad."
                )
                return

            for fila in range(self.tabla_medicos.rowCount()):
                item = self.tabla_medicos.item(fila, 1)
                if item and item.text().lower() == codigo.lower():
                    QMessageBox.warning(
                        self,
                        "Código duplicado",
                        "El código MINSA ya existe."
                    )
                    return

            fila = self.tabla_medicos.rowCount()
            self.tabla_medicos.insertRow(fila)

            datos = [
                str(fila + 1),
                codigo,
                nombre,
                especialidad,
                turno
            ]

            for columna, dato in enumerate(datos):
                self.tabla_medicos.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_medico()
            self.actualizar_medicos()
            self.actualizar_agenda()
            self.actualizar_citas()

        def editar_medico(self):
            fila = self.tabla_medicos.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un médico."
                )
                return

            datos = [
                self.codigo_minsa.text().strip(),
                self.nombre_medico.text().strip(),
                self.especialidad_medico.currentText(),
                self.turno_medico.currentText()
            ]

            if not datos[0] or not datos[1]:
                QMessageBox.warning(
                    self,
                    "Campos vacíos",
                    "Completa todos los campos."
                )
                return

            if self.especialidad_medico.currentIndex() == 0:
                QMessageBox.warning(
                    self,
                    "Especialidad",
                    "Selecciona una especialidad."
                )
                return

            for columna, dato in enumerate(datos, start=1):
                self.tabla_medicos.setItem(
                    fila, columna, QTableWidgetItem(dato)
                )

            self.limpiar_medico()
            self.actualizar_medicos()
            self.actualizar_agenda()
            self.actualizar_citas()

        def eliminar_medico(self):
            fila = self.tabla_medicos.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona un médico."
                )
                return

            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Deseas eliminar este médico?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.tabla_medicos.removeRow(fila)
                self.actualizar_medicos()
                self.actualizar_agenda()
                self.actualizar_citas()

        def limpiar_medico(self):
            self.codigo_minsa.clear()
            self.nombre_medico.clear()
            self.especialidad_medico.setCurrentIndex(0)
            self.turno_medico.setCurrentIndex(0)

        def seleccionar_medico(self, fila, columna):
            codigo = self.tabla_medicos.item(fila, 1)
            nombre = self.tabla_medicos.item(fila, 2)
            especialidad = self.tabla_medicos.item(fila, 3)
            turno = self.tabla_medicos.item(fila, 4)

            if codigo:
                self.codigo_minsa.setText(codigo.text())

            if nombre:
                self.nombre_medico.setText(nombre.text())

            if especialidad:
                indice = self.especialidad_medico.findText(
                    especialidad.text()
                )
                if indice >= 0:
                    self.especialidad_medico.setCurrentIndex(indice)

            if turno:
                indice = self.turno_medico.findText(turno.text())
                if indice >= 0:
                    self.turno_medico.setCurrentIndex(indice)

        def actualizar_medicos(self):
            combos = []

            if hasattr(self, "medico_agenda"):
                combos.append(self.medico_agenda)

            if hasattr(self, "medico_cita"):
                combos.append(self.medico_cita)

            if hasattr(self, "medico_consulta"):
                combos.append(self.medico_consulta)

            for combo in combos:
                combo.clear()
                combo.addItem("Seleccionar médico")

                for fila in range(self.tabla_medicos.rowCount()):
                    item = self.tabla_medicos.item(fila, 2)
                    if item:
                        combo.addItem(item.text())
