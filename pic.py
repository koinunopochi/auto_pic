import pyautogui
import keyboard
import os
import tkinter as tk
import json
import traceback

class AutoScreenShot:
    def __init__(self):
        self.baseGround = None
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def get_pos(self):
        while True:
            if keyboard.is_pressed(self.config["default_save_position_key"]):
                x, y = pyautogui.position()
                print(f"{x}:{y}")
                break
        print('座標を取得しました')
        return x, y

    def get_screenshot(
            self, name, path, key, start_num, finish_num, left_x, left_y, right_x, right_y, btn_x, btn_y):
        try:
            os.makedirs(path, exist_ok=True)
            right_x = right_x - left_x
            right_y = right_y - left_y
            for i in range(start_num, finish_num):
                screenshot = pyautogui.screenshot(region=(left_x, left_y, right_x, right_y))
                filename = f"{name}_{i}.png"
                filepath = os.path.join(path, filename)
                screenshot.save(filepath)
                if btn_x != "" and btn_y != "":
                  pyautogui.click(x=btn_x, y=btn_y, duration=1)
                print(filepath)
                if keyboard.is_pressed(key):
                    print('プログラムが終了されました')
                    return
        except KeyboardInterrupt:
            print('終了')
            traceback.print_exc()
        except NotADirectoryError:
            print(f"[WinError 267] ディレクトリ名が無効です。:'{path}'")
            traceback.print_exc()
        except OSError:
            print(f"[WinError 123] ファイル名、ディレクトリ名、またはボリューム ラベルの構文が間違っています。:'{path}'")
            traceback.print_exc()
        except ValueError:
            print(f"keyの値が不正です。値を確認してください。")
            traceback.print_exc()
        except Exception as e:
            print(f"予期せぬエラーが発生しました。エラー発生状況とエラー内容をご連絡ください。")
            traceback.print_exc()

    def set_pos(self, x_name, y_name):
        x, y = self.get_pos()
        x_name.delete(0, "end")
        y_name.delete(0, "end")
        x_name.insert(0, x)
        y_name.insert(0, y)
        self.baseGround.deiconify()

    def btn_start(self, name, path, key, start_num, finish_num, left_x, left_y, right_x, right_y, btn_x, btn_y):
        try:
          l_x, l_y, r_x, r_y = map(int, (left_x.get(), left_y.get(), right_x.get(), right_y.get()))
          btn_x, btn_y = btn_x.get(), btn_y.get()
          if btn_x != "" and btn_y != "":
            btn_x, btn_y = map(int, (btn_x, btn_y))
          s, f = map(int, (start_num.get(), finish_num.get()))
          name, path, key = map(str, (name.get(), path.get(), key.get()))
          if name == "" or path == "" or key == "":
            raise ValueError("name, path, keyのいずれかが空です")
        except ValueError:
          traceback.print_exc()
          return

        print(l_x, l_y, r_x, r_y)
        print(btn_x, btn_y)
        self.baseGround.withdraw()
        self.get_screenshot(name, path, key, s, f, l_x, l_y, r_x, r_y, btn_x, btn_y)
        self.baseGround.deiconify()

    def create_label_text(self, parent, text):
        label = tk.Label(parent, text=text)
        label.pack()

    def create_entry(self, parent):
        entry = tk.Entry(parent)
        entry.pack()
        return entry

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command)
        button.pack()

    def window(self):
        self.baseGround = tk.Tk()
        self.baseGround.geometry(self.config["default_window_size"])
        self.baseGround.title(self.config["default_window_title"])

        self.create_label_text(self.baseGround, 'start_num')
        start_num = self.create_entry(self.baseGround)
        start_num.insert(tk.END, self.config["default_start_num"])

        self.create_label_text(self.baseGround, 'finish_num')
        finish_num = self.create_entry(self.baseGround)
        finish_num.insert(tk.END, self.config["default_finish_num"])

        self.create_label_text(self.baseGround, 'name')
        name = self.create_entry(self.baseGround)
        name.insert(tk.END, self.config["default_save_name"])

        self.create_label_text(self.baseGround, 'path')
        path = self.create_entry(self.baseGround)
        path.insert(tk.END, self.config["default_save_path"])

        self.create_label_text(self.baseGround, 'key')
        key = self.create_entry(self.baseGround)
        key.insert(tk.END, self.config["default_stop_key"])

        self.create_label_text(self.baseGround, '左上')
        left_x = self.create_entry(self.baseGround)
        left_x.insert(tk.END, self.config["default_position_top_x"])
        left_y = self.create_entry(self.baseGround)
        left_y.insert(tk.END, self.config["default_position_top_y"])
        self.create_button(self.baseGround, '取得', lambda: self.set_pos(left_x, left_y))

        self.create_label_text(self.baseGround, '右下')
        right_x = self.create_entry(self.baseGround)
        right_x.insert(tk.END, self.config["default_position_bottom_x"])
        right_y = self.create_entry(self.baseGround)
        right_y.insert(tk.END, self.config["default_position_bottom_y"])
        self.create_button(self.baseGround, '取得', lambda: self.set_pos(right_x, right_y))

        self.create_label_text(self.baseGround, 'クリック位置')
        btn_x = self.create_entry(self.baseGround)
        btn_x.insert(tk.END, self.config["default_click_position_x"])
        btn_y = self.create_entry(self.baseGround)
        btn_y.insert(tk.END, self.config["default_click_position_y"])
        self.create_button(self.baseGround, '取得', lambda: self.set_pos(btn_x, btn_y))

        self.create_button(self.baseGround, '実行', lambda: self.btn_start(name, path, key, start_num, finish_num, left_x, left_y, right_x, right_y, btn_x, btn_y))

        self.baseGround.mainloop()

if __name__ == "__main__":
    app = AutoScreenShot()
    app.window()
