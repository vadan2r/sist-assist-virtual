import speech_recognition as sr
from gtts import gTTS
import playsound
import webbrowser
import wikipedia
import os

def ouvir_microfone():
    """Ouve o microfone e retorna o texto transcrito."""
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        print("Diga alguma coisa!")
        audio = microfone.listen(source)

    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        print("Você disse: " + frase)

    except sr.UnknownValueError:
        print("Não entendi")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

    return frase

def falar(texto):
    """Converte texto em fala e reproduz."""
    tts = gTTS(text=texto, lang='pt-BR')
    nome_arquivo = "audio.mp3"
    tts.save(nome_arquivo)
    playsound.playsound(nome_arquivo)
    os.remove(nome_arquivo) # Limpa o arquivo de áudio após a reprodução

def processar_comando(comando):
    """Processa o comando de voz."""
    if comando is None:
        return

    comando = comando.lower()

    if "wikipedia" in comando:
        try:
            falar("Pesquisando no Wikipedia...")
            termo = comando.replace("wikipedia", "").strip()
            resultado = wikipedia.summary(termo, sentences=2)  # Obtém um resumo curto
            falar(resultado)
        except wikipedia.exceptions.PageError:
            falar("Não encontrei nada sobre isso na Wikipedia.")
        except wikipedia.exceptions.DisambiguationError as e:
            falar("Encontrei várias opções.  Você pode ser mais específico?")
            print(e)

    elif "youtube" in comando:
        falar("Abrindo o YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif "farmácia" in comando:  # Simulação simples - localização não implementada
        falar("Abrindo o Google Maps para procurar farmácias próximas...") #Simula a ação
        webbrowser.open("https://www.google.com/maps/search/farmacias+proximas")

    elif "olá" in comando or "oi" in comando:
        falar("Olá! Como posso ajudar?")

    elif "desligar" in comando or "parar" in comando:
        falar("Desligando...")
        return False

    else:
        falar("Não entendi o comando. Pode repetir?")

    return True

# Loop principal
continuar = True
while continuar:
    comando = ouvir_microfone()
    continuar = processar_comando(comando)

print("Programa encerrado.")