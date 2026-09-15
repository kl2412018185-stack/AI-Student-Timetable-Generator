% ==========================================================
% AI STUDENT TIMETABLE GENERATOR
% PROLOG VALIDATION
% ==========================================================

% Rule 1: No time conflict
no_time_conflict(
    subject(S1, T1),
    subject(S2, T2)
) :-
    S1 \= S2,
    T1 \= T2.


% Rule 2: No lecturer conflict
no_lecturer_conflict(
    subject(S1, L1, T1),
    subject(S2, L2, T2)
) :-
    S1 \= S2,
    (
        L1 \= L2
        ;
        T1 \= T2
    ).


% Rule 3: No room conflict
no_room_conflict(
    subject(S1, R1, T1),
    subject(S2, R2, T2)
) :-
    S1 \= S2,
    (
        R1 \= R2
        ;
        T1 \= T2
    ).


% Rule 4: Lab subjects require lab rooms
valid_lab_room(lab, Room) :-
    sub_atom(
        Room,
        _,
        _,
        _,
        'Lab'
    ).


% Lecture subjects can use normal rooms
valid_lab_room(lecture, _).


% General subject validation
valid_subject(
    subject(Name, Lecturer, Room, Type, Time)
) :-
    Name \= '',
    Lecturer \= '',
    Room \= '',
    Time \= '',
    valid_lab_room(Type, Room).


% Example query
%
% ?-
% valid_subject(
%     subject(
%         ai,
%         dr_ali,
%         'Computer Lab 1',
%         lab,
%         monday_8am
%     )
% ).
%
% Expected: true.