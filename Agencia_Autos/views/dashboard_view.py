import matplotlib.pyplot as plt
from models.servicio import Servicio

class DashboardView:
    def __init__(self):
        self.servicio_model = Servicio()
    
    def show(self):
        while True:
            print("\n" + "="*50)
            print("         TABLERO DE CONTROL")
            print("="*50)
            print("1. Ver gráfica de servicios (Total)")
            print("2. Ver gráfica de servicios (Hoy)")
            print("3. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.show_chart('total')
            elif opcion == "2":
                self.show_chart('hoy')
            elif opcion == "3":
                break
            else:
                print("Opción inválida")
    
    def show_chart(self, filtro):
        estadisticas = self.servicio_model.get_estadisticas()
        
        if filtro == 'hoy':
            # Filtrar solo servicios de hoy
            servicios = self.servicio_model.get_all()
            from datetime import datetime
            hoy = datetime.now().date()
            servicios_hoy = [s for s in servicios if s['fecha_registro'] == hoy]
            
            conteo = {'En espera': 0, 'En proceso': 0, 'Finalizado': 0}
            for s in servicios_hoy:
                conteo[s['estatus']] += 1
            
            statuses = list(conteo.keys())
            counts = list(conteo.values())
        else:
            statuses = [e['estatus'] for e in estadisticas]
            counts = [e['cantidad'] for e in estadisticas]
        
        plt.figure(figsize=(10, 6))
        plt.bar(statuses, counts, color=['yellow', 'orange', 'green'])
        plt.title(f'Estado de Servicios - {"Hoy" if filtro == "hoy" else "Total"}')
        plt.xlabel('Estado')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        
        for i, v in enumerate(counts):
            plt.text(i, v + 0.5, str(v), ha='center')
        
        plt.tight_layout()
        plt.show()