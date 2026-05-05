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

# --- FONCTION DE COMPTAGE ---
def stats_cimet(liste):
    ter = sum(1 for c in liste if c in ["Island", "Mountain"])
    sor = sum(1 for c in liste if c in ["Counterspell", "Opt", "Lava Spike"])
    mon = sum(1 for c in liste if c in ["Hedron Crab", "Goblin Guide"])
    art = sum(1 for c in liste if c in ["Sol Ring"])
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
        with st.container(height=500):
            for log in g['history']: st.caption(log)

    with col_main:
        # ZONE IA (SYMÉTRIQUE HAUT)
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            with c1: # Bibliothèque et Cimetière IA
                st.caption(f"📚 IA: ??/60")
                with st.expander(f"💀 Cimetière IA ({len(g['ai_graveyard'])})"):
                    st.write(stats_cimet(g['ai_graveyard']))
            with c2:
                st.write(f"🖥️ **KAEL** - ❤️ {g['ai_hp']} PV")
                st.caption("🎴 " * g['ai_hand_count'])
            
            st.divider()
            st.write(f"⛰️ Terrains: {len(g['ai_land'])} | 👹 Board: {len(g['ai_board'])}")

        # ZONE DE COMBAT
        st.write("")
        with st.container(height=150, border=True):
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
                st.write("Le champ est libre...")

        # ZONE JOUEUR (SYMÉTRIQUE BAS)
        with st.container(border=True):
            st.write(f"⚔️ Board: {len(g['p_board'])} | 🛡️ Terrains: {len(g['p_land'])}")
            st.divider()
            
            c3, c4 = st.columns([2, 1])
            with c3:
                st.write(f"👤 **STEEVEN** - ❤️ {g['p_hp']} PV")
                cols_h = st.columns(len(g['p_hand']))
                for i, card in enumerate(g['p_hand']):
                    if cols_h[i].button(card, key=f"p_{i}"):
                        if card == "Island": g['p_land'].append(g['p_hand'].pop(i))
                        elif card == "Counterspell" and g['stack']:
                            g['p_graveyard'].append(g['p_hand'].pop(i))
                            g['ai_graveyard'].append(g['stack'])
                            g['stack'] = None
                        st.rerun()
            with c4: # Bibliothèque et Cimetière Joueur
                st.caption(f"📚 Ma Bibli: {len(g['p_deck'])}")
                with st.expander(f"💀 Mon Cimetière ({len(g['p_graveyard'])})"):
                    st.write(stats_cimet(g['p_graveyard']))

    with col_chat:
        st.subheader("💬 Chat")
        with st.container(height=250):
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
