from functools import wraps
from flask import request, redirect, session, render_template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def sorry(message, code=400):

    def escape(s):

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"), ("%", "~p"),
                         ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)

        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def calculate433(squad):
    a = 10
    b = 5
    c = 3  # 加点（適宜変更）
    add = 0
    for i in range(11):
        if i == 0:
            if "ST" in squad[i]["position"] or "LF" in squad[i]["position"] or "LW" in squad[i]["position"]:  # 左ウィング最適正
                add += a
            elif "CF" in squad[i]["position"] or "RF" in squad[i]["position"] or "RW" in squad[i]["position"]:  # 適正
                add += b
            elif "LM" in squad[i]["position"]:  # できる
                add += c

        elif i == 1:
            if "ST" in squad[i]["position"] or "CF" in squad[i]["position"]:  # センターフォワード
                add += a
            elif "LW" in squad[i]["position"] or "LF" in squad[i]["position"] or "RF" in squad[i]["position"] or "RW" in squad[i]["position"]:
                add += b
            elif "CAM" in squad[i]["position"]:
                add += c

        elif i == 2:
            if "ST" in squad[i]["position"] or "RF" in squad[i]["position"] or "RW" in squad[i]["position"]:  # 右ウィング
                add += a
            elif "LW" in squad[i]["position"] or "LF" in squad[i]["position"] or "CF" in squad[i]["position"]:
                add += b
            elif "RM" in squad[i]["position"]:
                add += c

        elif i == 3:
            if "LM" in squad[i]["position"]:  # 左ボランチ
                add += a
            elif "CAM" in squad[i]["position"] or "CM" in squad[i]["position"] or "CDM" in squad[i]["position"] or "RM" in squad[i]["position"]:
                add += b
            elif "LWB" in squad[i]["position"]:
                add += c

        elif i == 4:
            if "CAM" in squad[i]["position"] or "CM" in squad[i]["position"] or "CDM" in squad[i]["position"]:  # アンカー
                add += a
            elif "LM" in squad[i]["position"] or "RM" in squad[i]["position"]:
                add += b
            elif "CB" in squad[i]["position"]:
                add += c

        elif i == 5:
            if "RM" in squad[i]["position"]:  # 右ボランチ
                add += a
            elif "LM" in squad[i]["position"] or "CAM" in squad[i]["position"] or "CM" in squad[i]["position"] or "CDM" in squad[i]["position"]:
                add += b
            elif "RWB" in squad[i]["position"]:
                add += c

        elif i == 6:
            if "LWB" in squad[i]["position"] or "LB" in squad[i]["position"]:  # 左サイドバック
                add += a
            elif "CB" in squad[i]["position"] or "RB" in squad[i]["position"] or "RWB" in squad[i]["position"]:
                add += b
            elif "LM" in squad[i]["position"]:
                add += c

        elif i == 7:
            if "LB" in squad[i]["position"] or "CB" in squad[i]["position"]:  # 左センターバック
                add += a
            elif "LWB" in squad[i]["position"] or "RB" in squad[i]["position"] or "RWB" in squad[i]["position"]:
                add += b
            elif "CDM" in squad[i]["position"]:
                add += c

        elif i == 8:
            if "RB" in squad[i]["position"] or "CB" in squad[i]["position"]:  # 右センターバック
                add += a
            elif "LWB" in squad[i]["position"] or "LB" in squad[i]["position"] or "RWB" in squad[i]["position"]:
                add += b
            elif "CDM" in squad[i]["position"]:
                add += c

        elif i == 9:
            if "RWB" in squad[i]["position"] or "RB" in squad[i]["position"]:  # 右サイドバック
                add += a
            elif "LWB" in squad[i]["position"] or "LB" in squad[i]["position"] or "CB" in squad[i]["position"]:
                add += b
            elif "RM" in squad[i]["position"]:
                add += c

        elif i == 10:
            if "GK" in squad[i]["position"]:  # ゴールキーパー
                add += (a * 2)

    return add
