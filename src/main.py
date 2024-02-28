import os
from pdf_parser import PDFParser
from libs.json_saver import save_to_json

def main():
    base_path = os.path.join(os.path.dirname(__file__), "..", "dataset")
    parser = PDFParser()

    while True:
        print("\nPDF 파일명을 입력하세요. (여러 파일은 쉼표로 구분하세요)")
        print("Enter을 입력하면 프로그램이 종료됩니다.")
        file_input = input("파일명(쉼표 구분): ").strip()

        if file_input == "":
            print("프로그램을 종료합니다.")
            break

        # 쉼표 뒤 공백 제거 및 파일명 처리
        file_names = [name.strip() for name in file_input.split(",") if name.strip()]

        for file_name in file_names:
            file_path = os.path.join(base_path, file_name)

            if not os.path.isfile(file_path):
                print(f"파일을 찾을 수 없습니다: {file_path}")
                continue

            try:
                results = parser.parse_document(file_path)
                output_json = f"output/{results['parsed_content']['document_id']}.json"
                save_to_json(results, output_json)
                print(f"결과가 {output_json}에 저장되었습니다.")
            except Exception as e:
                print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()