import streamlit as st
import time

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

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
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")

with st.sidebar:
    st.header("⚙️ Réglages")
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
                    g['is_paused'] = False
                    g['logs'] = "🛡️ BIEN JOUÉ ! Sort contré !"
                else:
                    g['logs'] = f"❌ {card} ne sert à rien !"
                st.rerun()

with col2:
    st.info(g['logs'])
    
    if g['stack']:
        if not g['is_paused']:
            if st.button("🚨 STOP / PAUSE", use_container_width=True):
                g['is_paused'] = True
                st.rerun()

            barre = st.progress(1.0)
            # On divise le temps en petits morceaux pour être plus réactif
            nb_steps = 20 
            step_duration = temps_reaction / nb_steps
            
            for p in range(nb_steps, 0, -1):
                time.sleep(step_duration)
                barre.progress(p/nb_steps)
                # Si le stack a été vidé par un clic de bouton entre deux étapes
                if not st.session_state.game['stack']:
                    break
            
            # Vérification finale après la fin du timer
            if g['stack'] and not g['is_paused']: 
                g['p_hp'] -= 3
                g['logs'] = "💥 Trop tard ! Lava Spike te touche."
                g['stack'] = None
                st.rerun()
        else:
            if st.button("▶️ REPRENDRE", use_container_width=True):
                g['is_paused'] = False
                st.rerun()

    if not g['stack']:
        if st.button("▶️ TOUR DE L'IA", use_container_width=True):
            g['stack'] = "Lava Spike"
            g['is_paused'] = False
            g['logs'] = "⚠️ Kael lance Lava Spike !"
            st.rerun()
