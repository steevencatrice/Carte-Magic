import streamlit as st
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


# --- DECKS ---
DECKS = {
    "Meule": ["Hedron Crab"]*4 + ["Glimpse the Unthinkable"]*4 + ["Archive Trap"]*4 + ["Tasha's Hideous Laughter"]*4 + ["Jace's Phantasm"]*4 + ["Dark Ritual"]*4 + ["Visions of Beyond"]*3 + ["Polluted Delta"]*4 + ["Watery Grave"]*4 + ["Island"]*15 + ["Swamp"]*10,
    "Burn": ["Ball Lightning"]*4 + ["Lightning Bolt"]*4 + ["Lava Spike"]*4 + ["Skewer the Critics"]*4 + ["Rift Bolt"]*4 + ["Fireblast"]*4 + ["Shock"]*4 + ["Incinerate"]*4 + ["Chain Lightning"]*4 + ["Mountain"]*24
}


# --- INITIALISATION ---
if 'game' not in st.session_state:
    p_deck = DECKS["Meule"][:]
    ai_deck = DECKS["Burn"][:]
    random.shuffle(p_deck)
    random.shuffle(ai_deck)


    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20, 'p_mana': 0,
        'p_deck': p_deck[7:], 'p_hand': p_deck[:7],
        'p_land': [], 'p_board': [],
        'p_grave': {'Créas': 0, 'Sorts': 0, 'Lands': 0},
        'ai_deck': ai_deck[7:], 'ai_hand': ai_deck[:7],
        'ai_land': [], 'ai_board': [],
        'ai_grave': {'Créas': 0, 'Sorts': 0, 'Lands': 0},
        'history': ["Début de la partie"],
        'chat': [{"u": "Kael", "m": "Bonne chance Steeven !"}],
        'phase': "PRINCIPALE 1"
    }


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
def play_card(card_index):
    # On récupère l'état global
    g = st.session_state.game
    card_name = g['p_hand'][card_index]
   
def play_card(card_index):
    g = st.session_state.game
    card_name = g['p_hand'][card_index]
    lands = ["Island", "Swamp", "Polluted Delta", "Watery Grave"]
   
    if card_name in lands:
        # 1. On joue le terrain
        g['p_hand'].pop(card_index)
        g['p_land'].append({"name": card_name, "tapped": False})
       
        # 2. EFFET DU CRABE : Meule 3 cartes si un Crabe est là
        if any(c['name'] == "Hedron Crab" for c in g['p_board']):
            for _ in range(3):
                if g['ai_deck']:
                    card = g['ai_deck'].pop(0)
                    g['ai_grave'].append(card)
        st.rerun()
       
    else:
        # 3. CRÉATURE : Demande du mana
        if g['p_mana'] >= 1:
            g['p_hand'].pop(card_index)
            g['p_mana'] -= 1
            g['p_board'].append({"name": card_name, "tapped": False})
            st.rerun()
        else:
            st.error("⚠️ Pas assez de mana ! Engage une Island.")
    st.rerun()


# --- 3. CHAMP DE BATAILLE ---
    st.markdown('<div style="margin-top:25px;"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="background:#eceff1; border-radius:12px; border:2px solid #b0bec5; padding:20px; min-height:400px;">', unsafe_allow_html=True)
       
        # AFFICHAGE DES TERRAINS (p_land)
        if g['p_land']:
            cols_land = st.columns(10)
            for idx, land in enumerate(g['p_land']):
                with cols_land[idx % 10]:
                    angle = 90 if land['tapped'] else 0
                    st.markdown(f'<img src="{get_card(land["name"])}" style="transform:rotate({angle}deg); width:80px; transition:0.3s;">', unsafe_allow_html=True)
                    # Vérifie que cette ligne est unique dans tout ton fichier !
                    if st.button("🔄", key=f"battle_tap_{idx}"):
                        land['tapped'] = not land['tapped']
                        g['p_mana'] += 1 if land['tapped'] else -1
                        st.rerun()


        # AFFICHAGE DES CRÉATURES (p_board)
        if g['p_board']:
            st.write("---")
            cols_board = st.columns(6)
            for idx, crea in enumerate(g['p_board']):
                with cols_board[idx % 6]:
                    st.image(get_card(crea['name']), width=100)
                    st.caption("Creature")


        st.markdown('</div>', unsafe_allow_html=True)
# ==========================================
# 1. SIDEBAR (ZONES 1, 2, 3)
# ==========================================
with st.sidebar:
    st.header("🎮 MENU MAGIC")
   
    # Emplacement futur Chrono
    st.markdown('<div class="chrono-display">⏱️ 19:20 - OBJECTIF CERVEAU</div>', unsafe_allow_html=True)
   
    # Zone 1 : Gestion (Placeholder pour tes futurs boutons)
    with st.expander("🛠️ OPTIONS & JETONS", expanded=False):
        st.button("➕ Ajouter Jeton", use_container_width=True)
        st.button("⚙️ Paramètres", use_container_width=True)


    # Zone 2 : Chat
    st.caption("💬 CHAT")
    chat_content = "".join([f"<b>{m['u']}</b>: {m['m']}<br>" for m in g['chat'][-10:]])
    st.markdown(f'<div class="sidebar-box" style="height:250px; overflow-y:auto;">{chat_content}</div>', unsafe_allow_html=True)
    m_in = st.text_input("...", key="side_chat", label_visibility="collapsed")
    if st.button("Envoyer", key="side_btn", use_container_width=True):
        if m_in: g['chat'].append({"u": "Steeven", "m": m_in}); st.rerun()


    # Zone 3 : Historique
    st.caption("📜 ACTIONS")
    h_txt = "".join([f"• {a}<br>" for a in g.get('history', [])[-10:]])
    st.markdown(f'<div class="sidebar-box" style="height:150px; overflow-y:auto;">{h_txt}</div>', unsafe_allow_html=True)


# ==========================================
# 2. PLATEAU DE JEU (ZONE 4)
# ==========================================


# On laisse des colonnes vides (0.5) sur les côtés pour "aérer" comme demandé
_, center_col, _ = st.columns([0.5, 9, 0.5])


with center_col:
 # --- 1. SECTION KAEL (Haut) ---
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

    # --- ESPACE ICI ---
    st.write("") # Crée un saut de ligne standard
    # ------------------


    # --- 2. BOUTONS KAEL (Grisés / Dynamiques) ---
    ai_status = g.get('ai_status', 'thinking')
    kb = st.columns([1, 1, 1, 1, 1.5])
    kb[0].button("⚔️ ATK", key="btn_ai_at", type="primary" if ai_status == 'attacking' else "secondary", disabled=True, use_container_width=True)
    kb[1].button("🛡️ BLOC", key="btn_ai_bl", type="primary" if ai_status == 'blocking' else "secondary", disabled=True, use_container_width=True)
    kb[2].button("⚰️ GRAVE", key="btn_ai_gr", disabled=True, use_container_width=True)
    kb[3].button("🔍 BIBLIO", key="btn_ai_bi", disabled=True, use_container_width=True)
    kb[4].button("🏁 FIN", key="btn_ai_end", type="primary" if ai_status == 'ending' else "secondary", disabled=True, use_container_width=True)


# ==========================================
# ZONE JOUEUR (STEEVEN)
# ==========================================

# 1. Barre d'infos (Nom + HP à droite comme Kael)
st.markdown(f"""
    <div style="background:white; padding:10px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
        <b>👤 STEEVEN</b>
        <span style="color:#e91e63; font-weight:bold;">❤️ {st.session_state.game.get('p_hp', 20)} HP</span>
    </div>
""", unsafe_allow_html=True)

# 2. Affichage de la Main (Correction de la représentation des cartes)
if st.session_state.game['p_hand']:
    # On crée 7 colonnes pour les 7 cartes max en main
    p_cols = st.columns(7)
    for i, card_name in enumerate(st.session_state.game['p_hand'][:7]):
        with p_cols[i]:
            # Bouton pour jouer la carte
            if st.button("Jouer", key=f"btn_p_play_{i}"):
                play_card(i)
            
            # ICI : Affichage de l'image de la carte (La ligne manquante !)
            st.image(get_card(card_name), use_container_width=True)
else:
    st.info("Votre main est vide.")

# 3. Suppression du doublon (On s'arrête ici, ne remets pas de deuxième barre STEEVEN)


    # --- 2. TES TERRAINS (ALIGNÉS SUR LA MÊME TAILLE) ---
    st.markdown("#### 🌍 MES TERRAINS")
   
    if st.session_state.game['p_land']:
        cols_l = st.columns(10)
        for idx, land in enumerate(st.session_state.game['p_land']):
            with cols_l[idx % 10]:
                angle = 90 if land['tapped'] else 0
                # Largeur 80px pour tout le monde
                st.markdown(f'<img src="{get_card(land["name"])}" style="transform:rotate({angle}deg); width:80px; border-radius:5px;">', unsafe_allow_html=True)
                if st.button("TAP", key=f"t_land_{idx}"):
                    st.session_state.game['p_land'][idx]['tapped'] = not st.session_state.game['p_land'][idx]['tapped']
                    st.session_state.game['p_mana'] += 1 if st.session_state.game['p_land'][idx]['tapped'] else -1
                    st.rerun()


    st.markdown("---")
    # --- 3. TA SECTION (STEEVEN) ---
    st.markdown("---")
   
    # Barre d'actions (Annotation 1)
    col_atk, col_bloc, col_grave, col_biblio, col_fin = st.columns(5)
    with col_atk: st.button("⚔️ ATK", use_container_width=True)
    with col_bloc: st.button("🛡️ BLOC", use_container_width=True)
    with col_grave: st.button("⚰️ GRAVE", use_container_width=True)
    with col_biblio: st.button("🔍 BIBLIO", use_container_width=True)
    with col_fin: st.button("🏁 FIN", use_container_width=True)


    st.markdown("<br>", unsafe_allow_html=True)


    # Ligne d'info avec PV et Coeur (Annotation 2)
    col_p_cards, col_p_grave = st.columns([8, 2])


    with col_p_cards:
        # On remet le petit coeur et les PV à côté de ton nom
        st.markdown(f"""
            <div style="background:white; padding:10px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
                <b>👤 STEEVEN</b>
                <span style="color:#e91e63;">❤️ {st.session_state.game.get('p_hp', 20)} HP</span>
            </div>
        """, unsafe_allow_html=True)
       
        # Affichage de la main
        if st.session_state.game['p_hand']:
            p_cols = st.columns(7)
            for i, card_name in enumerate(st.session_state.game['p_hand'][:7]):
                with p_cols[i]:
                    if st.button("Jouer", key=f"btn_p_play_{i}"):
                        play_card(i)
                    st.image(get_card(card_name), width=150)

# Ligne d'info avec ton Cimetière
    col_p_cards, col_p_grave = st.columns([8, 2])

    with col_p_cards:
        st.markdown(f'<div style="background:white; padding:10px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-bottom:10px; display:flex; justify-content:space-between;"><b>👤 STEEVEN</b><span style="color:#e91e63;">❤️ {g.get("p_hp", 20)} HP</span></div>', unsafe_allow_html=True)
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
