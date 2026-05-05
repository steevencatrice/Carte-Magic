import streamlit as st
import time
import random

st.set_page_config(page_title="Magic Arena Pro", layout="wide")

# --- INITIALISATION DU JEU ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20,
        'p_deck': ["Island", "Counterspell", "Hedron Crab", "Opt", "Unsummon"] * 8,
        'p_hand': [],
        'p_land': [],
        'p_board': [],
        'p_graveyard': [],
        'ai_hand_count': 7,
        'ai_land': [],
        'ai_board': [],
        'ai_graveyard': [],
        'history': ["Bienvenue dans l'Arène !"],
        'chat': [{"user": "Kael", "msg": "Alors, Steeven, tu as peur ?"}],
        'stack': None,
        'difficulty_lvl': 5,
        'is_paused': False,
        'phase': 'SETUP',
        'turn_owner': None
    }

g = st.session_state.game
temps_reaction = 45 - (g['difficulty_lvl'] - 1) * 4.44

# --- LOGIQUE INTERNE ---
def ajouter_log(message):
    g['history'].insert(0, message)

def initialiser():
    random.shuffle(g['p_deck'])
    g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
    g['turn_owner'] = random.choice(["Steeven", "Kael"])
    g['phase'] = 'MULLIGAN'
    ajouter_log(f"Mélange terminé. {g['turn_owner']} commence.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    g['difficulty_lvl'] = st.slider("Difficulté", 1, 10, g['difficulty_lvl'])
    if st.button("🔄 Reset Total"):
        del st.session_state['game']
        st.rerun()

# --- PHASES DE DÉPART ---
if g['phase'] == 'SETUP':
    st.title("🧙‍♂️ Magic Arena")
    if st.button("🎲 MÉLANGER ET DISTRIBUER", use_container_width=True):
        initialiser()
        st.rerun()

elif g['phase'] == 'MULLIGAN':
    st.subheader(f"👋 Premier joueur : {g['turn_owner']}")
    cols = st.columns(7)
    for i, c in enumerate(g['p_hand']): cols[i].button(c, disabled=True, key=f"m_{i}")
    c1, c2 = st.columns(2)
    if c1.button("✅ Garder la main", use_container_width=True):
        g['phase'] = 'PLAY'
        st.rerun()
    if c2.button("❌ Mulligan", use_container_width=True):
        g['p_deck'].extend(g['p_hand'])
        random.shuffle(g['p_deck'])
        g['p_hand'] = [g['p_deck'].pop() for _ in range(7)]
        st.rerun()

# --- LE PLATEAU (DESIGN image_4.png) ---
else:
    # 1. RANGÉE DES RESSOURCES (METRICS)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📚 Ma Bibli", f"{len(g['p_deck'])}/60")
    m2.metric("💀 Mon Cimetière", len(g['p_graveyard']))
    m3.metric("📚 Bibli IA", "??/60")
    m4.metric("💀 Cimetière IA", len(g['ai_graveyard']))

    st.divider()

    # 2. DISPOSITION EN 3 COLONNES
    col_left, col_mid, col_right = st.columns([1, 2.5, 1])

    with col_left: # HISTORIQUE
        st.subheader("📜 Historique")
        with st.container(height=450):
            for log in g['history']: st.caption(log)

    with col_mid: # PLATEAU CENTRAL
        # ZONE IA
        with st.container(border=True):
            st.write(f"🖥️ **KAEL** - ❤️ {g['ai_hp']} PV")
            st.caption("🎴 " * g['ai_hand_count'])
            st.write(f"⛰️ Terrains: {len(g['ai_land'])} | 👹 Monstres: {len(g['ai_board'])}")

        # ZONE DE COMBAT (STACK)
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
                        ajouter_log(f"Lava Spike touche Steeven (-3 PV)")
                        g['stack'] = None
                        st.rerun()
            else:
                st.write("Zone de Combat Paisible...")

        # ZONE JOUEUR (STEEVEN)
        with st.container(border=True):
            st.write(f"⚔️ Terrains: {len(g['p_land'])} | 🛡️ Monstres: {len(g['p_board'])}")
            st.divider()
            st.write(f"👤 **STEEVEN** - ❤️ {g['p_hp']} PV")
            cols_h = st.columns(len(g['p_hand']))
            for i, card in enumerate(g['p_hand']):
                if cols_h[i].button(card, key=f"p_{i}"):
                    if card == "Island":
                        g['p_land'].append(g['p_hand'].pop(i))
                        ajouter_log("Steeven pose une Île")
                    elif card == "Counterspell" and g['stack']:
                        g['p_graveyard'].append(g['p_hand'].pop(i))
                        g['stack'] = None
                        ajouter_log("Sort contré avec succès !")
                    st.rerun()

    with col_right: # CHAT & BOUTONS
        st.subheader("💬 Chat IA")
        with st.container(height=200):
            for m in g['chat']: st.markdown(f"**{m['user']}:** {m['msg']}")
        
        # Le fameux cercle orange : Chat interactif
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
