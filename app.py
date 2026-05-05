import streamlit as st
import time
import random

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- BASE DE DONNÉES DES CARTES ---
CARDS_DB = {
    "Hedron Crab": {"type": "Monstre"},
    "Glimpse the Unthinkable": {"type": "Sort"},
    "Archive Trap": {"type": "Sort"},
    "Tasha's Hideous Laughter": {"type": "Sort"},
    "Jace's Phantasm": {"type": "Monstre"},
    "Dark Ritual": {"type": "Sort"},
    "Visions of Beyond": {"type": "Sort"},
    "Polluted Delta": {"type": "Terrain"},
    "Watery Grave": {"type": "Terrain"},
    "Island": {"type": "Terrain"},
    "Swamp": {"type": "Terrain"},
    "Archimage's Charm": {"type": "Sort"},
    "Counterspell": {"type": "Sort"},
    "Guile": {"type": "Monstre"},
    "Opt": {"type": "Sort"},
    "Mana Leak": {"type": "Sort"},
    "Negate": {"type": "Sort"},
    "Essence Scatter": {"type": "Sort"},
    "Various Draw": {"type": "Sort"}
}

# --- FONCTIONS SYSTÈME ---
def piocher(joueur, nb=1):
    for _ in range(nb):
        deck = st.session_state.game['p_deck'] if joueur == "Steeven" else st.session_state.game['ai_deck']
        hand = st.session_state.game['p_hand'] if joueur == "Steeven" else st.session_state.game['ai_hand']
        if deck:
            hand.append(deck.pop())

def meuler(cible, nb_cartes):
    deck_cible = st.session_state.game['ai_deck'] if cible == "Kael" else st.session_state.game['p_deck']
    cimetiere_cible = st.session_state.game['ai_graveyard'] if cible == "Kael" else st.session_state.game['p_graveyard']
    for _ in range(nb_cartes):
        if deck_cible:
            cimetiere_cible.append(deck_cible.pop())
    ajouter_log(f"📉 {cible} perd {nb_cartes} cartes !")

def stats_cimet(liste):
    mon = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Monstre")
    sor = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Sort")
    ter = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Terrain")
    art = sum(1 for c in liste if CARDS_DB.get(c, {}).get('type') == "Artefact")
    return f"👹 {mon} | ✨ {sor} | ⛰️ {ter} | 💎 {art}"

def ajouter_log(msg):
    st.session_state.game['history'].insert(0, msg)

# --- INITIALISATION DU JEU ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_deck': (["Hedron Crab"]*4 + ["Glimpse the Unthinkable"]*4 + ["Archive Trap"]*4 + ["Island"]*20 + ["Swamp"]*10),
        'ai_deck': (["Counterspell"]*4 + ["Island"]*24 + ["Opt"]*10 + ["Various Draw"]*10),
        'p_hand': [], 'p_land': [], 'p_board': [], 'p_graveyard': [],
        'ai_hand': [], 'ai_land': [], 'ai_board': [], 'ai_graveyard': [],
        'history': ["Duel chargé !"],
        'chat': [{"user": "Kael", "msg": "Prêt pour le duel ?"}],
        'phase': 'SETUP'
    }

g = st.session_state.game

# --- INTERFACE GRAPHIQUE ---
if g['phase'] == 'SETUP':
    st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")
    if st.button("🎲 LANCER LE DUEL", use_container_width=True):
        random.shuffle(g['p_deck'])
        random.shuffle(g['ai_deck'])
        piocher("Steeven", 7)
        piocher("Kael", 7)
        g['phase'] = 'PLAY'
        st.rerun()
else:
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
            with c2: st.markdown(f"<h3 style='text-align:center;'>🖥️ KAEL - ❤️ {g['ai_hp']}</h3>", unsafe_allow_html=True)
            
            st.write("")
            ai_cols = st.columns(max(len(g['ai_hand']), 1))
            for i in range(len(g['ai_hand'])):
                ai_cols[i].button("🎴", key=f"ai_h_{i}", disabled=True, use_container_width=True)

        # ZONE COMBAT
        st.write("")
        with st.container(height=100, border=True):
            st.markdown("<center>Zone de combat</center>", unsafe_allow_html=True)

        # ZONE JOUEUR
        with st.container(border=True):
            st.write(f"👹 Board: {len(g['p_board'])} | ⛰️ Terrains: {len(g['p_land'])}")
            st.divider()
            
            p_cols = st.columns(max(len(g['p_hand']), 1))
            for i, card in enumerate(g['p_hand']):
                if p_cols[i].button(card, key=f"p_{i}", use_container_width=True):
                    c_type = CARDS_DB.get(card, {}).get('type')
                    
                    if c_type == "Terrain":
                        g['p_land'].append(g['p_hand'].pop(i))
                        ajouter_log(f"📍 Steeven pose {card}")
                        # Effet Crabe
                        if any(c == "Hedron Crab" for c in g['p_board']):
                            meuler("Kael", 3)
                    elif c_type == "Monstre":
                        g['p_board'].append(g['p_hand'].pop(i))
                        ajouter_log(f"🃏 Steeven invoque {card}")
                    elif card == "Glimpse the Unthinkable":
                        g['p_graveyard'].append(g['p_hand'].pop(i))
                        meuler("Kael", 10)
                    elif card == "Archive Trap":
                        g['p_graveyard'].append(g['p_hand'].pop(i))
                        meuler("Kael", 13)
                    st.rerun()
            
            st.write("")
            c_low1, c_low2, c_low3 = st.columns([1, 1.5, 1])
            with c_low1: st.markdown(f"<h3>👤 STEEVEN - ❤️ {g['p_hp']}</h3>", unsafe_allow_html=True)
            with c_low3:
                st.caption(f"📑 Ma Bibli: {len(g['p_deck'])}")
                with st.expander(f"💀 Mon Cimetière ({len(g['p_graveyard'])})"):
                    st.write(stats_cimet(g['p_graveyard']))

    with col_chat:
        st.subheader("💬 Chat")
        with st.container(height=300):
            for m in g['chat']: st.markdown(f"**{m['user']}:** {m['msg']}")
        if st.button("▶️ TOUR IA", use_container_width=True):
            piocher("Kael")
            st.rerun()
