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

st.caption("Built with Python by Heider Jeffer")


# =========================================================
# DATE
# =========================================================

now = datetime.now()

today = now.strftime("%d/%m/%Y")
day_name = now.strftime("%A")


# =========================================================
# WORK INPUTS
# =========================================================

work_col1, work_col2, work_col3 = st.columns(3)


with work_col1:

    current_time = st.time_input(
        "⏰ Current Time",
        value=time(8, 0),
        step=60
    )


with work_col2:

    rooms_completed = st.number_input(
        "🛏️ Rooms Completed",
        min_value=0,
        max_value=TOTAL_ROOMS,
        value=0,
        step=1
    )


with work_col3:

    corridor_finished = st.checkbox(
        "🚿 Corridor Finished"
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


# =========================================================
# CORRIDOR TIME
# =========================================================

if corridor_finished:

    available_minutes = max(
        0,
        available_minutes - 20
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
    status_type = "success"

elif (
    current_minutes >= break_start_minutes
    and current_minutes < break_end_minutes
):

    status_text = "☕ Break time"
    status_type = "warning"

elif current_minutes >= end_minutes:

    status_text = "⛔ Working time finished"
    status_type = "error"

elif minutes_per_room >= 17.5:

    status_text = "🟢 On schedule"
    status_type = "success"

elif minutes_per_room >= 15:

    status_text = "🟡 Keep a steady pace"
    status_type = "warning"

else:

    status_text = "🔴 Time is tight"
    status_type = "error"


# =========================================================
# MAIN DASHBOARD — TOP ROW
# =========================================================

st.divider()

top1, top2, top3, top4 = st.columns(4)


# =========================================================
# WORK INFORMATION
# =========================================================

with top1:

    st.write(
        f"⏰ **Current Time**  \n"
        f"### {current_time.strftime('%I:%M %p')}"
    )

    st.write(
        f"🛏️ **Rooms Completed**  \n"
        f"### {rooms_completed} / {TOTAL_ROOMS}"
    )

    if corridor_finished:

        st.write(
            "🚿 **Corridor Finished**  \n"
            "### ✓"
        )

    else:

        st.write(
            "🚿 **Corridor Finished**  \n"
            "### —"
        )


# =========================================================
# TODAY
# =========================================================

with top2:

    st.write(
        f"🛏️ **{rooms_remaining} rooms remaining**"
    )

    st.write(
        f"⏱️ **{available_time_display} available**"
    )


# =========================================================
# ROOM TIME
# =========================================================

with top3:

    if rooms_remaining > 0:

        st.metric(
            "⏱️ Time / Room",
            f"{minutes_per_room:.1f} min"
        )

    else:

        st.success(
            "🏆 All rooms done"
        )


# =========================================================
# WORKING DAY
# =========================================================

with top4:

    st.write(
        "🕗 **08:00 AM → 01:00 PM**"
    )

    st.write(
        "☕ **10:00 AM → 10:20 AM**"
    )

    st.write(
        "🛏️ **16 rooms**"
    )

    st.caption(
        f"{day_name}, {today}"
    )


# =========================================================
# SECOND ROW
# =========================================================

st.divider()

bottom1, bottom2, bottom3 = st.columns(3)


# =========================================================
# PROGRESS
# =========================================================

with bottom1:

    st.metric(
        "📈 Progress",
        f"{int(progress * 100)}%"
    )

    st.progress(
        progress
    )


# =========================================================
# STATUS
# =========================================================

with bottom2:

    if status_type == "success":

        st.success(
            status_text
        )

    elif status_type == "warning":

        st.warning(
            status_text
        )

    else:

        st.error(
            status_text
        )


# =========================================================
# EXPECTED FINISH
# =========================================================

with bottom3:

    if rooms_remaining == 0:

        st.success(
            f"🎯 **{expected_finish}**"
        )

    elif expected_finish == "After 1:00 PM":

        st.error(
            f"🎯 **{expected_finish}**"
        )

    else:

        st.metric(
            "🎯 Expected Finish",
            expected_finish
        )


# =========================================================
# SIMPLE MESSAGE
# =========================================================

st.divider()

if rooms_completed == TOTAL_ROOMS:

    st.success(
        "🏆 Great work! All 16 rooms are completed."
    )

elif (
    current_minutes >= break_start_minutes
    and current_minutes < break_end_minutes
):

    st.info(
        "☕ Take your 20-minute break. "
        "Work continues at 10:20 AM."
    )

elif minutes_per_room >= 17.5:

    st.success(
        f"🟢 Keep your current pace — "
        f"about {minutes_per_room:.1f} minutes per room."
    )

elif minutes_per_room >= 15:

    st.warning(
        f"🟡 Stay focused — "
        f"about {minutes_per_room:.1f} minutes per room."
    )

else:

    st.error(
        f"🔴 Time is tight — "
        f"only {minutes_per_room:.1f} minutes per room."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🧹 CleanTrack Time Planner • "
    "Built with Python by Heider Jeffer"
)