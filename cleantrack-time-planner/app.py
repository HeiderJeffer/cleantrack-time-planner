
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
    layout="wide"
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

st.title("🧹 CleanTrack Time Planner")

st.markdown(
    "**Built with Python by Heider Jeffer**"
)

st.caption(
    "Simple cleaning time management for the working day."
)


# =========================================================
# WORKING DAY
# =========================================================

st.divider()

st.subheader("📅 Working Day")

st.markdown(
    """
🕗 **Start:** 08:00 AM &nbsp;&nbsp;&nbsp;
☕ **Break:** 10:00 AM – 10:20 AM

🏁 **Finish:** 01:00 PM &nbsp;&nbsp;&nbsp;
🛏️ **Rooms:** 16
"""
)


# =========================================================
# CURRENT DATE
# =========================================================

now = datetime.now()

today = now.strftime("%d/%m/%Y")
day_name = now.strftime("%A")


st.caption(
    f"📆 {day_name}, {today}"
)


# =========================================================
# WORK INFORMATION
# =========================================================

st.divider()

st.subheader("⚙️ Work Information")


col1, col2, col3 = st.columns(3)


with col1:

    current_time = st.time_input(
        "⏰ Current Time",
        value=time(8, 0),
        step=60
    )


with col2:

    rooms_completed = st.number_input(
        "🛏️ Rooms Completed",
        min_value=0,
        max_value=TOTAL_ROOMS,
        value=0,
        step=1
    )


with col3:

    corridor_finished = st.checkbox(
        "🚿 Corridor Finished"
    )


# =========================================================
# TIME CONVERSION
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
# REMAINING ROOMS
# =========================================================

rooms_remaining = (
    TOTAL_ROOMS
    - rooms_completed
)


# =========================================================
# AVAILABLE TIME
# =========================================================

if current_minutes < break_start_minutes:

    available_minutes = (
        end_minutes
        - current_minutes
        - BREAK_MINUTES
    )

elif (
    current_minutes >= break_start_minutes
    and current_minutes < break_end_minutes
):

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
# FORMAT MINUTES
# =========================================================

def format_minutes(minutes):

    minutes = max(
        0,
        int(round(minutes))
    )

    hours = minutes // 60
    mins = minutes % 60

    if hours > 0:

        if mins > 0:

            return f"{hours}h {mins}m"

        return f"{hours}h"

    return f"{mins}m"


# =========================================================
# CURRENT SITUATION
# =========================================================

st.divider()

st.subheader("📊 Current Situation")


metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    st.metric(
        "🛏️ Rooms Completed",
        f"{rooms_completed}/{TOTAL_ROOMS}"
    )


with metric2:

    st.metric(
        "📋 Rooms Remaining",
        rooms_remaining
    )


with metric3:

    st.metric(
        "⏱️ Time Available",
        format_minutes(
            available_minutes
        )
    )


with metric4:

    st.metric(
        "⏳ Minutes / Room",
        f"{minutes_per_room:.1f}"
    )


# =========================================================
# CLEANING PROGRESS
# =========================================================

st.divider()

st.subheader("📈 Cleaning Progress")


progress = (
    rooms_completed
    / TOTAL_ROOMS
)


st.progress(progress)


st.write(
    f"**{rooms_completed} of "
    f"{TOTAL_ROOMS} rooms completed**"
)


# =========================================================
# WORK STATUS
# =========================================================

st.divider()

st.subheader("🚦 Work Status")


if rooms_completed == TOTAL_ROOMS:

    st.success(
        "🏆 All 16 rooms are completed!"
    )


elif current_minutes < start_minutes:

    st.info(
        "🕗 Work has not started yet."
    )


elif (
    current_minutes >= break_start_minutes
    and current_minutes < break_end_minutes
):

    st.warning(
        "☕ BREAK TIME — "
        "10:00 AM → 10:20 AM"
    )


elif current_minutes >= end_minutes:

    st.error(
        "⛔ Working time has finished."
    )


elif minutes_per_room >= 17.5:

    st.success(
        f"🟢 You're on schedule — "
        f"you have approximately "
        f"**{minutes_per_room:.1f} minutes per room**."
    )


elif minutes_per_room >= 15:

    st.warning(
        f"🟡 Keep a steady pace — "
        f"you have approximately "
        f"**{minutes_per_room:.1f} minutes per room**."
    )


else:

    st.error(
        f"🔴 Time is tight — "
        f"you have only "
        f"**{minutes_per_room:.1f} minutes per room**."
    )


# =========================================================
# EXPECTED FINISH
# =========================================================

st.divider()

st.subheader("🎯 Expected Finish")


if rooms_remaining == 0:

    expected_finish = current_time.strftime(
        "%I:%M %p"
    )

    st.success(
        f"🏆 All rooms are finished "
        f"at approximately **{expected_finish}**."
    )


else:

    finish_minutes = (
        current_minutes
        + (
            rooms_remaining
            * minutes_per_room
        )
    )


    # Add the break if the estimated
    # schedule crosses 10:00 AM.

    if (
        current_minutes < break_start_minutes
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


        st.info(
            f"🎯 At your current pace, "
            f"you should finish around "
            f"**{expected_finish}**."
        )


    else:

        overtime = (
            finish_minutes
            - end_minutes
        )


        st.error(
            f"⚠️ At the current pace, "
            f"you may finish approximately "
            f"**{format_minutes(overtime)} "
            f"after 1:00 PM**."
        )


# =========================================================
# ROOM-BY-ROOM TIME PLAN
# =========================================================

st.divider()

st.subheader(
    "🗓️ Room-by-Room Time Plan"
)


if rooms_remaining > 0:

    st.metric(
        "⏱️ Time per Room",
        f"{minutes_per_room:.1f} min / Room"
    )

else:

    st.success(
        "🏆 All rooms completed."
    )


# =========================================================
# CORRIDOR
# =========================================================

st.divider()

st.subheader("🚿 Corridor")


if corridor_finished:

    st.success(
        "✅ Corridor completed."
    )

else:

    st.warning(
        "⏳ Corridor still needs to be completed."
    )


# =========================================================
# SIMPLE MOTIVATION
# =========================================================

st.divider()


if rooms_completed == 0:

    st.info(
        "💪 Start with Room 1. "
        "Stay focused and keep a steady pace!"
    )


elif rooms_completed < 4:

    st.info(
        "💪 Good start! Keep going."
    )


elif rooms_completed < 8:

    st.success(
        "🔥 You're making good progress!"
    )


elif rooms_completed < 12:

    st.success(
        "🚀 More than half completed. "
        "Keep the same pace!"
    )


elif rooms_completed < 16:

    st.success(
        "🏃 Almost there! Finish strong!"
    )


else:

    st.success(
        "🏆 Fantastic work! "
        "All 16 rooms are completed!"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    "### 🧹 CleanTrack Time Planner"
)

st.markdown(
    "***Built with Python by Heider Jeffer***"
)
