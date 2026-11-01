from .common import *


class EspecialidadesMixin:
        def crear_especialidades(self):
            pestaña = QWidget()
            layout = QVBoxLayout()
            formulario = FormularioCompacto()
            formulario.setContentsMargins(0, 0, 0, 8)
            formulario.setHorizontalSpacing(18)
            formulario.setVerticalSpacing(12)
            formulario.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            formulario.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

            self.nombre_especialidad = QLineEdit()

            formulario.addRow(
                "Nombre de especialidad:",
                self.nombre_especialidad
            )

            estilizar_formulario(formulario, layout)
            layout.addLayout(formulario)

            botones = QHBoxLayout()

            btn_guardar = QPushButton("Guardar")
            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")
            btn_limpiar = QPushButton("Limpiar")

            btn_guardar.clicked.connect(self.guardar_especialidad)
            btn_editar.clicked.connect(self.editar_especialidad)
            btn_eliminar.clicked.connect(self.eliminar_especialidad)
            btn_limpiar.clicked.connect(self.limpiar_especialidad)

            botones.addWidget(btn_guardar)
            botones.addWidget(btn_editar)
            botones.addWidget(btn_eliminar)
            botones.addWidget(btn_limpiar)

            layout.addLayout(botones)

            self.tabla_especialidades = QTableWidget()
            self.tabla_especialidades.setColumnCount(2)
            self.tabla_especialidades.setHorizontalHeaderLabels([
                "ID Especialidad",
                "Nombre Especialidad"
            ])

            self.tabla_especialidades.cellClicked.connect(
                self.seleccionar_especialidad
            )

            layout.addWidget(self.tabla_especialidades)

            pestaña.setLayout(layout)

            self.tabs.addTab(pestaña, "Especialidades")

        def guardar_especialidad(self):
            nombre = self.nombre_especialidad.text().strip()

            if not nombre:
                QMessageBox.warning(
                    self,
                    "Campo vacío",
                    "Debes ingresar el nombre de la especialidad."
                )
                return

            for fila in range(self.tabla_especialidades.rowCount()):
                item = self.tabla_especialidades.item(fila, 1)
                if item and item.text().lower() == nombre.lower():
                    QMessageBox.warning(
                        self,
                        "Registro duplicado",
                        "La especialidad ya existe."
                    )
                    return

            fila = self.tabla_especialidades.rowCount()
            self.tabla_especialidades.insertRow(fila)

            self.tabla_especialidades.setItem(
                fila, 0, QTableWidgetItem(str(fila + 1))
            )
            self.tabla_especialidades.setItem(
                fila, 1, QTableWidgetItem(nombre)
            )

            self.limpiar_especialidad()
            self.actualizar_especialidades()

        def editar_especialidad(self):
            fila = self.tabla_especialidades.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona una especialidad de la tabla."
                )
                return

            nombre = self.nombre_especialidad.text().strip()

            if not nombre:
                QMessageBox.warning(
                    self,
                    "Campo vacío",
                    "Escribe el nuevo nombre."
                )
                return

            self.tabla_especialidades.setItem(
                fila, 1, QTableWidgetItem(nombre)
            )

            self.limpiar_especialidad()
            self.actualizar_especialidades()
            self.actualizar_medicos()
            self.actualizar_citas()

        def eliminar_especialidad(self):
            fila = self.tabla_especialidades.currentRow()

            if fila < 0:
                QMessageBox.warning(
                    self,
                    "Seleccionar registro",
                    "Selecciona una especialidad."
                )
                return

            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Deseas eliminar esta especialidad?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                self.tabla_especialidades.removeRow(fila)
                self.actualizar_especialidades()

        def limpiar_especialidad(self):
            self.nombre_especialidad.clear()

        def seleccionar_especialidad(self, fila, columna):
            nombre = self.tabla_especialidades.item(fila, 1)

            if nombre:
                self.nombre_especialidad.setText(nombre.text())

        def actualizar_especialidades(self):
            if hasattr(self, "especialidad_medico"):
                self.especialidad_medico.clear()
                self.especialidad_medico.addItem("Seleccionar especialidad")

                for fila in range(self.tabla_especialidades.rowCount()):
                    item = self.tabla_especialidades.item(fila, 1)
                    if item:
                        self.especialidad_medico.addItem(item.text())
