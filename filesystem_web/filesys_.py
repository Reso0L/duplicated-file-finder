def find_duplicate_files_across_dirs(folder_paths):
    # key: ファイル名（拡張子込み）、value: ファイルのパスリスト
    file_map = defaultdict(list)

    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                file_map[file].append(os.path.join(root, file))

    # 複数の異なるディレクトリに同じファイル名があるものだけ抽出
    duplicates = {}
    for filename, paths in file_map.items():
        # ファイルが複数あること
        if len(paths) > 1:
            # フォルダ部分だけ取り出して重複チェック
            dirs = set(os.path.dirname(p) for p in paths)
            if len(dirs) > 1:
                duplicates[filename] = paths

    # 結果をファイルに書き出し
    if duplicates:
        output_path = "duplicate_files.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for filename, paths in duplicates.items():
                f.write(f"{filename}:\n")
                for p in paths:
                    f.write(f"  {p}\n")
                f.write("\n")
        return output_path
    else:
        return None

# --- 使い方例 ---
folders = [
    r"C:\path\to\folder1",
    r"C:\path\to\folder2",
    # 他のフォルダも追加可能
]

result = find_duplicate_files_across_dirs(folders)
if result:
    print(f"重複ファイル名が {result} に保存されました。")
else:
    print("重複ファイル名は見つかりませんでした。")