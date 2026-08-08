
# =========================================================
# CleanTrack Time Planner
# Built with Python by Heider Jeffer
# =========================================================

import streamlit as st
from datetime import datetime, time


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CleanTrack Time Planner",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PRO GUI STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background: #f7f8fa;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hide unnecessary Streamlit elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Main title */
    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }

    .app-subtitle {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.15rem;
        margin-bottom: 1.5rem;
    }

    /* Input area */
    .input-panel {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.2rem 1.4rem 0.8rem 1.4rem;
        margin-bottom: 1.2rem;
    }

    /* Main result cards */
    .result-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.25rem;
        min-height: 145px;
    }

    .result-label {
        color: #6b7280;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.4rem;
    }

    .result-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.1;
    }

    .result-small {
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    /* Center room time */
    .room-time {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1rem;
    }

    .room-time-label {
        color: #6b7280;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .room-time-value {
        font-size: 3rem;
        font-weight: 750;
        line-height: 1.1;
        margin-top: 0.3rem;
    }

    .room-time-unit {
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* Status */
    .status-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.3rem;
        margin-top: 1rem;
        text-align: center;
    }

    .status-title {
        color: #6b7280;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .status-value {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 0.3rem;
    }

    /* Working day */
    .working-day {
        text-align: center;
        color: #6b7280;
        font-size: 0.82rem;
        padding: 1rem 0 0.3rem 0;
    }

    /* Progress */
    .progress-label {
        display: flex;
        justify-content: space-between;
        color: #6b7280;
        font-size: 0.8rem;
        margin-bottom: 0.3rem;
    }

    /* Mobile */
    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .app-title {
            font-size: 1.7rem;
        }

        .result-value {
            font-size: 1.6rem;
        }

        .room-time-value {
            font-size: 2.4rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SETTINGS
# =========================================================

TOTAL_ROOMS = 16

START_TIME = time(8, 0)
END_TIME = time(13, 0)

BREAK_START = time(10, 0)
BREAK_END = time(10, 20)

BREAK_MINUTES = 20


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="app-title">🧹 CleanTrack Time Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Built with Python by Heider Jeffer'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DATE
# =========================================================

now = datetime.now()

today = now.strftime("%d/%m/%Y")
day_name = now.strftime("%A")


# =========================================================
# INPUT PANEL
# =========================================================

st.markdown(
    '<div class="input-panel">',
    unsafe_allow_html=True
)

input1, input2, input3 = st.columns(3)


with input1:

    current_time = st.time_input(
        "⏰ Current Time",
        value=time(8, 0),
        step=60
    )


with input2:

    rooms_completed = st.number_input(
        "🛏️ Rooms Completed",
        min_value=0,
        max_value=TOTAL_ROOMS,
        value=0,
        step=1
    )


with input3:

    corridor_finished = st.checkbox(
        "🚿 Corridor Finished"
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TIME CALCULATIONS
# =========================================================

current_minutes = (
    current_time.hour * 60
    + current_time.minute
)

start_minutes = (
    START_TIME.hour * 60
    + START_TIME.minute
)

end_minutes = (
    END_TIME.hour * 60
    + END_TIME.minute
)

break_start_minutes = (
    BREAK_START.hour * 60
    + BREAK_START.minute
)

break_end_minutes = (
    BREAK_END.hour * 60
    + BREAK_END.minute
)


# =========================================================
# ROOMS
# =========================================================

rooms_remaining = (
    TOTAL_ROOMS
    - rooms_completed
)


# =========================================================
# AVAILABLE TIME
# =========================================================

if current_minutes < start_minutes:

    available_minutes = (
        end_minutes
        - start_minutes
        - BREAK_MINUTES
    )

elif current_minutes < break_start_minutes:

    available_minutes = (
        end_minutes
        - current_minutes
        - BREAK_MINUTES
    )

elif current_minutes < break_end_minutes:

    available_minutes = (
        end_minutes
        - break_end_minutes
    )

else:

    available_minutes = (
        end_minutes
        - current_minutes
    )


available_minutes = max(
    0,
    available_minutes
)


# =========================================================
# AVAILABLE TIME DISPLAY
# =========================================================

available_hours = available_minutes // 60
available_remainder = available_minutes % 60


if available_hours > 0 and available_remainder > 0:

    available_time_display = (
        f"{available_hours}h "
        f"{available_remainder}m"
    )

elif available_hours > 0:

    available_time_display = (
        f"{available_hours}h"
    )

else:

    available_time_display = (
        f"{available_remainder}m"
    )


# =========================================================
# MINUTES PER ROOM
# =========================================================

if rooms_remaining > 0:

    minutes_per_room = (
        available_minutes
        / rooms_remaining
    )

else:

    minutes_per_room = 0


# =========================================================
# PROGRESS
# =========================================================

progress = (
    rooms_completed
    / TOTAL_ROOMS
)


# =========================================================
# EXPECTED FINISH
# =========================================================

if rooms_remaining == 0:

    expected_finish = current_time.strftime(
        "%I:%M %p"
    )

else:

    calculation_start = max(
        current_minutes,
        start_minutes
    )

    finish_minutes = (
        calculation_start
        + (
            rooms_remaining
            * minutes_per_room
        )
    )

    if (
        calculation_start < break_start_minutes
        and finish_minutes > break_start_minutes
    ):

        finish_minutes += BREAK_MINUTES


    if finish_minutes <= end_minutes:

        finish_hour = int(
            finish_minutes // 60
        )

        finish_minute = int(
            finish_minutes % 60
        )

        expected_finish = datetime(
            2026,
            1,
            1,
            finish_hour,
            finish_minute
        ).strftime(
            "%I:%M %p"
        )

    else:

        expected_finish = "After 1:00 PM"


# =========================================================
# STATUS
# =========================================================

if rooms_completed == TOTAL_ROOMS:

    status_text = "🏆 All rooms completed"
    status_class = "success"

elif (
    current_minutes >= break_start_minutes
    and current_minutes < break_end_minutes
):

    status_text = "☕ Break time"
    status_class = "warning"

elif current_minutes >= end_minutes:

    status_text = "⛔ Working time finished"
    status_class = "error"

elif minutes_per_room >= 17.5:

    status_text = "🟢 On schedule"
    status_class = "success"

elif minutes_per_room >= 15:

    status_text = "🟡 Keep a steady pace"
    status_class = "warning"

else:

    status_text = "🔴 Time is tight"
    status_class = "error"


# =========================================================
# TOP RESULTS
# =========================================================

result1, result2, result3 = st.columns(3)


with result1:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Rooms Remaining</div>
            <div class="result-value">{rooms_remaining}</div>
            <div class="result-small">
                of {TOTAL_ROOMS} total rooms
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with result2:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Time Available</div>
            <div class="result-value">
                {available_time_display}
            </div>
            <div class="result-small">
                working time remaining
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with result3:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-label">Expected Finish</div>
            <div class="result-value">
                {expected_finish}
            </div>
            <div class="result-small">
                estimated completion
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ROOM TIME
# =========================================================

if rooms_remaining > 0:

    st.markdown(
        f"""
        <div class="room-time">
            <div class="room-time-label">
                Room-by-Room Time Plan
            </div>

            <div class="room-time-value">
                {minutes_per_room:.1f}
            </div>

            <div class="room-time-unit">
                minutes per room
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.success(
        "🏆 All 16 rooms are completed!"
    )


# =========================================================
# PROGRESS + STATUS
# =========================================================

progress_col, status_col = st.columns(2)


with progress_col:

    st.markdown(
        f"""
        <div class="status-box">
            <div class="status-title">Progress</div>
            <div class="status-value">
                {int(progress * 100)}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress)


with status_col:

    if status_class == "success":

        st.success(status_text)

    elif status_class == "warning":

        st.warning(status_text)

    else:

        st.error(status_text)


# =========================================================
# BREAK MESSAGE
# =========================================================

if (
    current_minutes >= break_start_minutes
    and current_minutes < break_end_minutes
):

    st.info(
        "☕ Take your 20-minute break. "
        "Work continues at 10:20 AM."
    )


# =========================================================
# WORKING DAY
# =========================================================

st.markdown(
    f"""
    <div class="working-day">
        🕗 08:00 AM — 01:00 PM
        &nbsp;&nbsp;•&nbsp;&nbsp;
        ☕ 10:00 AM — 10:20 AM
        &nbsp;&nbsp;•&nbsp;&nbsp;
        🛏️ 16 Rooms
        &nbsp;&nbsp;•&nbsp;&nbsp;
        {day_name}, {today}
    </div>
    """,
    unsafe_allow_html=True
)
