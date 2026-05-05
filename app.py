import streamlit as st
import time
import random

st.set_page_config(page_title="Magic Arena Pro - Steeven vs Kael", layout="wide")

# --- INITIALISATION ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_deck': ["Island", "Counterspell", "Hedron Crab", "Opt", "Unsummon"] * 8,
        'p_hand': [],
        'p_land': [], # Terrains posés
        'p_board': [], # Monstres/Artefacts posés
        'ai_hand_count': 7,
        'ai_land': [],
        'ai_board': [],
        'history': ["Bienvenue dans l'Arène !"],
        'chat': ["Kael: Alors, tu as peur ?"],
        'stack': None,
        'difficulty_lvl': 5,
        'is_paused': False,
        'phase': 'SETUP'
    }

g = st.session_state.game
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- LOGIQUE ---
def ajouter_log(message):
    g['history'].insert(0, message)

def initialiser():
    random.shuffle(g['p_deck'])
    g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
    g['phase'] = 'PLAY'
    ajouter_log("Partie lancée !")

# --- INTERFACE (SIDEBAR GAUCHE) ---
with st.sidebar:
    st.title("⚙️ Configuration")
    g['difficulty_lvl'] = st.slider("Difficulté de l'IA", 1, 10, g['difficulty_lvl'])
    st.write(f"⏱️ Réaction: {temps_reaction:.1f}s")
    st.divider()
    st.write(f"🎴 Deck: {len(g['p_deck'])} / 60")
    if st.button("🔄 Reset Total"):
        del st.session_state['game']
        st.rerun()

# --- PLATEAU DE JEU (SELON TON DESSIN) ---
if g['phase'] == 'SETUP':
    st.header("🎮 Magic Arena")
    if st.button("🎲 MÉLANGER ET DISTRIBUER", use_container_width=True):
        initialiser()
        st.rerun()
else:
    # On crée 3 colonnes : Historique | Plateau | Stats/Chat
    col_hist, col_board, col_sys = st.columns([1, 3, 1])

    # 1. COLONNE GAUCHE : HISTORIQUE
    with col_hist:
        st.subheader("📜 Historique")
        for log in g['history'][:10]: # Affiche les 10 derniers
            st.caption(log)

    # 2. COLONNE CENTRALE : LE PLATEAU (IA en haut, Joueur en bas)
    with col_board:
        # ZONE IA
        with st.container(border=True):
            st.caption(f"🖥️ KAEL - {g['ai_hp']} PV")
            # Main IA (cachée)
            st.write("🎴 " * g['ai_hand_count'])
            # Terrains & Monstres IA
            c1, c2 = st.columns(2)
            c1.write(f"⛰️ Terrains: {len(g['ai_land'])}")
            c2.write(f"👹 Monstres: {len(g['ai_board'])}")

        st.write("") # Espace
        
        # ZONE DE COMBAT (LE STACK / TIMER)
        with st.container():
            if g['stack']:
                st.warning(f"⚡ SORT EN COURS : {g['stack']}")
                if not g['is_paused']:
                    barre = st.progress(1.0)
                    step = temps_reaction / 20
                    for p in range(20, 0, -1):
                        time.sleep(step)
                        barre.progress(p/20)
                        if not st.session_state.game['stack']: break
                    if g['stack'] and not g['is_paused']:
                        g['p_hp'] -= 3
                        ajouter_log(f"IA lance {g['stack']} -> -3 PV")
                        g['stack'] = None
                        st.rerun()
            else:
                st.write("--- Zone de Combat Paisible ---")

        st.write("") # Espace

        # ZONE JOUEUR (STEEVEN)
        with st.container(border=True):
            # Terrains & Monstres Joueur
            c3, c4 = st.columns(2)
            c3.write(f"💧 Terrains Posés: {len(g['p_land'])}")
            c4.write(f"⚔️ Monstres: {len(g['p_board'])}")
            
            st.divider()
            st.caption(f"👤 STEEVEN - {g['p_hp']} PV")
            # Main du joueur
            cols_h = st.columns(len(g['p_hand']))
            for i, card in enumerate(g['p_hand']):
                if cols_h[i].button(card, key=f"h_{i}"):
                    if card == "Island":
                        g['p_land'].append(g['p_hand'].pop(i))
                        ajouter_log("Steeven pose une Île")
                    elif card == "Counterspell" and g['stack']:
                        g['stack'] = None
                        g['p_hand'].pop(i)
                        ajouter_log("Steeven contre le sort !")
                    st.rerun()

    # 3. COLONNE DROITE : CHAT ET SYSTEME
    with col_sys:
        st.subheader("💬 Chat IA")
        with st.container(height=200):
            for msg in g['chat']:
                st.write(msg)
        
        st.divider()
        if st.button("▶️ TOUR IA", use_container_width=True):
            g['stack'] = "Lava Spike"
            g['is_paused'] = False
            st.rerun()
        
        if g['is_paused']:
            if st.button("▶️ REPRENDRE", use_container_width=True, type="primary"):
                g['is_paused'] = False
                st.rerun()
        else:
            if st.button("🚨 PAUSE", use_container_width=True):
                g['is_paused'] = True
                st.rerun()
