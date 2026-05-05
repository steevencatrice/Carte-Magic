import streamlit as st
import time
import random

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_deck': ["Island", "Counterspell", "Hedron Crab", "Opt", "Unsummon", "Sol Ring"] * 8, # Sol Ring = Artefact
        'p_hand': [], 'p_land': [], 'p_board': [], 'p_graveyard': [],
        'ai_deck_count': 60, 'ai_hand_count': 7, 'ai_land': [], 'ai_board': [], 'ai_graveyard': [],
        'history': ["Duel lancé !"],
        'chat': [{"user": "Kael", "msg": "Alors, Steeven, prêt à perdre ?"}],
        'stack': None, 'difficulty_lvl': 5, 'is_paused': False, 'phase': 'SETUP'
    }

g = st.session_state.game
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- FONCTIONS DE COMPTAGE DÉTAILLÉ ---
def stats_cimetiere(liste_cartes):
    """Compte précisément chaque type de carte selon ton dessin original."""
    terrains = sum(1 for c in liste_cartes if c in ["Island", "Mountain"])
    sorts = sum(1 for c in liste_cartes if c in ["Counterspell", "Opt", "Unsummon", "Lava Spike", "Shock"])
    monstres = sum(1 for c in liste_cartes if c in ["Hedron Crab", "Delver of Secrets", "Goblin Guide"])
    artefacts = sum(1 for c in liste_cartes if c in ["Sol Ring", "Mana Vault"]) # Ajout du type Artefact
    
    return f"🟢 {monstres} Monstres | ✨ {sorts} Sorts | ⛰️ {terrains} Terrains | 💎 {artefacts} Artefacts"

def ajouter_log(message):
    g['history'].insert(0, message)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    g['difficulty_lvl'] = st.slider("Difficulté", 1, 10, g['difficulty_lvl'])
    if st.button("🔄 Reset Total"):
        del st.session_state['game']
        st.rerun()

# --- JEU ---
if g['phase'] == 'SETUP':
    st.title("🧙‍♂️ Magic Arena")
    if st.button("🎲 MÉLANGER ET DISTRIBUER", use_container_width=True):
        random.shuffle(g['p_deck'])
        g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
        g['phase'] = 'PLAY'
        st.rerun()

else:
    col_left, col_mid, col_right = st.columns([1, 2.5, 1])

    # 1. COLONNE GAUCHE : HISTORIQUE + MES RESSOURCES
    with col_left:
        st.subheader("📜 Historique")
        with st.container(height=350):
            for log in g['history']: st.caption(log)
        
        st.write("---")
        st.subheader("🎒 Mes Ressources")
        st.metric("📚 Ma Bibliothèque", f"{len(g['p_deck'])}/60")
        with st.expander(f"💀 Mon Cimetière ({len(g['p_graveyard'])})"):
            st.write(stats_cimetiere(g['p_graveyard']))

    # 2. COLONNE CENTRALE : PLATEAU
    with col_mid:
        # ZONE IA (EN HAUT)
        with st.container(border=True):
            ia_top1, ia_top2 = st.columns([1.5, 1.5])
            ia_top1.write(f"🖥️ **KAEL** - ❤️ {g['ai_hp']} PV")
            # DÉTAIL DU CIMETIÈRE ADVERSE AJOUTÉ ICI (En haut à droite)
            with ia_top2:
                st.caption(f"📚 IA: ??/60 | 💀 Cimetière: {len(g['ai_graveyard'])}")
                with st.expander("Détails Cimetière IA"):
                    st.caption(stats_cimetiere(g['ai_graveyard']))
            
            st.caption("🎴 " * g['ai_hand_count'])
            st.write(f"⛰️ Terrains: {len(g['ai_land'])} | 👹 Monstres: {len(g['ai_board'])}")

        # ZONE DE COMBAT
        st.write("")
        with st.container(height=180, border=True):
            if g['stack']:
                st.warning(f"⚡ SORT EN COURS : {g['stack']}")
                if not g['is_paused']:
                    barre = st.progress(1.0)
                    for p in range(20, 0, -1):
                        time.sleep(temps_reaction / 20)
                        barre.progress(p/20)
                        if not st.session_state.game['stack']: break
                    if g['stack'] and not g['is_paused']:
                        g['p_hp'] -= 3
                        g['ai_graveyard'].append(g['stack']) # Le sort de l'IA va dans son cimetière
                        ajouter_log(f"Kael inflige 3 dégâts avec {g['stack']}")
                        g['stack'] = None
                        st.rerun()
            else:
                st.write("Zone de Combat Paisible...")

        # ZONE JOUEUR (EN BAS)
        with st.container(border=True):
            st.write(f"⚔️ Terrains: {len(g['p_land'])} | 🛡️ Monstres: {len(g['p_board'])}")
            st.divider()
            st.write(f"👤 **STEEVEN** - ❤️ {g['p_hp']} PV")
            cols_h = st.columns(len(g['p_hand']))
            for i, card in enumerate(g['p_hand']):
                if cols_h[i].button(card, key=f"p_{i}"):
                    if card == "Island":
                        g['p_land'].append(g['p_hand'].pop(i))
                    elif card == "Counterspell" and g['stack']:
                        g['p_graveyard'].append(g['p_hand'].pop(i)) # Ton contre va au cimetière
                        g['ai_graveyard'].append(g['stack']) # Le sort adverse contré y va aussi
                        g['stack'] = None
                        ajouter_log("Sort adverse contré et défaussé !")
                    st.rerun()

    # 3. COLONNE DROITE : CHAT ET BOUTONS
    with col_right:
        st.subheader("💬 Chat IA")
        with st.container(height=200):
            for m in g['chat']: st.markdown(f"**{m['user']}:** {m['msg']}")
        
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Répondre...")
            if st.form_submit_button("Envoyer"):
                if user_msg:
                    g['chat'].append({"user": "Moi", "msg": user_msg})
                    st.rerun()

        st.divider()
        if st.button("▶️ TOUR IA", use_container_width=True, type="primary"):
            g['stack'] = "Lava Spike"
            g['is_paused'] = False
            st.rerun()
        
        label_p = "▶️ REPRENDRE" if g['is_paused'] else "🚨 PAUSE"
        if st.button(label_p, use_container_width=True):
            g['is_paused'] = not g['is_paused']
            st.rerun()
