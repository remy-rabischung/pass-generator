import random
import hashlib
import string
import json
import tkinter as tk
from tkinter import *
import customtkinter
from customtkinter import *


speciaux = '*^$%&"!#@'

def verif(mdp):
    if len(mdp) < 8:
        return False 
    if not any(char.isdigit() for char in mdp):
        return False
    if not any(char.islower() for char in mdp) or not any(char.isupper()for char in mdp):
        return False
    speciaux = '*^$%&"!#@'
    if not any(char in speciaux for char in mdp):
        return False
    return True

def gen():
    majuscule = random.choice(string.ascii_uppercase)
    minuscule = random.choice(string.ascii_lowercase)
    chiffre = random.choice(string.digits)
    special = random.choice(speciaux)
    caracteres = majuscule + minuscule + chiffre + special
    longueur_restante = 12 - len(caracteres)
    reste = "".join(random.choice(string.ascii_letters + string.digits + speciaux) for _ in range(longueur_restante))
    mdp = ''.join(random.sample(caracteres + reste, 12))
    mdp_entry.delete(0, END)
    mdp_entry.insert(0, mdp)
    return mdp

def hash_mdp(mdp):
    return hashlib.sha256(mdp.encode('utf-8')).hexdigest()

def aff_msg(msg):
    text_aff.configure(state=tk.NORMAL)
    text_aff.delete("1.0", tk.END)
    text_aff.insert(tk.END, msg)
    text_aff.configure(state=tk.DISABLED)

def verif_affich():
    mdp = entry_mot_de_passe.get()
    if verif(mdp):
        aff_msg("Mot de passe valide")
    else:
        aff_msg("Mot de passe non valide, assurez-vous qu'il y est au moins 8 caractères, une majuscule et minuscule, ainsi qu'un chiffre et un caractère spécial")
        entry_mot_de_passe.delete(0, tk.END)

def save_mot_de_passe():
    mdp = entry_mot_de_passe.get()
    if mdp:
        mdp_hash = hash_mdp(mdp)
        if save(mdp_hash):
            aff_msg("Mot de passe sauvegardé avec succès")
        else:
            aff_msg("Le mot de passe existe déjà dans la base de données")
    else:
        aff_msg("Veuillez saisir un mot de passe avant de sauvegarder")

def save(mdp_hash, filename="mots_de_passe.json"):
    try:
        with open(filename, "r") as file:
            file_content = file.read().strip()
            if file_content:
                passwords = json.loads(file_content)
            else:
                passwords = []
    except FileNotFoundError:
        passwords = []

    if mdp_hash not in passwords:
        passwords.append(mdp_hash)
        with open(filename, "w") as file:
            json.dump(passwords, file)
        return True
    else:
        return False

def check():
    if show_pass.get():
        mdp_entry.configure(show="")
    else:
        mdp_entry.configure(show="*")

def list_mdp(filename="mots_de_passe.json"):
    with open(filename) as file:
        data=json.load(file)
        aff_msg(data)


# Fenêtre principale
fenetre = CTk()
fenetre.title("Vérificateur et Générateur de mot de passe")
fenetre.geometry("501x300")
fenetre.minsize(501,300)
set_appearance_mode("dark")
Grid.rowconfigure(fenetre,0,weight=1)
Grid.columnconfigure(fenetre,0,weight=1)
Grid.rowconfigure(fenetre,1,weight=1)

# Widgets
label_mot_de_passe = customtkinter.CTkLabel(master = fenetre, text="Mot de passe :")
label_mot_de_passe.grid(row=0, column=0, columnspan=2, pady=1)

entry_mot_de_passe = customtkinter.CTkEntry(master = fenetre, show="*")
entry_mot_de_passe.grid(row=1, column=0, columnspan=2, pady=1)
mdp_entry = entry_mot_de_passe

entry = customtkinter.CTkEntry
show_pass = tk.IntVar()
checkbutton = CTkCheckBox(master = fenetre, text='Afficher mot de passe', variable=show_pass, command=check)
checkbutton.grid(row=2, column=0, columnspan=2, pady=1)

bouton_verifier = customtkinter.CTkButton(master = fenetre, text="Vérifier", corner_radius = 30, fg_color='green',text_color='black',  border_color='black', border_width=2, command=verif_affich)
bouton_verifier.grid(row=3, column=0, columnspan=2, pady=1)

bouton_generer = customtkinter.CTkButton(master = fenetre, text="Générer mot de passe", corner_radius = 30, fg_color='blue',text_color='black',  border_color='black', border_width=2, command=gen)
bouton_generer.grid(row=4, column=0, columnspan=2, pady=1)

bouton_save = customtkinter.CTkButton(master = fenetre, text="Sauvegarder", corner_radius = 30, fg_color='red',text_color='black',  border_color='black', border_width=2, command=save_mot_de_passe)
bouton_save.grid(row=5, column=0, columnspan=2, pady=1)

bouton_list = customtkinter.CTkButton(master = fenetre, text="Liste mots de passe", corner_radius = 30, fg_color='yellow',text_color='black', border_color='black', border_width=2, command=list_mdp)
bouton_list.grid(row=6, column=0, columnspan=2, pady=1)

text_aff = customtkinter.CTkTextbox(master = fenetre, height=50, width=487, state=tk.DISABLED)
text_aff.grid(row=7, column=0, columnspan=2, pady=10)



# Lancement boucle principale
fenetre.mainloop()
