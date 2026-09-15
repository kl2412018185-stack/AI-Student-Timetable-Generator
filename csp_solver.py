# ==========================================================
# AI STUDENT TIMETABLE GENERATOR
# CSP + BACKTRACKING + PREFERENCE SCORING
# ==========================================================


def get_period(time_slot):
    """
    Determine whether a class is in the morning or afternoon.
    """

    if "8:00 AM" in time_slot or "10:00 AM" in time_slot:
        return "Morning"

    return "Afternoon"


def get_day(time_slot):
    """
    Extract the day from the time slot.
    """

    return time_slot.split()[0]


def check_constraints(subject, time, schedule):

    lecturer = subject["lecturer"]
    room = subject["room"]
    class_type = subject["type"]

    for assigned in schedule.values():

        if assigned["time"] == time:
            return False

    for assigned in schedule.values():

        if (
            assigned["lecturer"].lower() == lecturer.lower()
            and assigned["time"] == time
        ):
            return False

    for assigned in schedule.values():

        if (
            assigned["room"].lower() == room.lower()
            and assigned["time"] == time
        ):
            return False


    # ------------------------------------------------------
    # CONSTRAINT 4:
    # Laboratory classes must use a laboratory room.
    # ------------------------------------------------------

    if class_type.lower() == "lab":

        if "lab" not in room.lower():

            return False


    # All hard constraints satisfied
    return True


def calculate_score(subject, time, preferences):
    """
    Calculate a preference score for a possible assignment.

    Higher score = better match with student preferences.
    """

    score = 0

    day = get_day(time)

    period = get_period(time)


    # ------------------------------------------------------
    # PREFERRED DAY
    # ------------------------------------------------------

    preferred_day = preferences["preferred_day"]

    if preferred_day != "Any":

        if day == preferred_day:
            score += 10


    # ------------------------------------------------------
    # PREFERRED PERIOD
    # ------------------------------------------------------

    preferred_period = preferences["preferred_period"]

    if preferred_period != "Any":

        if period == preferred_period:
            score += 5


    # ------------------------------------------------------
    # AVOID FRIDAY
    # ------------------------------------------------------

    if preferences["avoid_friday"]:

        if day == "Friday":
            score -= 5


    return score


def solve_timetable(subjects, preferences):
    """
    Main CSP solver.

    Uses backtracking to search for valid timetable assignments.
    Among valid solutions, the system selects the solution
    with the highest preference score.
    """

    best_solution = None

    best_score = float("-inf")


    def backtrack(index, schedule, current_score):

        nonlocal best_solution
        nonlocal best_score


        # --------------------------------------------------
        # BASE CASE
        # --------------------------------------------------
        # All subjects have been successfully assigned.
        # --------------------------------------------------

        if index == len(subjects):

            if current_score > best_score:

                best_score = current_score

                best_solution = schedule.copy()

            return


        # --------------------------------------------------
        # CURRENT SUBJECT
        # --------------------------------------------------

        subject = subjects[index]


        # --------------------------------------------------
        # TRY EACH POSSIBLE TIME
        # --------------------------------------------------

        for time in subject["times"]:


            # --------------------------------------------------
            # CHECK HARD CONSTRAINTS
            # --------------------------------------------------

            if check_constraints(
                subject,
                time,
                schedule
            ):


                # --------------------------------------------------
                # CALCULATE PREFERENCE SCORE
                # --------------------------------------------------

                score = calculate_score(
                    subject,
                    time,
                    preferences
                )


                # --------------------------------------------------
                # ASSIGN SUBJECT
                # --------------------------------------------------

                schedule[subject["name"]] = {

                    "time": time,

                    "lecturer": subject["lecturer"],

                    "room": subject["room"],

                    "type": subject["type"]

                }


                # --------------------------------------------------
                # CONTINUE SEARCH
                # --------------------------------------------------

                backtrack(
                    index + 1,
                    schedule,
                    current_score + score
                )


                # --------------------------------------------------
                # BACKTRACK
                # --------------------------------------------------

                del schedule[subject["name"]]


    # Start backtracking
    backtrack(
        0,
        {},
        0
    )


    # Return best solution and score
    return best_solution, best_score