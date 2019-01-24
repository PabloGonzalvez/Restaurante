import locale

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import sqlite3
import calendar


class Maquina:
    def __init__(self):
        b = Gtk.Builder()
        b.add_from_file('restaurante.glade')

        self.venprincipal = b.get_object("venprincipal")
        self.mesa1=  b.get_object("mesa1")
        self.mesa2 = b.get_object("mesa2")
        self.mesa3 = b.get_object("mesa3")
        self.mesa4 = b.get_object("mesa4")
        self.mesa5 = b.get_object("mesa5")
        self.mesa6 = b.get_object("mesa6")
        self.mesa7 = b.get_object("mesa7")
        self.mesa8 = b.get_object("mesa8")
        self.notebook=b.get_object("notebook")
        self.error=b.get_object("error")
        self.venCalendar=b.get_object("venCalendar")
        self.calendar=b.get_object("calendar")
        self.meses = (
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
        'Diciembre')


        #login

        self.login=b.get_object("login")
        self.iniciasesion=b.get_object("iniciasesion")
        self.nombreCamarero=b.get_object("nombreCamarero")
        self.pwdCamarero=b.get_object("pwdCamarero")
        self.crearCamarero=b.get_object("crearCamarero")
        self.borrarCamareo=b.get_object("borrarCamarero")
        self.errorlogin=b.get_object("errorlogin")




        #cliente

        self.nombre1=b.get_object("nombre1")
        self.dni1=b.get_object("dni1")
        self.apellidos1=b.get_object("apellidos1")
        self.provincia1=b.get_object("provincia1")
        self.comunidad1=b.get_object("comunidad1")
        self.municipio1=b.get_object("municipio1")
        self.crearCliente=b.get_object("crearCliente1")
        self.borrarcliente=b.get_object("borrarClientes1")
        self.tree1=b.get_object("tree1")
        self.listaClientes=b.get_object("listaClientes")
        self.listaMunicipios=b.get_object("listaMunicipios")
        self.listaProvincias=b.get_object("listaProvincias")
        self.saludocamarero=b.get_object("saludocamarero")

         #Columnas Clientes
        self.nombre3 = b.get_object("nombre3")
        self.dni3 = b.get_object("dni3")
        self.apellidos3 = b.get_object("apellidos3")
        self.provincia3 = b.get_object("provincia3")
        self.comunidad3 = b.get_object("comunidad3")
        self.municipio3 = b.get_object("municipio3")

        #Productos

        self.servinombre=b.get_object("servinombre")
        self.serviprecio=b.get_object("serviprecio")
        self.tree2=b.get_object("tree2")
        self.listaservicios=b.get_object("listaservicios")

        #Columnas Servicios

        self.idservicio=b.get_object("idservicio")
        self.nombreservicio = b.get_object("nombreservicio")
        self.precioservicio = b.get_object("precioservicio")

        #Facturas


        self.mesaseleccionada=b.get_object("mesaseleccionada")
        self.numeropersonas=b.get_object("numeropersonas")
        self.facturaCamarero=b.get_object("facturaCamarero")
        self.combocli=b.get_object("combocli")
        self.fechaFactura=b.get_object("fechaFactura")
        self.seleccionaFecha=b.get_object("seleccionaFecha")
        self.tree3=b.get_object("tree3")
        self.listafacturas=b.get_object("listafacturas")

        #Columnas Facturas
        self.columnaidfactura=b.get_object("columnaidfactura")
        self.columnadnicliente = b.get_object("columnadnicliente")
        self.columnacamarero = b.get_object("columnacamarero")
        self.columnaidmesa = b.get_object("columnamesa")
        self.columnaidfecha = b.get_object("columnafecha")


        dic={"altaCliente": self.altaCliente,
             "borrarClientes": self.borrarClientes,
             "actualizarProvincias":self.actualizarProvincias,
             "actualizarMunicipios": self.actualizarMunicipios,
             "seleccionaCliente":self.seleccionarCliente,
             "crearservicio":self.altaServicio,
             "seleccionarServicio":self.seleccionarServicio,
             "borrarservicio":self.borrarServicio,
             "modificarServicio":self.modificarServicio,
             "mesa1": self.selMESA1,
             "mesa2": self.selMESA2,
             "mesa3": self.selMESA3,
             "mesa4": self.selMESA4,
             "mesa5": self.selMESA5,
             "mesa6": self.selMESA6,
             "mesa7": self.selMESA7,
             "mesa8": self.selMESA8,
             "inicia":self.iniciaSesion,
             "borracamarero":self.bajasCamarero,
             "altacamarero":self.altaCamarero,
             "iniciaCal":self.iniciaCal,
             "on_calendar_day_selected_double_click":self.FormatoFecha,
             "on_creaFactura_clicked":self.altaFactura}

        b.connect_signals(dic)

        self.venprincipal.connect('delete-event', lambda w, e: w.hide() or True)
        self.login.connect('delete-event', lambda w, e: w.hide() or True)
        self.venCalendar.connect('delete-event', lambda w, e: w.hide() or True)
        self.ConectaBBDD()
        self.cargaFacturas()
        self.cargaComunidad()
        self.cargaClientes()
        self.cargaServicios()
        self.cargaComboClientes()
        self.login.show()
        self.nombreCamarero.set_text("Admin")
        self.pwdCamarero.set_text("admin")





    def ConectaBBDD(self):
          # Establece conexion y estable el contenido
        try:
            self.conexion = sqlite3.Connection("Restaurante.sqlite")
            self.cur = self.conexion.cursor()
        except sqlite3.OperationalError as e:
            print(e)

    def cargaComunidad(self):

        i = 0
        self.cur.execute("select comunidad from comunidades  ")

        list = Gtk.ListStore(str)


        all_rows = self.cur.fetchall()
        list.clear()
        for row in all_rows:
            list.append([row[0]])
            i = i + 1


        for name in list:
            self.comunidad1.append_text(name[0])

    def actualizarProvincias(self, widget):

        self.comu = self.comunidad1.get_active_text()
        self.cargaProvincias()

    def actualizarMunicipios(self, widget):
        self.provi = self.provincia1.get_active_text()
        self.cargaMunicipios()

    def cargaProvincias(self):
        self.provincia1.remove_all()
        i = 0
        self.cur.execute(
            "select provincia from provincias where comunidad_id in (Select id from comunidades where comunidad='" + str(self.comu) + "')")

        list = Gtk.ListStore(str)

        all_rows = self.cur.fetchall()
        for row in all_rows:
            i = i + 1
            list.append([row[0]])

        for name in list:

            self.provincia1.append_text(name[0])


    def cargaMunicipios(self):
        self.municipio1.remove_all()
        i = 0
        self.cur.execute(
            "select municipio from municipios where provincia_id in (Select id from provincias where provincia='" + str(self.provi) + "')")
        row = self.cur.fetchone()
        list = Gtk.ListStore(str)

        all_rows = self.cur.fetchall()
        for row in all_rows:
            i = i + 1
            list.append([row[0]])

        for name in list:

            self.municipio1.append_text(name[0])



    def altaCliente(self,widget,data=None):
        dni = self.dni1.get_text()
        nombre = self.nombre1.get_text()
        apellido = self.apellidos1.get_text()

        if self.ValidarDni(dni):
            if nombre !="" or apellido!="":
                comunidad=self.comunidad1.get_active_text()
                if comunidad is not None:
                    provincia=self.provincia1.get_active_text()
                    if provincia is not None:

                        municipio=self.municipio1.get_active_text()
                        if municipio is not None:
                            fila = (dni, nombre, apellido,comunidad,provincia,municipio)
                            self.insertarCliente(fila)
                        else:
                            self.error.set_markup("<span color='red'>Error: Municipio No Seleccionado</span>")

                    else:
                        self.error.set_markup("<span color='red'>Error: Provincia No Seleccionada</span>")
                else:
                    self.error.set_markup("<span color='red'>Error: Comunidad No Seleecionada</span>")

            else:

                self.error.set_markup("<span color='red'>Debes cubrir todos los campos</span>")
        else:
            print("error")

    def seleccionarCliente(self,data=None):

            model, iter = self.tree1.get_selection().get_selected()
            if iter != None:
                self.dni1.set_text(model.get_value(iter, 0))
                self.nombre1.set_text(model.get_value(iter, 2))
                self.apellidos1.set_text(model.get_value(iter,1))


    def borrarClientes(self,data=None):
        self.cur.execute("delete from Clientes where Dni='" + self.dni1.get_text() + "'")

        self.conexion.commit()
        self.dni1.set_text("")
        self.nombre1.set_text("")
        self.apellidos1.set_text("")
        self.cargaClientes()


    def ValidarDni(self, dni):
            try:
                tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
                dig_ext = "XYZ"
                reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
                numeros = "1234567890"
                dni = dni.upper()
                if len(dni) == 9:
                    dig_control = dni[8]
                    dni = dni[:8]
                    if dni[0] in dig_ext:
                        dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                    if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                        self.error.set_text('')
                        return True
                    else:
                        self.error.set_markup("<span color='red'>Error: DNI no válido</span>")
                        return False
                else:
                    self.error.set_markup("<span color='red'>Error: DNI no válido</span>")
                    return False
            except:
                return False


    def insertarCliente(self,fila):
        try:
            self.cur.execute("insert into clientes (dni,nombre,apellidos,direccion,provincia,ciudad) values(?,?,?,?,?,?)",
                        fila)
            self.conexion.commit()
            self.cargaClientes()
        except sqlite3.OperationalError as e:
            print(e)
        self.cargaComboClientes()

    def cargaClientes(self):

        try:
            self.cur.execute("select * from Clientes")
            self.listado = self.cur.fetchall()
            self.listaClientes.clear()
            for n in self.listado:
                self.listaClientes.append(n)

        except sqlite3.Error as e:
            print(e)
            self.conexion.rollback()

    def altaServicio(self, widget, data=None):

        nombre = self.servinombre.get_text()
        precio = self.serviprecio.get_text()+" €"


        if nombre != "":

                if precio is not "":



                    fila = ( nombre,precio)
                    self.insertarServicio(fila)
                    self.serviprecio.set_text("")
                    self.servinombre.set_text("")


                else:
                    self.error.set_markup("<span color='red'>Error: Debe especificar un  precio</span>")
        else:
            self.error.set_markup("<span color='red'>Error: Nombre no seleccionado</span>")

    def insertarServicio(self,fila):
        try:
            self.cur.execute("insert into servicios (Servicio,PrecioUnidad) values(?,?)",
                        fila)
            self.conexion.commit()



            self.cargaServicios()
        except sqlite3.OperationalError as e:
            print(e)
    def cargaServicios(self):

        try:
            self.cur.execute("select * from Servicios")
            self.listado = self.cur.fetchall()
            self.listaservicios.clear()
            for n in self.listado:
                self.listaservicios.append(n)

        except sqlite3.Error as e:
            print(e)
            self.conexion.rollback()


    def seleccionarServicio(self,data=None):

            model, iter = self.tree2.get_selection().get_selected()
            if iter != None:
                self.servinombre.set_text(model.get_value(iter, 1))
                self.serviprecio.set_text(model.get_value(iter, 2))


    def borrarServicio(self, data=None):
        model, iter = self.tree2.get_selection().get_selected()
        if iter != None:
                self.cur.execute("delete from Servicios where Servicio='" +model.get_value(iter,1)+ "'")

                self.conexion.commit()
                self.serviprecio.set_text("")
                self.servinombre.set_text("")
                self.cargaServicios()
        else:
                self.error.set_markup("<span color='red'>Error: Selecciona un servicio antes</span>")

    def modificarServicio(self, data=None):
        model, iter = self.tree2.get_selection().get_selected()
        if iter != None:
            nuevonombre=self.servinombre.get_text()
            nuevoprecio=self.serviprecio.get_text()
            self.cur.execute("update  Servicios set Servicio='"+nuevonombre+"',PrecioUnidad ='"+nuevoprecio+"'  where IdServicio="+ str(model.get_value(iter, 0)) + "")
            self.conexion.commit()
            self.cargaServicios()
            self.serviprecio.set_text("")
            self.servinombre.set_text("")
        else:
            self.error.set_markup("<span color='red'>Error: Selecciona un servicio antes</span>")

    def selMESA1(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("1")
        self.numeropersonas.set_text("12")



    def selMESA2(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("2")
        self.numeropersonas.set_text("4")
    def selMESA3(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("3")
        self.numeropersonas.set_text("2")


    def selMESA4(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("4")
        self.numeropersonas.set_text("4")


    def selMESA5(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("5")
        self.numeropersonas.set_text("6")

    def selMESA6(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("6")
        self.numeropersonas.set_text("8")


    def selMESA7(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("7")
        self.numeropersonas.set_text("2")


    def selMESA8(self,data=None):
        self.notebook.set_current_page(2)
        self.mesaseleccionada.set_text("8")
        self.numeropersonas.set_text("10")





    def bajasCamarero(self,data=None):
        nombre = self.nombreCamarero.get_text()

        if len(nombre) > 0 :
            try:
                self.cur.execute("select nombre from camarero where nombre = '" + nombre + "'")
                nombre2 = str(self.cur.fetchone())


                if str(nombre2) != 'None':
                    try:
                        self.cur.execute("delete from Camarero where nombre='" + nombre + "'")
                        self.conexion.commit()
                        self.errorlogin.set_text("Usuario borrado con exito")

                        self.nombreCamarero.set_text("")
                        self.pwdCamarero.set_text("")

                    except sqlite3.OperationalError as e:
                        print(e)

                else:
                    self.errorlogin.set_text("Usuario no encontrado")
                    self.nombreCamarero.set_text("")
                    self.pwdCamarero.set_text("")

            except sqlite3.Error as e:
                print(e)
        else:
            self.errorlogin.set_text("Debe cubrir el nombre para borrar")



    def altaCamarero(self,data=None):
        nombre = self.nombreCamarero.get_text()
        pwd = self.pwdCamarero.get_text()
        if len(nombre) > 0 and len(pwd):
            try:
                self.cur.execute("select nombre from camarero where nombre = '" + nombre + "'")
                nombre2 = str(self.cur.fetchone())
                fila = (nombre, pwd)

                if str(nombre2) != 'None':
                        self.errorlogin.set_text("Usuario ya existente")
                        self.nombreCamarero.set_text("")
                        self.pwdCamarero.set_text("")
                else:
                    try:
                        self.cur.execute("insert into Camarero (Nombre,contrasena) values(?,?)",
                                                 fila)
                        self.conexion.commit()


                        self.errorlogin.set_text("Usuario registrado")
                        self.nombreCamarero.set_text("")
                        self.pwdCamarero.set_text("")

                    except sqlite3.OperationalError as e:
                            print(e)

            except sqlite3.Error as e:
                print(e)
        else:
            self.errorlogin.set_text("Debe cubrir todos los campos")

    def iniciaSesion(self,data=None):
        nombre = self.nombreCamarero.get_text()
        pwd = self.pwdCamarero.get_text()
        if len(nombre) > 0 and len(pwd):
            try:
                self.cur.execute("select nombre from camarero where nombre = '" + nombre + "'")
                nombre = str(self.cur.fetchone())
                for char in "(),'":
                    nombre = nombre.replace(char, '')
                    self.cur.execute("select contrasena from camarero where contrasena = '" + pwd + "'")
                    password = str(self.cur.fetchone())
                    for char in "(),'":
                        password = password.replace(char, '')
                        fila = (nombre, password)
                        self.conexion.commit()
                        if str(fila[0]) != 'None' and str(fila[1]) != 'None':
                            self.login.hide()
                            self.venprincipal.show()

                            self.saludocamarero.set_text("Hola "+nombre)
                            self.facturaCamarero.set_text(nombre)
                            self.nombreCamarero.set_text("")
                            self.pwdCamarero.set_text("")
                        else:
                            self.errorlogin.set_text("Usuario o contraseña no encontrado")
                            self.nombreCamarero.set_text("")
                            self.pwdCamarero.set_text("")

            except sqlite3.Error as e:
                print(e)




        else:
            self.errorlogin.set_text("Debe cubrir todos los campos")


    def iniciaCal(self, widget, data=None):
            self.venCalendar.show()
    def FormatoFecha(self, widget, Data=None): #Transforma el String de fecha
            agno, mes, dia = self.calendar.get_date()
            texto_dia = " %s" % dia
            texto_mes = " de %s" % self.meses[mes]
            texto_agno = " de  %s" % agno



            fecha = texto_dia + " " + texto_mes + " " + texto_agno
            self.fechaFactura.set_text(fecha)



            self.venCalendar.hide()
    def cargaComboClientes(self):

        i = 0
        self.cur.execute("select nombre from clientes  ")

        list = Gtk.ListStore(str)


        all_rows = self.cur.fetchall()
        list.clear()
        for row in all_rows:
            list.append([row[0]])
            i = i + 1
        for name in list:
            self.combocli.append_text(name[0])

    def altaFactura(self, widget, data=None):
        mesa = self.mesaseleccionada.get_text()
        camarero = self.facturaCamarero.get_text()
        pagado="No"


        if mesa != "" :
                self.cur.execute("select IdFactura from camarero where contrasena = '" + pwd + "'")

                cliente=self.combocli.get_active_text()
                if cliente is not None:
                    try:
                        self.cur.execute("select Dni from clientes where nombre = '" + cliente + "'")
                        dni = self.cur.fetchone()
                        for name in dni:
                            dni=name
                        print(dni)
                    except sqlite3.Error as e:
                        print(e)

                    fecha=self.fechaFactura.get_text()

                    if fecha !="":

                        fila = (dni, camarero, mesa, fecha,pagado)
                        self.insertarFactura(fila)

                    else:
                        self.error.set_markup("<span color='red'>Error: Fecha No Seleccionada</span>")
                else:
                    self.error.set_markup("<span color='red'>Error: Cliente no seleccionado</span>")

        else:

            self.error.set_markup("<span color='red'>Debes Selecionar una mesa</span>")


    def insertarFactura(self,fila):
        try:
            self.cur.execute("insert into facturas (Dnicliente,NombreCamarero,IdMesa,Fecha,Pagada) values(?,?,?,?,?)",
                        fila)
            self.conexion.commit()
        except sqlite3.Error as e:
            print(e)
        self.cargaFacturas()

    def cargaFacturas(self):

        try:
            self.cur.execute("select * from Facturas")
            self.listado = self.cur.fetchall()
            self.listafacturas.clear()
            for n in self.listado:
                self.listafacturas.append(n)

        except sqlite3.Error as e:
            print(e)
            self.conexion.rollback()




if __name__ == '__main__':
    main = Maquina()
    Gtk.main()