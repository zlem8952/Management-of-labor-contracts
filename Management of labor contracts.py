import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit

class FileProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF 파일 이름 처리")
        self.setGeometry(100, 100, 400, 300)

        # 버튼 및 입력 필드 생성 및 레이아웃 설정
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("쉼표로 구분하여 이름을 입력하세요")

        self.select_folder_btn = QPushButton("PDF 폴더 선택")
        self.select_txt_btn = QPushButton("결과 텍스트 파일 저장 위치 선택")
        self.process_btn = QPushButton("파일 처리 시작")

        layout.addWidget(self.name_input)
        layout.addWidget(self.select_folder_btn)
        layout.addWidget(self.select_txt_btn)
        layout.addWidget(self.process_btn)

        # 버튼 클릭 이벤트 연결
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.select_txt_btn.clicked.connect(self.select_txt_location)
        self.process_btn.clicked.connect(self.process_files)

        # 메인 위젯 설정
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 파일 경로 변수 초기화
        self.folder_path = None
        self.txt_path = None

    def select_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "PDF 폴더 선택", options=options)
        if folder_path:
            self.folder_path = folder_path
            print(f"PDF 폴더 선택됨: {self.folder_path}")

    def select_txt_location(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "결과 텍스트 파일 저장 위치 선택", "", "Text Files (*.txt)", options=options)
        if file_path:
            self.txt_path = file_path
            print(f"결과 텍스트 파일 저장 위치 선택됨: {self.txt_path}")

    def process_files(self):
        if not self.folder_path or not self.txt_path:
            print("PDF 폴더와 결과 텍스트 파일 저장 위치를 모두 선택하세요.")
            return

        # 입력된 이름 목록 처리 (쉼표로 구분하여 리스트로 변환)
        name_list = [name.strip() for name in self.name_input.text().split(',') if name.strip()]
        
        if not name_list:
            print("이름을 입력하세요.")
            return
        
        missing_names = name_list.copy()

        for filename in os.listdir(self.folder_path):
            if filename.endswith('.pdf'):
                name_found = False
                for name in name_list:
                    if name in filename:  # 이름이 파일명에 포함된 경우
                        name_found = True
                        if name in missing_names:
                            missing_names.remove(name)  # 누락된 이름 목록에서 제거
                # 이름이 포함된 파일만 이름 변경
                if name_found:
                    new_filename = f"!{filename}"
                    os.rename(
                        os.path.join(self.folder_path, filename),
                        os.path.join(self.folder_path, new_filename)
                    )

        # 누락된 이름을 TXT 파일에 기록
        with open(self.txt_path, 'w', encoding='utf-8') as txt_file:
            for name in missing_names:
                txt_file.write(name + '\n')

        print("파일 처리가 완료되었습니다.")

if __name__ == "__main__":
    app = QApplication([])
    window = FileProcessor()
    window.show()
    app.exec_()
