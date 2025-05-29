import streamlit as st
import random
import time

st.set_page_config(page_title="Emoji Horse Race Game", layout="wide")

# Setup
track_length = 20
players = {
    "🐎1": 0,
    "🐎2": 0,
    "🐎3": 0,
    "🐎4": 0,
    "🐎5": 0
}

if "positions" not in st.session_state:
    st.session_state.positions = players.copy()
    st.session_state.winner = None
    st.session_state.race_in_progress = False
    st.session_state.scores = {emoji: 0 for emoji in players}
    st.session_state.bet = None
    st.session_state.bet_locked = False

st.title("🏁🐎 Emoji Horse Race Game (Right to Left!)")

left_col, right_col = st.columns([3, 1])

with right_col:
    # Betting
    st.subheader("💰 Place Your Bet")
    if not st.session_state.bet_locked:
        st.session_state.bet = st.radio(
            "Which horse do you think will win?",
            list(players.keys()),
            index=0,
            key="bet_selection"
        )
    else:
        st.radio(
            "Which horse do you think will win?",
            list(players.keys()),
            index=list(players.keys()).index(st.session_state.bet),
            key="bet_selection_disabled",
            disabled=True
        )

    # Scoreboard
    st.subheader("📊 Scoreboard")
    for horse, score in st.session_state.scores.items():
        st.write(f"{horse}: {score} wins")

# Race display logic
race_placeholder = left_col.empty()
def display_race():
    with race_placeholder.container():
        for emoji, pos in st.session_state.positions.items():
            # Right-to-left movement, 🏁 is on the left
            spaces_after = track_length - pos
            track = "🏁" + "⬜" * spaces_after + emoji + "⬜" * pos
            st.write(track)

# Race progress logic
if st.session_state.race_in_progress:
    while not st.session_state.winner:
        for emoji in st.session_state.positions:
            if st.session_state.positions[emoji] < track_length:
                st.session_state.positions[emoji] += random.randint(1, 3)
                if st.session_state.positions[emoji] >= track_length:
                    st.session_state.positions[emoji] = track_length
                    st.session_state.winner = emoji
                    st.session_state.scores[emoji] += 1
                    break
        display_race()
        time.sleep(0.5)
    st.session_state.race_in_progress = False

# Show current race state when not running
if not st.session_state.race_in_progress:
    display_race()

# --- Race & Restart Buttons Side by Side ---
btn_col1, btn_col2 = st.columns([1, 1])

with btn_col1:
    if st.button("🎲 Race!"):
        if not st.session_state.winner:
            st.session_state.race_in_progress = True
            st.session_state.bet_locked = True
            st.rerun()

with btn_col2:
    if st.button("🔄 Restart"):
        st.session_state.positions = players.copy()
        st.session_state.winner = None
        st.session_state.race_in_progress = False
        st.session_state.bet_locked = False
        st.rerun()

# Result section
if st.session_state.winner:
    st.success(f"🏆 {st.session_state.winner} wins the race!")
    if st.session_state.bet == st.session_state.winner:
        st.balloons()
        st.success("🎉 Congratulations! You guessed correctly!")
    else:
        st.error("😢 Sorry, your bet didn't win this time.")
