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
        'stack': None, 
        'logs': "Prépare-toi, Steeven !",
        'difficulty': 45
    }

g = st.session_state.game  # On définit 'g' globalement pour tout le script

# --- FONCTIONS DE JEU ---
def resoudre_pile():
    if g['stack']:
        g['p_hp'] -= 3
        g['logs'] = f"💥 Trop tard ! {g['stack']} te touche (-3 PV)."
        g['stack'] = None

def tour_ia():
    g['stack'] = "Lava Spike"
    if g['difficulty'] < 10:
        g['logs'] = "⚡ KAEL : 'Tu n'auras jamais le temps !'"
    else:
        g['logs'] = "⚠️ Kael lance Lava Spike ! RÉAGIS !"

# --- INTERFACE ---
st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")

# Barre latérale pour la difficulté
with st.sidebar:
    st.header("⚙️ Réglages")
    niveau = st.slider("Niveau de l'IA (1=Relax, 10=Expert)", 1, 10, 1)
    # Mise à jour du temps selon le niveau
    g['difficulty'] = 45 - (niveau - 1) * 4.4 
    st.write(f"Temps de réaction : {g['difficulty']:.1f}s")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🖥️ Kael : {g['ai_hp']} PV")
    st.divider()
    st.subheader(f"👤 Steeven : {g['p_hp']} PV")
    
    # Affichage des cartes du joueur
    if len(g['p_hand']) > 0:
        cols = st.columns(len(g['p_hand']))
        for i, card in enumerate(g['p_hand']):
            if cols[i].button(f"🃏 {card}", key=f"c_{i}"):
                if g['stack'] and card == "Counterspell":
                    g['stack'] = None
                    g['logs'] = "🛡️ BIEN JOUÉ ! Sort contré !"
                    st.rerun()

with col2:
    st.info(g['logs'])
    
    # LOGIQUE DU TIMER
    if g['stack']:
        barre = st.progress(1.0)
        temps_max = g['difficulty']
        
        if st.button("🚨 INTERROMPRE !", use_container_width=True):
            g['logs'] = "⏱️ Jeu figé... Joue ton contre-sort !"
            st.rerun()
            
        # On divise le temps en 100 étapes pour la barre de progression
        step = temps_max / 100
        for p in range(100, 0, -1):
            time.sleep(step)
            barre.progress(p/100)
        
        # Si on arrive au bout
        resoudre_pile()
        st.rerun()

    if st.button("▶️ TOUR DE L'IA", use_container_width=True):
        tour_ia()
        st.rerun()
