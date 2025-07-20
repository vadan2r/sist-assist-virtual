# sist-assist-virtual
Projeto DIO Criando um sistema de assistência virtual do zero. 

# Assistente Virtual Simples com Python

Este README guia você na criação de um assistente virtual básico utilizando Python, com foco na praticidade e efetividade. Utilizaremos as bibliotecas `speech_recognition`, `gtts`, `playsound` (para Text-to-Speech), `webbrowser`, e `wikipedia`.

**Pré-requisitos:**

*   Python 3.6+
*   Conexão com a internet (para reconhecimento de fala e algumas funcionalidades)

**Instalação:**

1.  **Crie um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    venv\Scripts\activate  # No Windows
    ```

2.  **Instale as bibliotecas necessárias:**

    ```bash
    pip install speech_recognition gTTS playsound wikipedia
    ```
    *   `speech_recognition`: Para reconhecimento de fala.
    *   `gTTS`: Google Text-to-Speech.
    *   `playsound`: Para reproduzir o áudio gerado pelo gTTS.
    *   `wikipedia`: Para acesso rápido a informações da Wikipédia.
    *   `webbrowser`: Para abrir páginas da web (YouTube, etc.).

**Implementação:**

1.  **Crie um arquivo Python (ex: `assistente.py`) e cole o seguinte código:**

    ```python
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
    ```

2.  **Executar o script:**

    ```bash
    python assistente.py
    ```

**Explicação do Código:**

*   **`ouvir_microfone()`**:  Utiliza `speech_recognition` para capturar o áudio do microfone, transcrevê-lo para texto usando a API do Google e retorna a frase. Trata erros comuns como a falta de compreensão ou problemas de conexão.
*   **`falar()`**:  Converte o texto fornecido em fala usando `gTTS`, salva como um arquivo `audio.mp3`, reproduz o áudio usando `playsound`, e remove o arquivo temporário.
*   **`processar_comando()`**:  Analisa o texto do comando, extrai palavras-chave e executa ações correspondentes.
    *   **Wikipedia**:  Procura um resumo do termo pesquisado no Wikipedia.
    *   **YouTube**:  Abre o YouTube no navegador.
    *   **Farmácia**: Abre o Google Maps pesquisando por farmácias próximas (implementação simplificada).
    *   **Saudações**: Responde a saudações básicas.
    *   **Desligar/Parar**: Encerra o loop principal.
*   **Loop Principal**:  Executa continuamente, ouvindo o microfone, processando o comando e repetindo até que o comando de desligamento seja recebido.

**Como Usar:**

1.  Execute o script `assistente.py`.
2.  O programa imprimirá "Diga alguma coisa!".
3.  Fale um comando para o microfone.
4.  O assistente responderá de acordo com o comando.
5.  Para sair, diga "Desligar" ou "Parar".

**Melhorias Possíveis (Próximos Passos):**

*   **Localização:** Integração com APIs de geolocalização para encontrar a farmácia *mais próxima* com base na sua localização real.  (Requer configuração de APIs e permissões de localização).
*   **Personalização:**  Implementar um sistema para aprender e responder a comandos personalizados.
*   **Intenção e Entidades (NLP Avançado):** Utilizar bibliotecas como `spaCy` ou `NLTK` para uma análise mais profunda da intenção do usuário e extrair entidades (por exemplo, o nome da música a ser tocada, o local para o qual navegar).  Isso permite comandos mais complexos e flexíveis.
*   **Integração com APIs:** Integrar com APIs de previsão do tempo, calendários, e-mail, etc., para fornecer informações mais úteis.
*   **Interface Gráfica (GUI):**  Criar uma interface gráfica para facilitar a interação com o assistente. (Tkinter, PyQt, etc.)
*   **Melhor Tratamento de Erros:**  Implementar um tratamento de erros mais robusto para lidar com falhas na conexão de rede, erros de reconhecimento de fala, etc.

**Considerações:**

*   **Privacidade:** Lembre-se que o `speech_recognition` usa a API do Google para reconhecimento de fala, o que significa que seus comandos de voz serão enviados para os servidores do Google.  Considere alternativas offline se a privacidade for uma preocupação primordial (mas a precisão do reconhecimento de fala será menor).
*   **Qualidade do Microfone:** A qualidade do reconhecimento de fala depende muito da qualidade do seu microfone.
*   **Requisitos da API do Google:** Você pode precisar configurar uma chave de API do Google para usar o `speech_recognition` de forma consistente, especialmente para uso extensivo. Verifique a documentação do `speech_recognition` para obter detalhes.
