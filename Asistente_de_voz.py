import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


nombre = input("Hola, ¿Cual es tu nombre? ")


# escuchar microfono y devolver audio como texto
def trasnformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar")

        # guardar lo que escuches como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-col")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("Ups no entendi")

            # devolver error
            return "Sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("Ups no hay servicio")

            # devolver error
            return "Sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendio el audio
            print("Ups, algo ha salido mal")

            # devolver error
            return "Sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():

    # crear variables con datos de hoy
    dia = datetime.date.today()


    # crear variable dia de la semana
    dia_semana = dia.weekday()


    # diccionario con nombre dias
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # decir dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")


# informar que hora es
def pedir_hora():

    # crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f" En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    # decir hora
    hablar(hora)


# funcion saludo inicial
def saludo_incial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    # decir el saludo
    hablar(f"Hola, {momento} {nombre}, soy Helena, tu asistente personal. Porfavor dime en que te puedo ayudar")


# funcion central del asistente
def pedir_cosas():

    # activar el saludo inicial
    saludo_incial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el microfono y guardar pedido en un string
        pedido = trasnformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("Con gusto, estoy abriendo youtube")
            webbrowser.open("https://www.youtube.com/")
            continue
        elif "abrir navegador" in pedido:
            hablar("Claro, ya estoy en eso")
            webbrowser.open("https://www.google.com/")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Buscandolo en wikipedia")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Ya mismo lo hago")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Buena idea, lo hare ahora mismo")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple": "APPL",
                       "amazon": "AMZN",
                       "google": "GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontré, el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("Perdon pero no la he encontrado")
        elif "adiós" in pedido:
            hablar(f"Esta bien {nombre}, me voy a descansar, cualquiera cosa me avisas.")
            break
            

pedir_cosas()

