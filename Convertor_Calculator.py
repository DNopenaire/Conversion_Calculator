import tkinter as tk
from tkinter import messagebox

# === CONVERSIONS ===

def normaliser_ip(ip_adresse):
    octets = ip_adresse.strip().split('.')
    while len(octets) < 4:
        octets.append('0')
    return '.'.join(octets[:4])

def ip_vers_binaire(ip_adresse):
    ip_adresse = normaliser_ip(ip_adresse)
    octets = ip_adresse.strip().split('.')
    try:
        octets_int = [int(o) for o in octets]
        if not all(0 <= o <= 255 for o in octets_int):
            return "Erreur : Chaque octet doit être entre 0 et 255."
        binaire_octets = [bin(o)[2:].zfill(8) for o in octets_int]
        return '.'.join(binaire_octets)
    except ValueError:
        return "Erreur : L'adresse IP contient des caractères non numériques."

def binaire_vers_ip(binaire_adresse):
    octets = binaire_adresse.strip().split('.')
    if len(octets) != 4:
        return "Erreur : L'adresse binaire doit contenir 4 octets."
    if not all(len(b) == 8 and all(c in '01' for c in b) for b in octets):
        return "Erreur : Chaque octet binaire doit avoir 8 bits (0 ou 1)."
    try:
        ip_octets = [str(int(b, 2)) for b in octets]
        return '.'.join(ip_octets)
    except ValueError:
        return "Erreur : Format binaire incorrect."

def ip_vers_hexadecimal(ip_adresse):
    ip_adresse = normaliser_ip(ip_adresse)
    octets = ip_adresse.strip().split('.')
    try:
        hex_parts = [hex(int(o))[2:].zfill(2) for o in octets if 0 <= int(o) <= 255]
        if len(hex_parts) != 4:
            return "Erreur : IP invalide."
        return "0x" + ''.join(hex_parts).upper()
    except ValueError:
        return "Erreur : L'adresse IP contient des caractères non numériques."

def ip_vers_decimal(ip_adresse):
    ip_adresse = normaliser_ip(ip_adresse)
    octets = ip_adresse.strip().split('.')
    try:
        total = sum(int(octets[i]) << (8 * (3 - i)) for i in range(4))
        return str(total)
    except (ValueError, IndexError):
        return "Erreur : IP invalide."

def binaire_vers_hexadecimal(binaire_adresse):
    ip = binaire_vers_ip(binaire_adresse)
    if "Erreur" in ip:
        return ip
    return ip_vers_hexadecimal(ip)

def binaire_vers_decimal(binaire_adresse):
    binaire_adresse = binaire_adresse.strip().replace('.', '')
    if not set(binaire_adresse).issubset({'0', '1'}):
        return "Erreur : Le nombre binaire contient des caractères non valides."
    try:
        return str(int(binaire_adresse, 2))
    except ValueError:
        return "Erreur : Conversion impossible."

def hexadecimal_vers_ip(hex_adresse):
    try:
        hex_adresse = hex_adresse.strip().lower().replace("0x", "")
        hex_adresse = hex_adresse.zfill(8)
        octets = [str(int(hex_adresse[i:i+2], 16)) for i in range(0, 8, 2)]
        return '.'.join(octets)
    except ValueError:
        return "Erreur : Format hexadécimal incorrect."

def hexadecimal_vers_binaire(hex_adresse):
    ip = hexadecimal_vers_ip(hex_adresse)
    if "Erreur" in ip:
        return ip
    return ip_vers_binaire(ip)

def hexadecimal_vers_decimal(hex_adresse):
    ip = hexadecimal_vers_ip(hex_adresse)
    if "Erreur" in ip:
        return ip
    return ip_vers_decimal(ip)

def decimal_vers_ip(decimal_valeur):
    try:
        decimal_valeur = int(decimal_valeur)
        if not (0 <= decimal_valeur <= 4294967295):
            return "Erreur : Valeur décimale hors plage."
        return '.'.join(str((decimal_valeur >> (8 * i)) & 255) for i in reversed(range(4)))
    except ValueError:
        return "Erreur : Entrée non valide."

def decimal_vers_hexadecimal(decimal_valeur):
    ip = decimal_vers_ip(decimal_valeur)
    if "Erreur" in ip:
        return ip
    return ip_vers_hexadecimal(ip)

def decimal_vers_binaire(decimal_valeur):
    ip = decimal_vers_ip(decimal_valeur)
    if "Erreur" in ip:
        return ip
    return ip_vers_binaire(ip)

# === INTERFACE ===

def copier_resultat():
    resultat = label_resultat.cget("text").split(":", 1)[-1].strip()
    if resultat:
        fenetre.clipboard_clear()
        fenetre.clipboard_append(resultat)
        messagebox.showinfo("Copié", "Résultat copié dans le presse-papiers.")

def afficher_resultat(titre, texte):
    label_resultat.config(text=f"{titre} : {texte}")

def reset_champs():
    entree_ip.delete(0, tk.END)
    label_resultat.config(text="")

# === FENÊTRE ===

fenetre = tk.Tk()
fenetre.title("Convertisseur Adresse IP")
fenetre.geometry("520x520")
fenetre.resizable(False, False)

# === MODE SOMBRE ===
bg_color = "#2e2e2e"
fg_color = "#ffffff"
btn_color = "#444444"
entry_bg = "#3e3e3e"

fenetre.configure(bg=bg_color)

# === WIDGETS ===

label_instruction = tk.Label(fenetre, text="Entrez une adresse IP, binaire, hexadécimale ou décimale :", font=("Arial", 12), bg=bg_color, fg=fg_color)
label_instruction.pack(pady=10)

entree_ip = tk.Entry(fenetre, font=("Arial", 12), width=40, bg=entry_bg, fg=fg_color, insertbackground="white")
entree_ip.pack(pady=5)

frame_boutons = tk.Frame(fenetre, bg=bg_color)
frame_boutons.pack(pady=10)

# === BOUTONS ===

boutons = [
    ("IP → Binaire", lambda: afficher_resultat("Binaire", ip_vers_binaire(entree_ip.get()))),
    ("IP → Hexadécimal", lambda: afficher_resultat("Hexadécimal", ip_vers_hexadecimal(entree_ip.get()))),
    ("IP → Décimal", lambda: afficher_resultat("Décimal", ip_vers_decimal(entree_ip.get()))),
    ("Binaire → IP", lambda: afficher_resultat("IP", binaire_vers_ip(entree_ip.get()))),
    ("Binaire → Hexadécimal", lambda: afficher_resultat("Hexadécimal", binaire_vers_hexadecimal(entree_ip.get()))),
    ("Binaire → Décimal", lambda: afficher_resultat("Décimal", binaire_vers_decimal(entree_ip.get()))),
    ("Hexadécimal → Binaire", lambda: afficher_resultat("Binaire", hexadecimal_vers_binaire(entree_ip.get()))),
    ("Hexadécimal → IP", lambda: afficher_resultat("IP", hexadecimal_vers_ip(entree_ip.get()))),
    ("Hexadécimal → Décimal", lambda: afficher_resultat("Décimal", hexadecimal_vers_decimal(entree_ip.get()))),
    ("Décimal → IP", lambda: afficher_resultat("IP", decimal_vers_ip(entree_ip.get()))),
    ("Décimal → Hexadécimal", lambda: afficher_resultat("Hexadécimal", decimal_vers_hexadecimal(entree_ip.get()))),
    ("Décimal → Binaire", lambda: afficher_resultat("Binaire", decimal_vers_binaire(entree_ip.get())))
]

for i, (texte, commande) in enumerate(boutons):
    btn = tk.Button(frame_boutons, text=texte, width=24, bg=btn_color, fg=fg_color, command=commande)
    btn.grid(row=i//2, column=i%2, padx=5, pady=5)

label_resultat = tk.Label(fenetre, text="", font=("Arial", 12), fg="#00ffcc", bg=bg_color)
label_resultat.pack(pady=10)

btn_copier = tk.Button(fenetre, text="Copier le résultat", command=copier_resultat, bg=btn_color, fg=fg_color, width=20)
btn_copier.pack(pady=5)

btn_reset = tk.Button(fenetre, text="Reset", command=reset_champs, bg=btn_color, fg=fg_color, width=20)
btn_reset.pack(pady=5)


# === LANCEMENT ===
fenetre.mainloop()
