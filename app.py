import flet as ft
from sql import ContactManager
from fpdf import FPDF
import pandas as pd
import datetime as dt 

class PDF(FPDF):
    def header(self):
        self.set_font('Arial','B',12)
        self.cell(0, 10, 'Contactos',0,1,'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C' )

class form(ft.Container):
    # constructor
    def __init__(self, page):
        super().__init__(expand=True)#<- expande el contenedor
        
        self.page = page
        self.datos = ContactManager() #<- Contenedor
        self.selected_row = None
        
        #component
        self.name =ft.TextField(label='Nombre',border_color='green')
        self.edad=ft.TextField(label='Edad',border_color='green',
                               input_filter=ft.NumbersOnlyInputFilter(),
                               max_length=2)
        self.correo = ft.TextField(label='Correo',border_color='green') 
        self.cel=ft.TextField(label='Teléfono',border_color='green',
                               input_filter=ft.NumbersOnlyInputFilter(),
                               max_length=8)
        self.search_fil=ft.TextField(label='Buscar'
                                ,suffix_icon=ft.icons.SEARCH
                                ,border=ft.InputBorder.UNDERLINE
                                ,border_color='black'
                                ,label_style=ft.TextStyle(color='white')
                                ,on_change=self.search_data
                                )
        
        self.data_table=ft.DataTable(
            expand=True
            ,border=ft.border.all(2,'green')
            ,data_row_color={ft.MaterialState.SELECTED:'purple'
                             ,ft.MaterialState.PRESSED:ft.colors.BLACK}
            ,border_radius=10
            ,show_checkbox_column=True
            ,columns=[
                ft.DataColumn(ft.Text('Nombre',color='green',weight='bold'))
                ,ft.DataColumn(ft.Text('Edad',color='green',weight='bold'),numeric=True)
                ,ft.DataColumn(ft.Text('Correo',color='green',weight='bold'))
                ,ft.DataColumn(ft.Text('Teléfono',color='green',weight='bold'))
                ]
        )
        
        self.show_data()
        
        # formulario 
        self.form = ft.Container(
            bgcolor='#222222',
            border_radius=10,
            col=4,
            padding=10
            ,content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND
                ,horizontal_alignment=ft.MainAxisAlignment.SPACE_AROUND
                ,controls=[
                    ft.Container(
                        content=ft.Row(
                            spacing=5
                            ,alignment=ft.MainAxisAlignment.CENTER
                            ,controls=[
                                ft.Text(
                               'Ingrese sus datos'
                               ,size=48
                               ,text_align='center'
                               ,font_family='vivaldi',
                                ),
                            ]
                        )
                    ),
                    self.name,
                    self.edad,
                    self.correo,
                    self.cel,
                    ft.Container(
                        content=ft.Row(
                            spacing=5,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.TextButton(
                                    'Guardar',
                                    icon=ft.icons.SAVE,
                                    style=ft.ButtonStyle(
                                        color='white',bgcolor='green'
                                    ),
                                    on_click=self.add_dt
                                ),
                                ft.TextButton(
                                    'Acualizar',
                                    icon=ft.icons.UPDATE,
                                    style=ft.ButtonStyle(
                                        color='white',bgcolor='green'
                                    )
                                    ,on_click=self.update_f
                                ),
                                ft.TextButton(
                                    'Borrar',
                                    icon=ft.icons.DELETE,
                                    style=ft.ButtonStyle(
                                        color='white',bgcolor='red'
                                    )
                                    ,on_click=self.delete_contact
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.table = ft.Container(
            bgcolor='#222222'
            ,border_radius=10
            ,col=8
            ,padding=20
            ,content=ft.Column(
                controls=[
                    ft.Container(
                        padding=10
                        ,content = ft.Row(
                            controls=[
                                self.search_fil
                                ,ft.IconButton(
                                    tooltip='editar'
                                    ,icon=ft.icons.EDIT
                                    ,icon_color='white'
                                    ,on_click=self.edit_fielfd
                                )
                                ,ft.IconButton(
                                    tooltip='Descargar en PDF'
                                    ,icon=ft.icons.PICTURE_AS_PDF
                                    ,icon_color='white'
                                    ,on_click=self.save_pdf1
                                )
                                ,ft.IconButton(
                                    tooltip='Descargar para Excel'
                                    ,icon=  ft.icons.SAVE_ALT
                                    ,icon_color='white'
                                    ,on_click= self.save_xlsx
                                )
                            ]
                        )
                    )
                    ,ft.Column(
                        expand=True
                        ,scroll='auto'
                        ,controls=[
                            ft.ResponsiveRow([self.data_table])
                        ]
                    )
                ]
            )
        )
        
        self.content = ft.ResponsiveRow(
            controls=[
                self.form,
                self.table
            ]
        )
    
    # ver datos 
    def show_data(self):
        self.data_table.rows=[]
        for x in self.datos.get_contact():
            self.data_table.rows.append(
                ft.DataRow(
                    on_select_changed=self.get_index,
                    cells=[
                         ft.DataCell(ft.Text(x[1]))
                        ,ft.DataCell(ft.Text( str(x[2])))
                        ,ft.DataCell(ft.Text(x[3]))
                        ,ft.DataCell(ft.Text(str(x[4])))
                    ]
                )
            )
        self.update()
    
    # añadir datos
    def add_dt(self, e):
        name=self.name.value
        edad=str(self.edad.value)
        correo=self.correo.value
        phone=str(self.cel.value)
        
        if len(name) and len(edad) and len(correo) and len(phone) >0:
            contact_exists=False
            for row in self.datos.get_contact():
                if row[1]==name:
                    contact_exists=True
                    break
            
            if not contact_exists:
                self.clean_fields()
                self.datos.adds(name=name,edad=edad,email=correo,phone=phone)
                self.show_data()
    
    # check box
    def get_index(self,e):
        if e.control.selected:
            e.control.selected=False
        else:
            e.control.selected=True
        
        name=e.control.cells[0].content.value
        for row in self.datos.get_contact():
            if row[1]==name:
                self.selected_row=row
                break
             
        self.update()

    # editar 
    def edit_fielfd (self, e):
        try:
            self.name.value=self.selected_row[1]
            self.edad.value= self.selected_row[2]
            self.correo.value= self.selected_row[3]
            self.cel.value= self.selected_row[4]
            self.update()
        except TypeError:
            print('Error')
    
    # actualizar 
    def update_f(self,e):
        name=self.name.value
        edad=str(self.edad.value)
        correo=self.correo.value
        phone=str(self.cel.value)
        
        if len(name) and len(edad) and len(correo) and len(phone) >0:
            self.clean_fields()
            self.datos.update__contact(contact_id=self.selected_row[0],name=name,edad=edad,email=correo, phone=phone)
            self.show_data()
    
    #busqueda    
    def search_data(self,e):
        busqueda = self.search_fil.value.lower()
        name=list( filter ( lambda x: busqueda in x[1].lower(), self.datos.get_contact() ) )
        self.data_table.rows=[]
        if not self.search_fil.value=='':
            if len(name)>0:
                for x in name:
                    self.data_table.rows.append(
                        ft.DataRow(
                            on_select_changed=self.get_index,
                            cells=[
                             ft.DataCell(ft.Text(x[1]))
                            ,ft.DataCell(ft.Text( str(x[2])))
                            ,ft.DataCell(ft.Text(x[3]))
                            ,ft.DataCell(ft.Text(str(x[4])))
                            ]
                        )
                    )
                self.update()
        else:
            self.show_data()
    
    # pdf download
    def save_pdf1(self, e):
        pdf=PDF()
        pdf.add_page()
        column_width=[10,40,20,80,40]
        data=self.datos.get_contact()
        header=('ID','NOMBRE','EDAD','CORREO','TELÉFONO')
        data.insert(0, header)
        for rown in data:
            for item,width in zip(rown,column_width):
                pdf.cell(width,10,str(item), border=1)
            pdf.ln()
        
        fill_name = dt.datetime.now()
        fill_name = fill_name.strftime('DATA %Y-%m-%d')+'.pdf'
        pdf.output(fill_name)
    
    def save_xlsx(self,e):
        fill_name = dt.datetime.now()
        fill_name = fill_name.strftime('DATA %Y-%m-%d')+'.xlsx'
        
        data = self.datos.get_contact ()
        df = pd.DataFrame(data, columns=['ID','NOMBRE','EDAD','CORREO','TELÉFONO'])
        df.to_excel(fill_name, index=False)
    
    def delete_contact(self,e):
        self.datos.delete__contacts(name=self.selected_row[1])
        self.show_data()
    
    
    # limpieza de datos
    def clean_fields(self):
        self.name.value=''
        self.edad.value=''
        self.correo.value=''
        self.cel.value=''
        
    def build(self):
        return self.content
        
def main (page: ft.Page):
    page.bgcolor= 'black'
    page.title='Crud with python and SQLite database'
    page.window_min_height=505
    page.window_min_width=320
    
    
    page.add(form(page))
    
    
    
ft.app(target=main)    