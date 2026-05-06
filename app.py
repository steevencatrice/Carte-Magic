import streamlit as st
import random

# ==========================================
# 1. CONFIGURATION & STYLE
# ==========================================
st.set_page_config(page_title="Magic: Steeven vs Kael", layout="wide")

st.markdown("""
    <style>
    .sidebar-box { background: #f8f9fa; border: 1px solid #ddd; padding: 10px; border-radius: 5px; }
    .grave-box { background: white; border-radius: 8px; padding: 10px; border: 2px solid #b0bec5; }
    .hp-bar { background: white; padding: 5px 15px; border-radius: 8px; border: 1px solid #dfe4ea; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIQUE & FONCTIONS
# ==========================================

def get_card_url(name):
    """Récupère l'image Scryfall. Gère les noms vides ou '0'."""
    if not name or str(name) == "0":
        return None
    name_url = str(name).replace(" ", "+")
    return f"https://api.scryfall.com/cards/named?fuzzy={name_url}&format=image"

def kael_turn():
    """Logique simplifiée pour le tour de l'IA."""
    g = st.session_state.game
    if g['ai_deck']:
        g['ai_hand'].append(g['ai_deck'].pop(0))
    for i, card in enumerate(g['ai_hand']):
        if card == "Mountain":
            land = g['ai_hand'].pop(i)
            g['ai_land'].append({"name": land, "tapped": False})
            g['history'].insert(0, "🔥 Kael joue une Montagne")
            break

def play_card(card_index):
    """Déplace une carte de la main vers le champ de bataille."""
    g = st.session_state.game
    # Filtrage de la main pour correspondre à l'affichage
    valid_hand_indices = [i for i, c in enumerate(g['p_hand']) if str(c) != "0"]
    
    if card_index < len(valid_hand_indices):
        real_idx = valid_hand_indices[card_index]
        card_name = g['p_hand'].pop(real_idx)
        
        liste_terrains = ["Island", "Swamp", "Mountain", "Watery Grave", "Polluted Delta"]
        
        if card_name in liste_terrains:
            g['p_land'].append({"name": card_name, "tapped": False})
            g['history'].insert(0, f"🌍 Steeven joue {card_name}")
            # Effet Crabe
            if any(c['name'] == "Hedron Crab" for c in g['p_board']):
                if g['ai_deck']:
                    for _ in range(min(3, len(g['ai_deck']))):
                        g['ai_grave']['Sorts'] += 1
                        g['ai_deck'].pop(0)
                    g['history'].insert(0, "🦀 Le Crabe meule 3 cartes !")
        else:
            g['p_board'].append({"name": card_name, "tapped": False})
            g['history'].insert(0, f"⚔️ Steeven joue {card_name}")

# ==========================================
# 3. INITIALISATION DU JEU
# ==========================================
DECKS = {
    "Meule": ["Hedron Crab"]*4 + ["Glimpse the Unthinkable"]*4 + ["Archive Trap"]*4 + ["Tasha's Hideous Laughter"]*4 + ["Jace's Phantasm"]*4 + ["Dark Ritual"]*4 + ["Visions of Beyond"]*3 + ["Polluted Delta"]*4 + ["Watery Grave"]*4 + ["Island"]*15 + ["Swamp"]*10,
    "Burn": ["Ball Lightning"]*4 + ["Lightning Bolt"]*4 + ["Lava Spike"]*4 + ["Skewer the Critics"]*4 + ["Rift Bolt"]*4 + ["Fireblast"]*4 + ["Shock"]*4 + ["Incinerate"]*4 + ["Chain Lightning"]*4 + ["Mountain"]*24
}

if 'game' not in st.session_state:
    p_deck = DECKS["Meule"][:]
    ai_deck = DECKS["Burn"][:]
    random.shuffle(p_deck)
    random.shuffle(ai_deck)
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20, 'p_mana': 0,
        'p_deck': p_deck[7:], 'p_hand': p_deck[:7],
        'p_land': [], 'p_board': [],
        'p_grave': {'Créas': 0, 'Sorts': 0, 'Lands': 0, 'Artifacts': 0, 'Enchants': 0},
        'ai_deck': ai_deck[7:], 'ai_hand': ai_deck[:7],
        'ai_land': [], 'ai_board': [],
        'ai_grave': {'Créas': 0, 'Sorts': 0, 'Lands': 0, 'Artifacts': 0, 'Enchants': 0},
        'history': ["Début de la partie"],
        'chat': [{"u": "Kael", "m": "Bonne chance Steeven !"}],
        'phase': "PRINCIPALE 1"
    }

g = st.session_state.game

# ==========================================
# 4. INTERFACE UTILISATEUR (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("🎮 MENU MAGIC")
    if st.button("♻️ RESET PARTIE", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.caption("💬 CHAT")
    chat_content = "".join([f"<b>{m['u']}</b>: {m['m']}<br>" for m in g['chat'][-10:]])
    st.markdown(f'<div class="sidebar-box" style="height:200px; overflow-y:auto;">{chat_content}</div>', unsafe_allow_html=True)
    
    m_in = st.text_input("Message...", key="side_chat")
    if st.button("Envoyer", use_container_width=True):
        if m_in: 
            g['chat'].append({"u": "Steeven", "m": m_in})
            st.rerun()

    st.caption("📜 ACTIONS")
    h_txt = "".join([f"• {a}<br>" for a in g['history'][-10:]])
    st.markdown(f'<div class="sidebar-box" style="height:150px; overflow-y:auto;">{h_txt}</div>', unsafe_allow_html=True)

# ==========================================
# 5. PLATEAU DE JEU PRINCIPAL
# ==========================================
_, center_col, _ = st.columns([0.5, 9, 0.5])

with center_col:
    # --- SECTION KAEL ---
    col_k_cards, col_k_grave = st.columns([8, 2])
    with col_k_cards:
        k_cols = st.columns(7)
        for i in range(min(len(g['ai_hand']), 7)):
            k_cols[i].image("https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/thumb/f/f8/Magic_card_back.jpg/250px-Magic_card_back.jpg", use_container_width=True)
        st.markdown(f'<div class="hp-bar"><b>🖥️ KAEL</b> | <span style="color:#ff4757;">❤️ {g["ai_hp"]} HP</span></div>', unsafe_allow_html=True)

    with col_k_grave:
        st.markdown(f"""<div class="grave-box"><p style="font-size:0.8em; color:#ef5350;"><b>🪦 CIMETIÈRE KAEL</b></p><hr>
            <p style="font-size:0.7em; margin:0;">🌍 Terrains: {g['ai_grave']['Lands']}<br>👾 Créas: {g['ai_grave']['Créas']}<br>📜 Sorts: {g['ai_grave']['Sorts']}</p></div>""", unsafe_allow_html=True)

    # --- ZONE DE COMBAT ---
    st.markdown('<div style="background:#eceff1; border-radius:12px; padding:20px; border:2px solid #b0bec5; min-height:200px;">', unsafe_allow_html=True)
    st.caption("⚔️ CHAMP DE BATAILLE")
    if g['p_board']:
        cols_b = st.columns(8)
        for idx, crea in enumerate(g['p_board']):
            with cols_b[idx % 8]:
                st.image(get_card_url(crea["name"]), width=100)
    else:
        st.write("*(Vide)*")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MES TERRAINS ---
    st.markdown("#### 🌍 MES TERRAINS")
    if g['p_land']:
        cols_l = st.columns(10)
        for idx, land in enumerate(g['p_land']):
            with cols_l[idx % 10]:
                angle = 90 if land['tapped'] else 0
                st.markdown(f'<img src="{get_card_url(land["name"])}" style="transform:rotate({angle}deg); width:80px; border-radius:5px;">', unsafe_allow_html=True)
                if st.button("TAP", key=f"t_land_{idx}"):
                    land['tapped'] = not land['tapped']
                    g['p_mana'] += 1 if land['tapped'] else -1
                    st.rerun()

    # --- SECTION JOUEUR ---
    st.write("---")
    col_atk, col_bloc, col_comb, col_m2, col_fin = st.columns(5)
    col_atk.button("?? PIOCHE", use_container_width=True)
    col_fin.button("🏁 FIN TOUR", use_container_width=True, on_click=kael_turn)

    col_p_cards, col_p_grave = st.columns([8, 2])
    with col_p_cards:
        st.markdown(f'<div class="hp-bar"><b>👤 STEEVEN</b> | <span style="color:#e91e63;">❤️ {g["p_hp"]} HP</span> | 💧 Mana: {g["p_mana"]}</div>', unsafe_allow_html=True)
        p_hand = [c for c in g['p_hand'] if str(c) != "0"]
        if p_hand:
            cols_hand = st.columns(len(p_hand))
            for i, card_name in enumerate(p_hand):
                with cols_hand[i]:
                    st.button("Jouer", key=f"play_{i}_{card_name}", on_click=play_card, args=(i,))
                    url = get_card_url(card_name)
                    if url: st.image(url, use_container_width=True)
        else:
            st.info("Main vide")

    with col_p_grave:
        st.markdown(f"""<div class="grave-box"><p style="font-size:0.8em; color:#42a5f5;"><b>🪦 MON CIMETIÈRE</b></p><hr>
            <p style="font-size:0.7em; margin:0;">🌍 Terrains: {g['p_grave']['Lands']}<br>👾 Créas: {g['p_grave']['Créas']}<br>📜 Sorts: {g['p_grave']['Sorts']}</p></div>""", unsafe_allow_html=True)
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
    col_k_cards, col_k_grave = st.columns([8, 2])
    with col_k_cards:
        # Main de Kael
        k_cols = st.columns(7)
        for i in range(7):
            k_cols[i].image("https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/thumb/f/f8/Magic_card_back.jpg/250px-Magic_card_back.jpg", use_container_width=True)
       
        # Barre HP Kael
        st.markdown(f'<div style="background:white; padding:5px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-top:10px;"><b>🖥️ KAEL</b> | <span style="color:#ff4757;">❤️ {g["ai_hp"]} HP</span></div>', unsafe_allow_html=True)


    with col_k_grave:
        # Cimetière Kael
         st.markdown(f"""
            <div style="border:2px solid #ef5350; border-radius:10px; padding:10px; background:white;">
                <p style="margin:0; font-size:0.8em; color:#1e88e5;"><b>🪦 CIMETIÈRE</b></p>
                <hr style="margin:5px 0;">
                <p style="margin:0; font-size:0.8em;">🌍 Terrains: <b>{g.get('Lands', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">👾 Créature: <b>{g.get('Créas', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">📜 Sorts: <b>{g.get('Sorts', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">💎 Artéfact: <b>{g.get('Artifacts', 0)}</b></p>
                <p style="margin:0; font-size:0.8em;">✨ Enchantement: <b>{g.get('Enchants', 0)}</b></p>
            </div>
        """, unsafe_allow_html=True)


    # --- ESPACE ICI ---
    st.write("") # Crée un saut de ligne standard
    # ------------------


    # --- 2. BOUTONS KAEL (Grisés / Dynamiques) ---
    ai_status = g.get('ai_status', 'thinking')
    kb = st.columns([1, 1, 1, 1, 1])
    kb[0].button("?? PIOCHE", key="btn_ai_at", type="primary" if ai_status == 'attacking' else "secondary", disabled=True, use_container_width=True)
    kb[1].button("🛡️ MAIN 1", key="btn_ai_bl", type="primary" if ai_status == 'blocking' else "secondary", disabled=True, use_container_width=True)
    kb[2].button("⚔️ COMBAT", key="btn_ai_gr", disabled=True, use_container_width=True)
    kb[3].button("🛡️ MAIN 2", key="btn_ai_bi", disabled=True, use_container_width=True)
    kb[4].button("🏁 FIN", key="btn_ai_end", type="primary" if ai_status == 'ending' else "secondary", disabled=True, use_container_width=True)


# ==========================================
    # ZONE JOUEUR (STEEVEN)
    # ==========================================


    # --- 1. LE CHAMP DE BATAILLE (CREATURES - TAILLE RÉDUITE) ---
    st.markdown("---")
    st.markdown("### ⚔️ CHAMP DE BATAILLE")
   
    if st.session_state.game['p_board']:
        # On passe à 10 colonnes pour aligner plus de créatures
        cols_b = st.columns(10)
        for idx, crea in enumerate(st.session_state.game['p_board']):
            with cols_b[idx % 10]:
                # Taille fixée à 80px comme les terrains
                st.image(get_card(crea["name"]), width=80)
                st.caption(f"{crea['name'][:8]}...") # Nom abrégé pour pas déborder
    else:
        st.write("*(Champ de bataille vide)*")


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

# Barre d'actions (Phases)
col_atk, col_bloc, col_grave_btn, col_biblio, col_fin = st.columns(5)
with col_atk: st.button("?? PIOCHE", use_container_width=True)
with col_bloc: st.button("🛡️ MAIN 1", use_container_width=True)
with col_grave_btn: st.button("⚔️ COMBAT", use_container_width=True)
with col_biblio: st.button("🛡️ MAIN 2", use_container_width=True)
with col_fin: st.button("🏁 FIN", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ZONE CARTES + CIMETIÈRE ---
col_p_cards, col_p_grave = st.columns([8, 2])

with col_p_cards:
    st.markdown(f"""
        <div style="background:white; padding:10px 15px; border-radius:8px; border:1px solid #dfe4ea; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
            <b>👤 STEEVEN</b>
            <span style="color:#e91e63;">❤️ {st.session_state.game.get('p_hp', 20)} HP</span>
        </div>
    """, unsafe_allow_html=True)
    
    # On filtre pour ne garder que les vrais noms de cartes (exclut les "0")
    p_hand = [c for c in st.session_state.game.get('p_hand', []) if str(c) != "0"]
    
    if p_hand:
        # Création dynamique des colonnes selon le nombre de cartes réelles
        cols_hand = st.columns(len(p_hand))
        for i, card_name in enumerate(p_hand):
            with cols_hand[i]:
                # On passe l'index original ou le nom pour la fonction play_card
                st.button("Jouer", key=f"play_{i}_{card_name}", on_click=play_card, args=(i,))
                
                img_url = get_card_url(card_name)
                if img_url:
                    st.image(img_url, use_container_width=True)
                else:
                    st.warning("Nom invalide")
    else:
        st.info("Votre main est vide ou contient des données erronées.")
with col_p_grave:
    pg = st.session_state.game.get('p_grave', {})
    st.markdown(f"""
        <div style="border:2px solid #42a5f5; border-radius:10px; padding:10px; background:white;">
            <p style="margin:0; font-size:0.8em; color:#1e88e5;"><b>🪦 CIMETIÈRE</b></p>
            <hr style="margin:5px 0; border-top:1px solid #42a5f5;">
            <p style="margin:0; font-size:0.8em;">🌍 Terrains: <b>{pg.get('Lands', 0)}</b></p>
            <p style="margin:0; font-size:0.8em;">👾 Créas: <b>{pg.get('Créas', 0)}</b></p>
            <p style="margin:0; font-size:0.8em;">📜 Sorts: <b>{pg.get('Sorts', 0)}</b></p>
            <p style="margin:0; font-size:0.8em;">💎 Arts: <b>{pg.get('Artifacts', 0)}</b></p>
            <p style="margin:0; font-size:0.8em;">✨ Ench: <b>{pg.get('Enchants', 0)}</b></p>
        </div>
    """, unsafe_allow_html=True)
