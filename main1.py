import flet as ft
from flet import Icons, Colors
from datetime import datetime, timedelta
import random
import json
import time

class SmartTrainingApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_index = 0
        self.history = [0]
        self.selected_sport = None
        self.training_mode = None
        self.camera_active = False
        self.session_active = False
        self.session_start_time = None
        self.session_timer = None
        
        # Données utilisateur et statistiques
        self.user_data = self.load_user_data()
        self.stats = self.user_data.get("stats", {
            "sessions": 0, 
            "total_time": 0, 
            "streak": 3,
            "calories": 0,
            "level": 1,
            "xp": 0
        })
        
        self.sports_progress = self.user_data.get("sports_progress", {})
        
        self.setup_page()
        self.create_ui()
        
    def load_user_data(self):
        """Charge les données utilisateur depuis le stockage local"""
        try:
            # En production, vous utiliseriez le stockage réel
            return {
                "stats": {
                    "sessions": 12, 
                    "total_time": 345, 
                    "streak": 3,
                    "calories": 2450,
                    "level": 2,
                    "xp": 450
                },
                "sports_progress": {
                    "Judo": {"level": 3, "xp": 750, "sessions": 8},
                    "Yoga": {"level": 2, "xp": 300, "sessions": 5},
                    "Musculation": {"level": 1, "xp": 150, "sessions": 3}
                }
            }
        except:
            return {"stats": {}, "sports_progress": {}}
    
    def save_user_data(self):
        """Sauvegarde les données utilisateur"""
        # En production, implémentez la sauvegarde réelle
        pass
        
    def setup_page(self):
        self.page.title = "Smart Training Assistant"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0a0022"
        self.page.window_width = 420
        self.page.window_height = 880
        self.page.window_resizable = False
        self.page.padding = 0
        self.page.spacing = 0
        self.page.fonts = {
            "Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
        }
        self.page.theme = ft.Theme(font_family="Poppins")
        
    def create_ui(self):
        # Avatar avec badge de niveau
        self.avatar = ft.Stack([
            ft.CircleAvatar(
                foreground_image_src="https://i.pravatar.cc/300?u=oussama2025",
                radius=50,
            ),
            ft.Container(
                content=ft.Text(
                    f"Nv.{self.stats['level']}",
                    size=12,
                    weight="bold",
                    color="white"
                ),
                bgcolor="#ff6d00",
                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                border_radius=10,
                right=0,
                bottom=0,
            )
        ], width=100, height=100)
        
        # Boutons de navigation
        self.hamburger = ft.IconButton(
            icon=Icons.MENU_ROUNDED,
            icon_color="white",
            icon_size=34,
            on_click=self.open_drawer,
            tooltip="Menu",
            visible=True
        )
        
        self.back_button = ft.IconButton(
            icon=Icons.ARROW_BACK_IOS_NEW_ROUNDED,
            icon_color="white",
            icon_size=34,
            visible=False,
            on_click=lambda _: self.go_back(),
            tooltip="Retour"
        )
        
        # AppBar
        self.page.appbar = ft.AppBar(
            leading=self.hamburger,
            leading_width=60,
            title=ft.Text("Accueil", size=24, weight="bold"),
            center_title=True,
            bgcolor=Colors.with_opacity(0.95, "#140535"),
            elevation=10,
            actions=[
                ft.IconButton(
                    icon=Icons.NOTIFICATIONS,
                    icon_color="white",
                    on_click=self.show_notifications
                )
            ]
        )
        
        # Drawer
        self.create_drawer()
        
        # Premier écran
        self.animate_to(0)
        
    def create_drawer(self):
        self.page.drawer = ft.NavigationDrawer(
            bgcolor=Colors.with_opacity(0.96, "#140535"),
            indicator_color="#7c4dff",
            selected_index=0,
            elevation=20,
            controls=[
                ft.Container(height=30),
                ft.Column([
                    self.avatar,
                    ft.Text("Oussama", size=26, weight="bold", color="white"),
                    ft.Text("Athlète Pro", size=16, color="#b388ff"),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(Icons.LOCAL_FIRE_DEPARTMENT, color="#ff6d00", size=20),
                            ft.Text(f"{self.stats['streak']} jours", color="#ff6d00", weight="bold")
                        ], spacing=5),
                        padding=10
                    )
                ], alignment="center", spacing=8),
                ft.Divider(color="#555", height=20),
                ft.NavigationDrawerDestination(
                    icon=Icons.HOME_OUTLINED,
                    selected_icon=Icons.HOME,
                    label="Accueil"
                ),
                ft.NavigationDrawerDestination(
                    icon=Icons.FITNESS_CENTER_OUTLINED,
                    selected_icon=Icons.FITNESS_CENTER,
                    label="Sports"
                ),
                ft.NavigationDrawerDestination(
                    icon=Icons.PERSON_OUTLINED,
                    selected_icon=Icons.PERSON,
                    label="Solo IA"
                ),
                ft.NavigationDrawerDestination(
                    icon=Icons.GROUP_OUTLINED,
                    selected_icon=Icons.GROUP,
                    label="Groupe"
                ),
                ft.NavigationDrawerDestination(
                    icon=Icons.ANALYTICS_OUTLINED,
                    selected_icon=Icons.ANALYTICS,
                    label="Statistiques"
                ),
                ft.Divider(color="#555", height=20),
                ft.NavigationDrawerDestination(
                    icon=Icons.SETTINGS_OUTLINED,
                    label="Paramètres"
                ),
                ft.NavigationDrawerDestination(
                    icon=Icons.INFO_OUTLINE,
                    label="À propos"
                ),
            ],
            on_change=lambda e: self.go_to(e.control.selected_index)
        )
    
    def open_drawer(self, e):
        self.page.drawer.selected_index = self.current_index
        self.page.open(self.page.drawer)
        
    def show_notifications(self, e):
        self.page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Notifications"),
                content=ft.Column([
                    ft.ListTile(
                        title=ft.Text("Nouveau défi disponible"),
                        subtitle=ft.Text("Complétez 5 séances cette semaine"),
                        leading=ft.Icon(Icons.EMOJI_EVENTS, color="#ffd700"),
                    ),
                    ft.ListTile(
                        title=ft.Text("Votre série continue !"),
                        subtitle=ft.Text("3 jours d'affilée - Continuez comme ça !"),
                        leading=ft.Icon(Icons.LOCAL_FIRE_DEPARTMENT, color="#ff6d00"),
                    ),
                ], tight=True),
                actions=[ft.TextButton("Fermer", on_click=lambda _: self.page.close_dialog())]
            )
        )
        
    def go_to(self, index: int):
        if self.current_index == index:
            return
        self.history.append(index)
        self.current_index = index
        self.animate_to(index)
        
    def go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current_index = self.history[-1]
            self.animate_to(self.history[-1])
            
    def animate_to(self, index: int):
        titles = ["Accueil", "Sports", "Solo IA", "Groupe", "Statistiques", "Paramètres", "À propos"]
        self.page.appbar.title.value = titles[index]
        
        # Basculer entre hamburger et bouton retour
        if index == 0:
            self.page.appbar.leading = self.hamburger
            self.hamburger.visible = True
            self.back_button.visible = False
        else:
            self.page.appbar.leading = self.back_button
            self.hamburger.visible = False
            self.back_button.visible = True
            
        if self.page.drawer:
            self.page.drawer.selected_index = index
        self.page.update()
        
        new_content = ft.Container(
            content=self.build_screen(index),
            expand=True,
            opacity=0,
            animate_opacity=ft.Animation(500, "easeOutCubic"),
        )
        
        self.page.controls.clear()
        self.page.add(new_content)
        self.page.update()
        new_content.opacity = 1
        self.page.update()
        
    def build_screen(self, index):
        screens = [
            self.home_screen,
            self.sports_screen,
            self.solo_screen,
            self.group_screen,
            self.stats_screen,
            self.settings_screen,
            self.about_screen
        ]
        return screens[index]()
        
    def home_screen(self):
        # Progression du niveau
        xp_needed = 1000
        xp_progress = self.stats['xp'] / xp_needed
        
        return ft.Column([
            ft.Container(height=40),
            
            # En-tête avec progression
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(f"Niveau {self.stats['level']}", size=16, color="#b388ff"),
                            ft.Text(f"{self.stats['xp']}/{xp_needed} XP", size=12, color="#888"),
                        ], expand=True),
                        ft.Container(
                            content=ft.Text(f"#{random.randint(150, 250)}", size=14, color="#ffd700"),
                            bgcolor=Colors.with_opacity(0.2, "#ffd700"),
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=15,
                        )
                    ]),
                    ft.Container(
                        content=ft.Container(
                            width=xp_progress * 100,
                            height=6,
                            bgcolor="#7c4dff",
                            border_radius=3,
                        ),
                        width=100,
                        height=6,
                        bgcolor=Colors.with_opacity(0.2, "white"),
                        border_radius=3,
                    ),
                ]),
                padding=20
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Bonjour, Oussama !",
                        size=32,
                        weight="bold",
                        color="#e0e0ff",
                    ),
                    ft.Text(
                        datetime.now().strftime("%A %d %B %Y").title(),
                        size=16,
                        color="#888",
                    ),
                ], spacing=5),
                padding=ft.padding.symmetric(horizontal=20)
            ),
            
            # Message motivationnel
            ft.Container(
                content=ft.Row([
                    ft.Icon(Icons.LIGHTBULB, size=20, color="#ffd700"),
                    ft.Text(self.get_motivational_quote(), size=14, color="#ccc", expand=True),
                ], spacing=10),
                bgcolor=Colors.with_opacity(0.1, "#ffd700"),
                padding=15,
                margin=20,
                border_radius=15,
            ),
            
            # Statistiques rapides
            ft.Container(
                content=ft.Row([
                    self.stat_card("Séances", str(self.stats['sessions']), Icons.FITNESS_CENTER, "#9c27b0"),
                    self.stat_card("Minutes", str(self.stats['total_time']), Icons.TIMER, "#00bcd4"),
                    self.stat_card("Calories", f"{self.stats['calories']}", Icons.LOCAL_FIRE_DEPARTMENT, "#ff6d00"),
                ], alignment="center", spacing=10),
                padding=ft.padding.symmetric(horizontal=20)
            ),
            
            ft.Container(height=30),
            
            # Sport du jour
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Sport recommandé", size=20, weight="bold", color="white"),
                        ft.Icon(Icons.TRENDING_UP, color="#7c4dff"),
                    ]),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Row([
                            ft.Text("🥋", size=40),
                            ft.Column([
                                ft.Text("Judo", size=18, weight="bold", color="white"),
                                ft.Text("Niveau 3 • 8 séances", size=12, color="#888"),
                            ], expand=True),
                            ft.Icon(Icons.CHEVRON_RIGHT, color="#888"),
                        ], spacing=15),
                        bgcolor=Colors.with_opacity(0.05, "white"),
                        padding=15,
                        border_radius=15,
                        on_click=lambda _: self.select_sport("Judo")
                    ),
                ]),
                padding=ft.padding.symmetric(horizontal=20)
            ),
            
            ft.Container(height=30),
            
            # Boutons d'action
            ft.Container(
                content=ft.Column([
                    ft.ElevatedButton(
                        "Commencer l'entraînement",
                        icon=Icons.PLAY_ARROW,
                        width=340,
                        height=70,
                        bgcolor="#9c27b0",
                        color="white",
                        elevation=15,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=35),
                            overlay_color=Colors.with_opacity(0.1, "white")
                        ),
                        on_click=lambda _: self.go_to(1)
                    ),
                    ft.Row([
                        ft.OutlinedButton(
                            "Statistiques",
                            icon=Icons.ANALYTICS,
                            width=165,
                            height=60,
                            style=ft.ButtonStyle(
                                color="white",
                                side=ft.BorderSide(2, "#7c4dff"),
                                shape=ft.RoundedRectangleBorder(radius=30)
                            ),
                            on_click=lambda _: self.go_to(4)
                        ),
                        ft.OutlinedButton(
                            "Solo IA",
                            icon=Icons.SMART_TOY,
                            width=165,
                            height=60,
                            style=ft.ButtonStyle(
                                color="white",
                                side=ft.BorderSide(2, "#00bcd4"),
                                shape=ft.RoundedRectangleBorder(radius=30)
                            ),
                            on_click=lambda _: self.go_to(2)
                        ),
                    ], spacing=10),
                ], spacing=15, horizontal_alignment="center"),
                padding=20
            ),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def get_motivational_quote(self):
        quotes = [
            "La discipline est le pont entre les objectifs et leur réalisation.",
            "Chaque séance vous rapproche de votre meilleur vous-même.",
            "La persévérance transforme l'obstacle en opportunité.",
            "Votre corps peut accomplir tout ce que votre esprit croit.",
            "Le succès est la somme de petits efforts répétés jour après jour."
        ]
        return random.choice(quotes)
        
    def stat_card(self, label, value, icon, color):
        return ft.Container(
            width=110,
            height=100,
            bgcolor=Colors.with_opacity(0.1, color),
            border_radius=20,
            border=ft.border.all(2, Colors.with_opacity(0.3, color)),
            content=ft.Column([
                ft.Icon(icon, color=color, size=30),
                ft.Text(value, size=24, weight="bold", color=color),
                ft.Text(label, size=12, color="#888"),
            ], alignment="center", horizontal_alignment="center", spacing=5),
            padding=10,
            animate_scale=ft.Animation(200, "easeOut"),
        )
        
    def sports_screen(self):
        sports_data = [
            ("Judo", "🥋", "#ad1457", "#f50057", self.sports_progress.get("Judo", {})),
            ("Yoga", "🧘", "#00695c", "#009688", self.sports_progress.get("Yoga", {})),
            ("Musculation", "💪", "#b71c1c", "#f44336", self.sports_progress.get("Musculation", {})),
            ("Karaté", "🥊", "#e65100", "#ff9800", self.sports_progress.get("Karaté", {})),
            ("Course", "🏃", "#1565c0", "#2196f3", self.sports_progress.get("Course", {})),
            ("Natation", "🏊", "#006064", "#00bcd4", self.sports_progress.get("Natation", {})),
        ]
        
        cards = []
        for i in range(0, len(sports_data), 2):
            row_sports = [sports_data[i]]
            if i + 1 < len(sports_data):
                row_sports.append(sports_data[i + 1])
            
            row = ft.Row(
                [self.sport_card(*sport) for sport in row_sports],
                alignment="center",
                spacing=15
            )
            cards.append(row)
            cards.append(ft.Container(height=15))
            
        return ft.Column([
            ft.Container(height=30),
            ft.Text(
                "Choisissez votre sport",
                size=28,
                weight="bold",
                color="white",
                text_align="center"
            ),
            ft.Text(
                "Sélectionnez une discipline pour commencer",
                size=16,
                color="#888",
                text_align="center"
            ),
            ft.Container(height=30),
            *cards
        ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO, expand=True)
        
    def sport_card(self, title, emoji, color_from, color_to, progress):
        level = progress.get("level", 1)
        sessions = progress.get("sessions", 0)
        
        card = ft.Container(
            width=180,
            height=200,
            gradient=ft.LinearGradient(
                colors=[color_from, color_to],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right
            ),
            border_radius=25,
            shadow=ft.BoxShadow(
                blur_radius=15,
                color=Colors.with_opacity(0.5, color_from),
                offset=ft.Offset(0, 5)
            ),
            content=ft.Column([
                ft.Container(height=15),
                ft.Row([
                    ft.Text(f"Nv.{level}", size=12, color="white", weight="bold"),
                    ft.Container(expand=True),
                    ft.Text(f"{sessions} séances", size=10, color=Colors.with_opacity(0.8, "white")),
                ]),
                ft.Text(emoji, size=60, text_align="center"),
                ft.Text(title, size=20, weight="bold", color="white", text_align="center"),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Container(
                        width=140 * min(progress.get("xp", 0) / 1000, 1.0),
                        height=6,
                        bgcolor="white",
                        border_radius=3,
                    ),
                    width=140,
                    height=6,
                    bgcolor=Colors.with_opacity(0.3, "white"),
                    border_radius=3,
                ),
            ], alignment="center", horizontal_alignment="center"),
            animate_scale=ft.Animation(200, "easeOut"),
            on_click=lambda _, s=title: self.select_sport(s)
        )
        
        def on_hover(e):
            card.scale = 1.05 if e.data == "true" else 1.0
            card.update()
            
        card.on_hover = on_hover
        return card
        
    def select_sport(self, sport):
        self.selected_sport = sport
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(f"🎯 {sport} sélectionné - Prêt pour l'entraînement !"),
                bgcolor="#7c4dff",
                action="OK"
            )
        )
        self.go_to(2)
        
    def solo_screen(self):
        # Créer les contrôles conditionnels
        camera_view = ft.Container()  # Conteneur vide par défaut
        
        session_controls = [
            ft.ElevatedButton(
                "Démarrer la session IA" if not self.session_active else "Arrêter la session",
                icon=Icons.PLAY_ARROW if not self.session_active else Icons.STOP,
                width=340,
                height=70,
                bgcolor="#00bcd4" if not self.session_active else "#f44336",
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=35),
                ),
                on_click=self.toggle_session
            )
        ]
        
        if self.session_active:
            session_controls.extend([
                ft.Container(height=10),
                ft.Text(
                    f"Session en cours: 00:00",
                    size=16,
                    color="#00bcd4",
                    weight="bold"
                )
            ])
        
        return ft.Column([
            ft.Container(height=40),
            
            # En-tête dynamique
            ft.Container(
                content=ft.Row([
                    ft.Icon(Icons.SMART_TOY, size=30, color="#7c4dff"),
                    ft.Column([
                        ft.Text("Mode Solo IA", size=24, weight="bold", color="white"),
                        ft.Text(
                            f"Sport : {self.selected_sport or 'Non sélectionné'}",
                            size=14,
                            color="#7c4dff"
                        ),
                    ], expand=True),
                    ft.IconButton(
                        icon=Icons.INFO,
                        icon_color="#7c4dff",
                        on_click=lambda _: self.show_ai_info()
                    )
                ]),
                padding=20
            ),
            
            # État de la caméra
            ft.Container(
                content=ft.Row([
                    ft.Icon(
                        Icons.CAMERA if not self.camera_active else Icons.CAMERA_ENHANCE,
                        color="#00bcd4" if self.camera_active else "#888",
                        size=24
                    ),
                    ft.Text(
                        "Caméra IA " + ("Active" if self.camera_active else "Inactive"),
                        color="white",
                        expand=True
                    ),
                    ft.Switch(
                        value=self.camera_active,
                        active_color="#00bcd4",
                        on_change=self.toggle_camera
                    )
                ]),
                bgcolor=Colors.with_opacity(0.05, "white"),
                padding=15,
                margin=ft.margin.symmetric(horizontal=20),
                border_radius=15,
            ),
            
            ft.Container(height=20),
            
            # Vue caméra simulée (conditionnelle)
            camera_view,
            
            ft.Container(
                content=ft.Column([
                    self.feature_item("Détection de posture avancée", Icons.VISIBILITY, "Analyse en temps réel"),
                    self.feature_item("Comptage automatique des répétitions", Icons.FORMAT_LIST_NUMBERED, "Précis à 98%"),
                    self.feature_item("Feedback vocal personnalisé", Icons.VOLUME_UP, "Instructions audio"),
                    self.feature_item("Correction de forme en direct", Icons.FACT_CHECK, "Prévient les blessures"),
                    self.feature_item("Analyse de performance", Icons.ANALYTICS, "Statistiques détaillées"),
                ], spacing=12),
                padding=20
            ),
            
            ft.Container(height=20),
            
            # Contrôles de session
            ft.Container(
                content=ft.Column(session_controls, horizontal_alignment="center", spacing=15),
                padding=20
            ),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def show_ai_info(self):
        self.page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Technologie IA"),
                content=ft.Text(
                    "Notre système utilise l'apprentissage automatique pour analyser vos mouvements "
                    "en temps réel. La technologie MediaPipe permet une détection précise de la posture "
                    "et des angles articulaires pour des corrections optimales.",
                    size=14
                ),
                actions=[ft.TextButton("Compris", on_click=lambda _: self.page.close_dialog())]
            )
        )
        
    def toggle_camera(self, e):
        self.camera_active = e.control.value
        self.page.update()
        
    def toggle_session(self, e):
        self.session_active = not self.session_active
        if self.session_active:
            self.session_start_time = datetime.now()
            self.start_session_timer()
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("🎯 Session d'entraînement démarrée !"),
                    bgcolor="#00bcd4"
                )
            )
        else:
            if self.session_timer:
                self.page.controls.remove(self.session_timer)
            session_duration = (datetime.now() - self.session_start_time).seconds // 60
            self.stats['sessions'] += 1
            self.stats['total_time'] += session_duration
            self.stats['calories'] += random.randint(50, 150)
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"✅ Session terminée ! {session_duration} minutes d'entraînement."),
                    bgcolor="#4caf50"
                )
            )
        self.page.update()
        
    def start_session_timer(self):
        # Implémentation simplifiée du timer
        pass
        
    def feature_item(self, text, icon, subtitle):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#7c4dff", size=28),
                ft.Column([
                    ft.Text(text, size=16, color="white", weight="bold"),
                    ft.Text(subtitle, size=12, color="#888"),
                ], expand=True, spacing=2),
                ft.Icon(Icons.CHECK_CIRCLE, color="#4caf50", size=20),
            ], spacing=15),
            padding=15,
            bgcolor=Colors.with_opacity(0.05, "#7c4dff"),
            border_radius=15,
            width=380
        )
        
    def group_screen(self):
        return ft.Column([
            ft.Container(height=60),
            ft.Icon(Icons.GROUPS, size=120, color="#ff6d00"),
            ft.Text("Mode Groupe", size=36, weight="bold", color="#ff6d00"),
            ft.Text("Entraînez-vous ensemble", size=18, color="#ccc", text_align="center"),
            
            ft.Container(height=40),
            
            # Statut groupe
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(Icons.PEOPLE, color="#ff6d00"),
                        ft.Text("Communauté Active", size=20, weight="bold", color="white", expand=True),
                        ft.Container(
                            content=ft.Text(f"{random.randint(50, 200)} en ligne", size=12, color="#4caf50"),
                            bgcolor=Colors.with_opacity(0.1, "#4caf50"),
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            border_radius=10,
                        )
                    ]),
                    ft.Container(height=15),
                    ft.Text(
                        "Rejoignez des sessions de groupe en direct et défiez vos amis !",
                        size=14,
                        color="#888",
                        text_align="center"
                    ),
                ]),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "#ff6d00"),
                border_radius=20,
                margin=20,
            ),
            
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Fonctionnalités à venir :", size=20, weight="bold", color="white"),
                    ft.Container(height=15),
                    self.feature_item("Sessions multijoueurs en direct", Icons.PEOPLE, "Jusqu'à 10 participants"),
                    self.feature_item("Classements compétitifs", Icons.LEADERBOARD, "Défis hebdomadaires"),
                    self.feature_item("Défis d'équipe collaboratifs", Icons.EMOJI_EVENTS, "Travail d'équipe"),
                    self.feature_item("Chat vocal intégré", Icons.MIC, "Communication en temps réel"),
                    self.feature_item("Sessions d'entraînement partagées", Icons.SHARE, "Partagez vos progrès"),
                ], spacing=12),
                padding=20
            ),
            
            ft.Container(height=30),
            
            ft.ElevatedButton(
                "Me prévenir au lancement",
                icon=Icons.NOTIFICATIONS,
                width=340,
                height=60,
                bgcolor="#ff6d00",
                color="white",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                ),
                on_click=lambda _: self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("✅ Nous vous tiendrons au courant !"))
                )
            ),
            
            ft.Container(height=20),
            ft.Text("Lancement prévu : Décembre 2024", size=14, color="#888", italic=True),
        ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO, expand=True)
        
    def stats_screen(self):
        weekly_data = [0.6, 0.8, 0.5, 0.9, 0.7, 0.4, 0.0]
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        
        return ft.Column([
            ft.Container(height=30),
            ft.Text("Vos Statistiques", size=32, weight="bold", color="white"),
            ft.Container(height=20),
            
            # Graphique de progression
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Activité cette semaine", size=20, weight="bold", color="white", expand=True),
                        ft.Text(f"{sum(weekly_data[:5])/5:.0%} moyenne", size=14, color="#7c4dff"),
                    ]),
                    ft.Container(height=15),
                    ft.Row([
                        self.progress_bar(days[i], weekly_data[i], "#7c4dff" if weekly_data[i] > 0 else "#555")
                        for i in range(7)
                    ], alignment="center", spacing=5),
                ], horizontal_alignment="center"),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=20,
                margin=20,
            ),
            
            # Stats détaillées
            ft.Container(
                content=ft.Column([
                    self.stat_row("Total des séances", f"{self.stats['sessions']}", Icons.FITNESS_CENTER, "#9c27b0"),
                    ft.Divider(color="#333"),
                    self.stat_row("Temps total", f"{self.stats['total_time']} min", Icons.TIMER, "#00bcd4"),
                    ft.Divider(color="#333"),
                    self.stat_row("Calories brûlées", f"{self.stats['calories']} kcal", Icons.LOCAL_FIRE_DEPARTMENT, "#ff6d00"),
                    ft.Divider(color="#333"),
                    self.stat_row("Série actuelle", f"{self.stats['streak']} jours", Icons.TRENDING_UP, "#4caf50"),
                    ft.Divider(color="#333"),
                    self.stat_row("Niveau actuel", f"{self.stats['level']}", Icons.STAR, "#ffd700"),
                    ft.Divider(color="#333"),
                    self.stat_row("Prochain niveau", f"{1000 - self.stats['xp']} XP", Icons.FLAG, "#7c4dff"),
                ], spacing=8),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=20,
                margin=20,
            ),
            
            # Sports maîtrisés
            ft.Container(
                content=ft.Column([
                    ft.Text("Sports Maîtrisés", size=20, weight="bold", color="white"),
                    ft.Container(height=15),
                    *[self.sport_stat_row(sport, data) for sport, data in self.sports_progress.items()]
                ]),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=20,
                margin=20,
            ),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
        
    def progress_bar(self, day, value, color):
        return ft.Column([
            ft.Container(
                width=35,
                height=120,
                bgcolor=Colors.with_opacity(0.1, "white"),
                border_radius=8,
                content=ft.Container(
                    alignment=ft.alignment.bottom_center,
                    content=ft.Container(
                        width=35,
                        height=120 * value,
                        bgcolor=color,
                        border_radius=8,
                    )
                )
            ),
            ft.Container(height=5),
            ft.Text(day, size=12, color="#888"),
            ft.Text(f"{value:.0%}", size=10, color=color),
        ], spacing=2, horizontal_alignment="center")
        
    def stat_row(self, label, value, icon, color):
        return ft.Row([
            ft.Icon(icon, color=color, size=28),
            ft.Text(label, size=16, color="white", expand=True),
            ft.Text(value, size=18, weight="bold", color=color),
        ], spacing=15)
    
    def sport_stat_row(self, sport, data):
        return ft.Container(
            content=ft.Row([
                ft.Text("🥋", size=20),
                ft.Column([
                    ft.Text(sport, size=16, color="white", weight="bold"),
                    ft.Text(f"Niveau {data.get('level', 1)} • {data.get('sessions', 0)} séances", 
                           size=12, color="#888"),
                ], expand=True),
                ft.Container(
                    content=ft.Text(f"{data.get('xp', 0)} XP", size=14, color="#7c4dff"),
                    bgcolor=Colors.with_opacity(0.1, "#7c4dff"),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=15,
                ),
            ]),
            padding=ft.padding.symmetric(vertical=8),
        )
        
    def settings_screen(self):
        return ft.Column([
            ft.Container(height=40),
            ft.Text("Paramètres", size=32, weight="bold", color="white"),
            ft.Container(height=30),
            
            # Profil
            ft.Container(
                content=ft.Column([
                    ft.Text("Profil", size=20, weight="bold", color="white"),
                    ft.Container(height=15),
                    ft.ListTile(
                        leading=ft.Icon(Icons.PERSON, color="#7c4dff"),
                        title=ft.Text("Informations personnelles", color="white"),
                        subtitle=ft.Text("Nom, âge, objectifs", color="#888"),
                        trailing=ft.Icon(Icons.CHEVRON_RIGHT, color="#888"),
                        on_click=lambda _: self.edit_profile()
                    ),
                    ft.Divider(color="#333"),
                    ft.ListTile(
                        leading=ft.Icon(Icons.FITNESS_CENTER, color="#7c4dff"),
                        title=ft.Text("Objectifs d'entraînement", color="white"),
                        subtitle=ft.Text("Définir vos objectifs", color="#888"),
                        trailing=ft.Icon(Icons.CHEVRON_RIGHT, color="#888"),
                    ),
                ]),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=20,
                margin=20,
            ),
            
            # Préférences
            ft.Container(
                content=ft.Column([
                    ft.Text("Préférences", size=20, weight="bold", color="white"),
                    ft.Container(height=15),
                    ft.ListTile(
                        leading=ft.Icon(Icons.DARK_MODE, color="#7c4dff"),
                        title=ft.Text("Mode sombre", color="white"),
                        trailing=ft.Switch(value=True, active_color="#7c4dff"),
                    ),
                    ft.Divider(color="#333"),
                    ft.ListTile(
                        leading=ft.Icon(Icons.NOTIFICATIONS, color="#7c4dff"),
                        title=ft.Text("Notifications", color="white"),
                        trailing=ft.Switch(value=True, active_color="#7c4dff"),
                    ),
                    ft.Divider(color="#333"),
                    ft.ListTile(
                        leading=ft.Icon(Icons.VOLUME_UP, color="#7c4dff"),
                        title=ft.Text("Sons et audio", color="white"),
                        trailing=ft.Switch(value=True, active_color="#7c4dff"),
                    ),
                    ft.Divider(color="#333"),
                    ft.ListTile(
                        leading=ft.Icon(Icons.LANGUAGE, color="#7c4dff"),
                        title=ft.Text("Langue : Français", color="white"),
                        trailing=ft.Icon(Icons.CHEVRON_RIGHT, color="#888"),
                    ),
                ]),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=20,
                margin=20,
            ),
            
            # À propos
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(Icons.INFO, color="#7c4dff"),
                    title=ft.Text("À propos de l'application", color="white"),
                    trailing=ft.Icon(Icons.CHEVRON_RIGHT, color="#888"),
                    on_click=lambda _: self.go_to(6)
                ),
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=15,
                margin=20,
            ),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def edit_profile(self):
        self.page.show_dialog(
            ft.AlertDialog(
                title=ft.Text("Modifier le profil"),
                content=ft.Column([
                    ft.TextField(label="Nom", value="Oussama"),
                    ft.TextField(label="Âge", value="25"),
                    ft.Dropdown(
                        label="Niveau",
                        value="Intermediaire",
                        options=[
                            ft.dropdown.Option("Débutant"),
                            ft.dropdown.Option("Intermédiaire"),
                            ft.dropdown.Option("Avancé"),
                            ft.dropdown.Option("Expert"),
                        ]
                    ),
                ], tight=True),
                actions=[
                    ft.TextButton("Annuler", on_click=lambda _: self.page.close_dialog()),
                    ft.TextButton("Sauvegarder", on_click=lambda _: self.page.close_dialog()),
                ]
            )
        )
        
    def about_screen(self):
        return ft.Column([
            ft.Container(height=80),
            ft.Icon(Icons.FITNESS_CENTER, size=100, color="#b388ff"),
            ft.Text("Smart Training Assistant", size=28, weight="bold", color="#b388ff", text_align="center"),
            ft.Container(height=10),
            ft.Text("Votre coach personnel intelligent", size=16, color="#888", text_align="center"),
            
            ft.Container(height=30),
            ft.Divider(color="#555", height=2),
            ft.Container(height=30),
            
            ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(Icons.VERIFIED, color="#4caf50"),
                        title=ft.Text("Version 2.1.0", size=16, color="white"),
                        subtitle=ft.Text("Build 21.11.2025", size=12, color="#888"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(Icons.UPDATE, color="#ff6d00"),
                        title=ft.Text("Dernière mise à jour", size=16, color="white"),
                        subtitle=ft.Text("15 Novembre 2024", size=12, color="#888"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(Icons.SECURITY, color="#00bcd4"),
                        title=ft.Text("Sécurité des données", size=16, color="white"),
                        subtitle=ft.Text("Toutes vos données sont cryptées", size=12, color="#888"),
                    ),
                ]),
                padding=20,
                bgcolor=Colors.with_opacity(0.05, "white"),
                border_radius=20,
                margin=20,
            ),
            
            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Développé avec", size=16, color="#888", text_align="center"),
                    ft.Row([
                        ft.Text("❤️", size=24),
                        ft.Text("Python", size=18, color="white", weight="bold"),
                        ft.Text("+", size=18, color="#888"),
                        ft.Text("Flet", size=18, color="#7c4dff", weight="bold"),
                    ], alignment="center", spacing=8),
                    ft.Container(height=10),
                    ft.Text("et des technologies IA avancées", size=14, color="#888"),
                ], horizontal_alignment="center", spacing=10),
                padding=20
            ),
            
            ft.Container(height=30),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Contact & Support", size=18, weight="bold", color="white", text_align="center"),
                    ft.Container(height=10),
                    ft.Row([
                        ft.IconButton(Icons.EMAIL, icon_color="#7c4dff"),
                        ft.IconButton(Icons.WEB, icon_color="#7c4dff"),
                        ft.IconButton(Icons.HELP, icon_color="#7c4dff"),
                    ], alignment="center"),
                ]),
                padding=20
            ),
            
            ft.Container(height=20),
            ft.Text("© 2024 Smart Training Inc.", size=14, color="#666"),
            ft.Text("Tous droits réservés", size=12, color="#555"),
        ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO, expand=True)

def main(page: ft.Page):
    SmartTrainingApp(page)

if __name__ == "__main__":
    ft.app(target=main)