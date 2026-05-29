#Validacion con while - Contrase;a correcta
print("Bienvenido")
while True:
    contrasena = input("Ingrese la contraseña: ")
    if contrasena == "python123":
        print("contraseña correcta") 
        break
    else:
        print("Contraseña incorrecta")
        