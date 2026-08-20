#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git GUI — графический интерфейс для Git
Простое приложение на Tkinter для управления Git-репозиторием.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import shutil


class GitGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐙 Git GUI")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.repo_path = tk.StringVar(value=os.path.expanduser("~"))

        self._build_ui()

    # ==================== СТРОКА С ПУТЁМ ====================
    def _build_ui(self):
        # --- Панель выбора папки ---
        path_frame = tk.Frame(self.root)
        path_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(path_frame, text="📁 Репозиторий:", font=("Segoe UI", 11)).pack(side=tk.LEFT)
        tk.Entry(path_frame, textvariable=self.repo_path, font=("Segoe UI", 11)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(path_frame, text="Обзор", font=("Segoe UI", 10), command=self._browse_folder).pack(side=tk.LEFT)
        tk.Button(path_frame, text="🔄 Обновить", font=("Segoe UI", 10), command=self._refresh_all).pack(side=tk.LEFT, padx=(5, 0))

        # --- Панель кнопок действий ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="➕ git add .", font=("Segoe UI", 10), bg="#4CAF50", fg="white",
                command=self._git_add_all).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="✅ git commit", font=("Segoe UI", 10), bg="#2196F3", fg="white",
                command=self._git_commit_dialog).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🚀 git push", font=("Segoe UI", 10), bg="#FF9800", fg="white",
                command=self._git_push).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="📜 git log", font=("Segoe UI", 10), bg="#9C27B0", fg="white",
                command=self._git_log).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="🔧 git init", font=("Segoe UI", 10), bg="#607D8B", fg="white",
                command=self._git_init).pack(side=tk.LEFT, padx=2)

        # --- Статус репозитория ---
        status_frame = tk.LabelFrame(self.root, text="📊 Статус (git status)", font=("Segoe UI", 11, "bold"))
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.status_text = tk.Text(status_frame, font=("Consolas", 10), wrap=tk.WORD,
                                   bg="#f5f5f5", state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=scrollbar.set)

        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- История коммитов ---
        log_frame = tk.LabelFrame(self.root, text="📜 История коммитов (git log --oneline)", font=("Segoe UI", 11, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, font=("Consolas", 10), wrap=tk.WORD,
                                bg="#f5f5f5", height=8, state=tk.DISABLED)
        log_scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=log_scroll.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Консоль вывода ---
        console_frame = tk.LabelFrame(self.root, text="💻 Консоль", font=("Segoe UI", 11, "bold"))
        console_frame.pack(fill=tk.X, padx=10, pady=5)

        self.console_text = tk.Text(console_frame, font=("Consolas", 9), wrap=tk.WORD,
                                    bg="#1e1e1e", fg="#d4d4d4", height=6, state=tk.DISABLED)
        console_scroll = ttk.Scrollbar(console_frame, command=self.console_text.yview)
        self.console_text.config(yscrollcommand=console_scroll.set)

        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Строка состояния ---
        self.statusbar = tk.Label(self.root, text="Готово. Выберите папку с Git-репоиторием.",
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Segoe UI", 9))
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Автообновление при запуске
        self._refresh_all()

    # ==================== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ====================
    def _log(self, message, tag="info"):
        """Выводит сообщение в консоль приложения."""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, message + "\n", tag)
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)

    def _run_git(self, args):
        """Выполняет git-команду и возвращает (stdout, stderr, returncode)."""
        path = self.repo_path.get()
        if not os.path.isdir(path):
            return "", f"Папка не найдена: {path}", 1

        # Проверяем, что git установлен
        if not shutil.which("git"):
            return "", "Git не найден! Установите: sudo apt install git", 1

        try:
            result = subprocess.run(
                ["git", "-C", path] + args,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1

    def _is_git_repo(self):
        """Проверяет, является ли папка Git-репозиторием."""
        path = self.repo_path.get()
        git_dir = os.path.join(path, ".git")
        return os.path.isdir(git_dir)

    def _set_text(self, widget, text):
        """Безопасно устанавливает текст в Text-виджет."""
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state=tk.DISABLED)

    # ==================== ДЕЙСТВИЯ ====================
    def _browse_folder(self):
        """Диалог выбора папки."""
        folder = filedialog.askdirectory(initialdir=self.repo_path.get())
        if folder:
            self.repo_path.set(folder)
            self._refresh_all()

    def _refresh_all(self):
        """Обновляет статус и лог."""
        self._refresh_status()
        self._refresh_log()

    def _refresh_status(self):
        """Обновляет git status."""
        if not self._is_git_repo():
            self._set_text(self.status_text, "⚠️  Это не Git-репозиторий.\n\nНажмите \"🔧 git init\", чтобы создать репозиторий.")
            self.statusbar.config(text="Не Git-репозиторий")
            return

        stdout, stderr, rc = self._run_git(["status"])
        if rc != 0:
            self._set_text(self.status_text, f"❌ Ошибка:\n{stderr}")
            self.statusbar.config(text="Ошибка при получении статуса")
            return

        self._set_text(self.status_text, stdout)
        self.statusbar.config(text=f"✅ Репозиторий: {self.repo_path.get()}")

    def _refresh_log(self):
        """Обновляет git log --oneline."""
        if not self._is_git_repo():
            self._set_text(self.log_text, "Нет истории — репозиторий не инициализирован.")
            return

        stdout, stderr, rc = self._run_git(["log", "--oneline", "--graph", "--decorate", "-20"])
        if rc != 0 or not stdout.strip():
            self._set_text(self.log_text, "Нет коммитов. Сделайте первый коммит!")
            return

        self._set_text(self.log_text, stdout)

    def _git_init(self):
        """Инициализирует Git-репозиторий."""
        path = self.repo_path.get()
        if self._is_git_repo():
            messagebox.showinfo("Информация", "Эта папка уже является Git-репозиторием!")
            return

        stdout, stderr, rc = self._run_git(["init"])
        if rc != 0:
            messagebox.showerror("Ошибка", f"Не удалось инициализировать:\n{stderr}")
            self._log(f"❌ git init failed: {stderr}")
            return

        messagebox.showinfo("Успех", f"✅ Git-репозиторий создан!\n\n{stdout}")
        self._log(f"✅ git init: {stdout}")
        self._refresh_all()

    def _git_add_all(self):
        """Добавляет все изменения (git add .)."""
        if not self._is_git_repo():
            messagebox.showwarning("Внимание", "Сначала инициализируйте репозиторий (🔧 git init)")
            return

        stdout, stderr, rc = self._run_git(["add", "."])
        if rc != 0:
            messagebox.showerror("Ошибка", f"git add failed:\n{stderr}")
            self._log(f"❌ git add . failed: {stderr}")
            return

        self._log("✅ git add . — выполнено")
        self._refresh_status()
        messagebox.showinfo("Успех", "✅ Все изменённые файлы добавлены в зону сохранения (staging).\n\nТеперь сделайте коммит!")

    def _git_commit_dialog(self):
        """Диалог для ввода сообщения коммита."""
        if not self._is_git_repo():
            messagebox.showwarning("Внимание", "Сначала инициализируйте репозиторий (🔧 git init)")
            return

        # Проверим, есть ли что коммитить
        stdout, stderr, rc = self._run_git(["diff", "--cached", "--quiet"])
        # rc=1 значит есть изменения в staging, rc=0 значит нет
        stdout2, stderr2, rc2 = self._run_git(["diff", "--quiet"])
        # rc2=1 значит есть незакоммиченные изменения

        has_staged = (rc == 1)
        has_unstaged = (rc2 == 1)

        if not has_staged and not has_unstaged:
            messagebox.showinfo("Информация", "Нет изменений для коммита.")
            return

        # Диалоговое окно для сообщения
        dialog = tk.Toplevel(self.root)
        dialog.title("✅ git commit")
        dialog.geometry("450x200")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)

        tk.Label(dialog, text="Сообщение коммита:", font=("Segoe UI", 11)).pack(pady=(15, 5))

        entry = tk.Entry(dialog, font=("Segoe UI", 11), width=45)
        entry.pack(padx=20, pady=5)
        entry.focus()

        # Подсказка
        hint = tk.Label(dialog, text="Пример: \"Добавлена кнопка сохранения\"",
                        font=("Segoe UI", 9), fg="gray")
        hint.pack()

        def do_commit():
            msg = entry.get().strip()
            if not msg:
                messagebox.showwarning("Внимание", "Введите сообщение коммита!")
                return

            stdout, stderr, rc = self._run_git(["commit", "-m", msg])
            if rc != 0:
                # Может быть ошибка "nothing to commit" или другая
                messagebox.showerror("Ошибка", f"git commit failed:\n{stderr}")
                self._log(f"❌ git commit failed: {stderr}")
            else:
                messagebox.showinfo("Успех", f"✅ Коммит создан!\n\n{stdout}")
                self._log(f"✅ git commit -m \"{msg}\":\n{stdout}")
                self._refresh_all()
                dialog.destroy()

        tk.Button(dialog, text="Закоммитить", font=("Segoe UI", 11),
                  bg="#2196F3", fg="white", command=do_commit).pack(pady=15)

        # Enter = коммит
        entry.bind("<Return>", lambda e: do_commit())

    def _git_push(self):
        """Отправляет коммиты на удалённый репозиторий."""
        if not self._is_git_repo():
            messagebox.showwarning("Внимание", "Сначала инициализируйте репозиторий (🔧 git init)")
            return

        # Проверим, есть ли remote
        stdout, stderr, rc = self._run_git(["remote"])
        if rc != 0 or not stdout.strip():
            messagebox.showwarning("Внимание",
                "Удалённый репозиторий не настроен.\n\n"
                "Сначала выполните в терминале:\n"
                "git remote add origin https://github.com/ВАШ_НИК/РЕПО.git")
            return

        remote = stdout.strip().split("\n")[0]
        self.statusbar.config(text=f"🚀 Отправка на {remote}...")
        self.root.update()

        stdout, stderr, rc = self._run_git(["push", remote, "HEAD"])

        self.statusbar.config(text="Готово")

        if rc != 0:
            # Иногда stderr содержит инфо, а не ошибку
            full = (stdout + "\n" + stderr).strip()
            messagebox.showerror("Ошибка push", f"git push failed:\n{full}")
            self._log(f"❌ git push failed:\n{full}")
        else:
            output = (stdout + "\n" + stderr).strip()
            messagebox.showinfo("Успех", f"✅ Код отправлен на GitHub!\n\n{output}")
            self._log(f"✅ git push:\n{output}")
            self._refresh_all()

    def _git_log(self):
        """Показывает расширенный git log."""
        if not self._is_git_repo():
            messagebox.showwarning("Внимание", "Сначала инициализируйте репозиторий (🔧 git init)")
            return

        stdout, stderr, rc = self._run_git([
            "log", "--oneline", "--graph", "--decorate",
            "--all", "-50"
        ])
        if rc != 0:
            messagebox.showerror("Ошибка", f"git log failed:\n{stderr}")
            return

        # Покажем в отдельном окне
        window = tk.Toplevel(self.root)
        window.title("📜 Git Log")
        window.geometry("700x500")

        text = tk.Text(window, font=("Consolas", 10), wrap=tk.WORD, bg="#f5f5f5")
        scroll = ttk.Scrollbar(window, command=text.yview)
        text.config(yscrollcommand=scroll.set)

        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        text.insert(tk.END, stdout if stdout else "Нет коммитов.")
        text.config(state=tk.DISABLED)


# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = GitGUIApp(root)
    root.mainloop()
