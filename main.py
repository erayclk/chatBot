import tkinter as tk
from tkinter import ttk, scrolledtext, font
from PIL import Image, ImageTk
import openai
import time
import speech_recognition as sr
from translate import Translator
from gtts import gTTS
import random
import os
from playsound import playsound
import threading
from PIL import Image, ImageTk, ImageSequence

before_talks = []
bot_response = ""
user_input_text = ""
grammer_error = 0

translator = Translator(to_lang="tr")
translation = translator.translate("Hello, how are you?")

print(translation)


class ColorfulChat(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("you look lonely")
        self.geometry("1035x450")
        self.resizable(False, False)

        # Stil oluştur
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#FFEF96")
        self.style.configure("TButton", background="#FF6347", font=("Helvetica", 12))
        self.style.configure("TLabel", background="#FFEF96", font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", background="#FAD02E", font=("Helvetica", 12))
        self.style.configure("TText", background="#FAD02E", font=("Helvetica", 12))

        self.gif_path = "image.gif"
        self.load_gif()
        self.create_widgets()

    def load_gif(self):
        self.gif = Image.open(self.gif_path)
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(self.gif)]

    def play_gif(self):
        # Butona basıldığında gif'in hareket etmesi için animate fonksiyonunu çağır
        self.animate(0)

    def animate(self, frame_num):
        # Gif'i güncelle
        self.label.config(image=self.frames[frame_num])

        # Bir sonraki kareye geçmek için rekürsif olarak çağrı yap
        frame_num = (frame_num + 1) % len(self.frames)
        self.after_id = self.after(35, self.animate, frame_num)

    def stop_gif(self):
        print("DEBUG: Stop button pressed.")
        # Durdur butonuna basıldığında animasyonu durdur
        self.after_cancel(self.after_id)

    def on_enter_pressed(self, event):
        # Entry widget'ının içeriğini al
        entry_content = self.user_input.get()
        self.send_message()

    def create_widgets(self):

        self.bg_image = ImageTk.PhotoImage(file="you-look-lonely-cyberpunk-edgerunners-thumb.png")
        background_label = tk.Label(self, image=self.bg_image)
        background_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(self, image=self.frames[0])
        self.label.place(x=600,y=50)


        self.message_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED)

        self.message_display.place(x=20, y=20)
        self.fnt = tk.font.Font(family="Helvetica", size=13, weight="bold", underline=0)
        self.message_display.config(font=self.fnt)

        # Kullanıcı girişi

        self.user_in = tk.StringVar()
        self.user_input = ttk.Entry(self, width=93, textvariable=self.user_in)
        self.user_input.bind('<Return>', self.on_enter_pressed)
        self.user_input.place(x=21, y=412)

        self.translate = tk.Button(self, text="Çevir", command=self.ceviri)
        self.translate.place(x=620, y=412)

        self.micro = tk.Button(self, text="Ses Kayıt", command=self.microAktif)
        self.micro.place(x=730, y=412)

        # Gönder düğmesi
        send_button = ttk.Button(self, text="Send", command=self.send_message)
        send_button.place(x=800, y=412)

    def ceviri(self):
        global bot_response
        global before_talks
        second_window = tk.Toplevel(self)
        second_window.title("Türkçe Çevirisi")
        second_window.geometry("582x410")

        message_display2 = scrolledtext.ScrolledText(second_window, width=60, height=20, wrap=tk.WORD)
        fnt = tk.font.Font(family="Helvetica", size=13, weight="bold", underline=0)
        message_display2.config(font=fnt)
        message_display2.place(x=5, y=5)

        print(before_talks)
        for i in before_talks:
            message_display2.insert(tk.END, f"ing:{i}\n")
            translator = Translator(to_lang="tr")
            translation = translator.translate(i)
            message_display2.insert(tk.END, f"tr:{translation}\n")

    def microAktif(self):
        global user_input_text
        rec = sr.Recognizer()

        with sr.Microphone() as mic:
            rec.adjust_for_ambient_noise(mic)
            print("Say something!")
            audio = rec.listen(mic)

            print(rec.recognize_google(audio))
            self.user_in.set(rec.recognize_google(audio))
            user_input_text = self.user_in.get()

    def send_message(self):
        print(self.user_input.get())
        global bot_response
        user_input_text = self.user_input.get().strip()

        if user_input_text:
            self.message_display.config(state=tk.NORMAL)
            self.message_display.insert(tk.END, "You: " + (user_input_text) + "\n", "user_message")
            # Sohbet botu mantığı
            bot_response = self.chat_logic(user_input_text)
            self.grammer_check(user_input_text)

        def textin():
            self.message_display.insert(tk.END, "Joe: " + bot_response + "\n", )
            self.message_display.config(state=tk.DISABLED)
            self.user_input.delete(0, tk.END)

        def sound():
            print("Bot response: " + bot_response)
            # global anahtar kelimesini kullanarak bot_response'un global değişken olduğunu belirtin
            if bot_response:
                tts = gTTS(bot_response, lang='en')
                rand = random.randint(1, 10000)
                file = 'audio' + str(rand) + '.mp3'
                tts.save(file)
                self.animate(0)
                playsound(file)
                self.stop_gif()

                os.remove(file)
            print("55555")

        before_talks.append(bot_response)

        thread3 = threading.Thread(target=textin)
        thread3.start()

        thread4 = threading.Thread(target=sound)
        thread4.start()

    def chat_logic(self, user_input):
        # Initialize the client
        client = openai.OpenAI(
            api_key='your-apikey'
        )

        # Step 1: Create an Assistant
        assistant = client.beta.assistants.create(
            name="Joe",
            instructions=f""" 
                previous conversations = {before_talks}
                1- You are an English teacher.
                2- Write a sentence to continue the short conversation on line 1.
                3-Answer like a friend and don't answer to anyone else except your question.
                4-Don't write sentences like "Here's a sentence to keep things short."
                5-The sentences should be short and consist of a few sentences.
                6-Answer in 25 words or less    
                """,
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo-16k"
        )

        # Step 2: Create a Thread
        thread = client.beta.threads.create()

        # Step 3: Add a Message to a Thread
        if self.user_in != '':
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=(f"""
                                previous conversations = {before_talks}
                                1- You are an English teacher.
                                2- Write a sentence to continue the short conversation on line 1.
                                3-Answer like a friend and don't answer to anyone else except your question.
                                4-Don't write sentences like "Here's a sentence to keep things short."
                                5-The sentences should be short and consist of a few sentences.
                                6-Answer in 25 words or less
                                User's message: """ + self.user_input.get()
                         )
            )

        else:
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=(f"""        previous conversations = {before_talks}
                                        1- You are an English teacher.
                                        2- Write a sentence to continue the short conversation on line 1.
                                        3-Answer like a friend and don't answer to anyone else except your question.
                                        4-Don't write sentences like "Here's a sentence to keep things short."
                                        5-The sentences should be short and consist of a few sentences.
                                        6-Answer in 45 words or less
                                        User's message: """ + self.user_in.get()
                         ))

        # Step 4: Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please address the user as Officer K. The user has a premium account."
        )

        while True:
            print("*****")
            # Retrieve the run status
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )

                # Loop through messages and print content based on role
                for msg in messages.data:
                    print(msg)
                    role = msg.role
                    content = msg.content[0].text.value
                    if role != "user":
                        return f"{content}"

    def grammer_check(self, user_input):
        print("oooo")
        client = openai.OpenAI(
            api_key='your-apikey'
        )
        assistant2 = client.beta.assistants.create(
            name="bot2",
            instructions=""" 

                                If there is a grammatical error, just write -1 and nothing else.
                                Do not write any other explanation. Only if you find a grammatical error, write -1. If there is no grammatical error, write 0.

                                """,
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo-16k"
        )
        # Step 2: Create a Thread
        thread2 = client.beta.threads.create()

        message2 = client.beta.threads.messages.create(
            thread_id=thread2.id,
            role="user",
            content=("""
                                            If there is a grammatical error, just write -1 and nothing else.
                                            Do not write any other explanation. Only if you find a grammatical error, write -1. If there is no grammatical error, write 0.

                                            User's message: """ + self.user_input.get()
                     )
        )

        run2 = client.beta.threads.runs.create(
            thread_id=thread2.id,
            assistant_id=assistant2.id,
            instructions="Please address the user as Officer K. The user has a premium account."
        )

        run_status2 = client.beta.threads.runs.retrieve(
            thread_id=thread2.id,
            run_id=run2.id
        )
        while True:
            print("--")

            # Retrieve the run status
            run_status2 = client.beta.threads.runs.retrieve(
                thread_id=thread2.id,
                run_id=run2.id
            )


            # If run is completed, get messages
            if run_status2.status == 'completed':
                messages2 = client.beta.threads.messages.list(
                    thread_id=thread2.id
                )

                # Loop through messages and print content based on role
                for msg2 in messages2.data:
                    print(msg2)
                    role = msg2.role
                    content2 = msg2.content[0].text.value
                    if role != "user":
                        print(f"{role.capitalize()}: {content2}")
                        print("aaa")
                        print(content2.split())
                        if int(content2.strip()) == -1:
                            self.message_display.configure(bg="red")
                        else:
                            self.message_display.configure(bg="white")

                        break

                break


if __name__ == "__main__":
    app = ColorfulChat()
    app.mainloop()
