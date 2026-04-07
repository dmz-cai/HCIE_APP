"""
HCIE备考记账助手 V2.0
核心功能：记账、学习打卡、任务管理、数据可视化
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineListItem, ThreeLineListItem, OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.widget import MDWidget
from kivymd.uix.tab import MDTabs
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.spinner import MDSpinner
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.clock import Clock
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import math

# ================== 数据存储 ==================
DATA_FILE = "hcie_tracker_v2.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return get_default_data()
    return get_default_data()

def get_default_data():
    return {
        "expenses": [],
        "study_logs": [],
        "tasks": [],
        "budgets": {},
        "accounts": {"现金": 0, "储蓄卡": 0, "信用卡": 0, "花呗": 0},
        "goals": [],
        "settings": {"theme": "Light", "currency": "CNY"}
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ================== 绘图组件 ==================
class PieChart(MDFloatLayout):
    def __init__(self, data_dict, size_hint=(None, None), size=(200, 200), **kwargs):
        super().__init__(size_hint=size_hint, size=size, **kwargs)
        self.data_dict = data_dict
        self.bind(pos=self.draw, size=self.draw)
        
    def draw(self, *args):
        self.canvas.clear()
        if not self.data_dict:
            return
            
        total = sum(self.data_dict.values())
        if total == 0:
            return
            
        cx = self.center_x
        cy = self.center_y
        radius = min(self.width, self.height) / 2 - 20
        
        colors = [
            (0.2, 0.6, 0.9, 1),   # 蓝
            (0.9, 0.4, 0.4, 1),   # 红
            (0.4, 0.8, 0.4, 1),   # 绿
            (0.9, 0.7, 0.2, 1),   # 黄
            (0.6, 0.4, 0.8, 1),   # 紫
            (0.9, 0.5, 0.7, 1),   # 粉
        ]
        
        angle_start = 0
        with self.canvas:
            for i, (name, value) in enumerate(self.data_dict.items()):
                if value <= 0:
                    continue
                angle_end = angle_start + (value / total) * 360
                Color(*colors[i % len(colors)])
                Line(circle=(cx, cy, radius, angle_start, angle_end), width=3)
                angle_start = angle_end

class ProgressCircle(MDFloatLayout):
    def __init__(self, progress=0, text="", size_hint=(None, None), size=(80, 80), **kwargs):
        super().__init__(size_hint=size_hint, size=size, **kwargs)
        self.progress = progress
        self.text = text
        self.bind(pos=self.draw, size=self.draw)
        
    def draw(self, *args):
        self.canvas.clear()
        cx = self.center_x
        cy = self.center_y
        radius = min(self.width, self.height) / 2 - 5
        
        with self.canvas:
            # 背景圆
            Color(0.9, 0.9, 0.9, 1)
            Line(circle=(cx, cy, radius, 0, 360), width=6)
            
            # 进度圆
            Color(0.2, 0.6, 0.9, 1)
            if self.progress > 0:
                Line(circle=(cx, cy, radius, 90, 90 + self.progress * 3.6), width=6)

# ================== 首页仪表盘 ==================
class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = load_data()
        self.build_ui()
        
    def build_ui(self):
        self.layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10)
        
        # 顶部栏
        top_bar = MDTopAppBar(
            title="HCIE 备考助手 V2.0",
            md_bg_color=(0.13, 0.38, 0.72, 1),
            specific_text_color=(1, 1, 1, 1),
            right_action_items=[["refresh", lambda x: self.refresh()]]
        )
        self.layout.add_widget(top_bar)
        
        # 统计卡片区
        self.stats_card = self.build_stats_card()
        self.layout.add_widget(self.stats_card)
        
        # 本月概览
        self.monthly_card = self.build_monthly_overview()
        self.layout.add_widget(self.monthly_card)
        
        # 快捷操作按钮
        self.quick_actions = self.build_quick_actions()
        self.layout.add_widget(self.quick_actions)
        
        # 最近记录
        self.recent_card = self.build_recent_records()
        self.layout.add_widget(self.recent_card)
        
        self.scroll = MDScrollView()
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
        
        # 悬浮按钮
        self.fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            md_bg_color=(0.13, 0.38, 0.72, 1),
            on_press=self.show_quick_add
        )
        self.add_widget(self.fab)
        
    def build_stats_card(self):
        card = MDCard(padding=15, size_hint_y=None, height=120, md_bg_color=(0.95, 0.96, 0.98, 1))
        content = MDBoxLayout(orientation="horizontal", spacing=20)
        
        # 总支出
        total_expense = sum(e["amount"] for e in self.data["expenses"])
        expense_box = MDBoxLayout(orientation="vertical", size_hint_x=0.33)
        expense_box.add_widget(MDLabel(text="💰 总支出", font_size=12, halign="center"))
        expense_box.add_widget(MDLabel(text=f"¥{total_expense:.0f}", font_size=24, halign="center", theme_text_color="Primary"))
        content.add_widget(expense_box)
        
        # 总学习时长
        total_study = sum(s["duration"] for s in self.data["study_logs"])
        study_box = MDBoxLayout(orientation="vertical", size_hint_x=0.33)
        study_box.add_widget(MDLabel(text="📚 学习时长", font_size=12, halign="center"))
        study_box.add_widget(MDLabel(text=f"{total_study:.1f}h", font_size=24, halign="center", theme_text_color="Primary"))
        content.add_widget(study_box)
        
        # 任务完成率
        total_tasks = len(self.data["tasks"])
        done_tasks = len([t for t in self.data["tasks"] if t.get("done", False)])
        task_box = MDBoxLayout(orientation="vertical", size_hint_x=0.33)
        task_box.add_widget(MDLabel(text="✅ 任务完成", font_size=12, halign="center"))
        task_box.add_widget(MDLabel(text=f"{done_tasks}/{total_tasks}", font_size=24, halign="center", theme_text_color="Primary"))
        content.add_widget(task_box)
        
        card.add_widget(content)
        return card
        
    def build_monthly_overview(self):
        card = MDCard(padding=15, size_hint_y=None, height=180, md_bg_color=(1, 1, 1, 1))
        content = MDBoxLayout(orientation="vertical", spacing=10)
        content.add_widget(MDLabel(text="📊 本月概览", font_size=16, theme_text_color="Primary"))
        
        # 计算本月数据
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0)
        
        month_expenses = defaultdict(float)
        month_study = defaultdict(float)
        
        for e in self.data["expenses"]:
            try:
                date = datetime.strptime(e["date"], "%Y-%m-%d %H:%M")
                if date >= month_start:
                    month_expenses[e["category"]] += e["amount"]
            except:
                pass
                
        for s in self.data["study_logs"]:
            try:
                date = datetime.strptime(s["date"], "%Y-%m-%d %H:%M")
                if date >= month_start:
                    month_study[s["topic"]] += s["duration"]
            except:
                pass
        
        # 显示消费结构
        grid = MDGridLayout(cols=2, spacing=10)
        if month_expenses:
            top_category = max(month_expenses.items(), key=lambda x: x[1])
            grid.add_widget(MDLabel(text=f"最大支出: {top_category[0]}", font_size=12))
            grid.add_widget(MDLabel(text=f"¥{top_category[1]:.0f}", font_size=12, halign="right"))
        else:
            grid.add_widget(MDLabel(text="暂无消费记录", font_size=12))
            grid.add_widget(MDLabel(text="", font_size=12))
            
        if month_study:
            top_topic = max(month_study.items(), key=lambda x: x[1])
            grid.add_widget(MDLabel(text=f"最学主题: {top_topic[0]}", font_size=12))
            grid.add_widget(MDLabel(text=f"{top_topic[1]:.1f}h", font_size=12, halign="right"))
        else:
            grid.add_widget(MDLabel(text="暂无学习记录", font_size=12))
            grid.add_widget(MDLabel(text="", font_size=12))
            
        content.add_widget(grid)
        card.add_widget(content)
        return card
        
    def build_quick_actions(self):
        card = MDCard(padding=10, size_hint_y=None, height=80, md_bg_color=(0.95, 0.96, 0.98, 1))
        content = MDBoxLayout(orientation="horizontal", spacing=10)
        
        actions = [
            ("💰", "记账", self.show_expense),
            ("📚", "学习", self.show_study),
            ("✅", "任务", self.show_tasks),
            ("📊", "统计", self.show_stats),
        ]
        
        for icon, text, callback in actions:
            btn = MDRaisedButton(
                text=f"{icon} {text}",
                size_hint_x=0.25,
                font_size=12,
                on_press=callback,
                md_bg_color=(0.13, 0.38, 0.72, 1)
            )
            content.add_widget(btn)
            
        card.add_widget(content)
        return card
        
    def build_recent_records(self):
        card = MDCard(padding=15, size_hint_y=None, height=200, md_bg_color=(1, 1, 1, 1))
        content = MDBoxLayout(orientation="vertical", spacing=5)
        content.add_widget(MDLabel(text="📝 最近记录", font_size=16, theme_text_color="Primary"))
        
        # 最近5条记录
        all_records = []
        for e in self.data["expenses"][-5:]:
            all_records.append(("expense", e["date"], f"{e['category']} -¥{e['amount']}"))
        for s in self.data["study_logs"][-5:]:
            all_records.append(("study", s["date"], f"{s['topic']} - {s['duration']}h"))
            
        all_records.sort(key=lambda x: x[1], reverse=True)
        
        for r in all_records[:5]:
            icon = "💰" if r[0] == "expense" else "📚"
            content.add_widget(MDLabel(text=f"{icon} {r[2]}", font_size=12))
            
        card.add_widget(content)
        return card
        
    def show_quick_add(self, *args):
        """快速添加入口"""
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        layout.add_widget(MDLabel(text="选择记录类型", font_size=16, halign="center"))
        
        btns = [
            ("💰 记一笔消费", self.show_expense),
            ("📚 记录学习", self.show_study),
            ("✅ 添加任务", self.show_tasks),
            ("🎯 设定目标", self.show_goals),
        ]
        
        for text, callback in btns:
            layout.add_widget(MDRaisedButton(text=text, on_press=lambda x, c=callback: c(), size_hint_y=None, height=50))
            
        self.dialog = MDDialog(title="快速记录", type="custom", content_cls=layout)
        self.dialog.open()
        
    def show_expense(self, *args):
        categories = ["餐饮", "交通", "房租", "学习", "娱乐", "其他"]
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        
        self.expense_cat = MDTextField(hint_text=f"类别 (1-6: {', '.join(categories)})", input_filter="int")
        self.expense_amount = MDTextField(hint_text="金额", input_filter="float")
        self.expense_note = MDTextField(hint_text="备注")
        
        layout.add_widget(self.expense_cat)
        layout.add_widget(self.expense_amount)
        layout.add_widget(self.expense_note)
        
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="💰 记一笔",
            type="custom",
            content_cls=layout,
            buttons=[MDRaisedButton(text="保存", on_press=self.save_expense)]
        )
        self.dialog.open()
        
    def save_expense(self, *args):
        try:
            categories = ["餐饮", "交通", "房租", "学习", "娱乐", "其他"]
            cat_idx = int(self.expense_cat.text.strip()) - 1
            category = categories[cat_idx] if 0 <= cat_idx < 6 else "其他"
            amount = float(self.expense_amount.text.strip())
            note = self.expense_note.text.strip()
            
            self.data["expenses"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": category,
                "amount": amount,
                "note": note
            })
            save_data(self.data)
            self.dialog.dismiss()
            self.refresh()
        except Exception as e:
            print(f"Error: {e}")
            
    def show_study(self, *args):
        topics = ["HCIA", "eNSP", "路由", "交换", "安全", "刷题"]
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        
        self.study_topic = MDTextField(hint_text=f"主题 (1-6: {', '.join(topics)})", input_filter="int")
        self.study_duration = MDTextField(hint_text="时长(小时)", input_filter="float")
        self.study_note = MDTextField(hint_text="收获")
        
        layout.add_widget(self.study_topic)
        layout.add_widget(self.study_duration)
        layout.add_widget(self.study_note)
        
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="📚 学习打卡",
            type="custom",
            content_cls=layout,
            buttons=[MDRaisedButton(text="保存", on_press=self.save_study)]
        )
        self.dialog.open()
        
    def save_study(self, *args):
        try:
            topics = ["HCIA", "eNSP", "路由", "交换", "安全", "刷题"]
            topic_idx = int(self.study_topic.text.strip()) - 1
            topic = topics[topic_idx] if 0 <= topic_idx < 6 else "其他"
            duration = float(self.study_duration.text.strip())
            note = self.study_note.text.strip()
            
            self.data["study_logs"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "topic": topic,
                "duration": duration,
                "note": note
            })
            save_data(self.data)
            self.dialog.dismiss()
            self.refresh()
        except Exception as e:
            print(f"Error: {e}")
            
    def show_tasks(self, *args):
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        layout.height = 400
        
        self.task_title = MDTextField(hint_text="任务名称")
        self.task_desc = MDTextField(hint_text="描述")
        layout.add_widget(self.task_title)
        layout.add_widget(self.task_desc)
        layout.add_widget(MDRaisedButton(text="添加任务", on_press=self.add_task))
        
        # 任务列表
        self.task_list = MDList()
        for i, t in enumerate(self.data["tasks"]):
            icon = "✅" if t.get("done") else "⬜"
            item = TwoLineListItem(
                text=f"{icon} {t['title']}",
                secondary_text=t.get("desc", ""),
                on_press=lambda x, idx=i: self.toggle_task(idx)
            )
            self.task_list.add_widget(item)
            
        scroll = MDScrollView()
        scroll.add_widget(self.task_list)
        layout.add_widget(scroll)
        
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(title="✅ 任务管理", type="custom", content_cls=layout, size_hint=(0.9, 0.8))
        self.dialog.open()
        
    def add_task(self, *args):
        title = self.task_title.text.strip()
        if title:
            self.data["tasks"].append({
                "title": title,
                "desc": self.task_desc.text.strip(),
                "done": False,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_data(self.data)
            self.dialog.dismiss()
            self.show_tasks()
            
    def toggle_task(self, idx):
        self.data["tasks"][idx]["done"] = not self.data["tasks"][idx]["done"]
        save_data(self.data)
        self.dialog.dismiss()
        self.show_tasks()
        self.refresh()
        
    def show_stats(self, *args):
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        layout.height = 500
        
        # 统计数据
        total_expense = sum(e["amount"] for e in self.data["expenses"])
        total_study = sum(s["duration"] for s in self.data["study_logs"])
        total_tasks = len(self.data["tasks"])
        done_tasks = len([t for t in self.data["tasks"] if t.get("done")])
        
        layout.add_widget(MDLabel(text=f"💰 总支出: ¥{total_expense:.2f}", font_size=16))
        layout.add_widget(MDLabel(text=f"📚 总学习: {total_study:.1f} 小时", font_size=16))
        layout.add_widget(MDLabel(text=f"✅ 任务: {done_tasks}/{total_tasks} 完成", font_size=16))
        
        # 分类统计
        layout.add_widget(MDLabel(text="", size_hint_y=None, height=10))
        layout.add_widget(MDLabel(text="📊 消费分类", font_size=14, theme_text_color="Primary"))
        
        categories = defaultdict(float)
        for e in self.data["expenses"]:
            categories[e["category"]] += e["amount"]
        for cat, amount in sorted(categories.items(), key=lambda x: -x[1]):
            layout.add_widget(MDLabel(text=f"  {cat}: ¥{amount:.0f}", font_size=12))
            
        # 学习主题统计
        layout.add_widget(MDLabel(text="", size_hint_y=None, height=10))
        layout.add_widget(MDLabel(text="📚 学习主题", font_size=14, theme_text_color="Primary"))
        
        topics = defaultdict(float)
        for s in self.data["study_logs"]:
            topics[s["topic"]] += s["duration"]
        for topic, dur in sorted(topics.items(), key=lambda x: -x[1]):
            layout.add_widget(MDLabel(text=f"  {topic}: {dur:.1f}h", font_size=12))
        
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(title="📊 数据统计", type="custom", content_cls=layout, size_hint=(0.95, 0.85))
        self.dialog.open()
        
    def show_goals(self, *args):
        layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, size_hint_y=None)
        
        self.goal_title = MDTextField(hint_text="目标名称")
        self.goal_target = MDTextField(hint_text="目标值", input_filter="float")
        layout.add_widget(self.goal_title)
        layout.add_widget(self.goal_target)
        layout.add_widget(MDRaisedButton(text="添加目标", on_press=self.add_goal))
        
        for g in self.data.get("goals", []):
            layout.add_widget(MDLabel(text=f"🎯 {g['title']}: {g.get('current', 0)}/{g['target']}"))
        
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(title="🎯 目标设定", type="custom", content_cls=layout)
        self.dialog.open()
        
    def add_goal(self, *args):
        title = self.goal_title.text.strip()
        target = self.goal_target.text.strip()
        if title and target:
            self.data.setdefault("goals", []).append({
                "title": title,
                "target": float(target),
                "current": 0
            })
            save_data(self.data)
            self.dialog.dismiss()
            self.show_goals()
            
    def refresh(self):
        self.clear_widgets()
        self.data = load_data()
        self.build_ui()

# ================== APP 入口 ==================
class HCIETrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return DashboardScreen()

if __name__ == "__main__":
    HCIETrackerApp().run()
