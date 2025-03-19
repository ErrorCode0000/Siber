import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import random
from datetime import datetime
import requests

class CocukSiberGuvenlik:
    def __init__(self, root):
        self.root = root
        self.root.title("Siber Kahraman - Çocuklar için Siber Güvenlik")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFE5E5")

        # Renkler ve stiller
        self.colors = {
            'primary': '#FFE5E5',
            'secondary': '#FFC4C4',
            'button': '#FF9EAA',
            'success': '#77DD77',
            'warning': '#FFB347'
        }

        # Stil tanımlamaları
        style = ttk.Style()
        style.configure("Title.TLabel", font=('Comic Sans MS', 24, 'bold'), background=self.colors['primary'])
        style.configure("Custom.TLabel", font=('Comic Sans MS', 12), background=self.colors['primary'])
        style.configure("Custom.TFrame", background=self.colors['primary'])

        # Ana frame
        self.main_frame = ttk.Frame(root, style="Custom.TFrame")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Kullanıcı verileri
        self.users = self.load_users()
        self.current_user = None
        self.points = 0
        self.selected_character = None

        # Başarı rozetleri tanımlamaları
        self.badges = {
            "internet_expert": {"name": "İnternet Uzmanı", "description": "5 internet güvenliği testini başarıyla tamamla"},
            "password_master": {"name": "Şifre Ustası", "description": "3 güçlü şifre oluştur"},
            "cyber_hero": {"name": "Siber Kahraman", "description": "Tüm güvenlik görevlerini tamamla"},
            "helper_badge": {"name": "Yardımsever", "description": "3 arkadaşına siber güvenliği öğret"},
            "quiz_champion": {"name": "Quiz Şampiyonu", "description": "100 puan topla"}
        }

        # Siber güvenlik haberleri
        self.news_data = [
            {
                "title": "Yeni Çocuk Oyunu Güvenlik Önlemleri",
                "content": "Popüler çocuk oyunlarına yeni güvenlik özellikleri eklendi!"
            },
            {
                "title": "İnternet Güvenliği Haftası",
                "content": "Bu hafta okullarda internet güvenliği etkinlikleri düzenleniyor."
            },
            {
                "title": "Güvenli İnternet Günü",
                "content": "Yarın Güvenli İnternet Günü! Özel etkinlikleri kaçırma!"
            }
        ]

        self.show_welcome_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Siber Kahramanlara Hoş Geldin!",
                  style="Title.TLabel").pack(pady=20)

        # Karakter seçimi
        character_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        character_frame.pack(pady=20)

        ttk.Label(character_frame,
                  text="Karakterini Seç:",
                  style="Custom.TLabel").pack(pady=10)

        characters = ["Siber Ninja", "Veri Koruyucusu", "Ağ Dedektifi"]
        self.selected_character = tk.StringVar(value=characters[0])

        for char in characters:
            ttk.Radiobutton(character_frame,
                            text=char,
                            variable=self.selected_character,
                            value=char).pack(pady=5)

        # Giriş ve kayıt butonları
        button_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        button_frame.pack(pady=20)

        tk.Button(button_frame,
                  text="Giriş Yap",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['button'],
                  fg='white',
                  command=self.show_login_screen).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame,
                  text="Yeni Kahraman Oluştur",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['success'],
                  fg='white',
                  command=self.show_register_screen).pack(side=tk.LEFT, padx=10)

    def show_login_screen(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Süper Kahraman Girişi",
                  style="Title.TLabel").pack(pady=20)

        login_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        login_frame.pack(pady=20)

        ttk.Label(login_frame,
                  text="Süper Kahraman Adın:",
                  style="Custom.TLabel").pack(pady=5)
        username_entry = ttk.Entry(login_frame, font=('Comic Sans MS', 12))
        username_entry.pack(pady=5)

        ttk.Label(login_frame,
                  text="Gizli Şifren:",
                  style="Custom.TLabel").pack(pady=5)
        password_entry = ttk.Entry(login_frame, show="★", font=('Comic Sans MS', 12))
        password_entry.pack(pady=5)

        tk.Button(login_frame,
                  text="Maceraya Başla!",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['button'],
                  fg='white',
                  command=lambda: self.login(
                      username_entry.get(),
                      password_entry.get()
                  )).pack(pady=10)

        tk.Button(login_frame,
                  text="Geri Dön",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=self.show_welcome_screen).pack(pady=5)

    def show_register_screen(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Yeni Kahraman Oluştur",
                  style="Title.TLabel").pack(pady=20)

        register_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        register_frame.pack(pady=20)

        ttk.Label(register_frame,
                  text="Süper Kahraman Adın:",
                  style="Custom.TLabel").pack(pady=5)
        username_entry = ttk.Entry(register_frame, font=('Comic Sans MS', 12))
        username_entry.pack(pady=5)

        ttk.Label(register_frame,
                  text="Gizli Şifren:",
                  style="Custom.TLabel").pack(pady=5)
        password_entry = ttk.Entry(register_frame, show="★", font=('Comic Sans MS', 12))
        password_entry.pack(pady=5)

        ttk.Label(register_frame,
                  text="Gizli Şifreni Tekrar Yaz:",
                  style="Custom.TLabel").pack(pady=5)
        password_confirm_entry = ttk.Entry(register_frame, show="★", font=('Comic Sans MS', 12))
        password_confirm_entry.pack(pady=5)

        tk.Button(register_frame,
                  text="Maceraya Başla!",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['button'],
                  fg='white',
                  command=lambda: self.register(
                      username_entry.get(),
                      password_entry.get(),
                      password_confirm_entry.get()
                  )).pack(pady=10)

        tk.Button(register_frame,
                  text="Geri Dön",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=self.show_welcome_screen).pack(pady=5)

    def register(self, username, password, password_confirm):
        if not username or not password:
            messagebox.showerror("Hata", "Tüm alanları doldurmalısın!")
            return

        if password != password_confirm:
            messagebox.showerror("Hata", "Şifreler aynı değil!")
            return

        if username in self.users:
            messagebox.showerror("Hata", "Bu süper kahraman adı zaten kullanılıyor!")
            return

        self.users[username] = {
            "password": password,
            "character": self.selected_character.get(),
            "join_date": str(datetime.now()),
            "points": 0,
            "badges": []
        }
        self.save_users()
        messagebox.showinfo("Başarılı", "Süper kahraman kimliğin oluşturuldu!")
        self.current_user = username
        self.points = 0
        self.show_main_menu()

    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.points = self.users[username].get("points", 0)
            self.show_main_menu()
        else:
            messagebox.showerror("Hata", "Yanlış süper kahraman adı veya şifre!")

    def show_main_menu(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text=f"Hoş geldin {self.current_user}!",
                  style="Title.TLabel").pack(pady=20)

        ttk.Label(self.main_frame,
                  text=f"Süper Puanların: {self.points}",
                  style="Custom.TLabel").pack(pady=10)

        menu_items = [
            ("İnternet Güvenliği Macerası", "internet"),
            ("Şifre Süper Kahramanı", "password"),
            ("Siber Zorbalıkla Mücadele", "bullying"),
            ("Güvenli Oyun Dünyası", "games"),
            ("Süper Kahraman Görevleri", "missions"),
            ("Siber Güvenlik Haberleri", self.show_cyber_news),
            ("Rozetlerim", self.show_badges),
            ("Profil Ayarları", self.show_profile_settings)
        ]

        for text, command in menu_items:
            tk.Button(self.main_frame,
                      text=text,
                      font=('Comic Sans MS', 12),
                      bg=self.colors['button'],
                      fg='white',
                      command=command if callable(command) else lambda c=command: self.show_lesson(c)).pack(pady=10)

    def show_lesson(self, lesson_type):
        self.clear_frame()

        lessons = {
            "internet": {
                "title": "İnternet Güvenliği Macerası",
                "topics": [
                    "Güvenli Web Siteleri Nasıl Anlaşılır?",
                    "Kişisel Bilgilerimizi Nasıl Koruruz?",
                    "İnternette Kiminle Konuşmalıyız?"
                ]
            },
            "password": {
                "title": "Şifre Süper Kahramanı",
                "topics": [
                    "Güçlü Şifre Nasıl Oluşturulur?",
                    "Şifrelerimizi Nasıl Korumalıyız?",
                    "Şifre Güvenlik Testi"
                ]
            },
            "bullying": {
                "title": "Siber Zorbalıkla Mücadele",
                "topics": [
                    "Siber Zorbalık Nedir?",
                    "Zorbalıkla Karşılaşınca Ne Yapmalıyız?",
                    "Arkadaşlarımızı Nasıl Koruruz?"
                ]
            }
        }

        lesson = lessons.get(lesson_type)
        if lesson:
            ttk.Label(self.main_frame,
                      text=lesson["title"],
                      style="Title.TLabel").pack(pady=20)

            for topic in lesson["topics"]:
                tk.Button(self.main_frame,
                          text=topic,
                          font=('Comic Sans MS', 12),
                          bg=self.colors['button'],
                          fg='white',
                          command=lambda t=topic: self.show_topic(lesson_type, t)).pack(pady=10)

            tk.Button(self.main_frame,
                      text="Ana Menüye Dön",
                      font=('Comic Sans MS', 12),
                      bg=self.colors['warning'],
                      fg='white',
                      command=self.show_main_menu).pack(pady=20)

    def show_topic(self, lesson_type, topic):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text=topic,
                  style="Title.TLabel").pack(pady=20)

        content_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        content_frame.pack(pady=20)

        if lesson_type == "internet":
            self.show_internet_safety_content(content_frame, topic)
        elif lesson_type == "password":
            self.show_password_safety_content(content_frame, topic)
        elif lesson_type == "bullying":
            self.show_cyberbullying_content(content_frame, topic)

        tk.Button(self.main_frame,
                  text="Ana Menüye Dön",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=self.show_main_menu).pack(pady=10)

    def show_internet_safety_content(self, frame, topic):
        if topic == "Güvenli Web Siteleri Nasıl Anlaşılır?":
            content = """
            🌟 Güvenli web sitelerinin özellikleri:

            1. Adres çubuğunda kilit işareti var
            2. Web adresi 'https://' ile başlıyor
            3. Yazım hataları yok
            4. Anne-babamız bu siteyi biliyor
            """
        elif topic == "Kişisel Bilgilerimizi Nasıl Koruruz?":
            content = """
            🌟 Kişisel bilgilerimizi koruma kuralları:

            1. Adımızı, adresimizi internette paylaşmıyoruz
            2. Fotoğraflarımızı izinsiz paylaşmıyoruz
            3. Ailemize danışmadan form doldurmuyoruz
            4. Şifrelerimizi kimseyle paylaşmıyoruz
            """
        else:
            content = """
            🌟 İnternette güvenli sohbet kuralları:

            1. Sadece tanıdığımız kişilerle konuşuyoruz
            2. Yabancılardan gelen mesajları açmıyoruz
            3. Rahatsız olduğumuz durumları ailemize söylüyoruz
            4. Özel bilgilerimizi paylaşmıyoruz
            """

        ttk.Label(frame,
                  text=content,
                  style="Custom.TLabel",
                  wraplength=500).pack(pady=10)

    def show_password_safety_content(self, frame, topic):
        if topic == "Güçlü Şifre Nasıl Oluşturulur?":
            content = """
            🌟 Süper güçlü şifre oluşturma rehberi:

            1. En az 8 karakter kullan
            2. Büyük ve küçük harfler ekle
            3. Sayılar ekle
            4. Özel karakterler kullan (!,@,#)
            5. Kolay tahmin edilebilir bilgiler kullanma
            """
        elif topic == "Şifrelerimizi Nasıl Korumalıyız?":
            content = """
            🌟 Şifre koruma kuralları:

            1. Şifreni kimseyle paylaşma
            2. Her hesap için farklı şifre kullan
            3. Şifrelerini düzenli olarak değiştir
            4. Şifrelerini güvenli bir yerde sakla
            """
        else:
            content = """
            🌟 Şifre güvenlik testi:

            Hadi şifreni test edelim!
            (Not: Gerçek şifreni yazma, örnek bir şifre dene)
            """

        ttk.Label(frame,
                  text=content,
                  style="Custom.TLabel",
                  wraplength=500).pack(pady=10)

    def show_cyberbullying_content(self, frame, topic):
        if topic == "Siber Zorbalık Nedir?":
            content = """
            🌟 Siber zorbalığı tanıyalım:

            1. İnternette başkalarına kötü davranmak
            2. Kırıcı mesajlar göndermek
            3. İzinsiz fotoğraf paylaşmak
            4. Başkalarını oyunlardan dışlamak
            """
        elif topic == "Zorbalıkla Karşılaşınca Ne Yapmalıyız?":
            content = """
            🌟 Siber zorbalıkla mücadele adımları:

            1. Sakin ol ve cevap verme
            2. Ekran görüntüsü al
            3. Hemen bir büyüğüne söyle
            4. Zorbalık yapan kişiyi engelle
            """
        else:
            content = """
            🌟 Arkadaşlarımızı koruma rehberi:

            1. Zorbalığa tanık olunca sessiz kalma
            2. Arkadaşına destek ol
            3. Büyüklerine haber ver
            4. İyi bir örnek ol
            """

        ttk.Label(frame,
                  text=content,
                  style="Custom.TLabel",
                  wraplength=500).pack(pady=10)

    def show_profile_settings(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Profil Ayarları",
                  style="Title.TLabel").pack(pady=20)

        settings_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        settings_frame.pack(pady=20)

        ttk.Label(settings_frame,
                  text="Karakterini Değiştir:",
                  style="Custom.TLabel").pack(pady=5)

        characters = ["Siber Ninja", "Veri Koruyucusu", "Ağ Dedektifi"]
        character_var = tk.StringVar(value=self.users[self.current_user]["character"])

        for char in characters:
            ttk.Radiobutton(settings_frame,
                            text=char,
                            variable=character_var,
                            value=char).pack(pady=5)

        ttk.Label(settings_frame,
                  text="Yeni Şifre:",
                  style="Custom.TLabel").pack(pady=5)
        new_password_entry = ttk.Entry(settings_frame, show="★", font=('Comic Sans MS', 12))
        new_password_entry.pack(pady=5)

        ttk.Label(settings_frame,
                  text="Yeni Şifre Tekrar:",
                  style="Custom.TLabel").pack(pady=5)
        new_password_confirm_entry = ttk.Entry(settings_frame, show="★", font=('Comic Sans MS', 12))
        new_password_confirm_entry.pack(pady=5)

        def save_profile_changes():
            new_password = new_password_entry.get()
            new_password_confirm = new_password_confirm_entry.get()

            if new_password:
                if new_password != new_password_confirm:
                    messagebox.showerror("Hata", "Yeni şifreler eşleşmiyor!")
                    return
                self.users[self.current_user]["password"] = new_password

            self.users[self.current_user]["character"] = character_var.get()
            self.save_users()
            messagebox.showinfo("Başarılı", "Profil bilgilerin güncellendi!")
            self.show_main_menu()

        tk.Button(settings_frame,
                  text="Değişiklikleri Kaydet",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['success'],
                  fg='white',
                  command=save_profile_changes).pack(pady=10)

        tk.Button(settings_frame,
                  text="Geri Dön",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=self.show_main_menu).pack(pady=5)

    def show_badges(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Başarı Rozetlerim",
                  style="Title.TLabel").pack(pady=20)

        badges_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        badges_frame.pack(pady=20)

        user_badges = self.users[self.current_user].get("badges", [])

        for badge_id, badge_info in self.badges.items():
            badge_frame = ttk.Frame(badges_frame, style="Custom.TFrame")
            badge_frame.pack(pady=10, fill='x')

            status = "✅" if badge_id in user_badges else "🔒"

            ttk.Label(badge_frame,
                      text=f"{status} {badge_info['name']}",
                      style="Custom.TLabel").pack(side=tk.LEFT, padx=5)

            ttk.Label(badge_frame,
                      text=badge_info['description'],
                      style="Custom.TLabel").pack(side=tk.LEFT, padx=5)

        tk.Button(self.main_frame,
                  text="Ana Menüye Dön",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=self.show_main_menu).pack(pady=20)

    def show_cyber_news(self):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Siber Güvenlik Haberleri",
                  style="Title.TLabel").pack(pady=20)

        news_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        news_frame.pack(pady=20, fill='x', padx=20)

        for news in self.news_data:
            news_item = ttk.Frame(news_frame, style="Custom.TFrame")
            news_item.pack(pady=10, fill='x')

            ttk.Label(news_item,
                      text=f"📰 {news['title']}",
                      style="Custom.TLabel",
                      font=('Comic Sans MS', 14, 'bold')).pack(anchor='w')

            ttk.Label(news_item,
                      text=news['content'],
                      style="Custom.TLabel",
                      wraplength=600).pack(anchor='w', pady=5)

        tk.Button(self.main_frame,
                  text="Haberleri Yenile",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['success'],
                  fg='white',
                  command=self.refresh_news).pack(pady=10)

        tk.Button(self.main_frame,
                  text="Ana Menüye Dön",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=self.show_main_menu).pack(pady=10)

    def refresh_news(self):
        new_news = {
            "title": f"Yeni Güvenlik İpucu #{random.randint(1, 100)}",
            "content": random.choice([
                "Şifrelerini düzenli olarak değiştirmeyi unutma!",
                "Tanımadığın kişilerden gelen mesajları açma!",
                "Güvenli olmayan web sitelerine dikkat et!",
                "Kişisel bilgilerini internette paylaşma!",
                "Şüpheli linklere tıklama!"
            ])
        }
        self.news_data.insert(0, new_news)
        if len(self.news_data) > 5:
            self.news_data.pop()

        self.show_cyber_news()
        messagebox.showinfo("Başarılı", "Haberler güncellendi!")

    def load_users(self):
        try:
            with open('cocuk_siber_users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open('cocuk_siber_users.json', 'w') as f:
            json.dump(self.users, f)

    def start_mini_game(self, game_type):
        self.clear_frame()

        ttk.Label(self.main_frame,
                  text="Mini Oyun Zamanı!",
                  style="Title.TLabel").pack(pady=20)

        if game_type == "internet":
            self.play_safe_website_game()
        elif game_type == "password":
            self.play_password_game()
        elif game_type == "bullying":
            self.play_cyberbullying_game()

    def play_safe_website_game(self):
        websites = [
            {"url": "https://www.google.com", "safe": True},
            {"url": "http://www.youtude.com", "safe": False},
            {"url": "https://www.goggle.com", "safe": False},
            {"url": "https://www.github.com", "safe": True},
            {"url": "https://www.google.xyz", "safe": False},
        ]

        website = random.choice(websites)

        ttk.Label(self.main_frame,
                  text="Bu site güvenli mi?",
                  style="Custom.TLabel").pack(pady=10)

        ttk.Label(self.main_frame,
                  text=website["url"],
                  style="Custom.TLabel").pack(pady=10)

        def check_answer(answer):
            if answer == website["safe"]:
                self.points += 10
                messagebox.showinfo("Tebrikler!", "Doğru cevap! 10 puan kazandın!")
            else:
                messagebox.showinfo("Üzgünüm!", "Yanlış cevap! Tekrar dene!")
            self.show_main_menu()

        tk.Button(self.main_frame,
                  text="Güvenli",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['success'],
                  fg='white',
                  command=lambda: check_answer(True)).pack(pady=10)

        tk.Button(self.main_frame,
                  text="Güvenli Değil",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=lambda: check_answer(False)).pack(pady=10)

    def play_password_game(self):
        passwords = [
            {"password": "abc123", "strong": False},
            {"password": "Süper123!", "strong": True},
            {"password": "password", "strong": False},
            {"password": "K@hraman2024", "strong": True}
        ]

        password = random.choice(passwords)

        ttk.Label(self.main_frame,
                  text="Bu şifre güçlü mü?",
                  style="Custom.TLabel").pack(pady=10)

        ttk.Label(self.main_frame,
                  text=password["password"],
                  style="Custom.TLabel").pack(pady=10)

        def check_answer(answer):
            if answer == password["strong"]:
                self.points += 10
                messagebox.showinfo("Tebrikler!", "Doğru cevap! 10 puan kazandın!")
            else:
                messagebox.showinfo("Üzgünüm!", "Yanlış cevap! Tekrar dene!")
            self.show_main_menu()

        tk.Button(self.main_frame,
                  text="Güçlü Şifre",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['success'],
                  fg='white',
                  command=lambda: check_answer(True)).pack(pady=10)

        tk.Button(self.main_frame,
                  text="Zayıf Şifre",
                  font=('Comic Sans MS', 12),
                  bg=self.colors['warning'],
                  fg='white',
                  command=lambda: check_answer(False)).pack(pady=10)

    def play_cyberbullying_game(self):
        scenarios = [
            {
},
            {
                "scenario": "Biri sana internette kötü mesajlar atıyor. Ne yapmalısın?",
                "options": [
                    {"text": "Mesajları görmezden gel ve bir büyüğüne söyle", "correct": True},
                    {"text": "Hemen cevap ver ve tartışmaya başla", "correct": False},
                    {"text": "Mesajları sil ve unut", "correct": False}
                ]
            },
            {
                "scenario": "Bir arkadaşın izinsiz olarak senin fotoğrafını internette paylaştı. Ne yapmalısın?",
                "options": [
                    {"text": "Arkadaşına durumu anlat ve bir büyüğüne haber ver", "correct": True},
                    {"text": "Fotoğrafı görmezden gel", "correct": False},
                    {"text": "Sen de onun fotoğrafını paylaş", "correct": False}
                ]
            }
        ]

        scenario = random.choice(scenarios)

        ttk.Label(self.main_frame,
                  text="Siber Zorbalık Durumu:",
                  style="Custom.TLabel").pack(pady=10)

        ttk.Label(self.main_frame,
                  text=scenario["scenario"],
                  style="Custom.TLabel",
                  wraplength=600).pack(pady=10)

        def check_answer(correct):
            if correct:
                self.points += 10
                messagebox.showinfo("Tebrikler!", "Doğru cevap! 10 puan kazandın!")
            else:
                messagebox.showinfo("Üzgünüm!", "Yanlış cevap! Tekrar dene!")
            self.show_main_menu()

        for option in scenario["options"]:
            tk.Button(self.main_frame,
                      text=option["text"],
                      font=('Comic Sans MS', 12),
                      bg=self.colors['button'] if option["correct"] else self.colors['warning'],
                      fg='white',
                      command=lambda c=option["correct"]: check_answer(c)).pack(pady=10)

    def load_users(self):
        try:
            with open('cocuk_siber_users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open('cocuk_siber_users.json', 'w') as f:
            json.dump(self.users, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = CocukSiberGuvenlik(root)
    root.mainloop()
