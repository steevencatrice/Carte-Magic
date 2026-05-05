import streamlit as st
import time

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION DU JEU ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_hand': ["Counterspell", "Island", "Hedron Crab"],
        'stack': None, 
        'logs': "Prépare-toi, Steeven !",
        'difficulty_lvl': 1,
        'is_paused': False
    }

g = st.session_state.game

# --- CALCUL DYNAMIQUE DU TEMPS ---
# Niveau 1 = 45s / Niveau 10 = 5s
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- INTERFACE ---
st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")

# Barre latérale de configuration
with st.sidebar:
    st.header("⚙️ Réglages")
    g['difficulty_lvl'] = st.slider("Niveau de l'IA (1=Relax, 10=Expert)", 1, 10, g['difficulty_lvl'])
    st.write(f"⏱️ Temps de réaction : **{temps_reaction:.1f}s**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🖥️ Kael : {g['ai_hp']} PV")
    st.divider()
    st.subheader(f"👤 Steeven : {g['p_hp']} PV")
    
    # Cartes en main
    cols = st.columns(len(g['p_hand']))
    for i, card in enumerate(g['p_hand']):
        if cols[i].button(f"🃏 {card}", key=f"c_{i}"):
            if g['stack']:
                if card == "Counterspell":
                    g['stack'] = None
                    g['is_paused'] = False
                    g['logs'] = "🛡️ BIEN JOUÉ ! Sort contré !"
                else:
                    g['logs'] = f"❌ {card} ne sert à rien ! Vite !"
                st.rerun()

with col2:
    st.info(g['logs'])
    
    # GESTION DU SORT EN ATTENTE (LA PILE)
    if g['stack']:
        # Bouton Stop réactif
        if not g['is_paused']:
            if st.button("🚨 STOP ! (Pause réflexion/Chaton)", use_container_width=True):
                g['is_paused'] = True
                g['logs'] = "⏸️ JEU EN PAUSE. Respire et joue une carte !"
                st.rerun()
        else:
            if st.button("▶️ REPRENDRE LE CHRONO", use_container_width=True):
                g['is_paused'] = False
                st.rerun()

        # Le Timer visuel
        if not g['is_paused']:
            barre = st.progress(1.0)
            step = temps_reaction / 100
            for p in range(100, 0, -1):
                time.sleep(step)
                barre.progress(p/100)
            
            # VÉRIFICATION FINALE : Le joueur a-t-il agi pendant le chrono ?
            # On vérifie une dernière fois si g['stack'] est toujours là
            if g['stack']: 
                g['p_hp'] -= 3
                g['logs'] = "💥 Trop tard ! Lava Spike te touche (-3 PV)."
                g['stack'] = None
                st.rerun()
        else:
            st.warning("⏳ Le temps est figé. L'IA attend ton action.")

    # Bouton pour lancer le tour de l'IA
    if not g['stack']:
        if st.button("▶️ TOUR DE L'IA", use_container_width=True):
            g['stack'] = "Lava Spike"
            g['is_paused'] = False
            g['logs'] = "⚠️ Kael lance Lava Spike ! RÉAGIS !"
            st.rerun()
