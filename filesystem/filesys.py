import sys
import os
from collections import defaultdict
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QListWidget, QListWidgetItem
)
from pathlib import Path

def find_duplicate_files_across_dirs(folder_paths):
    file_map = defaultdict(list)
    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                file_map[file].append(os.path.join(root, file))

    duplicates = {}
    for filename, paths in file_map.items():
        if len(paths) > 1:
            dirs = set(os.path.dirname(p) for p in paths)
            if len(dirs) > 1:
                duplicates[filename] = paths

    if duplicates:
        download_folder=Path.home() / "Downloads"
        output_path = download_folder / "duplicate_files.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for filename, paths in duplicates.items():
                f.write(f"ファイル名: {filename}:\n")
                for p in paths:
                    f.write(f"  {Path(p).as_posix()}\n")
                f.write("\n")
        return str(output_path)
    else:
        return None

class DuplicateCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("重複ファイルチェッカー")
        self.setGeometry(300, 300, 500, 400)

        self.layout = QVBoxLayout()

        self.info_label = QLabel("フォルダを追加してください（複数可）:")
        self.layout.addWidget(self.info_label)

        self.folder_list = QListWidget()
        self.layout.addWidget(self.folder_list)

        self.add_folder_btn = QPushButton("フォルダを追加")
        self.add_folder_btn.clicked.connect(self.add_folder)
        self.layout.addWidget(self.add_folder_btn)

        self.run_btn = QPushButton("重複ファイルを探す")
        self.run_btn.clicked.connect(self.run_duplicate_check)
        self.layout.addWidget(self.run_btn)

        self.setLayout(self.layout)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
        if folder:
            # 重複登録防止
            existing_folders = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
            if folder not in existing_folders:
                self.folder_list.addItem(folder)

    def run_duplicate_check(self):
        folders = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
        if not folders:
            QMessageBox.warning(self, "警告", "フォルダを1つ以上追加してください。")
            return

        result = find_duplicate_files_across_dirs(folders)
        if result:
            QMessageBox.information(self, "完了", f"重複ファイル名が「{result}」に保存されました。")
        else:
            QMessageBox.information(self, "完了", "重複ファイル名は見つかりませんでした。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DuplicateCheckerApp()
    window.show()
    sys.exit(app.exec())