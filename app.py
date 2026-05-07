import streamlit as st


# --- ÉTAPE 1 : ON DÉFINIT LE SAC À DOS 'g' (OBLIGATOIRE ICI) ---
g = st.session_state



# --- ÉTAPE 2 : LA BARRE LATÉRALE AVEC LES DEUX FENÊTRES ---
with st.sidebar:
    st.title("🎮 Magic the Gathering")
   
    # 📜 FENÊTRE 1 : L'HISTORIQUE (Les actions de jeu uniquement)
    st.subheader("📜 Historique du Duel")
    if 'history' not in g:
        g['history'] = ["Début de la partie"]
   
    # On affiche les 15 dernières actions de jeu pour que ce soit clair
    hist_text = "\n".join(g['history'][-15:])
    st.text_area("Actions", value=hist_text, height=180, disabled=True, key="hist_area")


    st.markdown("---")


    # 💬 FENÊTRE 2 : LE CHAT (Ta discussion avec l'IA)
    st.subheader("💬 Discussion avec Kael")
    if 'chat_msgs' not in g:
        g['chat_msgs'] = ["Kael : Je t'attends, Steeven. Tu es prêt ?"]
   
    chat_text = "\n".join(g['chat_msgs'])
    st.text_area("Chat", value=chat_text, height=220, disabled=True, key="chat_area")


    # Zone de saisie pour parler à l'IA
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_input = st.text_input("Lui dire quelque chose :", placeholder="Taquine-le...")
        if st.form_submit_button("Envoyer") and user_input:
            g['chat_msgs'].append(f"Steeven : {user_input}")
            # Réponse auto de Kael
            g['chat_msgs'].append("Kael : On verra si tu es aussi fort avec tes cartes qu'avec tes mots.")
            st.rerun()


    # ⚙️ LE RESTE (Paramètres / Jetons)
    st.markdown("---")
    with st.expander("⚙️ PARAMÈTRES & JETONS"):
        st.write("💎 Jetons actifs :")
        for t in g.get('player_tokens', []):
            st.write(f"• {t['name']}")


# --- ÉTAPE 1 : MISE À JOUR DE LA BIBLIOTHÈQUE AVEC SYMBOLES ---
CARD_DB = {
    "Hedron Crab": {
        "name_fr": "Crabe d'Hédron",
        "type": "Créature",
        "mana": "💧",
        "desc": "Toucheterre — À chaque fois qu'un terrain arrive sur le champ de bataille sous votre contrôle, le joueur ciblé meule trois cartes."
    },
    "Polluted Delta": {
        "name_fr": "Delta pollué",
        "type": "Terrain",
        "mana": "🔘",
        "desc": "Engagez, payez 1 PV, sacrifiez le Delta pollué : Cherchez dans votre bibliothèque une carte d'Île ou de Marais et mettez-la sur le champ de bataille."
    },
    "Tasha's Hideous Laughter": {
        "name_fr": "Rire atroce de Tasha",
        "type": "Rituel",
        "mana": "🔘💧💧",
        "desc": "Chaque adversaire exile les cartes du dessus de sa bibliothèque jusqu'à ce qu'il ait exilé des cartes d'une valeur de mana totale de 20 ou plus."
    },
    "Glimpse the Unthinkable": {
        "name_fr": "Aperçu de l'inimaginable",
        "type": "Rituel",
        "mana": "💧💀",
        "desc": "Le joueur ciblé meule dix cartes."
    },
    "Archive Trap": {
        "name_fr": "Piège d'archive",
        "type": "Éphémère",
        "mana": "🔘🔘🔘💧💧 (ou 0)",
        "desc": "Si un adversaire a cherché dans sa bibliothèque ce tour-ci, vous pouvez payer 0 au lieu de payer le coût de mana de ce sort. Le joueur ciblé meule treize cartes."
    },
    "Dark Ritual": {
        "name_fr": "Messe noire",
        "type": "Éphémère",
        "mana": "💀",
        "desc": "Ajoutez 💀💀💀 à votre réserve de mana."
    },
    "Jace's Phantasm": {
        "name_fr": "Phantasme de Jace",
        "type": "Créature",
        "mana": "💧",
        "desc": "Vol. Le Phantasme de Jace gagne +4/+4 tant qu'un adversaire a au moins dix cartes dans son cimetière."
    },
    "Visions of Beyond": {
        "name_fr": "Visions de l'au-delà",
        "type": "Éphémère",
        "mana": "💧",
        "desc": "Piochez une carte. Si un cimetière contient vingt cartes ou plus, piochez trois cartes à la place."
    },
    "Watery Grave": {
        "name_fr": "Tombeau aquatique",
        "type": "Terrain",
        "mana": "🔘",
        "desc": "(💧 ou 💀) Arrive engagé à moins que vous ne payiez 2 points de vie. Est une Île et un Marais."
    },
    "Island": {
        "name_fr": "Île",
        "type": "Terrain",
        "mana": "💧",
        "desc": "Terrain de base : Génère 1 mana Bleu."
   },
    "Swamp": {
        "name_fr": "Marais",
        "type": "Terrain",
        "mana": "💀",
        "desc": "Terrain de base : Génère 1 mana Noir."
   },
    "Archimage's Charm":   {"name_fr": "Charme de l'archimage",   "type": "Sort",     "mana": "💧💧💧", "desc": "Contre / Pioche 2 / Vole coût 1."},
    "Counterspell":        {"name_fr": "Contresort",              "type": "Sort",     "mana": "💧💧",   "desc": "Annule le sort ciblé."},
    "Guile":               {"name_fr": "Ruse",                    "type": "Créature", "mana": "💧💧💧3", "desc": "6/6 imblocable. Si tu contres, joue le sort gratos."},
    "Opt":                 {"name_fr": "Opter",                   "type": "Sort",     "mana": "💧",     "desc": "Regard 1, puis pioche 1."},
    "Mana Leak":           {"name_fr": "Fuite de mana",           "type": "Sort",     "mana": "💧1",    "desc": "Contre sauf si l'adversaire paie 3."},
    "Negate":              {"name_fr": "Négation",                "type": "Sort",     "mana": "💧1",    "desc": "Contre sort non-créature."},
    "Essence Scatter":     {"name_fr": "Dispersion d'essence",    "type": "Sort",     "mana": "💧1",    "desc": "Contre sort de créature."},
    "Visions of Beyond":   {"name_fr": "Visions de l'au-delà",    "type": "Sort",     "mana": "💧",     "desc": "Pioche 1 (ou 3 si cimetière > 20)."},
    "Island":              {"name_fr": "Île",                     "type": "Terrain",  "mana": "",       "desc": "Ajoute 💧"},
    "Lava Spike":          {"name_fr": "Pointe de lave",          "type": "Sort",     "mana": "🔥",     "desc": "3 blessures au joueur."},
    "Lightning Bolt":      {"name_fr": "Foudre",                  "type": "Sort",     "mana": "🔥",     "desc": "3 blessures n'importe où."},
    "Skewer the Critics":  {"name_fr": "Embrocher les critiques", "type": "Sort",     "mana": "🔥2",    "desc": "3 blessures. Spectacle : 🔥."},
    "Rift Bolt":           {"name_fr": "Foudre de faille",        "type": "Sort",     "mana": "🔥2",    "desc": "3 blessures. Suspension : 🔥."},
    "Fireblast":           {"name_fr": "Salve de feu",            "type": "Sort",     "mana": "🔥2",    "desc": "4 blessures. Sacrifice 2 Montagnes pour gratuit."},
    "Ball Lightning":      {"name_fr": "Boule fulgurante",        "type": "Créature", "mana": "🔥🔥🔥", "desc": "6/1 Piétinement, Célérité. Meurt à la fin du tour."},
    "Shock":               {"name_fr": "Choc",                    "type": "Sort",     "mana": "🔥",     "desc": "2 blessures n'importe où."},
    "Incinerate":          {"name_fr": "Incinération",            "type": "Sort",     "mana": "🔥1",    "desc": "3 blessures, pas de régénération."},
    "Chain Lightning":     {"name_fr": "Chaîne d'éclairs",        "type": "Sort",     "mana": "🔥",     "desc": "3 blessures. Peut être dupliqué."},
    "Mountain":            {"name_fr": "Montagne",                "type": "Terrain",  "mana": "",       "desc": "Ajoute 🔥"},
}




# --- ÉTAPE 2 : LE MOTEUR D'AFFICHAGE AVEC BULLE TRADUITE ---




def show_card(name, width=None):
    """Affiche une carte avec une bulle de traduction système (Tooltip) au survol."""
    # 1. On récupère les données dans ta CARD_DB
    info = CARD_DB.get(name, {})
    nom_fr = info.get("name_fr", name)
    mana = info.get("mana", "0")
    txt = info.get("desc", "")
   
    # 2. Préparation du texte de la bulle (le title ne supporte pas le HTML, on reste simple)
    # On nettoie les sauts de ligne pour que la bulle soit bien formatée par le navigateur
    bulle_propre = f"{nom_fr} (Mana: {mana}) - {txt}".replace("\n", " ")
   
    # 3. Récupération du lien de l'image
    img_url = get_card(name)
   
    # 4. Définition de la largeur (width)
    # Si width est précisé (ex: 80), on l'applique. Sinon, on prend 100% de la colonne.
    style_largeur = f"width:{width}px;" if width else "width:100%;"




    # 5. Création du code HTML
    # L'attribut 'title' crée la bulle. 'cursor:help' change le curseur en point d'interrogation.
    html_code = f"""
    <div title="{bulle_propre}" style="cursor:help; {style_largeur} display:inline-block;">
        <img src="{img_url}" style="width:100%; border-radius:8px;">
    </div>
    """
   
    # 6. Affichage final
    st.markdown(html_code, unsafe_allow_html=True)
    # Au lieu d'une bulle au survol, on affiche un petit texte discret
    # qui contient la traduction juste au-dessus de l'image
    #with st.container():
        #st.markdown(f"**{nom_fr}** ({mana})")
        #return st.image(get_card(name), width=width, use_container_width=(width is None))








def get_card(name):
    # Cette fonction transforme le nom de la carte en lien URL pour l'image
    name_url = name.replace(" ", "+")
    return f"https://api.scryfall.com/cards/named?fuzzy={name_url}&format=image"








# --- CONFIGURATION V66 : SIDEBAR + ESPACE AÉRÉ ---
st.set_page_config(page_title="Magic: Steeven vs Kael", layout="wide")








st.markdown("""
    <style>
    .grave-box {
        background: white; border-radius: 8px; padding: 5px;
        border: 1px solid #cfd8dc; width: 100%;
    }
    .grave-item { font-size: 0.65em; display: flex; justify-content: space-between; line-height: 1.2; }
    .phase-bar {
        display: flex; justify-content: space-around;
        background: #2c3e50; padding: 6px; border-radius: 6px;
        margin: 10px 0; width: 100%;
    }
    .phase-step { color: #7f8c8d; font-size: 0.65em; font-weight: bold; text-transform: uppercase; }
    .phase-active { color: #2ecc71; border-bottom: 2px solid #2ecc71; }
    </style>
    """, unsafe_allow_html=True)


import random


DECKS = {
    "Meule (Bleu / Noir)": ["Hedron Crab"]*4 + ["Glimpse the Unthinkable"]*4 + ["Archive Trap"]*4 + ["Tasha's Hideous Laughter"]*4 + ["Jace's Phantasm"]*4 + ["Dark Ritual"]*4 + ["Visions of Beyond"]*3 + ["Polluted Delta"]*4 + ["Watery Grave"]*24,
    "Contrôle (Bleu)": ["Archimage's Charm"]*4 + ["Counterspell"]*4 + ["Guile"]*2 + ["Opt"]*4 + ["Mana Leak"]*4 + ["Negate"]*4 + ["Essence Scatter"]*4 + ["Visions of Beyond"]*4 + ["Island"]*24,
    "Burn (Rouge)":    ["Ball Lightning"]*4 + ["Lightning Bolt"]*4 + ["Lava Spike"]*4 + ["Skewer the Critics"]*4 + ["Rift Bolt"]*4 + ["Fireblast"]*4 + ["Shock"]*4 + ["Incinerate"]*4 + ["Chain Lightning"]*4 + ["Mountain"]*24
}


# --- INITIALISATION DYNAMIQUE ---
    

# --- ÉCRAN D'ACCUEIL (MENU) ---
if 'game' not in st.session_state or not st.session_state.game.get('started', False):
    st.title("⚔️ MAGIC THE GATHERING")
    st.subheader("Menu Principal")
    
    col_a, col_b = st.columns(2)
    with col_a:
        choix_p = st.selectbox("Ton Deck (Steeven) :", list(DECKS.keys()), index=0)
    with col_b:
        choix_ai = st.selectbox("Deck de Kael :", list(DECKS.keys()), index=1)
    
    diff_ai = st.select_slider("Niveau de difficulté de Kael :", options=range(1, 11), value=5)
    
    if st.button("🚀 LANCER LE DUEL", use_container_width=True):
        p_deck = DECKS[choix_p][:]
        ai_deck = DECKS[choix_ai][:]
        random.shuffle(p_deck)
        random.shuffle(ai_deck)
        
        st.session_state.game = {
            'started': True,
            'p_hp': 20, 'ai_hp': 20, 'p_mana': 0,
            'p_deck': p_deck[7:], 'p_hand': p_deck[:7],
            'p_land': [], 'p_board': [],
            'p_grave': {'Créas': 0, 'Sorts': 0, 'Lands': 0},
            'ai_deck': ai_deck[7:], 'ai_hand': ai_deck[:7],
            'ai_land': [], 'ai_board': [],
            'ai_grave': {'Créas': 0, 'Sorts': 0, 'Lands': 0},
            'history': ["Début de la partie"],
            'chat': [{"u": "Kael", "m": "Bonne chance Steeven !"}],
            'phase': "PRINCIPALE 1",
            'diff_ai': diff_ai
        }
        st.rerun()
    st.stop()

# --- SI LA PARTIE EST LANCÉE ---
else:
    with st.sidebar:
        st.write("---")
        # On utilise un "popover" pour la confirmation (plus propre)
        with st.popover("❌ Abandonner le Duel"):
            st.warning("Es-tu sûr de vouloir quitter ?")
            st.error("⚠️ Quitter sans sauvegarder sera compté comme une **DÉFAITE** dans tes stats.")
            
            # Le bouton de confirmation finale
            if st.button("Confirmer l'abandon"):
                # Ici on pourra plus tard ajouter : st.session_state.stats['defaites'] += 1
                st.session_state.game['started'] = False
                st.rerun()
        
        # Optionnel : bouton de sauvegarde (pour plus tard)
        if st.button("💾 Sauvegarder et Quitter"):
            st.info("Sauvegarde bientôt disponible...")
            # Ici on pourra mettre la logique de sauvegarde SQL ou fichier
    # Ton raccourci habituel
    g = st.session_state.game

g = st.session_state.game # On crée un raccourci pour plus tard


# --- LES FONCTIONS (Le Cerveau du Jeu) ---

def kael_turn():
    # 1. Kael pioche
    if g['ai_deck']:
        g['ai_hand'].append(g['ai_deck'].pop(0))
    # 2. Kael joue une Montagne s'il en a une
    for i, card in enumerate(g['ai_hand']):
        if card == "Mountain":
            land = g['ai_hand'].pop(i)
            g['ai_land'].append({"name": land, "tapped": False})
            g['history'].insert(0, "🔥 Kael joue une Montagne")
            break
    st.rerun()


# --- LOGIQUE DE JEU ---

def execute_mill(target_deck, target_grave, amount):
    """Meule un nombre 'amount' de cartes du deck vers le cimetière."""
    g = st.session_state.game
    for _ in range(amount):
        if g.get(target_deck):
            card = g[target_deck].pop(0)
            # Sécurité : force le cimetière à être une liste
            if not isinstance(g.get(target_grave), list):
                g[target_grave] = []
            g[target_grave].append(card)




def play_card(card_index):
    g = st.session_state.game
    card_name = g['p_hand'][card_index]
   
    lands = ["Island", "Swamp", "Polluted Delta", "Watery Grave"]




    # 1. ACTION : On vérifie si c'est un terrain
    if card_name in lands:
        # On retire la carte de la main
        g['p_hand'].pop(card_index)
       
        # 1. On retire la carte de la main
        card_obj = g['p_hand'].pop(card_index)
       
        # 2. On l'ajoute à tes terrains sur le plateau
        if 'player_land' not in g:
            g['player_land'] = []
        g['player_land'].append(card_obj)
       
        # 3. On met à jour ton nouvel historique (en haut à gauche)
        g['history'].append(f"Steeven joue un terrain : {card_name}")
       
        st.rerun()
        g['p_land'] = []
        g['p_land'].append({"name": card_name, "tapped": False})




        # 2. EFFET SECONDAIRE : Le Crabe vérifie si on a joué un terrain
        if any(c['name'] == "Hedron Crab" for c in g.get('p_board', [])):
            execute_mill('ai_deck', 'ai_grave', 3)
       
        # On rafraîchit l'écran
        st.rerun()
       
        # SÉCURITÉ : On s'assure que p_land est une LISTE
        if not isinstance(g.get('p_land'), list):
            g['p_land'] = []
        g['p_land'].append({"name": card_name, "tapped": False})




        # 2. EFFET DU CRABE
        if any(c['name'] == "Hedron Crab" for c in g.get('p_board', [])):
            for _ in range(3):
                if g.get('ai_deck'):
                    card = g['ai_deck'].pop(0)
                   
                    # CORRECTION CRITIQUE : On force ai_grave à être une LISTE ici
                    if not isinstance(g.get('ai_grave'), list):
                        g['ai_grave'] = []
                   
                    g['ai_grave'].append(card)
         
        st.rerun()
    else:
        # Ici on ajoutera plus tard la logique pour les sorts et créatures
        pass
        # 3. CRÉATURE : Demande du mana
        if g['p_mana'] >= 1:
            g['p_hand'].pop(card_index)
            g['p_mana'] -= 1
            g['p_board'].append({"name": card_name, "tapped": False})
            st.rerun()
        else:
            st.error("⚠️ Pas assez de mana ! Engage une Island.")
    st.rerun()


# ==========================================
# 2. PLATEAU DE JEU (ZONE 4)
# ==========================================


# On laisse des colonnes vides (0.5) sur les côtés pour "aérer" comme demandé
_, center_col, _ = st.columns([0.5, 9, 0.5])


with center_col:
# ==========================================
    # ZONE JOUEUR (KAEL)
    # ==========================================
    # On définit les colonnes ici pour qu'elles existent avant d'être utilisées
    col_k_cards, col_k_grave = st.columns([8, 2])
   
    with col_k_cards:
        # Main de Kael (dos des cartes)
        k_cols = st.columns(7)
        for i in range(7):
            k_cols[i].image("https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/thumb/f/f8/Magic_card_back.jpg/250px-Magic_card_back.jpg", use_container_width=True)
        st.markdown(f'<div style="background:white; padding:5px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-top:10px;"><b>🖥️ KAEL</b> | <span style="color:#ff4757;">❤️ {g["ai_hp"]} HP</span></div>', unsafe_allow_html=True)




    with col_k_grave:
        # On récupère les données du cimetière de l'IA
        ai_g = g.get('ai_grave', {'Créas': 0, 'Sorts': 0, 'Lands': 0, 'Artifacts': 0, 'Enchants': 0})
        total_ai = sum(ai_g.values()) if isinstance(ai_g, dict) else len(ai_g)
       
        st.markdown(f"""
            <div style="border:2px solid #ef5350; border-radius:10px; padding:10px; background:white;">
                <p style="margin:0; font-size:0.8em; color:#ef5350;"><b>🪦 CIMETIÈRE ({total_ai})</b></p>
                <hr style="margin:5px 0;">
                <p style="margin:0; font-size:0.8em;">🌍 Terrains: <b>{ai_g.get('Lands', 0) if isinstance(ai_g, dict) else 0}</b></p>
                <p style="margin:0; font-size:0.8em;">👾 Créature: <b>{ai_g.get('Créas', 0) if isinstance(ai_g, dict) else 0}</b></p>
                <p style="margin:0; font-size:0.8em;">📜 Sorts: <b>{ai_g.get('Sorts', 0) if isinstance(ai_g, dict) else 0}</b></p>
                <p style="margin:0; font-size:0.8em;">💎 Artéfact: <b>{g.get('Artifacts', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">✨ Enchantement: <b>{g.get('Enchants', 0)}</b></p>
            </div>
        """, unsafe_allow_html=True)
        # ... (Code du cimetière finit ici)
# --- 1. ZONE KAEL (ADVERSAIRE) ---
    st.write("")


    # A. TITRE ET LOGIQUE DES TERRAINS
    st.markdown("#### 🌍 TERRAINS DE KAEL")
   
    # Intelligence pour que Kael joue ses terrains
    if g.get('turn_owner') == 'ai' and not g.get('ai_land_played'):
        ai_hand = g.get('ai_hand', [])
        lands = [c for c in ai_hand if CARD_DB.get(c['name'], {}).get('type') == 'Land']
        if lands:
            land_to_play = lands[0]
            g['ai_land'].append({'name': land_to_play['name'], 'tapped': False})
            g['ai_hand'].remove(land_to_play)
            g['ai_land_played'] = True
            st.rerun()


    # B. AFFICHAGE RÉEL DES TERRAINS (LES IMAGES)
    ai_lands = g.get('ai_land', [])
    if ai_lands:
        cols_ai_l = st.columns(10)
        for idx, land in enumerate(ai_lands):
            with cols_ai_l[idx % 10]:
                img_url = get_card(land["name"])
                st.markdown(f'<img src="{img_url}" style="width:80px; border-radius:5px; border:1px solid #444;">', unsafe_allow_html=True)
    else:
        st.write("*(Kael n'a pas encore de terrains en jeu)*")


    st.write("")


    # C. SES BOUTONS (POUR LA SYMÉTRIE)
    kb = st.columns([1, 1, 1, 1, 1])
    kb[0].button("?? PIOCHE", key="btn_ai_at", disabled=True, use_container_width=True)
    kb[1].button("🛡️ MAIN 1", key="btn_ai_bl", disabled=True, use_container_width=True)
    kb[2].button("⚔️ COMBAT", key="btn_ai_gr", disabled=True, use_container_width=True)
    kb[3].button("🛡️ MAIN 2", key="btn_ai_bi", disabled=True, use_container_width=True)
    kb[4].button("🏁 FIN", key="btn_ai_end", disabled=True, use_container_width=True)


    st.markdown("---") # Séparation vers le CHAMP DE BATAILLE




      # ==========================================
    # ZONE JOUEUR (steeven)
    # ==========================================


    st.markdown("---")
   
    # 1. TES BOUTONS (Bien collés au champ de bataille)
    # On réduit l'écart avec st.container()
    with st.container():
        kb_player = st.columns([1, 1, 1, 1, 1])
        kb_player[0].button("?? PIOCHE", key="p_draw", use_container_width=True)
        kb_player[1].button("🛡️ MAIN 1", key="p_m1", use_container_width=True)
        kb_player[2].button("⚔️ COMBAT", key="p_comb", use_container_width=True)
        kb_player[3].button("🛡️ MAIN 2", key="p_m2", use_container_width=True)
        kb_player[4].button("🏁 FIN", key="p_end", use_container_width=True)


   
    # 2. TES TERRAINS (Tout en bas)
    st.markdown("#### 🌍 MES TERRAINS")
    player_lands = g.get('player_land', [])
    if player_lands:
        cols_p_l = st.columns(10)
        for idx, land in enumerate(player_lands):
            with cols_p_l[idx % 10]:
                img_url = get_card(land["name"])
                st.markdown(f'<img src="{img_url}" style="width:80px; border-radius:5px; border:1px solid #444; margin-bottom:5px;">', unsafe_allow_html=True)
    else:
        st.write("*(Aucun terrain en jeu)*")
   
        st.markdown("<br>", unsafe_allow_html=True)


    # Ligne d'info avec PV et Coeur (Annotation 2)
    col_p_cards, col_p_grave = st.columns([8, 2])


    with col_p_cards:
        # On remet le petit coeur et les PV à côté de ton nom
        st.markdown(f'<div style="background:white; padding:5px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-top:10px;"><b>🖥️ STEEVEN</b> | <span style="color:#ff4757;">❤️ {g["ai_hp"]} HP</span></div>', unsafe_allow_html=True)
     
        # Affichage de la main
        if st.session_state.game['p_hand']:
            p_cols = st.columns(7)
            for i, card_name in enumerate(st.session_state.game['p_hand'][:7]):
                with p_cols[i]:
                    if st.button("Jouer", key=f"btn_p_play_{i}"):
                        play_card(i)
                    show_card(card_name)




# Ligne d'info avec ton Cimetière
    col_p_cards, col_p_grave = st.columns([8, 2])




        # ... (ton code pour afficher la main ici) ...




    with col_p_grave:
        p_g = g.get('p_grave', {'Créas': 0, 'Sorts': 0, 'Lands': 0, 'Artifacts': 0, 'Enchants': 0})
        total_p = sum(p_g.values()) if isinstance(p_g, dict) else len(p_g)
       
        st.markdown(f"""
            <div style="border:2px solid #42a5f5; border-radius:10px; padding:10px; background:white;">
                <p style="margin:0; font-size:0.8em; color:#1e88e5;"><b>🪦 CIMETIÈRE ({total_p})</b></p>
                <hr style="margin:5px 0; border-top:1px solid #42a5f5;">
                <p style="margin:0; font-size:0.8em;">🌍 Terrains: <b>{g.get('Lands', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">👾 Créature: <b>{g.get('Créas', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">📜 Sorts: <b>{g.get('Sorts', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">💎 Artéfact: <b>{g.get('Artifacts', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">✨ Enchantement: <b>{g.get('Enchants', 0)}</b></p>
            </div>
        """, unsafe_allow_html=True)






