import streamlit as st
import time
import random

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- BASE DE DONNÉES DES CARTES (Cerveau) ---
# On définit ici les types et propriétés pour que l'IA puisse "réfléchir"
CARDS_DB = {
    # Deck Steeven (Mill)
    "Hedron Crab": {"type": "Monstre", "mana": "💧", "attr": "Mill 3"},
    "Glimpse the Unthinkable": {"type": "Sort", "mana": "💧💀", "attr": "Mill 10"},
    "Archive Trap": {"type": "Sort", "mana": "5💧", "attr": "Mill 13"},
    "Tasha's Hideous Laughter": {"type": "Sort", "mana": "1💧💀", "attr": "Mill X"},
    "Jace's Phantasm": {"type": "Monstre", "mana": "💧", "attr": "5/5 if 10+ cards"},
    "Dark Ritual": {"type": "Sort", "mana": "💀", "attr": "Add 3 Mana"},
    "Visions of Beyond": {"type": "Sort", "mana": "💧", "attr": "Draw 1 or 3"},
    "Polluted Delta": {"type": "Terrain", "mana": "0", "attr": "Fetch"},
    "Watery Grave": {"type": "Terrain", "mana": "0", "attr": "Dual Land"},
    "Island": {"type": "Terrain", "mana": "0", "attr": "Mana 💧"},
    "Swamp": {"type": "Terrain", "mana": "0", "attr": "Mana 💀"},
    
    # Deck Kael (Control)
    "Archimage's Charm": {"type": "Sort", "mana": "💧💧💧", "attr": "Counter/Draw/Steal"},
    "Counterspell": {"type": "Sort", "mana": "💧💧", "attr": "Counter"},
    "Guile": {"type": "Monstre", "mana": "3💧💧💧", "attr": "6/6 & Steal Counters"},
    "Opt": {"type": "Sort", "mana": "💧", "attr": "Scry 1 Draw 1"},
    "Mana Leak": {"type": "Sort", "mana": "1💧", "attr": "Counter unless 3"},
    "Negate": {"type": "Sort", "mana": "1💧", "attr": "Counter non-creature"},
    "Essence Scatter": {"type": "Sort", "mana": "1💧", "attr": "Counter creature"},
    "Various Draw": {"type": "Sort", "mana": "2💧", "attr": "Draw 2"}
}

# --- INITIALISATION ---
if 'game' not in st.session_state:
    # Construction du deck Steeven (60 cartes)
    steeven_deck = (["Hedron Crab"]*4 + ["Glimpse the Unthinkable"]*4 + ["Archive Trap"]*4 + 
                    ["Tasha's Hideous Laughter"]*4 + ["Jace's Phantasm"]*4 + ["Dark Ritual"]*4 + 
                    ["Visions of Beyond"]*3 + ["Polluted Delta"]*4 + ["Watery Grave"]*4 + 
                    ["Island"]*11 + ["Swamp"]*11 + ["Opt"]*3)
    
    # Construction du deck Kael (60 cartes)
    kael_deck = (["Archimage's Charm"]*4 + ["Counterspell"]*4 + ["Guile"]*2 + ["Opt"]*4 + 
                 ["Mana Leak"]*4 + ["Negate"]*4 + ["Essence Scatter"]*4 + ["Visions of Beyond"]*4 + 
                 ["Island"]*24 + ["Various Draw"]*6)

    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_deck': steeven_deck,
        'ai_deck': kael_deck,
        'p_hand': [], 'p_land': [], 'p_board': [], 'p_graveyard': [],
        'ai_hand': [], 'ai_land': [], 'ai_board': [], 'ai_graveyard': [],
        'history': ["Decks chargés : Meule vs Contrôle !"],
        'chat': [{"user": "Kael", "msg": "Bonne chance pour me meuler, j'ai prévu de tout contrer."}],
        'stack': None, 'difficulty_lvl': 5, 'is_paused': False, 'phase': 'SETUP'
    }

g = st.session_state.game

# --- LOGIQUE ---
def piocher(joueur, nb=1):
    for _ in range(nb):
        deck = g['p_deck'] if joueur == "Steeven" else g['ai_deck']
        hand = g['p_hand'] if joueur == "Steeven" else g['ai_hand']
        if deck:
            hand.append(deck.pop())
        else:
            ajouter_log(f"GAME OVER : {joueur} n'a plus de bibliothèque !")

def stats_cimet(liste):
    mon = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Monstre")
    sor = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Sort")
    ter = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Terrain")
    art = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Artefact")
    return f"👹 {mon} | ✨ {sor} | ⛰️ {ter} | 💎 {art}"

def ajouter_log(msg): g['history'].insert(0, msg)

# --- INTERFACE ---
if g['phase'] == 'SETUP':
    st.title("🧙‍♂️ Magic Arena : Mill vs Control")
    if st.button("🎲 MÉLANGER ET DISTRIBUER", use_container_width=True):
        random.shuffle(g['p_deck'])
        random.shuffle(g['ai_deck'])
        piocher("Steeven", 7)
        piocher("Kael", 7)
        g['phase'] = 'PLAY'
        st.rerun()
else:
    # (Ici on garde ton interface symétrique V14)
    col_hist, col_main, col_chat = st.columns([1, 2.5, 1])

    with col_hist:
        st.subheader("📜 Historique")
        with st.container(height=600):
            for log in g['history']: st.caption(log)

    with col_main:
        # ZONE IA
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 1.5, 1])
            with c1: 
                st.caption(f"📑 IA: {len(g['ai_deck'])}/60")
                with st.expander(f"💀 Cimetière IA ({len(g['ai_graveyard'])})"):
                    st.write(stats_cimet(g['ai_graveyard']))
            with c2: 
                st.markdown(f"<h3 style='text-align: center; margin:0;'>🖥️ KAEL - ❤️ {g['ai_hp']}</h3>", unsafe_allow_html=True)
            
            st.write("")
            ai_hand_cols = st.columns(max(len(g['ai_hand']), 1))
            for i in range(len(g['ai_hand'])):
                ai_hand_cols[i].button("🎴", key=f"ai_h_{i}", disabled=True, use_container_width=True)
            
            st.divider()
            st.write(f"⛰️ Terrains: {len(g['ai_land'])} | 👹 Board: {len(g['ai_board'])}")

        # ZONE DE COMBAT
        st.write("")
        with st.container(height=120, border=True):
            if g['stack']:
                st.warning(f"⚡ PILE : {g['stack']}")
            else:
                st.markdown("<div style='text-align: center; color: gray; padding-top: 20px;'>Le champ est libre...</div>", unsafe_allow_html=True)

        # ZONE JOUEUR
        with st.container(border=True):
            st.write(f"👹 Board: {len(g['p_board'])} | ⛰️ Terrains: {len(g['p_land'])}")
            st.divider()
            
            p_hand_cols = st.columns(max(len(g['p_hand']), 1))
            for i, card in enumerate(g['p_hand']):
                # --- LOGIQUE DE JEU STEEVEN (Remplacement lignes 132-141) ---
            if p_hand_cols[i].button(card, key=f"p_{i}", use_container_width=True):
                c_data = CARDS_DB.get(card, {})
                
                # 1. Gestion des Terrains & Landfall (Crabe)
                if c_data['type'] == "Terrain":
                    g['p_land'].append(g['p_hand'].pop(i))
                    ajouter_log(f"📍 Steeven pose {card}")
                    # Effet Crabe d'Hédron
                    crabes = sum(1 for c in g['p_board'] if c == "Hedron Crab")
                    if crabes > 0:
                        meuler("Kael", 3 * crabes)

                # 2. Invocation des Monstres
                elif c_data['type'] == "Monstre":
                    g['p_board'].append(g['p_hand'].pop(i))
                    ajouter_log(f"🃏 Steeven invoque {card}")

                # 3. Sorts de Meule directs
                elif card == "Glimpse the Unthinkable":
                    g['p_graveyard'].append(g['p_hand'].pop(i))
                    meuler("Kael", 10)
                    
                elif card == "Archive Trap":
                    g['p_graveyard'].append(g['p_hand'].pop(i))
                    meuler("Kael", 13)

                # 4. Sorts de Pioche
                elif card == "Visions of Beyond":
                    g['p_graveyard'].append(g['p_hand'].pop(i))
                    nb_p = 3 if len(g['ai_graveyard']) >= 20 else 1
                    piocher("Steeven", nb_p)
                    ajouter_log(f"🔮 Visions : Steeven pioche {nb_p}")

                # Par défaut pour les autres cartes
                else:
                    g['p_graveyard'].append(g['p_hand'].pop(i))
                    ajouter_log(f"✨ Steeven joue {card}")
                
                st.rerun()
            
            st.write("")
            c_low1, c_low2, c_low3 = st.columns([1, 1.5, 1])
            with c_low1: 
                 st.markdown(f"<h3 style='text-align: left; margin:0;'>👤 STEEVEN - ❤️ {g['p_hp']}</h3>", unsafe_allow_html=True)
            with c_low3: 
                st.caption(f"📑 Ma Bibli: {len(g['p_deck'])}")
                with st.expander(f"💀 Mon Cimetière ({len(g['p_graveyard'])})"):
                    st.write(stats_cimet(g['p_graveyard']))

    with col_chat:
        st.subheader("💬 Chat")
        with st.container(height=300):
            for m in g['chat']: st.markdown(f"**{m['user']}:** {m['msg']}")
        
        with st.form("chat", clear_on_submit=True):
            msg = st.text_input("Répondre...")
            if st.form_submit_button("Envoyer"):
                if msg: g['chat'].append({"user": "Moi", "msg": msg}); st.rerun()

        st.divider()
        if st.button("▶️ TOUR IA", use_container_width=True, type="primary"):
            piocher("Kael")
            ajouter_log("Kael pioche et analyse...")
            st.rerun()
