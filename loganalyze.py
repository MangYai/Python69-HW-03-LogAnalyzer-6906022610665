from collections import Counter
import os

def _is_valid_timestamp(timestamp_str):
    if len(timestamp_str) != 19:
        return False
    if timestamp_str[4] != "-" or timestamp_str[7] != "-":
        return False
    if timestamp_str[10] != "T":
        return False
    if timestamp_str[13] != ":" or timestamp_str[16] != ":":
        return False

    date_part = timestamp_str[0:4] + timestamp_str[5:7] + timestamp_str[8:10]
    time_part = timestamp_str[11:13] + timestamp_str[14:16] + timestamp_str[17:19]
    return date_part.isdigit() and time_part.isdigit()


def _is_valid_duration(duration_str):
    if duration_str.startswith("-"):
        duration_str = duration_str[1:]
    return duration_str.isdigit()


def analyze_user_activity(log_file_path: str) -> dict:
    if not os.path.exists(log_file_path):
        return {
            "total_users": 0,
            "action_counts": {},
            "most_active_user": None,
            "average_session_time": 0.0,
        }

    action_counts = Counter()
    user_action_counts = Counter()
    login_durations = []
    unique_users = set()

    with open(log_file_path, "r", encoding="utf-8") as log_file:
        for raw_line in log_file:
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 4:
                continue

            timestamp_str, user_id, action, duration_str = parts

            if not _is_valid_timestamp(timestamp_str):
                continue

            if not user_id or not action:
                continue

            if not _is_valid_duration(duration_str):
                continue

            duration = int(duration_str)

            unique_users.add(user_id)
            action_counts[action] += 1
            user_action_counts[user_id] += 1

            if action == "login":
                login_durations.append(duration)

    total_users = len(unique_users)

    most_active_user = None
    if user_action_counts:
        highest_action_count = max(user_action_counts.values())
        top_users = sorted(
            user_id
            for user_id, count in user_action_counts.items()
            if count == highest_action_count
        )
        most_active_user = top_users[0]

    average_session_time = 0.0
    if login_durations:
        average_session_time = sum(login_durations) / len(login_durations)

    return {
        "total_users": total_users,
        "action_counts": dict(action_counts),
        "most_active_user": most_active_user,
        "average_session_time": average_session_time,
    }


if __name__ == "__main__":
    result = analyze_user_activity("activity.log")
    from pprint import pprint
    pprint(result)

# {'action_counts': {'login': 2, 'logout': 2, 'submit': 1, 'view': 2},
#  'average_session_time': 160.0,
#  'most_active_user': 'u002',
#  'total_users': 2}