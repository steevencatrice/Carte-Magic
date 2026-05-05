import streamlit as st
import time
import random

# Configuration de la page
st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION DU GAME STATE ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 
        'ai_hp': 20,
        'p_deck': ["Counterspell", "Island", "Hedron Crab", "Opt", "Unsummon", "Negate", "Delver of Secrets"] * 4,
        'p_hand': [],
        'ai_deck': ["Mountain", "Lava Spike", "Shock", "Lightning Bolt", "Goblin Guide"] * 4,
        'stack': None,
        'logs': "Prêt pour le duel ?",
        'difficulty_lvl': 1,
        'is_paused': False,
        'phase': 'SETUP', # Phases: SETUP -> MULLIGAN -> PLAY
        'turn_owner': None
    }

g = st.session_state.game

# --- CALCUL DU TEMPS (Niveau 1 = 45s / Niveau 10 = 5s) ---
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- FONCTIONS LOGIQUES ---
def initialiser_partie():
    """Mélange les decks et prépare la main de départ."""
    random.shuffle(g['p_deck'])
    random.shuffle(g['ai_deck'])
    # Distribution de 7 cartes
    g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
    g['turn_owner'] = random.choice(["Steeven", "Kael"])
    g['phase'] = 'MULLIGAN'

def mulligan():
    """Remet la main dans le deck, mélange et repioche 7 cartes."""
    g['p_deck'].extend(g['p_hand'])
    g['p_hand'] = []
    random.shuffle(g['p_deck'])
    g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
    g['logs'] = "🔄 Mulligan effectué. Nouvelle main distribuée !"

# --- INTERFACE UTILISATEUR ---
st.title("🧙‍♂️ Magic Arena : Steeven vs Kael")

# Barre latérale (Réglages et Reset)
with st.sidebar:
    st.header("⚙️ Réglages")
    g['difficulty_lvl'] = st.slider("Niveau de l'IA (1=Relax, 10=Expert)", 1, 10, g['difficulty_lvl'])
    st.write(f"⏱️ Temps de réaction : **{temps_reaction:.1f}s**")
    st.divider()
    if st.button("🔄 Reset / Nouvelle Partie"):
        del st.session_state['game']
        st.rerun()

# --- LOGIQUE DES PHASES ---

# PHASE 1 : SETUP (Le mélange et la coupe)
if g['phase'] == 'SETUP':
    st.info("Bienvenue Steeven. Les decks sont prêts sur la table.")
    if st.button("🎲 Mélanger, couper et décider qui commence", use_container_width=True):
        initialiser_partie()
        st.rerun()

# PHASE 2 : MULLIGAN (Validation de la main)
elif g['phase'] == 'MULLIGAN':
    st.subheader(f"👋 Premier joueur désigné : {g['turn_owner']}")
    st.write("Analyse ta main de départ :")
    
    cols_m = st.columns(7)
    for i, card in enumerate(g['p_hand']):
        cols_m[i].button(f"🃏 {card}", disabled=True, key=f"mulli_view_{i}")
    
    st.write("---")
    col_m1, col_m2 = st.columns(2)
    if col_m1.button("✅ Garder cette main", use_container_width=True):
        g['phase'] = 'PLAY'
        g['logs'] = f"Le duel commence ! {g['turn_owner']} prend la main."
        st.rerun()
    if col_m2.button("❌ Mulligan (Trop risqué)", use_container_width=True):
        mulligan()
        st.rerun()

# PHASE 3 : LE DUEL (Phase de jeu)
else:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"🖥️ Kael : {g['ai_hp']} PV")
        st.progress(g['ai_hp'] / 20)
        st.divider()
        st.subheader(f"👤 Steeven : {g['p_hp']} PV")
        st.progress(max(g['p_hp'] / 20, 0.0))
        
        # Affichage des cartes en main (interactives)
        if len(g['p_hand']) > 0:
            cols_p = st.columns(len(g['p_hand']))
            for i, card in enumerate(g['p_hand']):
                if cols_p[i].button(f"🃏 {card}", key=f"play_card_{i}"):
                    if g['stack'] and card == "Counterspell":
                        g['stack'] = None
                        g['is_paused'] = False
                        g['p_hand'].pop(i) # La carte est consommée
                        g['logs'] = "🛡️ BIEN JOUÉ ! Sort contré !"
                        st.rerun()
        else:
            st.warning("Ta main est vide !")

    with col2:
        st.info(g['logs'])
        
        # GESTION DU CHRONO SI L'IA ATTAQUE
        if g['stack']:
            if not g['is_paused']:
                if st.button("🚨 STOP (Réflexion / Chaton)", use_container_width=True):
                    g['is_paused'] = True
                    st.rerun()

                # Barre de progression du temps
                barre = st.progress(1.0)
                nb_steps = 20
                step_duration = temps_reaction / nb_steps
                
                for p in range(nb_steps, 0, -1):
                    time.sleep(step_duration)
                    barre.progress(p/nb_steps)
                    # Si le joueur a cliqué sur une carte pendant le sommeil du script
                    if not st.session_state.game['stack']:
                        break
                
                # Sanction si le temps est écoulé
                if g['stack'] and not g['is_paused']: 
                    g['p_hp'] -= 3
                    g['logs'] = "💥 Trop tard ! Lava Spike te touche (-3 PV)."
                    g['stack'] = None
                    st.rerun()
            else:
                st.warning("⏳ Temps figé...")
                if st.button("▶️ REPRENDRE LE CHRONO", use_container_width=True):
                    g['is_paused'] = False
                    st.rerun()

        # ACTION DE L'IA
        if not g['stack']:
            if st.button("▶️ TOUR DE L'IA", use_container_width=True):
                g['stack'] = "Lava Spike"
                g['is_paused'] = False
                g['logs'] = "⚠️ KAEL : 'Lava Spike dans ta tête !'"
                st.rerun()
