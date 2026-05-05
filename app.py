import streamlit as st
import random

st.set_page_config(page_title="Magic Arena", layout="wide")

# Base de données simple des cartes
DB = {
    "Island": {"type": "Land", "mana": 0, "power": 0},
    "Mountain": {"type": "Land", "mana": 0, "power": 0},
    "Lava Spike": {"type": "Spell", "mana": 1, "dmg": 3},
    "Hedron Crab": {"type": "Creature", "mana": 1, "power": 0}
}

if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_mana': 0, 'ai_mana': 0,
        'p_hand': ["Island", "Counterspell", "Archive Trap"],
        'ai_hand': ["Mountain", "Lava Spike"],
        'ai_lands': 0,
        'logs': "Le duel commence !"
    }

def tour_ia():
    g = st.session_state.game
    log_ia = " | Tour de l'IA : "
    
    # 1. L'IA pioche (cerveau)
    nouvelle_carte = "Lava Spike"
    g['ai_hand'].append(nouvelle_carte)
    
    # 2. L'IA joue un terrain si elle en a un
    for i, card in enumerate(g['ai_hand']):
        if DB.get(card, {}).get("type") == "Land":
            g['ai_lands'] += 1
            g['ai_hand'].pop(i)
            log_ia += "Pose une Montagne. "
            break
            
    # 3. L'IA attaque si elle a assez de mana
    mana_dispo = g['ai_lands']
    for i, card in enumerate(g['ai_hand']):
        cout = DB.get(card, {}).get("mana", 99)
        if cout <= mana_dispo:
            g['p_hp'] -= DB[card]['dmg']
            g['ai_hand'].pop(i)
            log_ia += f"Lance {card} (-3 PV) !"
            break
            
    g['logs'] = log_ia

st.title("🧙‍♂️ Magic : Arena Steeven")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🖥️ Adversaire : {st.session_state.game['ai_hp']} PV")
    st.write(f"🎴 Cartes en main IA : {len(st.session_state.game['ai_hand'])}")
    st.write(f"🔥 Terrains IA : {st.session_state.game['ai_lands']}")
    st.divider()
    st.subheader(f"👤 Steeven : {st.session_state.game['p_hp']} PV")
    
    # Tes cartes
    cols = st.columns(len(st.session_state.game['p_hand']) + 1)
    for i, card in enumerate(st.session_state.game['p_hand']):
        if cols[i].button(f"Jouer {card}", key=f"p_{i}"):
            st.session_state.game['logs'] = f"Tu as joué {card}"
            st.rerun()

with col2:
    st.info(st.session_state.game['logs'])
    if st.button("🔴 TERMINER MON TOUR", use_container_width=True):
        tour_ia()
        st.rerun()
