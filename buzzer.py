import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import os
import sys

# Fonction pour obtenir le chemin des ressources
def resource_path(relative_path):
    """Obtenez le chemin vers une ressource, que ce soit lors de l'exécution du script ou du programme empaqueté."""
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans `_MEIPASS`
        base_path = sys._MEIPASS
    except AttributeError:
        # PyInstaller n'est pas en train d'exécuter en tant que bundle
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Initialisation de pygame pour jouer le son
pygame.mixer.init()

# Définir le chemin complet vers le fichier son par défaut
default_sound_path = resource_path("buzzersong.mp3")
current_sound_path = default_sound_path

# Chargement du son
try:
    pygame.mixer.music.load(default_sound_path)
except pygame.error:
    print(f"Erreur : le fichier son {default_sound_path} est introuvable.")
    sys.exit()

def play_sound():
    # Joue le son courant
    pygame.mixer.music.load(current_sound_path)
    pygame.mixer.music.play()

def change_background_color(color):
    # Applique la couleur à toutes les fenêtres et boutons (sauf pour les boutons principaux)
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.configure(bg=color)
            for child in window.winfo_children():
                if not isinstance(child, tk.Button):  # Exclut les boutons de la modification de couleur
                    child.configure(bg=color)
        elif not isinstance(window, tk.Button):  # Exclut le bouton principal de la modification de couleur
            window.configure(bg=color)
    
    # Applique la couleur à la fenêtre principale
    root.configure(bg=color)
    for button in color_buttons.values():
        button.config(bd=2, relief=tk.RAISED)
    color_buttons[color].config(bd=4, relief=tk.SOLID)

def set_background_image(image_path):
    # Définit l'image en tant que fond d'écran
    image = Image.open(image_path)
    image = image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    
    background_label = tk.Label(root, image=bg_image)
    background_label.image = bg_image  # Pour éviter que l'image soit garbage collected
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.lower()  # Place l'image en arrière-plan

def import_background_image():
    # Permet d'importer une image pour le fond d'écran
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    if file_path:
        set_background_image(file_path)

def open_color_window():
    # Ouvre une fenêtre pour choisir la couleur de fond
    color_window = tk.Toplevel(root)
    color_window.title("Choisir la couleur de fond")
    color_window.geometry("300x400")
    color_window.grab_set()

    canvas = tk.Canvas(color_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(color_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    color_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=color_frame, anchor="nw")

    # Liste des couleurs disponibles
    colors = [
        "skyblue", "lightgreen", "lightpink", "lightyellow", "lightcoral", "lightcyan", 
        "lightgoldenrodyellow", "lightgray", "blue", "green", "pink", "yellow", "coral", 
        "cyan", "gold", "gray", "purple", "orange", "brown"
    ]

    global color_buttons
    color_buttons = {}

    # Création de boutons pour chaque couleur
    for i, color in enumerate(colors):
        button = tk.Button(
            color_frame, bg=color, width=10, height=2, 
            command=lambda c=color: change_background_color(c)
        )
        button.grid(row=i//3, column=i%3, padx=5, pady=5)
        color_buttons[color] = button

    # Bouton pour importer une image
    import_button = tk.Button(
        color_frame, text="Importer", command=import_background_image, 
        bg='grey', fg='white', relief=tk.RAISED, width=10, height=2
    )
    import_button.grid(row=(i+1)//3, column=i%3, padx=5, pady=5)

    color_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.config(yscrollcommand=scrollbar.set)

    # Bouton pour fermer la fenêtre
    close_button = tk.Button(
        color_window, text="Fermer", command=color_window.destroy, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    close_button.pack(pady=10)

def open_sound_menu():
    # Ouvre une fenêtre pour le menu des sons
    sound_menu_window = tk.Toplevel(root)
    sound_menu_window.title("Menu des sons")
    sound_menu_window.geometry("300x200")
    sound_menu_window.grab_set()
    sound_menu_window.configure(bg=root.cget('bg'))  # Définit la couleur de fond

    def set_default_sound():
        # Définit le son par défaut
        global current_sound_path
        current_sound_path = default_sound_path

    def import_sound():
        # Permet d'importer un fichier son
        global current_sound_path
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            current_sound_path = file_path

    # Bouton pour réinitialiser au son par défaut
    default_sound_button = tk.Button(
        sound_menu_window, text="Son par défaut", command=set_default_sound, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    default_sound_button.pack(pady=5)

    # Bouton pour importer un nouveau son
    import_sound_button = tk.Button(
        sound_menu_window, text="Importer un son", command=import_sound, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    import_sound_button.pack(pady=5)

    # Bouton pour fermer la fenêtre
    close_button = tk.Button(
        sound_menu_window, text="Fermer", command=sound_menu_window.destroy, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    close_button.pack(pady=10)

def open_button_customization_window():
    # Ouvre une fenêtre pour personnaliser le bouton
    button_custom_window = tk.Toplevel(root)
    button_custom_window.title("Personnalisation des boutons")
    button_custom_window.geometry("300x400")
    button_custom_window.grab_set()
    button_custom_window.configure(bg=root.cget('bg'))  # Définit la couleur de fond

    tk.Label(button_custom_window, text="Taille du bouton (largeur, hauteur)").pack(pady=5)
    width_var = tk.IntVar(value=20)
    height_var = tk.IntVar(value=2)
    tk.Entry(button_custom_window, textvariable=width_var).pack(pady=5)
    tk.Entry(button_custom_window, textvariable=height_var).pack(pady=5)

    tk.Label(button_custom_window, text="Forme du bouton").pack(pady=5)
    shape_var = tk.StringVar(value="rectangle")
    shape_options = ["carré", "rectangle"]
    shape_menu = tk.OptionMenu(button_custom_window, shape_var, *shape_options)
    shape_menu.pack(pady=5)

    def apply_button_customization():
        # Applique la personnalisation du bouton
        width = width_var.get()
        height = height_var.get()
        shape = shape_var.get()

        button.config(width=width, height=height, bd=2, relief=tk.RAISED)

        if shape == "carré":
            button.config(width=height, height=height)

    def import_button_image():
        # Permet d'importer une image pour le bouton
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((200, 200), Image.LANCZOS)  # Redimensionne l'image pour s'adapter au bouton
            photo = ImageTk.PhotoImage(image)
            button.config(image=photo, compound="center")
            button.image = photo  # Pour éviter que l'image soit garbage collected

    def reset_button_to_defaults():
        # Réinitialise le bouton à ses valeurs par défaut
        button.config(
            text="Buzzer", width=20, height=2, bg='red', fg='white', 
            font=('Helvetica', 16, 'bold'), image='', relief=tk.RAISED, bd=2
        )
        width_var.set(20)
        height_var.set(2)
        shape_var.set("rectangle")

    # Bouton pour appliquer les personnalisations
    apply_button_button = tk.Button(
        button_custom_window, text="Appliquer", command=apply_button_customization, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    apply_button_button.pack(pady=10)

    # Bouton pour importer une image pour le bouton
    import_image_button = tk.Button(
        button_custom_window, text="Importer une image", command=import_button_image, 
        bg='grey', fg='white', relief=tk.RAISED, width=20
    )
    import_image_button.pack(pady=10)

    # Bouton pour réinitialiser les paramètres par défaut
    reset_button = tk.Button(
        button_custom_window, text="Défauts", command=reset_button_to_defaults, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    reset_button.pack(pady=10)

    # Bouton pour fermer la fenêtre
    close_button = tk.Button(
        button_custom_window, text="Fermer", command=button_custom_window.destroy, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    close_button.pack(pady=10)

def open_more_info_window():
    # Ouvre une fenêtre avec plus d'informations
    more_info_window = tk.Toplevel(root)
    more_info_window.title("Plus d'informations")
    more_info_window.geometry("400x200")
    more_info_window.grab_set()
    more_info_window.configure(bg=root.cget('bg'))  # Définit la couleur de fond

    # Texte pour les dons avec PayPal
    paypal_label = tk.Label(
        more_info_window, text="Don avec PayPal :\nwww.paypal.me/EvanEnzo0219", 
        bg=root.cget('bg'), fg='black', font=('Helvetica', 12, 'bold'), justify=tk.LEFT
    )
    paypal_label.pack(pady=10)

    # Texte pour donner des idées
    ideas_label = tk.Label(
        more_info_window, text="Donner des idées :\n evan.barreiros.pro@gmail.com", 
        bg=root.cget('bg'), fg='black', font=('Helvetica', 12, 'bold'), justify=tk.LEFT
    )
    ideas_label.pack(pady=10)

    # Bouton pour fermer la fenêtre
    close_button = tk.Button(
        more_info_window, text="Fermer", command=more_info_window.destroy, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    close_button.pack(pady=10)

def open_menu():
    # Ouvre le menu principal
    menu_window = tk.Toplevel(root)
    menu_window.title("Menu")
    menu_window.geometry("200x300")
    menu_window.grab_set()
    menu_window.configure(bg=root.cget('bg'))  # Définit la couleur de fond

    def close_menu():
        # Ferme le menu
        menu_window.destroy()

    def quit_game():
        # Quitte le jeu
        root.quit()

    def open_color_menu():
        # Ouvre le menu de sélection de couleur
        open_color_window()

    # Bouton pour changer la couleur de fond
    change_color_button = tk.Button(
        menu_window, text="Couleur de fond", command=open_color_menu, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    change_color_button.pack(pady=5)

    # Bouton pour ouvrir le menu des sons
    sound_menu_button = tk.Button(
        menu_window, text="Menu des sons", command=open_sound_menu, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    sound_menu_button.pack(pady=5)

    # Bouton pour personnaliser les boutons
    button_custom_button = tk.Button(
        menu_window, text="Personnalisation des boutons", command=open_button_customization_window, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    button_custom_button.pack(pady=5)

    # Bouton pour afficher plus d'informations
    more_info_button = tk.Button(
        menu_window, text="Plus", command=open_more_info_window, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    more_info_button.pack(pady=5)

    # Bouton pour fermer le menu
    close_button = tk.Button(
        menu_window, text="Fermer", command=close_menu, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    close_button.pack(pady=10)

    # Bouton pour quitter le jeu
    quit_button = tk.Button(
        menu_window, text="Quitter le jeu", command=quit_game, 
        bg='grey', fg='white', relief=tk.RAISED
    )
    quit_button.pack(side=tk.BOTTOM, pady=5)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Bouton avec son")
root.geometry("400x300")
root.configure(bg='skyblue')

# Création du bouton rouge pour le son
button = tk.Button(
    root, text="Buzzer", command=play_sound, 
    bg='red', fg='white', font=('Helvetica', 16, 'bold'), relief=tk.RAISED, bd=2
)
button.pack(expand=True)

# Création du bouton pour ouvrir le menu
menu_button = tk.Button(
    root, text="Menu", command=open_menu, 
    bg='grey', fg='white', relief=tk.RAISED, bd=2
)
menu_button.place(x=0, y=0)

# Lancement de la boucle principale de l'interface graphique
root.mainloop()
