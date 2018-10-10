import os
from collections import OrderedDict
import pandas as pd
import arrow


def get_times(log_file, out_path):
    times = pd.read_csv(log_file)
    # 离开时间减去进入时间
    times.fillna("雷锋", inplace=True)

    times["离开时间"] = pd.to_datetime(times["离开时间"])
    times["进入时间"] = pd.to_datetime(times["进入时间"])

    # times["在岗时间"] = times["离开时间"] - times["进入时间"]

    def get_second(df):
        diff = arrow.get(df["离开时间"]) - arrow.get(df['进入时间'])
        return diff.seconds

    def get_timedelta(second):
        return "{:.2f}小时| {:.2f}分钟 | {}秒".format(second/3600, second/60, second)

    times["在岗秒数"] = times.apply(get_second, axis=1)

    # 删去无用列
    times.drop(labels=["卡号", "学号", "学院", "备注", "进入时间"], inplace=True, axis=1)

    group = times.groupby("姓名")
    worktime = group['在岗秒数'].apply(list).to_dict()
    worktime = {person: sum(worktime[person]) for person in worktime}
    # sort
    worktime = OrderedDict(sorted(worktime.items(), key=lambda x:x[1], reverse=True))
    # to timedelta
    worktime = {person: get_timedelta(worktime[person]) for person in worktime}
    # print(group)
    names = [name for name in worktime]
    working = [worktime[person] for person in worktime]
    out_filename = os.path.join(out_path, arrow.now(tz="Asia/Shanghai").format("YYYYMMDD-HHmmss"))
    out_filename += ".xls"
    pd.DataFrame(columns=["姓名", "在岗时间"], data={"姓名": names, "在岗时间": working}).to_excel("{}".format(out_filename))
    return out_filename

if __name__ == "__main__":
    filename = 'data/visitors-stat-2018-10-9.csv'
    out_path = "download/"

    times = get_times(filename, out_path)

