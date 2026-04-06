from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.widget import MDWidget
import json
import os
from datetime import datetime

DATA_FILE = "hcie_tracker_app.json"

# ================== 数据存储 ==================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"expenses": [], "study_logs": [], "tasks": []}
    return {"expenses": [], "study_logs": [], "tasks": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ================== 主界面 ==================
class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = load_data()
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation="vertical", spacing=12, padding=16)

        # 顶部栏
        top_bar = MDTopAppBar(
            title="HCIE 备考记账助手",
            md_bg_color=(0.1, 0.4, 0.8, 1),
            specific_text_color=(1, 1, 1, 1)
        )
        self.layout.add_widget(top_bar)
        self.layout.add_widget(MDWidget(size_hint_y=None, height=10))

        # 统计卡片
        total_cost = round(sum(e["amount"] for e in self.data["expenses"]), 2)
        total_study = round(sum(s["duration"] for s in self.data["study_logs"]), 1)
        total_task = len(self.data["tasks"])
        done_task = len([t for t in self.data["tasks"] if t["done"]])

        card = MDCard(
            padding=16,
            md_bg_color=(0.95, 0.95, 0.98, 1),
            size_hint_y=None,
            height=140
        )
        card_content = MDBoxLayout(orientation="vertical", spacing=4)
        card_content.add_widget(MDLabel(text=f"总支出：{total_cost} 元", font_size=16))
        card_content.add_widget(MDLabel(text=f"总学习：{total_study} 小时", font_size=16))
        card_content.add_widget(MDLabel(text=f"任务：{done_task}/{total_task} 已完成", font_size=16))
        card.add_widget(card_content)
        self.layout.add_widget(card)

        # 功能按钮
        btn_style = {"size_hint": (1, None), "height": 52, "font_size": 16}
        self.layout.add_widget(MDRaisedButton(text="💰 记录开销", on_press=self.show_expense, **btn_style))
        self.layout.add_widget(MDRaisedButton(text="🧠 学习打卡", on_press=self.show_study, **btn_style))
        self.layout.add_widget(MDRaisedButton(text="✅ 任务管理", on_press=self.show_tasks, **btn_style))
        self.layout.add_widget(MDRaisedButton(text="📊 数据统计", on_press=self.show_summary, **btn_style))
        self.layout.add_widget(MDRaisedButton(text="🚪 退出", on_press=self.exit_app, **btn_style))

        self.scroll = MDScrollView()
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)

    # ================== 记账 ==================
    def show_expense(self, *args):
        cate = ["餐饮伙食", "地铁通勤", "房租水电", "债务偿还", "HCIE备考基金", "其他"]
        layout = MDBoxLayout(orientation="vertical", spacing=12, padding=10, size_hint_y=None)
        self.cat_input = MDTextField(hint_text=f"类别序号 1~6：{cate}")
        self.amount_input = MDTextField(hint_text="金额（元）")
        self.note_input = MDTextField(hint_text="备注（可选）")
        layout.add_widget(self.cat_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.note_input)

        self.dialog = MDDialog(
            title="添加一笔支出",
            type="custom",
            content_cls=layout,
            buttons=[MDRaisedButton(text="保存", on_press=self.save_expense)]
        )
        self.dialog.open()

    def save_expense(self, *args):
        try:
            cate = ["餐饮伙食", "地铁通勤", "房租水电", "债务偿还", "HCIE备考基金", "其他"]
            c = int(self.cat_input.text.strip())
            category = cate[c-1] if 1 <= c <= 6 else "其他"
            amount = float(self.amount_input.text.strip())
            if amount <= 0: return
            note = self.note_input.text.strip()
            rec = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": category,
                "amount": amount,
                "note": note
            }
            self.data["expenses"].append(rec)
            save_data(self.data)
            self.dialog.dismiss()
            self.refresh()
        except:
            pass

    # ================== 学习打卡 ==================
    def show_study(self, *args):
        topics = ["HCIA基础", "eNSP实验", "安全策略", "跨厂商命令", "真题刷题", "其他"]
        layout = MDBoxLayout(orientation="vertical", spacing=12, padding=10, size_hint_y=None)
        self.topic_input = MDTextField(hint_text=f"内容序号 1~6：{topics}")
        self.dur_input = MDTextField(hint_text="学习时长（小时）")
        self.note2_input = MDTextField(hint_text="今日收获")
        layout.add_widget(self.topic_input)
        layout.add_widget(self.dur_input)
        layout.add_widget(self.note2_input)

        self.dialog = MDDialog(
            title="学习打卡",
            type="custom",
            content_cls=layout,
            buttons=[MDRaisedButton(text="保存", on_press=self.save_study)]
        )
        self.dialog.open()

    def save_study(self, *args):
        try:
            topics = ["HCIA基础", "eNSP实验", "安全策略", "跨厂商命令", "真题刷题", "其他"]
            c = int(self.topic_input.text.strip())
            topic = topics[c-1] if 1 <= c <= 6 else "其他"
            dur = float(self.dur_input.text.strip())
            if dur <= 0: return
            note = self.note2_input.text.strip()
            rec = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "topic": topic,
                "duration": dur,
                "note": note
            }
            self.data["study_logs"].append(rec)
            save_data(self.data)
            self.dialog.dismiss()
            self.refresh()
        except:
            pass

    # ================== 任务管理（行业打卡功能） ==================
    def show_tasks(self, *args):
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        self.task_title = MDTextField(hint_text="任务名称（如：OSPF 实验）")
        self.task_desc = MDTextField(hint_text="任务描述")
        layout.add_widget(self.task_title)
        layout.add_widget(self.task_desc)

        btn_add = MDRaisedButton(text="添加任务", on_press=self.add_task)
        self.task_list = MDList()

        for i, t in enumerate(self.data["tasks"]):
            icon = "check-circle" if t["done"] else "checkbox-blank-circle-outline"
            item = ThreeLineListItem(
                text=f"{i+1}. {t['title']}",
                secondary_text=t["desc"],
                tertiary_text=t["date"],
                leading_icon=icon
            )
            item.bind(on_press=lambda x, idx=i: self.finish_task(idx))
            item.bind(on_long_press=lambda x, idx=i: self.delete_task(idx))
            self.task_list.add_widget(item)

        scroll = MDScrollView()
        scroll.add_widget(self.task_list)
        layout.add_widget(btn_add)
        layout.add_widget(scroll)

        self.dialog = MDDialog(title="任务管理", type="custom", content_cls=layout, size_hint=(0.95, 0.8))
        self.dialog.open()

    def add_task(self, *args):
        title = self.task_title.text.strip()
        desc = self.task_desc.text.strip()
        if not title: return
        task = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title": title,
            "desc": desc,
            "done": False
        }
        self.data["tasks"].append(task)
        save_data(self.data)
        self.dialog.dismiss()
        self.refresh()

    def finish_task(self, idx):
        self.data["tasks"][idx]["done"] = not self.data["tasks"][idx]["done"]
        save_data(self.data)
        self.dialog.dismiss()
        self.refresh()

    def delete_task(self, idx):
        del self.data["tasks"][idx]
        save_data(self.data)
        self.dialog.dismiss()
        self.refresh()

    # ================== 数据统计 ==================
    def show_summary(self, *args):
        layout = MDBoxLayout(orientation="vertical", spacing=8, padding=10, size_hint_y=None)
        total_cost = round(sum(e["amount"] for e in self.data["expenses"]), 2)
        total_study = round(sum(s["duration"] for s in self.data["study_logs"]), 1)
        total_task = len(self.data["tasks"])
        done_task = len([t for t in self.data["tasks"] if t["done"]])

        layout.add_widget(MDLabel(text=f"总支出：{total_cost} 元", font_size=17))
        layout.add_widget(MDLabel(text=f"总学习时长：{total_study} 小时", font_size=17))
        layout.add_widget(MDLabel(text=f"任务完成：{done_task}/{total_task}", font_size=17))
        layout.add_widget(MDLabel(text="———— 最近记录 ————", font_size=14))

        scroll = MDScrollView()
        listw = MDList()
        for e in self.data["expenses"][-5:]:
            listw.add_widget(TwoLineListItem(text=f"{e['category']} {e['amount']}元", secondary_text=e['date']))
        for s in self.data["study_logs"][-5:]:
            listw.add_widget(TwoLineListItem(text=f"{s['topic']} {s['duration']}h", secondary_text=s['date']))
        scroll.add_widget(listw)
        layout.add_widget(scroll)

        self.dialog = MDDialog(title="数据统计", type="custom", content_cls=layout, size_hint=(0.95, 0.8))
        self.dialog.open()

    # ================== 工具 ==================
    def refresh(self):
        self.clear_widgets()
        self.data = load_data()
        self.build_ui()

    def exit_app(self, *args):
        MDApp.get_running_app().stop()

# ================== APP 入口 ==================
class HCIETrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return MainScreen()

if __name__ == "__main__":
    HCIETrackerApp().run()