import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Magic : Arena Steeven")

# --- DESIGN ULTRA-LISIBLE ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; } /* Fond noir total */
    .metric-label { font-size: 1.2rem !important; color: #ADB5BD !important; }
    .metric-value { font-size: 2rem !important; font-weight: bold; color: #FFFFFF !important; }
    .card-title { font-size: 1.1rem; font-weight: bold; color: #00D1FF; text-align: center; margin-top: 10px; }
    .card-desc { font-size: 0.9rem; color: #FFD700; text-align: center; font-style: italic; min-height: 40px; }
    .log-box { background: #111; color: #00FF00; border: 2px solid #00FF00; padding: 15px; font-size: 1.3rem; font-family: monospace; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

DB = {
    "Hedron Crab": {"fr": "🦀 Crabe d'Hédron", "m": 1, "t": "C", "desc": "Meule 3 cartes par terrain."},
    "Island": {"fr": "💧 Île", "m": 0, "t": "L", "desc": "Produit 1 mana bleu."},
    "Mountain": {"fr": "🔥 Montagne", "m": 0, "t": "L", "desc": "Terrain ennemi."},
    "Lava Spike": {"fr": "⚡ Pointe de lave", "m": 1, "t": "S", "desc": "Dégâts directs (3)."},
    "Archive Trap": {"fr": "🌀 Piège d'archive", "m": 5, "t": "S", "desc": "Meule 13 cartes d'un coup !"}
}

if 'game' not in st.session_state:
    p_deck = ["Island"]*20 + ["Hedron Crab"]*12 + ["Archive Trap"]*8 + ["Island"]*20
    random.shuffle(p_deck)
    st.session_state.game = {
        'p_hp': 20, 'ai_hp': 20, 'p_mana': 0, 'p_deck': p_deck, 'ai_deck': ["Mountain"]*30 + ["Lava Spike"]*30,
        'ai_grave': 0, 'p_hand': [], 'p_board': [], 'p_lands': [], 
        'ai_lands': ["Mountain"], 'active': False, 'land_played': False, 'logs': "DUEL LANCÉ !", 'winner': None
    }

def tour_ia():
    g = st.session_state.game
    if len(g['ai_lands']) < 10: g['ai_lands'].append("Mountain")
    g['p_hp'] -= 3
    g['logs'] = "💥 Gemini joue un sort ! (-3 PV)"
    if g['p_deck']: g['p_hand'].append(g['p_deck'].pop(0))
    g['land_played'] = False; g['p_mana'] = 0
    for l in g['p_lands']: l['status'] = 'untapped'
    if g['p_hp'] <= 0: g['winner'] = "Gemini"

if st.session_state.game['winner']:
    st.title(f"🏆 {st.session_state.game['winner']} a gagné !")
    if st.button("REJOUER"): del st.session_state['game']; st.rerun()
elif not st.session_state.game['active']:
    st.title("🎴 Magic Arena - Version 4.4 Stable")
    if st.button("LANCER LE MATCH"):
        st.session_state.game['p_hand'] = [st.session_state.game['p_deck'].pop(0) for _ in range(7)]
        st.session_state.game['active'] = True; st.rerun()
else:
    # 1. HUD HAUTE VISIBILITÉ
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("❤️ PV", st.session_state.game['p_hp'])
    h2.metric("🎴 DECK IA", len(st.session_state.game['ai_deck']))
    h3.metric("💀 MEULE", st.session_state.game['ai_grave'])
    h4.metric("💧 MANA", st.session_state.game['p_mana'])

    st.markdown(f'<div class="log-box">📜 {st.session_state.game["logs"]}</div>', unsafe_allow_html=True)
    
    # 2. PLATEAU
    st.write("---")
    c_plat, c_fin = st.columns([5, 1])
    with c_plat:
        # IA
        ia_zone = st.columns(12)
        for i, _ in enumerate(st.session_state.game['ai_lands']):
            ia_zone[i % 12].image("https://api.scryfall.com/cards/named?exact=Mountain&format=image", width=60)
        st.write("")
        # Joueur
        st_zone = st.columns(10)
        for i, _ in enumerate(st.session_state.game['p_board']):
            st_zone[i % 10].image("https://api.scryfall.com/cards/named?exact=Hedron+Crab&format=image", width=110)
        for i, l in enumerate(st.session_state.game['p_lands']):
            with st_zone[(len(st.session_state.game['p_board']) + i) % 10]:
                if l['status'] == 'untapped' and st.button("💧", key=f"mana{i}"):
                    l['status'] = 'tapped'; st.session_state.game['p_mana'] += 1; st.rerun()
                st.image("https://api.scryfall.com/cards/named?exact=Island&format=image", width=70 if l['status'] == 'untapped' else 50)

    with c_fin:
        if st.button("🔔 FINIR TOUR", key="end", use_container_width=True, type="primary"):
            tour_ia(); st.rerun()

    # 3. TA MAIN (AVEC DESCRIPTIONS CLAIRES)
    st.write("---")
    st.write(f"🃏 TA MAIN ({len(st.session_state.game['p_hand'])} cartes)")
    cols_h = st.columns(6)
    for i, nom in enumerate(st.session_state.game['p_hand']):
        info = DB.get(nom, {"fr": nom, "desc": "", "m": 0, "t": "S"})
        with cols_h[i % 6]:
            st.markdown(f'<div class="card-title">{info["fr"]}</div>', unsafe_allow_html=True)
            st.image(f"https://api.scryfall.com/cards/named?exact={nom.replace(' ', '+')}&format=image", width=190)
            st.markdown(f'<div class="card-desc">{info["desc"]}</div>', unsafe_allow_html=True) # Description ici !
            if st.button("JOUER", key=f"play{i}", use_container_width=True):
                if nom == "Island" and not st.session_state.game['land_played']:
                    st.session_state.game['p_lands'].append({'status': 'untapped'})
                    st.session_state.game['land_played'] = True
                    st.session_state.game['p_hand'].pop(i)
                    meule = len(st.session_state.game['p_board']) * 3
                    for _ in range(meule):
                        if st.session_state.game['ai_deck']: 
                            st.session_state.game['ai_deck'].pop(0); st.session_state.game['ai_grave'] += 1
                    st.session_state.game['logs'] = f"✅ Île posée ! Meule de {meule} cartes."
                    if len(st.session_state.game['ai_deck']) <= 0: st.session_state.game['winner'] = "Steeven (Meule !)"
                    st.rerun()
                elif st.session_state.game['p_mana'] >= info['m'] and info['t'] != "L":
                    st.session_state.game['p_mana'] -= info['m']
                    if info['t'] == "C": st.session_state.game['p_board'].append(nom)
                    else: 
                        for _ in range(13):
                            if st.session_state.game['ai_deck']: 
                                st.session_state.game['ai_deck'].pop(0); st.session_state.game['ai_grave'] += 1
                        st.session_state.game['logs'] = "🌀 PIÈGE D'ARCHIVE !"
                    st.session_state.game['p_hand'].pop(i); st.rerun()
