import streamlit as st
import time

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_hand': ["Counterspell", "Island", "Hedron Crab"],
        'stack': None, 
        'logs': "Prépare-toi, Steeven !",
        'difficulty_lvl': 1
    }

g = st.session_state.game

# --- CALCUL DU TEMPS ---
# Niveau 1 = 45s / Niveau 10 = 5s
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- FONCTIONS ---
def resoudre_pile():
    if g['stack']:
        g['p_hp'] -= 3
        g['logs'] = f"💥 Trop tard ! {g['stack']} te touche (-3 PV)."
        g['stack'] = None

# --- INTERFACE ---
st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")

with st.sidebar:
    st.header("⚙️ Réglages")
    # On stocke le niveau directement dans le game state pour qu'il soit persistant
    g['difficulty_lvl'] = st.slider("Niveau de l'IA", 1, 10, g['difficulty_lvl'])
    st.write(f"⏱️ Temps de réaction : **{temps_reaction:.1f}s**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🖥️ Kael : {g['ai_hp']} PV")
    st.divider()
    st.subheader(f"👤 Steeven : {g['p_hp']} PV")
    
    cols = st.columns(len(g['p_hand']))
    for i, card in enumerate(g['p_hand']):
        if cols[i].button(f"🃏 {card}", key=f"c_{i}"):
            if g['stack']:
                if card == "Counterspell":
                    g['stack'] = None
                    g['logs'] = "🛡️ BIEN JOUÉ ! Sort contré !"
                else:
                    g['logs'] = f"❌ {card} ne sert à rien contre ce sort ! Vite !"
                st.rerun()

with col2:
    st.info(g['logs'])
    
    if g['stack']:
        barre = st.progress(1.0)
        # On simule le timer. Attention : cliquer sur une mauvaise carte 
        # va relancer ce bloc, mais l'IA ne lâche pas l'affaire !
        step = temps_reaction / 100
        for p in range(100, 0, -1):
            time.sleep(step)
            barre.progress(p/100)
        
        resoudre_pile()
        st.rerun()

    if not g['stack']:
        if st.button("▶️ TOUR DE L'IA", use_container_width=True):
            g['stack'] = "Lava Spike"
            g['logs'] = "⚠️ Kael lance Lava Spike !"
            st.rerun()
