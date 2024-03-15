import streamlit as st
import google.generativeai as genai
import json

# Khởi tạo Google Cloud Client

def ner_analysis(input_text):
    """Thực hiện NER cho text

    Args:
        text: Chuỗi văn bản đầu vào

    Returns:
        Danh sách các thực thể NER
    """
    GOOGLE_GEMINI_API_KEY= st.secrets["GOOGLE_GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
    # Set up the model
    generation_config = {
    "temperature": 0.2,
    "top_p": 0.2,
    "top_k": 1,

    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    prompt_parts = [
    "1. Thực hiện phân tích NER để trích xuất thông tin thực thể cho các phân loại: Mã hồ sơ, Mã tài liệu, Lĩnh vực, Tên loại tài liệu giấy tờ, Con người, Thời gian, Địa điểm và các phân loại khác\n2. Trong kết quả phân tích chuyển đổi các phân loại thành các mã sau: - Mã hồ sơ thành PROFILE_ID, - mã tài liệu thành DOC_ID Lĩnh vực thành DOMAIN, - Tên loại tài liệu giấy tờ thành DOCTYPENAME, - Con người thành PER, - Địa điểm thành LOC, - Thời gian thành DT - phân loại khác thành MISC\n3. Kết quả trích xuất được định dạng JSON gồm danh sách các thực thể bắt đầu bằng entities. Mỗi entity trong danh sách entities gồm các thuộc tính: text , label\n5. Thực hiện chuẩn hóa dữ liệu cho mỗi thuộc tính trong entity theo các quy tắc sau: - Các trường dữ liệu trong mỗi entity nếu không có dữ liệu sẽ để là N/A - Thời gian nếu có một giá trị thì chuyển dạng dd/MM/yyyy., nếu có 2 giá trị từ thời gian đến thời gian thì chuyển thành  dd/MM/yyyy -  dd/MM/yyyy",
    "input: hồ sơ lĩnh vực đất đai có mã 012 đến 312 của huyện ứng hòa trong quý 1 2024",
    "output: {\n \"entities\": [\n  {\n   \"text\": \"012\",\n   \"label\": \"PROFILE_ID\"\n  },\n{\n   \"text\": \"312\",\n   \"label\": \"PROFILE_ID\"\n  },\n  {\n   \"text\": \"đất đai\",\n   \"label\": \"DOMAIN\"\n  },\n  {\n   \"text\": \"huyện ứng hòa\",\n   \"label\": \"LOC\"\n  },\n  {\n   \"text\": \"01/01/2024-31/03/2024\",\n   \"label\": \"DT\"\n  }\n ]\n}",
    "input: các hồ sơ có chứa giấy phép đăng ký kinh doanh của công ty cyber eye",
    "output: {\n \"entities\": [\n {\n   \"text\": \"giấy phép đăng ký kinh doanh\",\n   \"label\": \"DOCTYPENAME\"\n  },  \n{\n   \"text\": \"cyber eye\",\n   \"label\": \"PER\"\n  }\n ]\n}",

    ]
    
    prompt_parts = [
        "1. Thực hiện phân tích NER để trích xuất thông tin thực thể cho các phân loại: Mã hồ sơ, Mã tài liệu, Lĩnh vực, Tên loại tài liệu giấy tờ, Con người, Thời gian, Địa điểm và các phân loại khác\n2. Trong kết quả phân tích chuyển đổi các phân loại thành các mã sau: - Mã hồ sơ thành PROFILE_ID, - mã tài liệu thành DOC_ID Lĩnh vực thành DOMAIN, - Tên loại tài liệu giấy tờ thành DOCTYPENAME, - Con người thành PER, - Địa điểm thành LOC, - Thời gian thành DATETIME - phân loại khác thành MISC\n3. Kết quả trích xuất được định dạng JSON gồm danh sách các thực thể bắt đầu bằng entities. Mỗi entity trong danh sách entities gồm các thuộc tính: text , label\n5. Thực hiện chuẩn hóa dữ liệu cho mỗi thuộc tính trong entity theo các quy tắc sau: - Trường thông tin DATETIME trong entity tự động chuyển text thành dạng dd/MM/yyyy., nếu có 2 giá trị từ thời gian đến thời gian thì chuyển thành  dd/MM/yyyy -  dd/MM/yyyy",
        "input: hồ sơ lĩnh vực đất đai có mã 012 đến 312 của huyện ứng hòa trong quý 1 2024",
        "output: {\n \"entities\": [\n  {\n   \"text\": \"012\",\n   \"label\": \"PROFILE_ID\"\n  },\n{\n   \"text\": \"312\",\n   \"label\": \"PROFILE_ID\"\n  },\n  {\n   \"text\": \"đất đai\",\n   \"label\": \"DOMAIN\"\n  },\n  {\n   \"text\": \"huyện ứng hòa\",\n   \"label\": \"LOC\"\n  },\n  {\n   \"text\": \"01/01/2024-31/03/2024\",\n   \"label\": \"DATETIME\"\n  }\n ]\n}",
        "input: các hồ sơ có chứa giấy phép đăng ký kinh doanh của công ty cyber eye",
        "output: {\n \"entities\": [\n {\n   \"text\": \"giấy phép đăng ký kinh doanh\",\n   \"label\": \"DOCTYPENAME\"\n  },  \n{\n   \"text\": \"cyber eye\",\n   \"label\": \"PER\"\n  }\n ]\n}",
        "input: hôm nay trời đẹp",
        "output: {\n \"entities\": [\n{\n      \"text\": \"15/03/2024\",\n       \"label\": \"DATETIME\"\n},  \n{\n    \"text\": \"trời đẹp\".\n    \"label\": \"MISC\" \n  }\n]\n}",
        "input: người ký Phạm Minh Chính trong tháng 12 2023",
        "output: {\n \"entities\": [\n  {\n   \"text\": \"Phạm Minh Chính\",\n   \"label\": \"PER\"\n  },\n  {\n   \"text\": \"01/12/2023-31/12/2023\",\n   \"label\": \"DATETIME\"\n  }\n ]\n}",
        ]


    searchQuery=prompt_parts.copy()
    searchQuery.append("input: "+input_text)
    searchQuery.append("output: ")

    response = model.generate_content(searchQuery)
    result=""
    if len(response.parts)>0:
        result= response.text
    return result

def main():
    """Chức năng chính của chương trình"""
    
    st.header("Demo NLP:" )
    st.subheader("Phân tích lệnh tìm kiếm của người dùng ở dạng ngôn ngữ tự nhiên thành một tập các điều kiện tìm và giá trị cần tìm")
    text = st.text_input("Xin mời bạn nhập lệnh tìm kiếm:")
    sampleText= "hồ sơ tư pháp huyện ứng hòa trong quý 4 2023"
    st.text("Ví dụ mẫu:" +sampleText)

    if st.button("Phân tích"):
        with st.status("Đang xử lý...") as status:
            responseText= ner_analysis(text)
            status.update(label="Hoàn thành!", state="complete", expanded=True)
            st.write("**Kết quả phân tích:**")
            if(len(responseText)>0):
                entities=json.loads(responseText)
                st.write(entities)
            else:
                st.write("Không có kết quả")

if __name__ == "__main__":
    main()
