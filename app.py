import streamlit as st
import time
import random

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_deck': ["Island", "Counterspell", "Hedron Crab", "Sol Ring", "Opt"] * 12,
        'p_hand': [], 'p_land': [], 'p_board': [], 'p_graveyard': [],
        'ai_deck_count': 60, 'ai_hand_count': 7, 'ai_land': [], 'ai_board': [], 'ai_graveyard': [],
        'history': ["Duel symétrique lancé !"],
        'chat': [{"user": "Kael", "msg": "Voyons si ton organisation t'aide à mieux jouer..."}],
        'stack': None, 'difficulty_lvl': 5, 'is_paused': False, 'phase': 'SETUP'
    }

g = st.session_state.game
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- FONCTION DE COMPTAGE AVEC ICONES FIXES ---
def stats_cimet(liste):
    ter = sum(1 for c in liste if c in ["Island", "Mountain"])
    sor = sum(1 for c in liste if c in ["Counterspell", "Opt", "Lava Spike"])
    mon = sum(1 for c in liste if c in ["Hedron Crab", "Goblin Guide"])
    art = sum(1 for c in liste if c in ["Sol Ring"])
    # Ordre strict : Monstres, Sorts, Terrains, Artefacts
    return f"👹 {mon} | ✨ {sor} | ⛰️ {ter} | 💎 {art}"

# --- PLATEAU ---
if g['phase'] == 'SETUP':
    st.title("🧙‍♂️ Magic Arena")
    if st.button("🎲 PRÉPARER LE DUEL", use_container_width=True):
        random.shuffle(g['p_deck'])
        g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
        g['phase'] = 'PLAY'
        st.rerun()
else:
    col_hist, col_main, col_chat = st.columns([1, 2.5, 1])

    with col_hist:
        st.subheader("📜 Historique")
        with st.container(height=600):
            for log in g['history']: st.caption(log)

    with col_main:
        # --- ZONE IA (HAUT) ---
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 1.5, 1])
            with c1: 
                st.caption(f"📑 IA: ??/60")
                with st.expander(f"💀 Cimetière IA ({len(g['ai_graveyard'])})", expanded=True):
                    st.write(stats_cimet(g['ai_graveyard'])) # Icones 👹 ✨ ⛰️ 💎
            with c2: 
                st.markdown(f"<h3 style='text-align: center; margin:0;'>🖥️ KAEL - ❤️ {g['ai_hp']}</h3>", unsafe_allow_html=True)
            
            st.write("")
            ai_hand_cols = st.columns(max(g['ai_hand_count'], 1))
            for i in range(g['ai_hand_count']):
                ai_hand_cols[i].button("🎴", key=f"ai_h_{i}", disabled=True, use_container_width=True)
            
            st.divider()
            # Ici aussi on harmonise les icônes de la zone de jeu
            st.write(f"⛰️ Terrains: {len(g['ai_land'])} | 👹 Board: {len(g['ai_board'])}")

        # --- ZONE DE COMBAT ---
        st.write("")
        with st.container(height=120, border=True):
            if g['stack']:
                st.warning(f"⚡ PILE : {g['stack']}")
                barre = st.progress(1.0)
                if not g['is_paused']:
                    for p in range(20, 0, -1):
                        time.sleep(temps_reaction / 20)
                        barre.progress(p/20)
                        if not st.session_state.game['stack']: break
                    if g['stack'] and not g['is_paused']:
                        g['p_hp'] -= 3
                        g['ai_graveyard'].append(g['stack'])
                        g['stack'] = None
                        st.rerun()
            else:
                st.markdown("<div style='text-align: center; color: gray; padding-top: 20px;'>Le champ est libre...</div>", unsafe_allow_html=True)

        # --- ZONE JOUEUR (BAS) ---
        with st.container(border=True):
            # Harmonisation des icônes de board pour Steeven
            st.write(f"👹 Board: {len(g['p_board'])} | ⛰️ Terrains: {len(g['p_land'])}")
            st.divider()
            
            p_hand_cols = st.columns(max(len(g['p_hand']), 1))
            for i, card in enumerate(g['p_hand']):
                if p_hand_cols[i].button(card, key=f"p_{i}", use_container_width=True):
                    if card == "Island": g['p_land'].append(g['p_hand'].pop(i))
                    elif card == "Counterspell" and g['stack']:
                        g['p_graveyard'].append(g['p_hand'].pop(i))
                        g['ai_graveyard'].append(g['stack'])
                        g['stack'] = None
                    st.rerun()
            
            st.write("")
            c_low1, c_low2, c_low3 = st.columns([1, 1.5, 1])
            with c_low1: 
                 st.markdown(f"<h3 style='text-align: left; margin:0;'>👤 STEEVEN - ❤️ {g['p_hp']}</h3>", unsafe_allow_html=True)
            with c_low3: 
                st.caption(f"📑 Ma Bibli: {len(g['p_deck'])}")
                with st.expander(f"💀 Mon Cimetière ({len(g['p_graveyard'])})", expanded=True):
                    st.write(stats_cimet(g['p_graveyard'])) # Icones 👹 ✨ ⛰️ 💎 exactement comme l'IA

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
            g['stack'] = "Lava Spike"; g['is_paused'] = False; st.rerun()
        if st.button("🚨 PAUSE", use_container_width=True):
            g['is_paused'] = not g['is_paused']; st.rerun()
