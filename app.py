import streamlit as st
import time
import random

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_mana': 2, 'ai_mana': 1,
        'p_hand': ["Counterspell", "Island", "Hedron Crab"],
        'ai_hand': ["Mountain", "Lava Spike", "Shock"],
        'stack': None, # Sort en attente de résolution
        'logs': "Prépare-toi, Steeven !",
        'difficulty': 45
    }

# --- FONCTIONS DE JEU ---
def resoudre_pile():
    g = st.session_state.game
    if g['stack']:
        g['p_hp'] -= 3  # Dégâts par défaut pour le test
        g['logs'] = f"💥 Trop tard ! {g['stack']} te touche (-3 PV)."
        g['stack'] = None

def tour_ia():
    g = st.session_state.game
    # L'IA prépare un sort
    g['stack'] = "Lava Spike"
    g['logs'] = "⚠️ Kael lance Lava Spike ! INTERROMPS-LE !"

# --- INTERFACE ---
st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")

# Barre latérale pour la difficulté (Négociation signée !)
with st.sidebar:
    st.header("⚙️ Réglages")
    niveau = st.slider("Niveau de l'IA (1=Relax, 10=Expert)", 1, 10, 1)
    # Calcul du temps : Niveau 1 = 45s, Niveau 10 = 5s
    st.session_state.game['difficulty'] = 45 - (niveau - 1) * 4.4 
    st.write(f"Temps de réaction : {st.session_state.game['difficulty']:.1f}s")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🖥️ Kael : {st.session_state.game['ai_hp']} PV")
    st.divider()
    st.subheader(f"👤 Steeven : {st.session_state.game['p_hp']} PV")
    
    # Affichage des cartes du joueur
    cols = st.columns(len(st.session_state.game['p_hand']))
    for i, card in enumerate(st.session_state.game['p_hand']):
        if cols[i].button(f"🃏 {card}", key=f"c_{i}"):
            if g['stack'] and card == "Counterspell":
                st.session_state.game['stack'] = None
                st.session_state.game['logs'] = "🛡️ BIEN JOUÉ ! Sort contré !"
                st.rerun()

with col2:
    st.info(st.session_state.game['logs'])
    
    # --- LA LOGIQUE DU TIMER ---
    if st.session_state.game['stack']:
        barre = st.progress(1.0)
        temps_max = st.session_state.game['difficulty']
        
        # Le bouton d'interruption (pour figer le jeu)
        if st.button("🚨 INTERROMPRE !", use_container_width=True):
            st.session_state.game['logs'] = "⏱️ Jeu figé... Joue ton contre-sort !"
            st.rerun()
            
        # Simulation du temps qui passe (visuel)
        for p in range(100, 0, -1):
            time.sleep(temps_max / 100)
            barre.progress(p/100)
        
        # Si on arrive au bout du temps sans clic
        resoudre_pile()
        st.rerun()

    if st.button("▶️ TOUR DE L'IA", use_container_width=True):
        tour_ia()
        st.rerun()
