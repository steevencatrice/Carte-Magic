import streamlit as st
import random

# 1. CONFIGURATION COULEUR CLASSIQUE
st.set_page_config(page_title="Magic Arena", layout="wide")

# Initialisation du jeu
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_mana': 0, 'ai_mana': 0,
        'p_hand': ["Island", "Counterspell", "Archive Trap"],
        'p_lands': [], 'p_board': [],
        'ai_deck': ["Island"] * 20,
        'ai_grave': 0, 'logs': "Début du duel !"
    }

st.title("🧙‍♂️ Magic : Arena Steeven")

# --- INTERFACE CLASSIQUE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🖥️ Adversaire : {st.session_state.game['ai_hp']} PV")
    st.write(f"🎴 Deck adverse : {len(st.session_state.game['ai_deck'])} cartes")
    
    st.divider()
    
    st.subheader(f"👤 Steeven : {st.session_state.game['p_hp']} PV | Mana : {st.session_state.game['p_mana']}")
    
    # Zone de jeu
    cols = st.columns(len(st.session_state.game['p_hand']) + 1)
    for i, card in enumerate(st.session_state.game['p_hand']):
        if cols[i].button(f"Jouer\n{card}", key=f"p_{i}"):
            # Logique simplifiée pour le test
            st.session_state.game['p_hand'].pop(i)
            st.session_state.game['logs'] = f"Tu as joué {card}"
            st.rerun()

with col2:
    st.info(st.session_state.game['logs'])
    if st.button("🔴 FINIR LE TOUR", use_container_width=True):
        # ICI ON CODERA LE CERVEAU CET APREM
        st.session_state.game['logs'] = "L'IA réfléchit..."
        st.rerun()
