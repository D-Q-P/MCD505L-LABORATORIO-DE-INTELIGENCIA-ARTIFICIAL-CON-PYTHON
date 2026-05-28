PRESUPUESTO = 12000
monto = float(input("Ingrese el monto de la compra: RD$"))

print("Se ha excedido el limite" if monto > 11250
      else "Tiene bastante dinero disponible" if monto < 2500
      else "Ha hecho un compra óptima")